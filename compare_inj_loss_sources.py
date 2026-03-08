import os
import re
import glob
import numpy as np
import pandas as pd

BASE_PATH = "/Users/xylu/Desktop/Data/acoustic_vpp"
NEW_BASE = "/Users/xylu/Desktop/Data/Machine_Inj_BG_byDay"
RENAME_MAP = {
    "BMLDCCT:CURRENT": "A_BM_Current_mA",
    "BMLDCCT:RATE": "A_BM_Inj_Rate_mAps",
    "CGLINJ:EFFICIENCY": "A_INJ_Effi",
    "LIiEV:BEAM_REP:READ:KBP": "A_INJ_Rep_ep_Hz",
    "BTpBPM:QMD11P_K_1:NC_1Hz:C": "A_Qep_BT_end_nC",
}


def load_acoustic(date_str: str):
    files = sorted(glob.glob(os.path.join(BASE_PATH, date_str, f"{date_str}*.csv")))
    chunks = []
    for file in files:
        try:
            df = pd.read_csv(file)
            if "time_datetime" not in df.columns or "vpp_volts" not in df.columns:
                continue
            df["time_datetime"] = pd.to_datetime(df["time_datetime"], format="ISO8601", errors="coerce")
            df = df.dropna(subset=["time_datetime"])[["time_datetime", "vpp_volts"]]
            chunks.append(df)
        except Exception:
            pass
    if not chunks:
        return None
    return pd.concat(chunks, ignore_index=True).sort_values("time_datetime").reset_index(drop=True)


def read_machine(files):
    chunks = []
    for file in files:
        try:
            df = pd.read_csv(file)
            if "#date" in df.columns:
                df["#date"] = pd.to_datetime(df["#date"], format="ISO8601", errors="coerce")
                df = df.rename(columns={"#date": "time_datetime"})
            elif "Timestamp" in df.columns:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="ISO8601", errors="coerce")
                df = df.rename(columns={"Timestamp": "time_datetime"})
            elif "time_datetime" in df.columns:
                df["time_datetime"] = pd.to_datetime(df["time_datetime"], format="ISO8601", errors="coerce")
            else:
                continue
            df = df.dropna(subset=["time_datetime"]).rename(columns=RENAME_MAP)
            chunks.append(df)
        except Exception:
            pass
    if not chunks:
        return None
    return pd.concat(chunks, ignore_index=True).sort_values("time_datetime").reset_index(drop=True)


def load_new(date_str: str):
    mmdd = date_str[4:8]
    folder = os.path.join(NEW_BASE, mmdd)
    if not os.path.isdir(folder):
        return None
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    return read_machine(files)


def load_legacy(date_str: str):
    candidates = [
        os.path.join(BASE_PATH, date_str, "machine"),
        os.path.join(BASE_PATH, date_str, "Machine"),
    ]
    folder = None
    for candidate in candidates:
        if os.path.isdir(candidate):
            folder = candidate
            break
    if folder is None:
        return None
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    return read_machine(files)


def add_loss_rate(df):
    if "A_INJ_Effi" in df.columns and "A_BM_Inj_Rate_mAps" in df.columns:
        eff = df["A_INJ_Effi"] / 100.0
        df["Inj_Loss_Rate"] = np.where(eff != 0, (1 - eff) / eff * df["A_BM_Inj_Rate_mAps"], np.nan)
        df.loc[df["Inj_Loss_Rate"] < 0, "Inj_Loss_Rate"] = np.nan
    else:
        df["Inj_Loss_Rate"] = np.nan
    return df


def merge_and_compute(acoustic_df, machine_df):
    merged = pd.merge_asof(
        acoustic_df.sort_values("time_datetime"),
        machine_df.sort_values("time_datetime"),
        on="time_datetime",
        direction="nearest",
        tolerance=pd.Timedelta("10s"),
    )
    return add_loss_rate(merged)


def corr_vpp_vs_loss(df):
    valid = df["vpp_volts"].notna() & df["Inj_Loss_Rate"].notna()
    n = int(valid.sum())
    if n <= 10:
        return np.nan, n
    return float(df.loc[valid, "vpp_volts"].corr(df.loc[valid, "Inj_Loss_Rate"])), n


def main():
    date_regex = re.compile(r"^\d{8}$")
    dates = sorted(
        d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d)) and date_regex.match(d)
    )

    rows = []
    all_new = []
    all_legacy = []

    for date_str in dates:
        acoustic = load_acoustic(date_str)
        if acoustic is None:
            continue

        machine_new = load_new(date_str)
        machine_legacy = load_legacy(date_str)

        rec = {"date": date_str}

        if machine_new is not None:
            merged_new = merge_and_compute(acoustic, machine_new)
            r_new, n_new = corr_vpp_vs_loss(merged_new)
            rec.update(
                {
                    "r_new": r_new,
                    "n_new": n_new,
                    "new_machine_rows": len(machine_new),
                    "new_nonzero_effi": int((machine_new.get("A_INJ_Effi", pd.Series(dtype=float)).fillna(0) != 0).sum()),
                }
            )
            all_new.append(merged_new[["vpp_volts", "Inj_Loss_Rate"]])
        else:
            rec.update({"r_new": np.nan, "n_new": 0, "new_machine_rows": 0, "new_nonzero_effi": 0})

        if machine_legacy is not None:
            merged_legacy = merge_and_compute(acoustic, machine_legacy)
            r_legacy, n_legacy = corr_vpp_vs_loss(merged_legacy)
            rec.update(
                {
                    "r_legacy": r_legacy,
                    "n_legacy": n_legacy,
                    "legacy_machine_rows": len(machine_legacy),
                    "legacy_nonzero_effi": int((machine_legacy.get("A_INJ_Effi", pd.Series(dtype=float)).fillna(0) != 0).sum()),
                }
            )
            all_legacy.append(merged_legacy[["vpp_volts", "Inj_Loss_Rate"]])
        else:
            rec.update({"r_legacy": np.nan, "n_legacy": 0, "legacy_machine_rows": 0, "legacy_nonzero_effi": 0})

        rows.append(rec)

    cmp = pd.DataFrame(rows)
    cmp["both"] = cmp["r_new"].notna() & cmp["r_legacy"].notna()
    cmp["delta_r"] = cmp["r_new"] - cmp["r_legacy"]
    both = cmp[cmp["both"]].copy()

    print("=" * 80)
    print("DAILY AGREEMENT corr(vpp_volts, Inj_Loss_Rate)")
    print("=" * 80)
    print("dates with acoustic:", len(cmp))
    print("dates with both:", len(both))

    if len(both):
        print("sign agreement:", int((np.sign(both["r_new"]) == np.sign(both["r_legacy"])).sum()), "/", len(both))
        print("|delta r| <= 0.05:", int((both["delta_r"].abs() <= 0.05).sum()), "/", len(both))
        print("|delta r| <= 0.10:", int((both["delta_r"].abs() <= 0.10).sum()), "/", len(both))

        compact = both.sort_values("date").copy()
        compact["new_eff_nonzero_frac"] = np.where(
            compact["new_machine_rows"] > 0,
            compact["new_nonzero_effi"] / compact["new_machine_rows"],
            np.nan,
        )
        compact["legacy_eff_nonzero_frac"] = np.where(
            compact["legacy_machine_rows"] > 0,
            compact["legacy_nonzero_effi"] / compact["legacy_machine_rows"],
            np.nan,
        )

        compact_cols = [
            "date",
            "r_new",
            "r_legacy",
            "delta_r",
            "n_new",
            "n_legacy",
            "new_eff_nonzero_frac",
            "legacy_eff_nonzero_frac",
        ]
        print("\nCompact per-day table (all comparable days):")
        print(compact[compact_cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

        print("\nWorst 12 dates by |delta_r|:")
        cols = [
            "date",
            "r_new",
            "r_legacy",
            "delta_r",
            "n_new",
            "n_legacy",
            "new_machine_rows",
            "legacy_machine_rows",
            "new_nonzero_effi",
            "legacy_nonzero_effi",
        ]
        print(
            both.loc[both["delta_r"].abs().sort_values(ascending=False).index, cols]
            .head(12)
            .to_string(index=False)
        )

    all_new_df = pd.concat(all_new, ignore_index=True) if all_new else pd.DataFrame(columns=["vpp_volts", "Inj_Loss_Rate"])
    all_legacy_df = pd.concat(all_legacy, ignore_index=True) if all_legacy else pd.DataFrame(columns=["vpp_volts", "Inj_Loss_Rate"])

    r_new_all, n_new_all = corr_vpp_vs_loss(all_new_df)
    r_legacy_all, n_legacy_all = corr_vpp_vs_loss(all_legacy_df)

    print("\n" + "=" * 80)
    print("ALL-DATA AGREEMENT")
    print("=" * 80)
    print(f"new overall r = {r_new_all:.6f}, n = {n_new_all}")
    print(f"legacy overall r = {r_legacy_all:.6f}, n = {n_legacy_all}")
    if np.isfinite(r_new_all) and np.isfinite(r_legacy_all):
        print(f"delta overall r = {r_new_all - r_legacy_all:+.6f}")

    if len(both):
        print("\n" + "=" * 80)
        print("DIAGNOSTICS: corr(|delta_r|, count metrics)")
        print("=" * 80)
        for col in ["new_machine_rows", "legacy_machine_rows", "new_nonzero_effi", "legacy_nonzero_effi"]:
            if both[col].notna().sum() > 3:
                c = both["delta_r"].abs().corr(both[col])
                print(f"corr(|delta_r|, {col}) = {c:+.3f}")

    mmdd_counts = cmp["date"].str[4:8].value_counts()
    collisions = mmdd_counts[mmdd_counts > 1]
    print("\nMMDD collisions in available dates:", len(collisions))
    if len(collisions):
        print(collisions.head(10).to_string())


if __name__ == "__main__":
    main()

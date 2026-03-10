import os
import re
import glob
import numpy as np
import pandas as pd

BASE_PATH = "/Users/xylu/Desktop/Data/acoustic_vpp"
NEW_BASE = "/Users/xylu/Desktop/Data/Machine_Inj_BG_byDay"
RENAME_MAP = {
    "BMLDCCT:RATE": "A_BM_Inj_Rate_mAps",
    "CGLINJ:EFFICIENCY": "A_INJ_Effi",
}


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
            else:
                continue
            df = df.rename(columns=RENAME_MAP)
            cols = ["time_datetime", "A_INJ_Effi", "A_BM_Inj_Rate_mAps"]
            for c in cols:
                if c not in df.columns:
                    df[c] = np.nan
            df = df[cols].dropna(subset=["time_datetime"])
            chunks.append(df)
        except Exception:
            pass
    if not chunks:
        return None
    return pd.concat(chunks, ignore_index=True).sort_values("time_datetime").reset_index(drop=True)


def load_new(date_str):
    mmdd = date_str[4:8]
    folder = os.path.join(NEW_BASE, mmdd)
    if not os.path.isdir(folder):
        return None
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    return read_machine(files)


def load_legacy(date_str):
    for name in ["machine", "Machine"]:
        folder = os.path.join(BASE_PATH, date_str, name)
        if os.path.isdir(folder):
            files = sorted(glob.glob(os.path.join(folder, "*.csv")))
            return read_machine(files)
    return None


def main():
    date_re = re.compile(r"^\d{8}$")
    dates = sorted(d for d in os.listdir(BASE_PATH) if date_re.match(d) and os.path.isdir(os.path.join(BASE_PATH, d)))

    rows = []
    for d in dates:
        new_df = load_new(d)
        legacy_df = load_legacy(d)
        if new_df is None or legacy_df is None or len(new_df) == 0 or len(legacy_df) == 0:
            continue

        aligned = pd.merge_asof(
            new_df.sort_values("time_datetime"),
            legacy_df.sort_values("time_datetime"),
            on="time_datetime",
            direction="nearest",
            tolerance=pd.Timedelta("10s"),
            suffixes=("_new", "_legacy"),
        )

        eff_mask = aligned["A_INJ_Effi_new"].notna() & aligned["A_INJ_Effi_legacy"].notna()
        rate_mask = aligned["A_BM_Inj_Rate_mAps_new"].notna() & aligned["A_BM_Inj_Rate_mAps_legacy"].notna()

        row = {
            "date": d,
            "new_rows": len(new_df),
            "legacy_rows": len(legacy_df),
            "new_nonzero_effi_frac": float((new_df["A_INJ_Effi"].fillna(0) != 0).mean()),
            "legacy_nonzero_effi_frac": float((legacy_df["A_INJ_Effi"].fillna(0) != 0).mean()),
            "eff_overlap": int(eff_mask.sum()),
            "rate_overlap": int(rate_mask.sum()),
            "eff_corr": float(aligned.loc[eff_mask, "A_INJ_Effi_new"].corr(aligned.loc[eff_mask, "A_INJ_Effi_legacy"])) if eff_mask.sum() > 10 else np.nan,
            "rate_corr": float(aligned.loc[rate_mask, "A_BM_Inj_Rate_mAps_new"].corr(aligned.loc[rate_mask, "A_BM_Inj_Rate_mAps_legacy"])) if rate_mask.sum() > 10 else np.nan,
            "eff_median_abs_diff": float((aligned.loc[eff_mask, "A_INJ_Effi_new"] - aligned.loc[eff_mask, "A_INJ_Effi_legacy"]).abs().median()) if eff_mask.sum() > 0 else np.nan,
            "rate_median_abs_diff": float((aligned.loc[rate_mask, "A_BM_Inj_Rate_mAps_new"] - aligned.loc[rate_mask, "A_BM_Inj_Rate_mAps_legacy"]).abs().median()) if rate_mask.sum() > 0 else np.nan,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    print("=" * 80)
    print("DIRECT MACHINE-STREAM AGREEMENT (new vs legacy)")
    print("=" * 80)
    print("days compared:", len(df))
    if len(df) == 0:
        return

    print("\nMedian diagnostics across days:")
    print(df[["new_rows", "legacy_rows", "new_nonzero_effi_frac", "legacy_nonzero_effi_frac", "eff_corr", "rate_corr", "eff_median_abs_diff", "rate_median_abs_diff"]].median(numeric_only=True).to_string())

    print("\nWorst 10 days by low efficiency correlation:")
    print(df.sort_values("eff_corr").head(10)[["date", "eff_corr", "rate_corr", "new_nonzero_effi_frac", "legacy_nonzero_effi_frac", "eff_median_abs_diff", "rate_median_abs_diff"]].to_string(index=False))


if __name__ == "__main__":
    main()

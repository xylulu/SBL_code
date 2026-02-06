import struct
import matplotlib.pyplot as plt
import numpy as np

filepath = "/Users/xylu/Desktop/Data/ahfb_local/LERDV_06_Feb_2026_10_57_36.igp"

with open(filepath, 'rb') as f:
    data = f.read()

shorts = struct.unpack(f'{len(data)//2}h', data)
all_x = np.array(shorts)

print(f"Total values: {len(all_x):,}")
print(f"Testing different interpretations...\n")

# Try interpretation 1: consecutive series
print("Interpretation 1: All 491,520 as continuous time series")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
time = np.arange(len(all_x))
axes[0].plot(time, all_x, color='red', linewidth=0.3, alpha=0.7)
axes[0].fill_between(time, all_x, color='red', alpha=0.3)
axes[0].set_title('Interpretation 1: Continuous Series')
axes[0].set_xlabel('Time Index')
axes[0].set_ylabel('Deviation')

axes[1].scatter(np.arange(0, len(all_x), 500), all_x[::500], alpha=0.3, s=1, color='red')
axes[1].set_title('Scatter (decimated)')
plt.tight_layout()
plt.savefig('/Users/xylu/Desktop/Data/code/test_interp1.png', dpi=100, bbox_inches='tight')
plt.close()

# Try interpretation 2: Two separate phases
print("Interpretation 2: Two phases (first half and second half)")
half = len(all_x) // 2
phase1 = all_x[:half]
phase2 = all_x[half:]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
time1 = np.arange(len(phase1))
time2 = np.arange(len(phase2))
axes[0].plot(time1, phase1, color='red', linewidth=0.3, alpha=0.5, label='Phase 1')
axes[0].plot(time2 + len(phase1), phase2, color='blue', linewidth=0.3, alpha=0.5, label='Phase 2')
axes[0].set_title('Interpretation 2: Two Phases')
axes[0].set_xlabel('Time Index')
axes[0].set_ylabel('Deviation')
axes[0].legend()

axes[1].scatter(np.arange(0, len(phase1), 500), phase1[::500], alpha=0.3, s=1, color='red', label='Phase 1')
axes[1].scatter(np.arange(0, len(phase2), 500), phase2[::500], alpha=0.3, s=1, color='blue', label='Phase 2')
axes[1].set_title('Scatter')
axes[1].legend()
plt.tight_layout()
plt.savefig('/Users/xylu/Desktop/Data/code/test_interp2.png', dpi=100, bbox_inches='tight')
plt.close()

print(f"  Phase 1 (first {half:,}): range [{phase1.min()}, {phase1.max()}], mean={phase1.mean():.1f}")
print(f"  Phase 2 (second {half:,}): range [{phase2.min()}, {phase2.max()}], mean={phase2.mean():.1f}")

# Try interpretation 3: Grouped measurements (e.g., 2 measurements per time point)
print("\nInterpretation 3: Grouped pairs")
n_groups = len(all_x) // 2
group1 = all_x[::2]
group2 = all_x[1::2]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
time_g = np.arange(len(group1))
axes[0].plot(time_g, group1, color='red', linewidth=0.3, alpha=0.5, label='Odd indices')
axes[0].plot(time_g, group2, color='blue', linewidth=0.3, alpha=0.5, label='Even indices')
axes[0].set_title('Interpretation 3: Two Series (Odd/Even indices)')
axes[0].set_xlabel('Time Index')
axes[0].set_ylabel('Deviation')
axes[0].legend()

axes[1].scatter(np.arange(0, len(group1), 500), group1[::500], alpha=0.3, s=1, color='red')
axes[1].scatter(np.arange(0, len(group2), 500), group2[::500], alpha=0.3, s=1, color='blue')
axes[1].set_title('Scatter')
plt.tight_layout()
plt.savefig('/Users/xylu/Desktop/Data/code/test_interp3.png', dpi=100, bbox_inches='tight')
plt.close()

print(f"  Group 1 (odd): {len(group1):,} values, range [{group1.min()}, {group1.max()}]")
print(f"  Group 2 (even): {len(group2):,} values, range [{group2.min()}, {group2.max()}]")

print("\nGenerated 3 test plots!")
print("Which one matches your reference figure?")

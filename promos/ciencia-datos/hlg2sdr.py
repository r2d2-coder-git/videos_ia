"""Build a .cube 3D LUT: BT.2020 HLG (R'G'B') -> BT.709 SDR (gamma 2.4), with soft highlight roll-off."""
import sys, numpy as np
N = 65; gain = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
a, b, c = 0.17883277, 0.28466892, 0.55991073
v = np.linspace(0, 1, N)
B_, G_, R_ = np.meshgrid(v, v, v, indexing="ij")          # cube order: R fastest
E = np.stack([R_, G_, B_], -1)
lin = np.where(E <= 0.5, E ** 2 / 3, (np.exp((E - c) / a) + b) / 12)
Y = lin @ np.array([0.2627, 0.6780, 0.0593])
disp = lin * np.maximum(Y, 1e-6)[..., None] ** 0.2 * 1000 / 203 * gain   # OOTF (1000 nit, γ1.2) -> SDR ref white = 1
M = np.array([[1.6605, -0.5876, -0.0728], [-0.1246, 1.1329, -0.0083], [-0.0182, -0.1006, 1.1187]])
rgb = np.clip(disp @ M.T, 0, None)
L = rgb.max(-1, keepdims=True); k = 0.6                    # roll-off above the knee, 1.0 at ~3x
Lm = np.where(L > k, k + (1 - k) * np.tanh((L - k) / (1 - k) / 1.2) , L)
rgb = rgb * np.where(L > 0, Lm / np.maximum(L, 1e-9), 1)
out = np.clip(rgb, 0, 1) ** (1 / 2.4)
with open(sys.argv[1], "w") as f:
    f.write(f"LUT_3D_SIZE {N}\n")
    for row in out.reshape(-1, 3): f.write(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n")

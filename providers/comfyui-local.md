---
name: comfyui-local
title: ComfyUI（ローカル実行）
capability: [image, video]
runs_on: local
location: wsl-or-win
viable: false
min_ram_gb: 16
endpoint: http://127.0.0.1:8188
delegate: comfyui
blocked_reason: iGPU（Radeon Cezanne / 共有メモリ）では SDXL の必要 VRAM ~8GB を満たせない
---

# comfyui-local — このマシンでは不可

記録として残す。**なぜローカルで画像生成をやらないか**の根拠。

## 判定
| モデル | 必要 VRAM | 本機 |
|---|---|---|
| SD1.5 | ~4GB | 境界。共有メモリで実用速度にならない |
| SDXL | ~8GB | **不可** |
| Flux | ~12GB+ | **不可** |

- GPU: AMD Radeon iGPU (Cezanne, DEV_1638)、NVIDIA なし → CUDA 不可
- WSL の ROCm は gfx90c を実質サポートしない
- RAM 15.4GB 共有。画像生成に 8GB を割くと OS が死ぬ

## 例外
学習済みの超軽量モデル（SD1.5 + LCM + 低解像度 512px、`--lowvram`）を
「1枚 3〜5 分かかってもいい」用途でなら回る可能性はある。**未検証**。
試すなら `comfyui` スキルの `scripts/hardware_check.py` を先に走らせる。

## 実務の帰結
画像・動画は `comfyui-cloud` か `openrouter` へ。ローカル完結は捨てる。

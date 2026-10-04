---
name: inference-hub
description: >
  推論バックエンド（ローカル LLM / 埋め込み / 画像生成）を 1 つの契約に揃えて選ぶルータ。
  providers/<name>.md に 1 バックエンド 1 ファイルで「どこで動くか・必要資源・capability・
  起動コマンド・エンドポイント」を自己記述させ、route.py が用途から provider を選ぶ。
  実行そのものは lms-manager / comfyui / openrouter-models 等の既存スキルへ委譲する（疎結合）。
  「どのモデルで動かす」「ローカルで動かせるか」「推論先」「provider 選び」
  「ローカルLLM」「埋め込み」「画像生成どこで」「comfy cloud」「SDXL 動く？」
  「モデル実行先」「inference」「推論バックエンド」で発動。英語でも発動。
license: MIT
---

# inference-hub — 推論バックエンドの契約とルータ

## 答えを先に（このマシンの物理制約）

| 項目 | 実測 | 帰結 |
|---|---|---|
| GPU | AMD Radeon iGPU (Cezanne / DEV_1638)、NVIDIA なし | CUDA 不可、ROCm(gfx90c) WSL 非対応 |
| VRAM | 共有メモリ（固有不存在） | SDXL/Flux ローカル実行は**不可** |
| RAM | ホスト 15.4GB / WSL 割当 7GB | 3B Q4 程度まで。7B+ は実用外 |
| CPU | Ryzen 9 5900HX 8C/16T | CPU 推論は可能だが遅い |

- **ローカル可**: 埋め込み、1.5B〜4B Q4 の分類/抽出。Win 側 iGPU(Vulkan) が WSL CPU より速い。
- **ローカル不可**: SDXL/Flux 等の画像生成、7B+ の実用チャット、動画生成。→ リモート/クラウドへ。
- よって `lms は Win しかだめ` は正しい。理由は GPU であり、**Win=推論ホスト / WSL=消費側**が疎結合の分割線。

## 3 層構造

```
[契約]   OpenAI 互換 HTTP に寄せる
         chat: /v1/chat/completions   embed: /v1/embeddings
         画像:  ComfyUI のみ例外（POST /prompt + WS）
            ↑
[registry] providers/<name>.md  ← 1 backend 1 file。ここが唯一の真実
            ↑
[router]  route.py が capability で filter → provider 決定
            ↑
[委譲]    実行は既存スキルへ（lms-manager / comfyui / openrouter-models）
```

**新規バックエンド追加は `providers/` に md を 1 枚足すだけ。コードは触らない。**

## 使い方

```bash
# 一覧と可否
python3 route.py list
python3 route.py list --capability chat
python3 route.py list --viable-only

# 選ぶ（候補を理由付きで返す）
python3 route.py pick --capability chat --max-ram-gb 4
python3 route.py pick --capability image

# 選んだ provider の起動方法と委譲先スキルを出す
python3 route.py show lmstudio
```

`route.py` は選択までで、**実行しない**。出力の `delegate` を見て該当スキルを読む。

## 委譲先

| capability | 第一候補 | 委譲先スキル |
|---|---|---|
| chat / embed（ローカル小） | lmstudio | `lms-manager` |
| embed | lmstudio | `lms-manager` |
| chat（大・高品質） | openrouter | `openrouter-models` |
| image / video | comfyui-cloud | `comfyui` |
| image / video（ローカル） | — | このマシンでは不可（`providers/comfyui-local.md` 参照） |

## 規則

- provider の実体パス・URL・引数を skill 本文に直書きしない。必ず `providers/` を引く。
- 可否判定を推測で書かない。`viable` は実測（VRAM/RAM/対応 backend）に基づく。
- WSL→Win の到達性は**未検証**。`providers/lmstudio.md` の「到達性」節の手順で確認してから使う。

## 関連
- `cli`（registry 記述子の共通規約）
- `model-manager`（モデル台帳・DB）
- `model-match-search`（スペック照合の原型）
- `lms-manager` / `comfyui` / `openrouter-models` / `wsl-qwen-link`

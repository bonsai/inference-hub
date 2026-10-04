# inference-hub

推論バックエンド（ローカル LLM / 埋め込み / 画像生成）を **1 つの契約に揃えて選ぶルータ**。

## 責務
- `providers/<name>.md` に推論バックエンドを 1 件 1 ファイルで自己記述させる（registry）。
- `route.py` が用途（capability）と資源（RAM）から provider を選ぶ。
- 選んだ先の**実行は持たない**。`lms-manager` / `comfyui` / `openrouter-models` へ委譲する。

## 責務でないもの
- モデルの実体管理・ダウンロード → `model-manager`
- LM Studio の操作 → `lms-manager`
- ComfyUI の操作 → `comfyui`
- モデルカタログ → `openrouter-models`

## 設計
```
契約（OpenAI 互換 HTTP） ← registry（providers/*.md） ← router（route.py） ← 既存スキルへ委譲
```

新しいバックエンドを足すときは `providers/` に md を 1 枚置くだけ。コードは変更しない。

## 契約の例外
ComfyUI だけは OpenAI 互換ではない（`POST /prompt` + WebSocket）。`providers/comfyui-cloud.md` に明記。

## このマシンの結論
AMD Radeon iGPU / RAM 15.4GB → **SDXL のローカル実行は不可**。小モデル LLM は Win 側
iGPU(Vulkan) で動かす。詳細は `SKILL.md`。

## 使い方
```bash
python3 route.py list [--capability chat] [--viable-only]
python3 route.py pick --capability chat [--max-ram-gb 4] [--prefer local|remote]
python3 route.py show <name>
```
stdlib のみ。依存なし。

## 構成
- `SKILL.md` — ルータ本体（pi から読まれる）
- `providers/*.md` — registry
- `route.py` — 選択ロジック
- `HANDOVER.md` / `ISSUE_LOG.md`

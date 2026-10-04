---
name: comfyui-cloud
title: ComfyUI Cloud / リモート GPU
capability: [image, video]
runs_on: remote
location: cloud
viable: true
min_ram_gb: 0
endpoint: "(Comfy Cloud の base URL。/prompt は HTTP、進捗は WebSocket)"
delegate: comfyui
---

# comfyui-cloud

ローカル GPU が使えないため、画像/動画生成の第一候補。

## capability
- `image` — txt2img / img2img / inpaint（SDXL, Flux 等）
- `video` — AnimatedDiff / Wan 等

## インターフェース
ComfyUI は OpenAI 互換ではない。**この 1 つだけ契約から外れる**。
- 投入: `POST /prompt`（API 形式の workflow JSON）
- 進捗: WebSocket
- 成果物: `/view` 等でダウンロード

## 委譲
`comfyui` スキルが Cloud 検出・workflow 投入・WS 監視・DL を全部持っている。
`scripts/check_deps.py` は Cloud 対応の依存チェックを行う。

## 未確定
- 契約・上限・課金の実測値。`comfyui` の `health_check.py` で確認する。

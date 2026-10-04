---
name: openrouter
title: OpenRouter（リモート API）
capability: [chat, embed, image]
runs_on: remote
location: cloud
viable: true
min_ram_gb: 0
endpoint: https://openrouter.ai/api/v1
delegate: openrouter-models
---

# openrouter

ローカルで扱えない規模のモデル（7B+、高品質チャット、一部の画像生成）を賄う。

## capability
- `chat` — 大型モデル。ローカルの 3B では品質が足りない用途はここ
- `embed` — ローカル embed と同一モデルを使わないと次元が変わる点に注意
- `image` — 対応モデルがある場合のみ

## インターフェース
OpenAI 互換。`/v1/chat/completions` 等がそのまま使える。

## 委譲
`openrouter-models` スキルがモデルカタログと選択を持つ。
キーは Windows ENV にある（`powershell.exe` 経由で同期する運用）。

## 使い分けの線
- ローカル（lmstudio）: 分類・抽出・埋め込み・短い定型生成
- リモート（openrouter）: 長文推論・コーディング・品質要求が高い生成

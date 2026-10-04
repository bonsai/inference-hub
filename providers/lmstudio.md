---
name: lmstudio
title: LM Studio (Windows ネイティブ / iGPU Vulkan)
capability: [chat, embed]
runs_on: local
location: win
viable: true
min_ram_gb: 2
endpoint: http://127.0.0.1:1234/v1
delegate: lms-manager
---

# lmstudio

Windows ネイティブの LM Studio を推論ホストとして使う。WSL は消費側。

## なぜ Win か
このマシンの GPU は AMD Radeon iGPU（Cezanne, DEV_1638）。Windows 側は Vulkan で
iGPU を使えるが、WSL 側は CPU のみ。**同じモデルなら Win の方が速い。**

## モデル規模の目安（RAM 15.4GB 共有 / WSL 割当 7GB）
- 〜1.5B Q4: 快適
- 3B Q4: 実用
- 7B Q4: RAM を食い潰す。非推奨
- 14B 以上: 不可

## capability
- `chat` — /v1/chat/completions
- `embed` — /v1/embeddings（furui が使う経路）

## 起動
LM Studio アプリが起動している必要がある（lms CLI は daemon 依存）。
手順は `lms-manager` を読む。GUI 起動 → モデルロード → サーバ有効化。

## 到達性（WSL → Win、未検証）
現状の WSL は NAT モード（`ip route` の default が 172.29.x.x）。
`127.0.0.1:1234` が WSL から届くかは未検証。届かなければ次のどちらか:

1. LM Studio の「Serve on Local Network」を有効化 → WSL から Win ホスト IP:1234
   （Win ホスト IP は NAT ゲートウェイ IP を試す）
2. `%UserProfile%\.wslconfig` に `networkingMode=mirrored` → localhost が共有される
   （要 WSL 再起動。RAM 設定と同時にやると一石二鳥）

**検証してから使うこと。** 検証コマンド:
```bash
curl -sS -m 3 http://127.0.0.1:1234/v1/models || echo UNREACHABLE
```

## 未確定
- モデルの実体ディレクトリ（`~/.cache/lm-studio/models` は空。Win 側のパスを lms-manager で確認）
- 現在サーバ停止中（port 1234 応答なし）

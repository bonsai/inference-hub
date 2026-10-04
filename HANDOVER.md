# HANDOVER — inference-hub

**最終更新: 2026-10-05 01:33**

## 現在地
registry 4 件（`lmstudio` / `comfyui-local` / `comfyui-cloud` / `openrouter`）+ `route.py` 稼働。
`route.py list/pick/show` は動作確認済み（2026-10-04）。

## いまブロックしていること
**WSL→Win の到達性が未検証**。`http://127.0.0.1:1234/v1` が WSL から届かない。

**この 1 点は dev-hub の WSL 再起動待ちで、inference-hub 側では解けない。**
再起動後に `.wslconfig` の `networkingMode=mirrored` が効けば、`127.0.0.1:1234` が
そのまま届く見込み。

**手順と期待値は `~/.skills/dev-hub/HANDOVER.md` §1 が正。ここには重複して書かない。**
（重複させると片方だけ更新されて食い違う。実際 dev-hub 側でその事故が起きた）

## 再起動後にやること
```bash
curl -sS -m3 http://127.0.0.1:1234/v1/models && echo "OK" || echo "UNREACHABLE"
```
- 届いた → `providers/lmstudio.md` の「到達性」節を**検証済みに書き換える**
- 届かない → `networkingMode` を疑う（dev-hub の §1 の判定表を見る）。それでも駄目なら LM Studio 側の
  「Serve on Local Network」を有効化して Win ホスト IP 経由に切り替える

## その他の未着手
1. LM Studio のモデル実体パス。モデルが 1 件も入っていない
2. comfyui-cloud の契約・上限・課金が未実測
3. comfyui-local の「SD1.5 + LCM + lowvram なら回るか」は未検証（結論は「不可」のまま）

## 次の一手
1. dev-hub の再起動手順を実施（**前提。ここが動かないと先へ進めない**）
2. 1234 到達確認 → `providers/lmstudio.md` を更新
3. 小モデル 1 件（〜3B Q4）を lms に入れて実測。`route.py pick --capability chat --max-ram-gb 4` が `lmstudio` を返すことを確認

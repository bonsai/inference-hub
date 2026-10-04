# HANDOVER — inference-hub

## 現在地
registry 4 件（lmstudio / comfyui-local / comfyui-cloud / openrouter）+ router 稼働。
`route.py list/pick/show` 動作確認済み（2026-xx-xx 時点、この repo 初回 commit 時）。

## 未着手 / 未検証
1. **WSL→Win 到達性が未検証**。`http://127.0.0.1:1234/v1` が WSL から届くか未確認。
   → 届かなければ `.wslconfig` に `networkingMode=mirrored`（要 WSL 再起動）。
   → 同時に WSL の RAM を 7GB→8〜10GB に上げると良い（ホスト 15.4GB、現状は既定 50%）。
2. LM Studio のモデル実体パスと、モデルが 1 つも入っていない件。
3. comfyui-cloud の契約・上限・課金が未実測。
4. comfyui-local の「SD1.5 + LCM + lowvram なら回るか」は未検証（結論は不可のまま）。

## 次の一手
`.wslconfig` の mirrored + RAM 増（WSL 再起動を伴うので要許可）→ 1234 到達確認 → 小モデル 1 件で実測。

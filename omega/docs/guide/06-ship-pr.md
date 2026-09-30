# PR と land

## Opening a PR

他プレイブックの最後に **opening-a-pr**。`/verify-done` PASS 後に small ordered commits で PR を開く。

## Babysit

「get it green」「Bugbot 対応」「PR #123 どう？」→ **babysit** プレイブック（組み込み babysit ではない）。

- GitHub: `.cursor/skills/forge-mode/scripts/watch-pr/watch-pr`
- Bugbot: `references/bugbot-triage.md`（fix / dismiss / ask）
- merge-ready で止まる。merge 自体はしない

## Shipping

「land」「ship」「merge when ready」→ **shipping** プレイブック。

- PR ごと独立検証（書いた agent 以外の verdict）
- patch-id で verdict の有効性を再確認
- root から連続 verified run だけ land

## レビュー

出荷前の争点: `/review-orchestrator-triple-hybrid`（ブランチ差分、3 レーン）。

次: [離席・夜間](./07-overnight.md)

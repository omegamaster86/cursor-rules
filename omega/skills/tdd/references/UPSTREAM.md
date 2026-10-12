# 上流との同期

| 役割 | パス |
|------|------|
| 上流正本 | [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/tdd` |
| omega 採用 | `omega/skills/tdd/`（日本語 `SKILL.md` + 英語 `tests.md` / `mocking.md` + forge 向け bug fix 節） |

## 取り込み時の方針

- `GLOSSARY.md`（旧 `CONTEXT.md` 命名）参照は上流どおり維持。
- seam 提案時の catch / miss 1 行は上流 49dd158 以降の挙動を反映。
- omega 独自: `disable-model-invocation: true`、**Bug fix** 節（`forge-mode` bug-fix プレイブック連携）。

## 上流 SHA（最終同期）

`49dd158d1076134a641b33efb035946536778336`

```bash
git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/mattpocock-skills
# diff SKILL.md, tests.md, mocking.md → 手動マージ（日本語・bug fix 節は維持）
```

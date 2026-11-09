# 階段 4：Tasks 對話紀錄（節錄）

> 節錄整理版，非逐字紀錄。原始匯出檔由使用者保存。時間為 UTC。

## 使用者（2026-11-09 17:55）

已 merge，請進入 Tasks。

## Agent（2026-11-09 17:55）

- 工具：`gh pr view 6`、`gh api`（列出 PR #6 的留言）
- 工具：`git switch main`、`git pull --ff-only origin main`、`git switch -c docs/tasks`
- 工具：Skill `speckit-tasks`
- 工具：`setup-tasks.ps1 -Json`
- 工具：`Write specs/001-secondhand-book-marketplace/tasks.md`
- 工具：檢查 tasks 格式與數量

PR #6 已 merge，留言和 merge 都是組員 MushroomAdy 的帳號。

Plan 規定每個系統操作至少要有一個測試，所以 tasks 包含測試工作。

- 共 100 項工作，49 項可平行：Setup 6、Foundational 13、US1 10、US2 12、US3 5、US4 15、US5 6、US6 6、US7 11、US8 4、US9 6、Polish 6
- 100 項都符合 `- [ ] T### [P?] [US?] 說明＋檔案路徑` 的格式
- MVP 範圍：Setup、Foundational 與 US1 至 US4
- 建議把 Implement 分成 8 個 PR

待確認事項（AI 推測）：

| 編號 | 問題 | 建議 |
| --- | --- | --- |
| Q-01 | 搜尋結果要包含哪些狀態的刊登？ | 只列出「上架中」 |
| Q-02 | 管理員刪除帳號後，該使用者的歷史訂單、評價、訊息怎麼處理？ | 保留紀錄，使用者欄位設為空，畫面顯示「已刪除的使用者」 |

另外，`docs/reviews/03-plan.md` 的審查者要不要改成「HLinBu（判定與技術選型）、MushroomAdy（PR 審查與 merge）」？

## 使用者（2026-11-09 18:01）

03-plan 的審查者：照 02 的寫法改。Q-01、Q-02：都照建議。

## Agent（2026-11-09 18:01）

- 工具：`Edit docs/reviews/03-plan.md`（審查者改為「HLinBu（判定與技術選型）、MushroomAdy（PR 審查與 merge）」）
- 工具：`Edit specs/001-secondhand-book-marketplace/tasks.md`（待確認事項改為判定結果；T080 寫明刪除帳號時各欄位的處理）
- 工具：`Edit specs/001-secondhand-book-marketplace/spec.md`（FR-005、FR-011，文末新增 Q-01、Q-02）
- 工具：`Edit specs/001-secondhand-book-marketplace/data-model.md`（User 的驗證規則新增 Q-02）

Q-02 細節的第一版讓刊登隨帳號刪除，但保留的歷史訂單會指向不存在的刊登。已改為刊登保留、賣家欄位設為空，該使用者「上架中」的刊登改為「已下架」。

## 使用者（2026-11-09 18:02）

這個階段審查花了 13 分鐘，請開 PR。

## Agent（2026-11-09 18:02）

- 工具：`Edit docs/reviews/04-tasks.md`（填入審查時間）
- 工具：`git commit`、`git push -u origin docs/tasks`
- 工具：`gh pr create`

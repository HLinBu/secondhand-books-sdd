# 階段 4 Review：Tasks

| 欄位 | 內容 |
| --- | --- |
| 階段 | 4. Tasks（`/speckit-tasks`） |
| 審查對象 | `specs/001-secondhand-book-marketplace/tasks.md`，以及因 Q-01、Q-02 更新的 `spec.md`、`data-model.md` |
| 審查者 | MushroomAdy（判定待確認事項、PR 審查與 merge） |
| 審查日期 | 2026-11-10 |
| 結果（核准 / 修改後核准 / 否決） | 核准 |
| PR 連結 | https://github.com/HLinBu/secondhand-books-sdd/pull/7 |

## 核准的內容

- 100 項工作，依 Setup、Foundational、US1 至 US9、Polish 分成 12 個階段，含每個系統操作的測試。
- MVP 範圍為 Setup、Foundational 與 US1 至 US4。
- Implement 分成 8 個 PR（Implement-1 至 Implement-8）。
- 待確認事項照建議採用：

| 編號 | 問題 | 採用的做法 |
| --- | --- | --- |
| Q-01 | 搜尋結果要包含哪些狀態的刊登？ | 只列出「上架中」 |
| Q-02 | 管理員刪除帳號後，該使用者的歷史訂單、評價、訊息怎麼處理？ | 保留紀錄，使用者欄位設為空並顯示「已刪除的使用者」 |

## 修改或否決的內容與原因

| 項目 | 處理（修改 / 否決） | 原因 |
| --- | --- | --- |
| `docs/reviews/03-plan.md` 的審查者欄位 | 修改 | PR #6 的留言與 merge 由組員 MushroomAdy 執行，改為「HLinBu（判定與技術選型）、MushroomAdy（PR 審查與 merge）」 |

## AI 推測或錯誤的地方

- Q-01、Q-02 是 agent 產生 tasks 時發現的缺口，建議做法由 agent 提出，審查者照建議接受。
- Q-02 的細節由 agent 決定：哪些欄位設為空（訂單、刊登的賣家、評價、訊息、裁決者、操作紀錄）、「上架中」的刊登改為「已下架」、哪些資料隨帳號刪除（收藏、站內通知）。
- 錯誤：Q-02 細節的第一版讓刊登隨帳號刪除，但保留的歷史訂單仍指向該刊登，會造成資料不一致；提交審查前改為保留刊登、賣家欄位設為空。
- Implement 分成 8 個 PR 的切法由 agent 提出。
- 工作中選用的套件 `python-dotenv`（讀取 `.env`）與展示用假資料指令（T096）由 agent 提出。

## 花費時間

- 人類審查：約 13 分鐘
- 備註：

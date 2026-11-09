# 階段 2 Review：Clarify

| 欄位 | 內容 |
| --- | --- |
| 階段 | 2. Clarify（`/speckit-clarify`） |
| 審查對象 | `specs/001-secondhand-book-marketplace/spec.md`（Clarifications 與相關需求） |
| 審查者 | HLinBu（回答澄清問題）、MushroomAdy（PR 審查與 merge） |
| 審查日期 | 2026-11-10 |
| 結果（核准 / 修改後核准 / 否決） | 核准 |
| PR 連結 | https://github.com/HLinBu/secondhand-books-sdd/pull/4 |

## 核准的內容

審查者回答全部 5 題澄清問題，答案已寫進 spec：

| 問題 | 審查者的回答 | 修改的段落 |
| --- | --- | --- |
| 訂單被取消後，刊登還能不能再被下單？ | A：刊登解除鎖定，可以再被下單 | Clarifications、FR-015、Edge Cases、Listing |
| 收件資訊的「訂單進行中」包含哪些狀態？ | A：待出貨、運送中、待確認收貨、爭議處理中 | Clarifications、User Story 4、FR-022、NFR-007、SC-007 |
| 刪除帳號申請由誰執行？ | A：由管理員在後台執行刪除 | Clarifications、User Story 1、FR-005、FR-028、NFR-008 |
| 裁決依據的「照片與訊息」指什麼？ | A：刊登實拍照片、爭議證據、該刊登的站內訊息 | Clarifications、User Story 6、FR-025 |
| 平均評價是否合計買家與賣家身分？ | A：合起來算 | Clarifications、FR-004、User |

## 修改或否決的內容與原因

| 項目 | 處理（修改 / 否決） | 原因 |
| --- | --- | --- |
| User Story 1 的「Why this priority」 | 修改 | 原文「必須有已驗證的帳號才能交易」屬於已否決的 AI-01，改回規格書原文「最低要求為需驗證 Email」 |

## AI 推測或錯誤的地方

- 5 題的選項與推薦答案由 agent 提出，審查者 5 題都選了推薦答案。
- 錯誤：Specify 階段移除 AI-01 時，漏掉 User Story 1「Why this priority」裡的同樣內容，Clarify 開始前由 agent 發現並修正。

## 花費時間

- 人類審查：約 30 分鐘
- 備註：

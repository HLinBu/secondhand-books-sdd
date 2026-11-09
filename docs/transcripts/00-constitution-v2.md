# 階段 0 修訂：Constitution v2.0.0 對話紀錄（節錄）

> 節錄整理版，非逐字紀錄。原始匯出檔由使用者保存。時間為 UTC。

## 使用者（2026-11-09 17:33）

請修正：會進行程式實作，所以有缺漏的也得補上。

## Agent（2026-11-09 17:33）

- 工具：`pdftotext`（查作業 PDF 的範圍原文）

作業 PDF 寫 Bonus「same topic, up to Requirement Analysis」，繳交說明也寫「Upload your code」。Constitution 原則 I 目前禁止實作，要改範圍必須先修訂 constitution，屬於 MAJOR 版本變更。

Agent 提出 4 個問題，審查者的回答：

| 問題 | 回答 |
| --- | --- |
| Constitution 要怎麼修訂？ | 先開獨立 PR，把 constitution 升到 2.0.0，merge 後再修改 Plan |
| 實作技術由誰決定？ | agent 提選項，審查者選 |
| 「有缺漏的也得補上」要補哪些？ | 規格書未定義的值；重新檢視 AI-01 至 AI-13 |
| 程式實作由誰執行？ | agent 執行 `/speckit-implement` |

## Agent（2026-11-09 17:36）

- 工具：`git stash push -u -- specs docs`（暫存 Plan 階段未 commit 的改動）
- 工具：`git switch main`、`git switch -c docs/constitution-v2`
- 工具：Skill `speckit-constitution`
- 工具：`resolve-template.ps1 constitution-template`
- 工具：`Write .specify/memory/constitution.md`

**Agent 傳給 `/speckit-constitution` 的輸入。** 這段由 agent 撰寫，不是使用者的 prompt，以下為原文：

> 修訂 constitution 至 2.0.0（MAJOR：改變範圍）。依人類於 2026-11-10 的決定：(1) 範圍由「止於需求分析」改為「需求分析與程式實作」，程式實作由 agent 執行 /speckit-implement；(2) 技術選型由 agent 提出選項、人類選定；(3) 規格書未定義、但實作需要的值，由 agent 提出並標示「AI 推測」，經人類核准後採用；(4) 新增 Implement 階段與審查關卡；其餘原則（規格書為需求來源、AI 起草人類核准、PR 為唯一合併途徑、全程可追溯、資料安全與必須保留的非功能需求）維持。

Constitution v2.0.0 草稿寫好了，**還沒 commit**。

- **原則 I**：改為「範圍：需求分析與程式實作」；技術選型由人類選定前不得開始實作
- **原則 II**：實作需要、但規格書未定義的值，標示「AI 推測」，經人類核准後採用
- **階段表**：新增「5. Implement」

我自己做的決定，請你特別確認：

1. `/speckit-converge` 照舊禁止，除非人類另行核准
2. Implement 可以分成多個 PR
3. 資料安全新增「程式碼與設定檔不得提交密鑰」
4. 原則 II 標題改為「規格書為需求來源」，並把各階段經人類核准的決定列為需求來源
5. 檔案最上方的 Sync Impact Report 會在 commit 前刪除

## 使用者（2026-11-09 17:38）

可以，請準備 PR。

## Agent（2026-11-09 17:38）

- 工具：`Edit .specify/memory/constitution.md`（移除 Sync Impact Report）

## 使用者（2026-11-09 17:41）

可以，請開 PR。

## Agent（2026-11-09 17:41）

- 工具：`git commit`、`git push -u origin docs/constitution-v2`
- 工具：`gh pr create`

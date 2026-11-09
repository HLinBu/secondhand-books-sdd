# 二手書交易平台 SDD Constitution

## Core Principles

### I. 範圍限於需求分析
本專案為期中專題 Bonus「AI-Agent Method」，採 Spec-driven development（GitHub Spec Kit：
Specify → Plan → Tasks），工作範圍止於 Requirement Analysis（需求分析）。

- 不得撰寫、產生或提交任何應用程式原始碼、測試或部署設定。
- 不得執行 `/speckit-implement` 與 `/speckit-converge`。
- `/speckit-plan` 與 `/speckit-tasks` 的產出只描述需求、資料與分析工作，不得包含實作步驟。

理由：專題規定各方法只做到需求分析，三種方法才能在相同範圍內比較。

### II. 規格書為唯一需求來源
唯一需求來源是《二手書交易平台基礎規格書》（2026-11-01）。

- 規格書未提及的功能不得自行新增為需求。
- 規格書列為「MVP 不做」的項目一律排除：原生 App、競標、以物易物、實體店面後台、跨境交易、
  線上付款、真實物流串接、平台收費。
- 規格書標示「必做」的模組（帳號、上架、瀏覽、交易、售後、管理）必須完整涵蓋；
  「建議」模組（溝通、留存）必須標示為建議優先級。
- 業務規則的天數一律採規格書預設值（出貨 3 天、收貨確認 3 天、評價 14 天）。
- AI 推測、補充或新增的任何需求必須明確標示為「AI 推測」，並列入待人類判定清單；
  人類判定前不得視為已確認需求。

理由：讓審查者能分辨規格書原有需求、模糊需求與 AI 編造的需求，供報告比較使用。

### III. AI 起草、人類核准（不可協商）
AI agent 只能起草；人類對所有產出負最終責任。

- 每個階段（constitution、specify、clarify、plan、tasks）結束時，必須由具名的團隊成員
  review 並核准，agent 才能進入下一階段。
- 人類否決或修改的內容必須記錄原因。
- agent 不得自行核准、合併或略過任何審查關卡。

理由：專題規定「AI 可以起草，只有人類可以接受」，且人類必須負責。

### IV. 以 Pull Request 為唯一合併途徑
- agent 不得在人類 review 之前 commit 或 push。
- 每個階段的產出必須以一個 Pull Request 提交到 `main`。
- 合併前，人類必須在 PR 上留下 review 意見；合併動作必須由人類執行。
- 不得直接 push 到 `main`。

理由：PR 的評論與合併紀錄就是審查軌跡，助教可在 repository 歷史中查證。

### V. 全程可追溯
下列資料必須保存在本 Git repository：

- spec 與各階段產出：`specs/` 目錄（Spec Kit 預設位置）。
- agent 的 plans：`specs/` 下各功能的 `plan.md`、`tasks.md` 等。
- agent 對話紀錄（transcripts）：`docs/transcripts/`，每個階段至少一份。
- 人類 review 紀錄：`docs/reviews/`，每個階段一份，內容包含審查者、日期、核准或否決項目及原因、
  對應的 PR 連結。

理由：專題要求 spec、agent 計畫與對話紀錄、人類審查都留在 repository 中，並用於報告的
「AI in our process」表格。

## 資料安全與品質要求

### 資料安全
- prompt、transcripts 與 repository 中不得出現機密資料、密碼、存取權杖或真實個人資料。
- 範例資料（使用者、Email、地址、訂單）一律使用明顯虛構的假資料。
- 提交 transcripts 前，人類必須檢查並移除任何敏感內容。

### 必須保留的非功能需求
以下規格書「品質要求」必須在 spec 中保留為可驗證的非功能需求，不得刪減或弱化：

- 一致性：訂單狀態只能依規格書的訂單狀態流程轉換；同一本書（一筆刊登）不可被賣出兩次。
- 安全：密碼必須雜湊保存；管理後台必須有角色權限與操作紀錄；上傳圖片必須檢查類型與大小。
- 個資：只收集交易必要資料；買家收件資訊僅在訂單進行中提供給賣家；使用者可申請刪除帳號。

## 階段流程與審查關卡

| 階段 | Spec Kit 指令 | agent 產出 | 人類關卡 |
| --- | --- | --- | --- |
| 0. 原則 | `/speckit-constitution` | 本文件 | 核准 constitution PR |
| 1. Specify | `/speckit-specify` | `spec.md` | 核准需求範圍與 AI 推測項目 |
| 2. Clarify | `/speckit-clarify` | 更新後的 `spec.md` | 由人類回答所有澄清問題 |
| 3. Plan | `/speckit-plan` | `plan.md`、資料模型等分析文件 | 核准分析結果 |
| 4. Tasks | `/speckit-tasks` | `tasks.md`（需求分析工作項目） | 核准並結束本方法 |

- 每個階段的 PR 必須同時包含該階段的產出、transcript 與 review 紀錄。
- 上一階段的 PR 未合併前，不得開始下一階段。
- 任一階段被否決時，回到該階段修改並重新提交，不得跳過。

## Governance

- 本 constitution 優先於本 repository 中的其他做法；與之衝突的產出必須修正。
- 修訂 constitution 必須透過 Pull Request，並由人類 review 核准後合併。
- 版本採語意化版本：
  - MAJOR：移除或重新定義原則、改變範圍。
  - MINOR：新增原則或章節，或實質擴充規範。
  - PATCH：文字澄清、錯字修正等不影響語意的修改。
- 每個階段的 PR review 必須確認產出符合本 constitution，特別是原則 I（範圍）與原則 II（需求來源）。

**Version**: 1.0.0 | **Ratified**: 2026-11-09 | **Last Amended**: 2026-11-09

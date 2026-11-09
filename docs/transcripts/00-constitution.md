# 階段 0：環境建置與 Constitution 對話紀錄（節錄）

> 節錄整理版，非逐字紀錄。原始匯出檔由使用者保存。時間為 UTC。

## 使用者（2026-11-02 03:59）

（附件：`Midterm_Project_2026 (2).pdf`）請告訴我需要做什麼。我負責 Bonus。

## 使用者（2026-11-02 04:01）

（附件：`二手書交易平台基礎規格書.pdf`）更正：規格書是這一份。

## Agent（2026-11-02 04:01）

規格書讀完了，題目是 **二手書交易平台**：台灣個人對個人（C2C）的響應式網站，從上架、下單、出貨、收貨一路到評價，不處理金流和真實物流。

## 使用者（2026-11-02 04:04）

三組的需求範圍都已列在規格書上。請嚴格依照 Bonus 的要求，條列需要做哪些事。Bonus 我選擇第一個方法 SDD。

## Agent（2026-11-02 04:04）

以下只列投影片上 Bonus 有要求的事，用 **Spec-driven development（GitHub Spec Kit）** 來做。題目和需求範圍直接用規格書。

### 一、方法流程（投影片第 4 頁）
1. 採用 Spec Kit 的三個階段：**Specify → Plan → Tasks**。
2. 只做到 **Requirement Analysis（需求分析）** 為止，不寫程式實作。
3. 題目和其他兩組相同，用二手書交易平台規格書。

### 二、定義你們的方法（投影片第 4 頁，四項都要寫）
4. **角色**：寫清楚哪些工作由 agent 做，哪些由人做。
5. **產出物**：列出每個階段產出什麼，例如 spec、plan、tasks。
6. **循環**：說明 Specify → Plan → Tasks 怎麼跑，一輪或多輪都要說清楚。
7. **審查關卡**：標出每個「人類必須核准，agent 才能繼續」的點。至少每個階段結束都要有一個。

## 使用者（2026-11-02 08:30）

Repo 是 https://github.com/HLinBu/secondhand-books-sdd.git ，請放到 `C:\sideproject`。

## Agent（2026-11-02 08:30）

- 工具：`git clone`
- 工具：`git switch -c chore/speckit-init`
- 工具：`specify init --here --force --non-interactive --integration claude --script ps`

Repo 已經 clone 到 `C:\sideproject\secondhand-books-sdd`，Spec Kit 也在 `chore/speckit-init` 分支上初始化好了，integration 是 Claude，腳本用 PowerShell。**還沒有 commit 或 push。** 照 Bonus 的規則，要先由你 review。

## 使用者（2026-11-02 08:33）

好，請 commit 並 push。

## Agent（2026-11-02 08:33）

- 工具：`git commit --allow-empty`（`main` 的初始 commit）
- 工具：`git commit`（`chore/speckit-init`）
- 工具：`git push -u origin main`、`git push -u origin chore/speckit-init`

已經 commit 並 push 到 GitHub：

- **`main`**：`8e37218` Initial commit，是空的初始 commit，作為 PR 的合併目標
- **`chore/speckit-init`**：`bcd5dc2`，加入 Spec Kit 的 30 個檔案

## 使用者（2026-11-02 08:37）

已登入，請開 PR。

## Agent（2026-11-02 08:37）

- 工具：`gh pr create`

PR 開好了：https://github.com/HLinBu/secondhand-books-sdd/pull/1

照 Bonus 規則，merge 要由人類執行，所以這一步我不代勞。merge 完告訴我，我們就從 `/speckit-constitution` 開始。

## 使用者（2026-11-02 08:44）

審核沒問題，已 merge，請開始。

## Agent（2026-11-02 08:44）

- 工具：`gh pr view 1`
- 工具：`git switch -c docs/constitution`
- 工具：Skill `speckit-constitution`
- 工具：`Write .specify/memory/constitution.md`

Merge 確認了，你的 review 評論也在。接著開分支，執行 `/speckit-constitution`。

**Agent 傳給 `/speckit-constitution` 的輸入。** 這段由 agent 撰寫，不是使用者的 prompt，以下為原文：

> 專案：二手書交易平台（Midterm Bonus：AI-Agent Method，採 Spec-driven development / GitHub Spec Kit：Specify -> Plan -> Tasks）。請依下列原則起草 constitution，文件以繁體中文撰寫：
>
> 1. 範圍：只做到 Requirement Analysis（需求分析），不進行程式實作；不執行 /speckit-implement 與 /speckit-converge。
> 2. 需求來源：唯一需求來源是《二手書交易平台基礎規格書》（2026-11-01）。規格書未提及的功能不得自行新增；規格書明列「MVP 不做」的項目（原生 App、競標、以物易物、實體店面後台、跨境交易、線上付款、真實物流串接、平台收費）一律排除。AI 推測或新增的需求必須標示並交人類判定。
> 3. 人類負責：AI agent 只能起草；每個階段（constitution、specify、clarify、plan、tasks）結束都必須由人類 review 並核准後才能進入下一階段。
> 4. Git 規則：agent 不得未經人類 review 就 commit 或 push；每個階段的產出以 Pull Request 提交，由人類 review 留言並 merge。
> 5. 可追溯：spec、agent plans、agent 對話紀錄（transcripts）、人類 review 紀錄都必須保存在 Git repository。
> 6. 資料安全：prompt 與 repo 中不得放入機密資料或真實個資，範例資料一律使用假資料。
> 7. 規格書品質要求須保留為非功能需求：訂單狀態只能依流程轉換、同一本書不可賣出兩次、密碼雜湊、後台角色權限與操作紀錄、上傳圖片檢查類型與大小、個資最小化、可申請刪除帳號。
>
> Governance：修訂 constitution 須透過 PR 並由人類核准；版本採語意化版本。

Constitution 草稿寫好了，檔案在 `.specify/memory/constitution.md`，目前放在 `docs/constitution` 分支上，**還沒 commit**。

### 版本：1.0.0
這是第一次把範本填成正式內容，所以從 1.0.0 開始。

### 內容重點
- **I. 範圍限於需求分析**：不寫程式，不跑 `/speckit-implement` 和 `/speckit-converge`
- **II. 規格書為唯一需求來源**：MVP 不做的 8 個項目一律排除；AI 推測的需求要標成「AI 推測」，交給人類判定。這會直接成為報告裡「AI 編出來的需求」的證據
- **III. AI 起草、人類核准**：每個階段都要具名的組員核准
- **IV. 以 PR 為唯一合併途徑**：agent 不能自己 commit、push 或 merge
- **V. 全程可追溯**：spec 放在 `specs/`，對話紀錄放在 `docs/transcripts/`，review 紀錄放在 `docs/reviews/`
- **資料安全與品質要求**：規格書的一致性、安全、個資要求都保留下來，作為非功能需求
- **階段審查關卡表**：constitution → specify → clarify → plan → tasks，每一關由誰核准什麼

### 我自己做的決定，請你特別確認
1. **review 紀錄也要寫成檔案放進 `docs/reviews/`。** 投影片要求 review 必須留在 Git repository 裡。PR 評論是存在 GitHub 上，不在 repo 裡，所以我多加了這一條。
2. **Ratified 日期寫 2026-11-02。** 如果你不是今天 merge，再改成實際日期。
3. 檔案最上方有一段 Sync Impact Report 註解，是給你 review 用的。照 Spec Kit 的規定，commit 前我會把它刪掉。

## 使用者（2026-11-02 08:47）

內容可以，請準備 PR。

## Agent（2026-11-02 08:47）

- 工具：`Edit .specify/memory/constitution.md`（移除 Sync Impact Report 註解）

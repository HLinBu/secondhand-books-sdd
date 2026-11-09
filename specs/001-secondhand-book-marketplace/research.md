# Research: 二手書交易平台 MVP

**Date**: 2026-11-10 | **Plan**: [plan.md](plan.md)

R-01 由人類選定；R-02 起是 agent 依選定的技術提出的設計決策，交由人類審查。

## R-01 技術選型（人類選定）

- **Decision**: Python 3.12 + Django 5.2 LTS；資料庫 SQLite；只在本機執行；Email 驗證用開發用假信箱。
- **Rationale**: Django 內建密碼雜湊、帳號驗證、權限與後台，後台也會記錄操作，可直接對應規格書的安全要求；SQLite 不需另外安裝，組員與助教下載後就能執行。
- **Alternatives considered**: TypeScript + Next.js、Node.js Express + React（後台、權限、操作紀錄都要自己寫）；PostgreSQL（需要 Docker）；部署到雲端；真實寄信服務。人類未選。

## R-02 Django 版本

- **Decision**: 使用 Django 5.2 LTS。
- **Rationale**: 長期支援版本，支援 Python 3.12，課程期間不會遇到版本停止支援。
- **Alternatives considered**: Django 6.x。非長期支援版本，支援期較短。

## R-03 防止重複售出（NFR-002）

- **Decision**: 下單時在同一個資料庫交易中，用「狀態為上架中才更新為交易中」的條件更新鎖定刊登；更新筆數為 0 就表示已被別人下單，拒絕這次下單。
- **Rationale**: 條件更新由資料庫一次完成，兩個請求同時下單時只有一個會成功；SQLite 寫入時會鎖住整個資料庫，同樣只會成立一筆。
- **Alternatives considered**: 先查詢再更新。兩個請求可能同時查到「上架中」，會賣出兩次。

## R-04 訂單狀態轉換（NFR-001）

- **Decision**: 訂單狀態的變更集中在一個轉換函式，依 data-model 的轉換表檢查「目前狀態 + 事件」是否允許，不允許就拒絕；刊登狀態的連動（交易中、上架中、已售出）在同一個交易內完成。
- **Rationale**: 所有畫面、後台與期限處理都走同一個入口，不會繞過轉換表。
- **Alternatives considered**: 各畫面自行修改狀態欄位。容易漏檢查，無法保證只依流程轉換。

## R-05 期限自動處理（FR-019、FR-020）

- **Decision**: 寫一個 Django 管理指令，處理「下單滿 3 天未出貨 → 已取消」與「取貨滿 3 天未確認 → 訂單完成」；本機可用 Windows 工作排程器定時執行，展示與測試時手動執行。爭議處理中的訂單不處理（AI-05）。
- **Rationale**: 只在本機執行，不需要另外架設背景工作服務；測試時可指定「現在時間」，不用真的等 3 天。
- **Alternatives considered**: 背景工作佇列（如 Celery）。需要額外服務，超出本機展示需求。每次開頁面時才檢查。沒人開頁面時訂單不會轉換。

## R-06 權限、後台與操作紀錄（NFR-004、FR-028 至 FR-030）

- **Decision**:
  - 角色以 Django 的使用者與權限實作：一般使用者、管理員（AI-10）；管理員用 `createsuperuser` 或後台建立（AI-13）。
  - 後台使用 Django 內建後台，再加上裁決爭議、執行刪除帳號申請、停權等自訂操作。
  - 操作紀錄另外建立「後台操作紀錄」資料表（P-05），所有後台操作都寫入，不只依賴 Django 內建的後台紀錄。
- **Rationale**: Django 內建後台紀錄只涵蓋在後台表單裡的新增、修改、刪除，自訂操作（例如裁決）不會自動記錄。
- **Alternatives considered**: 只用 Django 內建後台紀錄。自訂操作會漏記，不符合「每一筆管理操作都要記錄」。

## R-07 密碼、圖片與密鑰（NFR-003、NFR-005）

- **Decision**:
  - 密碼使用 Django 預設的密碼雜湊（PBKDF2）。
  - 上傳圖片用 Pillow 確認檔案真的是 JPEG、PNG 或 WebP，不只看副檔名；單張最多 5 MB，每筆刊登 1 到 5 張（AI-11）。
  - Django 的密鑰放在 `.env`，不提交；repo 只放 `.env.example`。
- **Rationale**: 只看副檔名可以被改名繞過；密鑰不可提交是 constitution v2.0.0 的資料安全規定。
- **Alternatives considered**: 只檢查副檔名。容易被繞過。

## R-08 響應式畫面

- **Decision**: Django 範本搭配一份自己寫的 CSS，以手機寬度為基準，不使用需要建置流程的前端框架。
- **Rationale**: 不需要 Node 建置步驟，組員只要裝 Python 就能執行。
- **Alternatives considered**: Tailwind CSS（需要建置）、從 CDN 載入 Bootstrap（離線展示時無法載入）。

## R-09 規格書未定義的值

- **Decision**: V-01 至 V-05 與 AI-01 至 AI-13 的判定結果已寫進 spec；本計畫依 spec 實作，不另訂其他值。
- **Rationale**: constitution v2.0.0 原則 II 規定這些值要經人類核准；人類已於 2026-11-10 判定。
- **Alternatives considered**: 實作時由 agent 視需要自訂。違反原則 II。

## R-10 系統操作契約的形式

- **Decision**: 保留「操作、執行者、前置條件、結果、來源」的系統操作契約，再新增頁面契約，列出每個頁面的網址、可使用的角色與對應的操作。
- **Rationale**: 伺服器端產生頁面的網站，對使用者的介面就是頁面與表單，不另外提供 API。
- **Alternatives considered**: 設計 REST API 與 OpenAPI 文件。本專案沒有其他系統要串接，不需要。

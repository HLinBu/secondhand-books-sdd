# Implementation Plan: 二手書交易平台 MVP

**Branch**: `docs/plan` | **Date**: 2026-11-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-secondhand-book-marketplace/spec.md`

**Note**: 依 constitution v2.0.0，本專案範圍包含需求分析與程式實作。技術由人類於 2026-11-10 選定。

## Summary

以 Django 建立一個在本機執行的響應式網站，讓一本書走完上架、下單、出貨、收貨到評價的流程。規格書的 6 個必做模組與 2 個建議模組都會實作。

Plan 階段的產出：

- 技術選型與設計決策（[research.md](research.md)）
- 資料模型：規格書 9 個實體，加上「後台操作紀錄」與「站內通知」，含欄位、驗證規則與狀態轉換（[data-model.md](data-model.md)）
- 系統操作契約（[contracts/system-operations.md](contracts/system-operations.md)）與頁面契約（[contracts/pages.md](contracts/pages.md)）
- 本機執行與驗收步驟（[quickstart.md](quickstart.md)）

本階段的人類判定：

- P-01 至 P-08 資料缺口：全部接受
- AI-01 至 AI-13 重審：接受 12 項，AI-12 維持否決
- V-01 至 V-05 實作所需的值：全部接受

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.2 LTS；Pillow（檢查上傳圖片）；python-dotenv（讀取 `.env`）；django-unfold（後台主題）；Bootstrap 5.3.3 與 Bootstrap Icons 1.11.3（前台 design system，發行檔放在 `static/vendor/`）

**Storage**: SQLite（單一檔案，不需另外安裝）；上傳的照片存放在本機 `media/` 目錄

**Testing**: Django 內建測試框架（`manage.py test`）

**Target Platform**: 本機執行，以手機與電腦瀏覽器開啟（響應式網頁）

**Project Type**: Web 應用程式（伺服器端產生頁面）

**Performance Goals**: 規格書未定義；AI-12 已否決，不另訂

**Constraints**:

- 依規格書「MVP 不做」：不做原生 App、競標、以物易物、實體店面後台、跨境交易、線上付款、真實物流串接、平台收費
- Email 驗證信不真的寄出，使用 Django 的檔案寄信後端，信件存成本機檔案
- 不串接外部書目資料庫（AI-02）
- 程式碼與設定檔不得含密鑰，密鑰放在不提交的環境變數檔，repo 只放範例檔

**Scale/Scope**: 課程展示用，規格書未定義使用量；功能範圍為 6 個必做模組與 2 個建議模組

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

依 constitution v2.0.0 檢查。

| 原則 | 檢查內容 | Phase 0 前 | Phase 1 後 |
| --- | --- | --- | --- |
| I. 範圍：需求分析與程式實作 | 技術由人類選定；不執行 `/speckit-converge` | 通過：人類選定 Django、SQLite、本機執行、假信箱 | 通過 |
| II. 規格書為需求來源 | 不自行新增功能；AI 推測與實作所需的值須經人類核准 | 通過 | 通過：P-01 至 P-08、AI-01 至 AI-13、V-01 至 V-05 都已由人類判定 |
| III. AI 起草、人類核准 | 本階段產出需人類核准 | 待審查 | 待審查 |
| IV. 以 PR 為唯一合併途徑 | 以 PR 提交，由人類 merge | 待提交 | 待提交 |
| V. 全程可追溯 | 產出放在 `specs/`；程式碼目錄由本文件決定 | 通過 | 通過：見下方 Project Structure |
| 資料安全 | 測試資料用假資料；不提交密鑰 | 通過 | 通過：見 research R-07 |
| 必須保留的非功能需求 | NFR-001 至 NFR-008 不得刪減 | 通過 | 通過：見 research R-03 至 R-06 |

沒有違反項目，不需要填寫 Complexity Tracking。

## Project Structure

### Documentation (this feature)

```text
specs/001-secondhand-book-marketplace/
├── spec.md
├── plan.md              # 本文件
├── research.md          # 技術選型與設計決策
├── data-model.md        # 資料模型與狀態轉換
├── quickstart.md        # 本機執行與驗收步驟
├── contracts/
│   ├── system-operations.md   # 系統操作契約
│   └── pages.md               # 頁面契約
├── checklists/
│   └── requirements.md
└── tasks.md             # Tasks 階段產出（尚未建立）
```

### Source Code (repository root)

```text
pyproject.toml           # 依賴套件（以 uv 管理）
manage.py
.env.example             # 環境變數範例（真正的 .env 不提交）
config/                  # Django 專案設定、網址總表
apps/
├── accounts/            # 帳號：註冊、Email 驗證、登入、個人檔案、刪除帳號申請
├── catalog/             # 上架與瀏覽：書目、刊登、照片、搜尋、篩選、書籍頁
├── orders/              # 交易與售後：訂單、物流、取消、爭議、評價、期限處理指令
├── messaging/           # 溝通（建議）：站內訊息
├── favorites/           # 留存（建議）：收藏、站內通知
└── backoffice/          # 管理：後台、裁決、停權、刪除帳號、操作紀錄
templates/               # 共用版面與各頁面範本
static/
├── css/site.css         # 品牌主題，覆寫 Bootstrap
└── vendor/              # Bootstrap 5.3.3、Bootstrap Icons 1.11.3 發行檔
media/                   # 上傳照片（不提交）
```

每個 app 底下有自己的 `tests/`，用 Django 測試框架執行。

**Structure Decision**: 採單一 Django 專案，依規格書的模組切成 6 個 app，讓每個模組的程式與測試放在一起，方便對照 spec 與分工。

## Complexity Tracking

沒有違反 constitution 的項目。

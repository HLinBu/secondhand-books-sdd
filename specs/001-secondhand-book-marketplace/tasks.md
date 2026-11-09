---

description: "Task list for 二手書交易平台 MVP implementation"
---

# Tasks: 二手書交易平台 MVP

**Input**: Design documents from `/specs/001-secondhand-book-marketplace/`

**Prerequisites**: [plan.md](plan.md)、[spec.md](spec.md)、[research.md](research.md)、[data-model.md](data-model.md)、[contracts/](contracts/)、[quickstart.md](quickstart.md)

**Tests**: 包含測試工作。依 [contracts/system-operations.md](contracts/system-operations.md)，每個系統操作至少要有一個成功與一個前置條件不符的測試。測試先寫，確認失敗後再實作。

**Organization**: 依 spec 的 User Story 分階段。US1 至 US7 為必做（P1），US8、US9 為建議（P2）。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可平行進行（不同檔案，且不依賴未完成的工作）
- **[Story]**: 對應 spec 的 User Story（US1 至 US9）
- 每項工作都寫明檔案路徑

## Path Conventions

依 [plan.md](plan.md) 的 Project Structure：Django 專案設定在 `config/`，各模組在 `apps/<app>/`，測試在 `apps/<app>/tests/`，範本在 `templates/`，CSS 在 `static/css/`。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 建立 Django 專案與 6 個 app 的骨架

- [X] T001 建立 `pyproject.toml`：Python 3.12；依賴 `django>=5.2,<5.3`、`pillow`、`python-dotenv`；以 `uv sync` 安裝（research R-01、R-02）
- [X] T002 在 repo 根目錄建立 Django 專案：`manage.py` 與 `config/`（`settings.py`、`urls.py`、`wsgi.py`、`asgi.py`）
- [X] T003 [P] 建立 `apps/__init__.py`，以及 `apps/accounts/`、`apps/catalog/`、`apps/orders/`、`apps/messaging/`、`apps/favorites/`、`apps/backoffice/` 六個 app，各自的 `apps.py` 設定 `name = "apps.<app>"`，並建立空的 `tests/__init__.py`
- [X] T004 [P] 更新 `.gitignore`：加入 `.env`、`db.sqlite3`、`media/`、`sent_emails/`、`.venv/`、`__pycache__/`
- [X] T005 [P] 建立 `.env.example`：`DJANGO_SECRET_KEY`（範例值，註明需自行替換）、`DJANGO_DEBUG=True`、`EMAIL_FILE_PATH=sent_emails`（constitution 資料安全：不提交密鑰）
- [X] T006 設定 `config/settings.py`：用 python-dotenv 讀取 `.env`；`INSTALLED_APPS` 加入六個 app；SQLite 資料庫 `db.sqlite3`；`LANGUAGE_CODE="zh-hant"`、`TIME_ZONE="Asia/Taipei"`、`USE_TZ=True`；`AUTH_USER_MODEL="accounts.User"`；`EMAIL_BACKEND="django.core.mail.backends.filebased.EmailBackend"`、`EMAIL_FILE_PATH` 取自 `.env`；`MEDIA_ROOT=media/`、`STATICFILES_DIRS=[static/]`、`TEMPLATES` 的 `DIRS=[templates/]`；`LOGIN_URL="/accounts/login/"`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 所有 User Story 都會用到的使用者模型、版面、圖片檢查與操作紀錄

**⚠️ CRITICAL**: 這個階段完成前，不能開始任何 User Story

- [X] T007 在 `apps/accounts/models.py` 建立自訂 `User`（繼承 `AbstractBaseUser`、`PermissionsMixin`）：`email`（登入帳號，「作為登入帳號，不可重複」）、`nickname`（暱稱）、`role`（choices：一般使用者、管理員，「一般使用者或管理員（AI-10）」，預設一般使用者）、`email_verified`（預設 False）、`deletion_requested_at`（「沒有申請時為空」，可為空）、`is_active`（停權狀態，False 表示停權，AI-06）、`date_joined`；`is_staff` 在 `save()` 時依 `role == 管理員` 設定；`USERNAME_FIELD="email"`
- [X] T008 在 `apps/accounts/managers.py` 建立 `UserManager`：`create_user` 一律建立 role 為一般使用者的帳號；`create_superuser` 建立 role 為管理員、`email_verified=True` 的帳號（AI-13：管理員由平台建立）
- [X] T009 產生並套用 accounts 的初始 migration：`apps/accounts/migrations/0001_initial.py`
- [X] T010 [P] 建立 `templates/base.html`：以 Bootstrap 5.3 建立響應式導覽列（手機收合）、搜尋框、賣書按鈕、我的訂單、收藏、站內通知、個人選單（個人檔案、我的刊登、管理後台、登出）、Django messages 提示、頁尾；載入 `static/vendor/` 的 Bootstrap 與 Bootstrap Icons（research R-08，Implement-1 修訂）
- [X] T011 [P] 建立 `static/css/site.css`：覆寫 Bootstrap 的品牌色（青綠色）、字型、圓角、陰影，並提供卡片、書封、狀態標籤、窄表單等共用樣式；設定 django-unfold 後台主題使用相同品牌色（NFR-009、research R-08，Implement-1 修訂）
- [X] T012 [P] 在 `apps/catalog/validators.py` 建立 `validate_image(file)`：用 Pillow 開啟並確認格式為 JPEG、PNG 或 WEBP，不只看副檔名；檔案大小上限 5 MB；錯誤訊息說明原因（「只接受 JPEG、PNG、WebP，單張最多 5 MB」，NFR-005、AI-11、research R-07）
- [X] T013 [P] 在 `apps/catalog/tests/test_validators.py` 測試 `validate_image`：JPEG、PNG、WebP 通過；超過 5 MB 拒絕；副檔名改成 `.jpg` 的文字檔拒絕；GIF 拒絕
- [X] T014 [P] 在 `apps/backoffice/models.py` 建立 `AdminLog`：`actor`（操作者，FK User）、`created_at`（時間）、`target`（對象，文字，例如「Order #12」）、`content`（內容）；「紀錄只能新增，不能修改或刪除」：覆寫 `save()` 在已存在時拋出例外，覆寫 `delete()` 拋出例外（P-05、FR-030）
- [X] T015 在 `apps/backoffice/services.py` 建立 `record_admin_action(actor, target, content)`，寫入一筆 `AdminLog`（依賴 T014）
- [X] T016 [P] 在 `apps/backoffice/tests/test_admin_log.py` 測試：`record_admin_action` 會新增紀錄；修改或刪除既有紀錄會失敗
- [X] T017 [P] 在 `apps/accounts/decorators.py` 建立 `verified_required`：未登入導向登入頁；未驗證 Email 時顯示「請先完成 Email 驗證」並拒絕（AI-01）
- [X] T018 設定 `config/urls.py`：`/admin/` 與各 app 的 `urls.py`；`DEBUG` 時提供 `media/` 檔案
- [X] T019 產生並套用 backoffice 的 migration：`apps/backoffice/migrations/0001_initial.py`

**Checkpoint**: `uv run python manage.py test` 可執行且 T013、T016 通過

---

## Phase 3: User Story 1 - 註冊、驗證 Email 與管理個人檔案 (Priority: P1) 🎯 MVP

**Goal**: 訪客能註冊、驗證 Email、登入、維護個人檔案、申請刪除帳號

**Independent Test**: 用假 Email 註冊、開啟 `sent_emails/` 中的驗證信連結、登入、修改暱稱、申請刪除帳號

### Tests for User Story 1

- [ ] T020 [P] [US1] 在 `apps/accounts/tests/test_register.py` 測試 OP-01：註冊後建立 role 為一般使用者、`email_verified=False` 的帳號並寄出一封驗證信；重複 Email 被拒絕；密碼以雜湊保存（不等於明文，NFR-003）
- [ ] T021 [P] [US1] 在 `apps/accounts/tests/test_verify.py` 測試 OP-02：有效連結使 `email_verified=True`；無效或過期連結被拒絕
- [ ] T022 [P] [US1] 在 `apps/accounts/tests/test_login.py` 測試 OP-03：正確 Email 與密碼可登入；錯誤密碼被拒絕；`is_active=False`（停權）被拒絕
- [ ] T023 [P] [US1] 在 `apps/accounts/tests/test_profile.py` 測試 OP-04：登入後可查看與修改暱稱；未登入導向登入頁
- [ ] T024 [P] [US1] 在 `apps/accounts/tests/test_delete_request.py` 測試 OP-05：送出後 `deletion_requested_at` 有值；未登入不能送出

### Implementation for User Story 1

- [ ] T025 [P] [US1] 在 `apps/accounts/tokens.py` 建立 Email 驗證用的 token 產生器（繼承 `PasswordResetTokenGenerator`，雜湊值納入 `email_verified`）
- [ ] T026 [P] [US1] 在 `apps/accounts/forms.py` 建立 `RegistrationForm`（Email、暱稱、密碼、確認密碼，套用 Django 密碼驗證規則）與 `ProfileForm`（暱稱）
- [ ] T027 [US1] 在 `apps/accounts/views.py` 實作註冊（寄出含驗證連結的信）、驗證、登入、登出、個人檔案、申請刪除帳號；登入使用 Django `LoginView`（預設會拒絕 `is_active=False`）（依賴 T025、T026）
- [ ] T028 [US1] 在 `apps/accounts/urls.py` 設定 `register/`、`verify/<uidb64>/<token>/`、`login/`、`logout/`、`profile/`、`delete-request/`（contracts/pages.md）
- [ ] T029 [P] [US1] 建立範本 `templates/accounts/register.html`、`verify_result.html`、`login.html`、`profile.html`（顯示平均評價，沒有評價時顯示「尚無評價」）、`delete_request.html`

**Checkpoint**: T020 至 T024 通過；可在瀏覽器完成 Independent Test

---

## Phase 4: User Story 2 - 賣家上架與管理刊登 (Priority: P1)

**Goal**: 已驗證的賣家能以 ISBN 帶入或手動填寫書目，建立、修改、下架刊登

**Independent Test**: 已驗證的賣家建立一筆附 1 張照片的刊登，並在「我的刊登」看到它

### Tests for User Story 2

- [ ] T030 [P] [US2] 在 `apps/catalog/tests/test_isbn_lookup.py` 測試 OP-06：平台已有 ISBN 時帶入書名、作者、出版社、版次、分類、封面；沒有時提示手動填寫
- [ ] T031 [P] [US2] 在 `apps/catalog/tests/test_create_listing.py` 測試 OP-07：成功建立「上架中」刊登；未驗證 Email 被拒絕；0 張或 6 張照片被拒絕；價格 0 或非整數被拒絕；新 ISBN 會建立新書目，既有 ISBN 共用同一書目；建立後發出 `listing_published` 訊號
- [ ] T032 [P] [US2] 在 `apps/catalog/tests/test_manage_listing.py` 測試 OP-08、OP-09：賣家可修改、下架自己「上架中」的刊登；「交易中」「已售出」的刊登修改與下架被拒絕；非本人被拒絕

### Implementation for User Story 2

- [ ] T033 [US2] 在 `apps/catalog/models.py` 建立 `Book`：`isbn`（「不可重複」）、`title`、`author`、`publisher`、`edition`、`category`（choices：「教科書、文學小說、商業理財、語言學習、電腦資訊、藝術設計、兒童讀物、其他（V-01）」）、`cover`（ImageField，可為空，套用 `validate_image`）
- [ ] T034 [US2] 在 `apps/catalog/models.py` 建立 `Listing`：`seller`（FK User）、`book`（FK Book）、`condition_note`（書況說明）、`price`（正整數，「新台幣整數，至少 1 元（V-04）」）、`status`（choices：「上架中、交易中、已售出、已下架（AI-03）」，預設上架中）、`created_at`；以及 `ListingPhoto`：`listing`（FK）、`image`（套用 `validate_image`）
- [ ] T035 [US2] 產生並套用 catalog 的 migration：`apps/catalog/migrations/0001_initial.py`（依賴 T033、T034）
- [ ] T036 [P] [US2] 在 `apps/catalog/signals.py` 定義 `listing_published` 訊號（參數：listing），供 US9 訂閱
- [ ] T037 [US2] 在 `apps/catalog/forms.py` 建立 `BookForm`、`ListingForm` 與多檔上傳欄位；驗證照片「1 到 5 張」，每張套用 `validate_image`（FR-008、AI-11）
- [ ] T038 [US2] 在 `apps/catalog/services.py` 實作 `create_listing(seller, isbn, book_data, listing_data, photos)`：ISBN 已存在時使用既有書目，否則建立新書目（AI-02）；在同一交易中建立刊登與照片；完成後送出 `listing_published`
- [ ] T039 [US2] 在 `apps/catalog/views.py` 實作建立刊登（`verified_required`；GET 帶 `?isbn=` 時預先填入書目）、我的刊登、修改刊登、下架刊登；修改與下架只允許本人且狀態為「上架中」（FR-010、AI-03）
- [ ] T040 [US2] 在 `apps/catalog/urls.py` 設定 `listings/new/`、`listings/mine/`、`listings/<id>/edit/`、`listings/<id>/withdraw/`
- [ ] T041 [P] [US2] 建立範本 `templates/catalog/listing_form.html`、`listing_mine.html`、`listing_withdraw_confirm.html`

**Checkpoint**: T030 至 T032 通過

---

## Phase 5: User Story 3 - 買家搜尋、篩選與瀏覽書籍頁 (Priority: P1)

**Goal**: 依書名、作者、ISBN 搜尋，依分類、價格篩選，查看書籍頁與刊登詳情

**Independent Test**: 用測試資料建立數筆刊登，以三種搜尋條件與兩種篩選條件確認結果

### Tests for User Story 3

- [ ] T042 [P] [US3] 在 `apps/catalog/tests/test_search.py` 測試 OP-10、OP-11：書名、作者部分符合可找到；ISBN 完全符合可找到；分類篩選；最低價、最高價篩選；不符合的不出現；搜尋結果只包含「上架中」的刊登
- [ ] T043 [P] [US3] 在 `apps/catalog/tests/test_book_page.py` 測試 OP-12：書籍頁顯示書目資料與該書目下的刊登；刊登詳情顯示照片、書況、價格、賣家暱稱；未登入可瀏覽

### Implementation for User Story 3

- [ ] T044 [US3] 在 `apps/catalog/views.py` 實作首頁與搜尋（查詢參數 `q`、`category`、`min_price`、`max_price`；只列出「上架中」的刊登，依建立時間新到舊）、書籍頁、刊登詳情；不需登入（contracts/pages.md 設計決定）
- [ ] T045 [US3] 在 `apps/catalog/urls.py` 加入 `/`、`books/<isbn>/`、`listings/<id>/`
- [ ] T046 [P] [US3] 建立範本 `templates/catalog/home.html`（搜尋表單、分類與價格篩選、結果清單）、`book_detail.html`、`listing_detail.html`（登入後顯示下單、傳訊息、收藏書目按鈕的位置）

**Checkpoint**: T042、T043 通過；US1 至 US3 合起來可完成「上架並被找到」

---

## Phase 6: User Story 4 - 下單、出貨與收貨確認 (Priority: P1)

**Goal**: 下單鎖定刊登、出貨、取貨、確認收貨，以及 3 天期限自動處理

**Independent Test**: 一組假買家與假賣家從下單走到訂單完成，再以期限處理指令驗證兩種逾期情況

### Tests for User Story 4

- [ ] T047 [P] [US4] 在 `apps/orders/tests/test_transitions.py` 測試轉換表：data-model「訂單狀態轉換」中的每一條轉換都成功且刊登狀態正確連動；表外轉換（例如待出貨 → 訂單完成）拋出例外且資料不變（NFR-001、research R-04）
- [ ] T048 [P] [US4] 在 `apps/orders/tests/test_place_order.py` 測試 OP-13：成功建立「待出貨」訂單並記錄成交價與收件資訊，刊登變「交易中」；未驗證 Email 被拒絕；賣家對自己的刊登被拒絕（AI-08）；刊登不是「上架中」被拒絕；刊登已被另一筆訂單鎖定時，第二次下單被拒絕且只存在一筆訂單（NFR-002、research R-03）
- [ ] T049 [P] [US4] 在 `apps/orders/tests/test_fulfilment.py` 測試 OP-14 至 OP-16：出貨建立物流紀錄（已出貨、出貨時間）；取貨更新為已取貨並記錄取貨時間；確認收貨記錄完成時間且刊登「已售出」；非本人或狀態不符被拒絕
- [ ] T050 [P] [US4] 在 `apps/orders/tests/test_deadlines.py` 測試 OP-17：以 `--now` 指定時間，下單滿 3 天的「待出貨」變「已取消」（取消原因：下單後 3 天未出貨）且刊登回到「上架中」；取貨滿 3 天的「待確認收貨」變「訂單完成」且刊登「已售出」；未滿 3 天不變；「爭議處理中」不變（AI-05）
- [ ] T051 [P] [US4] 在 `apps/orders/tests/test_recipient_info.py` 測試 OP-18：待出貨、運送中、待確認收貨、爭議處理中時賣家看得到收件資訊；訂單完成、已取消時看不到；非訂單當事人不能開啟訂單詳情

### Implementation for User Story 4

- [ ] T052 [US4] 在 `apps/orders/models.py` 建立 `Order`：`buyer`、`seller`（FK User）、`listing`（FK Listing）、`price`（「下單當下的刊登價格」）、`created_at`、`status`（choices：待出貨、運送中、待確認收貨、訂單完成、已取消、爭議處理中）、`recipient_name`、`recipient_phone`、`recipient_address_or_store`（「收件人姓名、手機、收件地址或取貨門市（V-05）」）、`completed_at`、`cancelled_at`（可為空）、`cancel_reason`（choices：「下單後 3 天未出貨、出貨前取消（買家）、出貨前取消（賣家）、爭議裁決買家有理」，可為空）
- [ ] T053 [US4] 在 `apps/orders/models.py` 建立 `Shipment`：`order`（OneToOne，「一筆訂單一筆物流紀錄」）、`method`（choices：「超商取貨、宅配，皆為模擬（V-02）」）、`tracking_number`、`status`（choices：「已出貨、已取貨（V-03）」）、`shipped_at`、`picked_up_at`（可為空）
- [ ] T054 [US4] 產生並套用 orders 的 migration：`apps/orders/migrations/0001_initial.py`（依賴 T052、T053）
- [ ] T055 [US4] 在 `apps/orders/transitions.py` 實作轉換表與 `apply_event(order, event, now)`：以 data-model「訂單狀態轉換」為唯一依據，表外轉換拋出 `InvalidTransition`；在 `transaction.atomic()` 中同時更新訂單、刊登狀態、完成或取消時間與原因（research R-04）
- [ ] T056 [US4] 在 `apps/orders/services.py` 實作 `place_order(buyer, listing_id, recipient)`：檢查 Email 已驗證、不是自己的刊登；以 `Listing.objects.filter(pk=..., status="上架中").update(status="交易中")` 條件更新，回傳 0 時拒絕；成功後建立訂單（research R-03）；以及 `ship`、`pickup`、`confirm` 三個函式，皆透過 `apply_event`（依賴 T055）
- [ ] T057 [US4] 在 `apps/orders/management/commands/process_order_deadlines.py` 實作期限處理指令，支援 `--now` 參數；透過 `apply_event` 處理兩種逾期；不處理「爭議處理中」（research R-05）
- [ ] T058 [US4] 在 `apps/orders/forms.py` 建立 `OrderForm`（收件資訊三欄，皆必填）與 `ShipForm`（物流方式、託運單號）
- [ ] T059 [US4] 在 `apps/orders/views.py` 實作下單（`verified_required`）、我的訂單（買家、賣家分頁）、訂單詳情（只有當事人可開啟；收件資訊只在 4 個進行中狀態顯示給賣家）、出貨、取貨、確認收貨；違反前置條件時不改資料並顯示原因
- [ ] T060 [US4] 在 `apps/orders/urls.py` 設定 `listings/<id>/order/`、`orders/`、`orders/<id>/`、`orders/<id>/ship/`、`orders/<id>/pickup/`、`orders/<id>/confirm/`
- [ ] T061 [P] [US4] 建立範本 `templates/orders/order_form.html`、`order_list.html`、`order_detail.html`（依狀態與角色顯示可執行的按鈕）、`ship_form.html`

**Checkpoint**: T047 至 T051 通過；quickstart 情境 1 的步驟 1 至 6 可完成

---

## Phase 7: User Story 5 - 買賣雙方互評 (Priority: P1)

**Goal**: 訂單完成後 14 天內雙方互評，並計入平均評價

**Independent Test**: 讓一筆測試訂單完成，雙方各留一則評價，檢查平均評價

### Tests for User Story 5

- [ ] T062 [P] [US5] 在 `apps/orders/tests/test_reviews.py` 測試 OP-21：訂單完成未滿 14 天，買家與賣家各可評價一次；第二次被拒絕（AI-04）；星等 0 或 6 被拒絕；訂單完成滿 14 天後被拒絕；「已取消」被拒絕；非當事人被拒絕
- [ ] T063 [P] [US5] 在 `apps/accounts/tests/test_average_rating.py` 測試 FR-004：平均評價合計當買家與當賣家收到的評價；沒有評價時為空

### Implementation for User Story 5

- [ ] T064 [US5] 在 `apps/orders/models.py` 建立 `Review`：`order`（FK）、`reviewer`、`reviewee`（FK User）、`stars`（「1 到 5 的整數（AI-04）」）、`content`、`created_at`；`UniqueConstraint(order, reviewer)`（「同一評價者對同一訂單只能評價一次」），並產生 migration
- [ ] T065 [US5] 在 `apps/orders/services.py` 實作 `create_review(order, reviewer, stars, content, now)`：只允許「訂單完成」且 `now - completed_at` 未滿 14 天；評價者必須是買家或賣家，被評價者為另一方（FR-026）
- [ ] T066 [US5] 在 `apps/accounts/models.py` 為 `User` 加上 `average_rating` 屬性：以 `reviewee=self` 的所有評價星等取平均，沒有評價時回傳 None（FR-004）
- [ ] T067 [US5] 在 `apps/orders/views.py`、`apps/orders/urls.py` 加入 `orders/<id>/review/`，並建立範本 `templates/orders/review_form.html`；訂單詳情在可評價時顯示評價按鈕

**Checkpoint**: T062、T063 通過；quickstart 情境 1 全部完成

---

## Phase 8: User Story 6 - 取消訂單與爭議處理 (Priority: P1)

**Goal**: 出貨前雙方可取消；取貨後確認前，買家可提出爭議

**Independent Test**: 一筆待出貨訂單由賣家取消；另一筆待確認收貨訂單由買家提出爭議

### Tests for User Story 6

- [ ] T068 [P] [US6] 在 `apps/orders/tests/test_cancel.py` 測試 OP-19：「待出貨」時買家取消（取消原因：出貨前取消（買家））、賣家取消（出貨前取消（賣家））皆成功且刊登回到「上架中」；「運送中」及之後被拒絕；非當事人被拒絕
- [ ] T069 [P] [US6] 在 `apps/orders/tests/test_dispute.py` 測試 OP-20：「待確認收貨」時買家提出爭議（原因與 1 張證據照片）後訂單變「爭議處理中」；其他狀態被拒絕；賣家不能提出；證據照片不符 `validate_image` 被拒絕

### Implementation for User Story 6

- [ ] T070 [US6] 在 `apps/orders/models.py` 建立 `Dispute`：`order`（OneToOne，「一筆訂單最多一筆爭議」）、`reason`、`ruling`（choices：賣家有理、買家有理，「裁決前為空」）、`ruled_by`（FK User，可為空）、`ruled_at`（可為空）；以及 `DisputeEvidence`：`dispute`（FK）、`image`（「照片，規則同刊登照片」：1 到 5 張，套用 `validate_image`）；產生 migration
- [ ] T071 [US6] 在 `apps/orders/services.py` 實作 `cancel_order(order, user, now)` 與 `open_dispute(order, buyer, reason, photos, now)`，皆透過 `apply_event`
- [ ] T072 [US6] 在 `apps/orders/forms.py` 建立 `DisputeForm`（原因、證據照片 1 到 5 張）
- [ ] T073 [US6] 在 `apps/orders/views.py`、`apps/orders/urls.py` 加入 `orders/<id>/cancel/`、`orders/<id>/dispute/`，並建立範本 `templates/orders/cancel_confirm.html`、`dispute_form.html`

**Checkpoint**: T068、T069 通過

---

## Phase 9: User Story 7 - 管理後台 (Priority: P1)

**Goal**: 管理員在後台管理資料、裁決爭議、下架刊登、停權、執行刪除帳號，並留下操作紀錄

**Independent Test**: 以 `createsuperuser` 建立的管理員對每一類資料各做一次操作，再查看操作紀錄

### Tests for User Story 7

- [ ] T074 [P] [US7] 在 `apps/backoffice/tests/test_access.py` 測試 OP-22：一般使用者開啟 `/admin/` 被拒絕；管理員可進入
- [ ] T075 [P] [US7] 在 `apps/backoffice/tests/test_ruling.py` 測試 OP-24：爭議頁面顯示刊登照片、爭議證據與該刊登的站內訊息；裁決賣家有理 → 訂單完成、刊登已售出；裁決買家有理 → 已取消（取消原因：爭議裁決買家有理）、刊登上架中；記錄裁決者與時間；各寫入一筆 `AdminLog`
- [ ] T076 [P] [US7] 在 `apps/backoffice/tests/test_admin_actions.py` 測試 OP-25 至 OP-27：下架「上架中」刊登成功、其他狀態被拒絕；停權後該使用者無法登入；有進行中訂單（待出貨、運送中、待確認收貨、爭議處理中）時執行刪除被拒絕，沒有時刪除成功（AI-09）；每個操作都寫入 `AdminLog`
- [ ] T077 [P] [US7] 在 `apps/backoffice/tests/test_admin_log_coverage.py` 測試：在後台新增、修改、刪除使用者、刊登、訂單、爭議時，都寫入 `AdminLog`（FR-030）

### Implementation for User Story 7

- [ ] T078 [US7] 在 `apps/backoffice/admin_base.py` 建立 `LoggedModelAdmin`：覆寫 `log_addition`、`log_change`、`log_deletion`，在 Django 內建紀錄之外同時呼叫 `record_admin_action`（research R-06）
- [ ] T079 [US7] 在 `apps/accounts/admin.py` 註冊 `User`（繼承 `LoggedModelAdmin`）：清單顯示 Email、暱稱、角色、驗證狀態、停權狀態、刪除帳號申請時間；動作「停權」與「執行刪除帳號申請」（後者在有進行中訂單時拒絕並顯示原因），皆寫入 `AdminLog`
- [ ] T080 [US7] 依 Q-02「保留紀錄，使用者欄位設為空並顯示『已刪除的使用者』」，將 `Order.buyer`、`Order.seller`、`Review.reviewer`、`Review.reviewee`、`Message.sender`、`Message.recipient`、`Dispute.ruled_by`、`AdminLog.actor`、`Listing.seller` 設為 `null=True, on_delete=SET_NULL`，範本中為空時顯示「已刪除的使用者」；執行刪除前，將該使用者「上架中」的刊登改為「已下架」；`Favorite.user`、`Notification.recipient` 隨帳號刪除（`CASCADE`）；產生 migration
- [ ] T081 [P] [US7] 在 `apps/catalog/admin.py` 註冊 `Book`、`Listing`（繼承 `LoggedModelAdmin`），`Listing` 加上動作「下架」（只允許「上架中」）
- [ ] T082 [P] [US7] 在 `apps/orders/admin.py` 註冊 `Order`、`Shipment`、`Review`（繼承 `LoggedModelAdmin`；訂單狀態欄位唯讀，狀態只能透過 `apply_event` 變更）
- [ ] T083 [US7] 在 `apps/orders/admin.py` 註冊 `Dispute`（繼承 `LoggedModelAdmin`）：詳情頁顯示刊登照片、爭議證據、該刊登的站內訊息（US8 尚未完成時顯示「無訊息」）；動作「裁決賣家有理」「裁決買家有理」，透過 `apply_event` 並記錄裁決者、時間，寫入 `AdminLog`
- [ ] T084 [US7] 在 `apps/backoffice/admin.py` 註冊 `AdminLog` 為唯讀（不能新增、修改、刪除）

**Checkpoint**: T074 至 T077 通過；quickstart 情境 4、5 可完成。US1 至 US7 完成即達成所有必做模組

---

## Phase 10: User Story 8 - 針對刊登提問的站內訊息 (Priority: P2)

**Goal**: 使用者可針對刊登傳訊息給賣家，賣家回覆

**Independent Test**: 假買家對一筆刊登提問，假賣家回覆，雙方都看得到訊息紀錄

### Tests for User Story 8

- [ ] T085 [P] [US8] 在 `apps/messaging/tests/test_messages.py` 測試 OP-28：買家傳訊息給刊登的賣家；賣家回覆給提問者；訊息記錄刊登、寄件者、收件者、內容、時間；未登入被拒絕；只有寄件者與收件者看得到

### Implementation for User Story 8

- [ ] T086 [US8] 在 `apps/messaging/models.py` 建立 `Message`：`listing`（FK）、`sender`、`recipient`（FK User）、`content`、`created_at`；產生 migration
- [ ] T087 [US8] 在 `apps/messaging/views.py`、`apps/messaging/urls.py` 實作 `listings/<id>/messages/`：依登入者列出相關訊息並可送出新訊息（買家送給賣家；賣家選擇回覆對象）
- [ ] T088 [P] [US8] 建立範本 `templates/messaging/thread.html`，並在 `listing_detail.html` 加上訊息連結

**Checkpoint**: T085 通過；T083 的爭議頁面顯示站內訊息

---

## Phase 11: User Story 9 - 收藏書目與到貨通知 (Priority: P2)

**Goal**: 收藏書目並開啟通知；同書目有新刊登時產生站內通知

**Independent Test**: 使用者 C 收藏書目並開啟通知，B 上架同書目，C 看到一則站內通知

### Tests for User Story 9

- [ ] T089 [P] [US9] 在 `apps/favorites/tests/test_favorites.py` 測試 OP-29：收藏書目成功；重複收藏被拒絕；可切換是否通知
- [ ] T090 [P] [US9] 在 `apps/favorites/tests/test_notifications.py` 測試 OP-30、OP-31：新刊登上架時，為每位開啟通知的收藏者建立一則通知；關閉通知者不建立；查看通知頁後標為已讀

### Implementation for User Story 9

- [ ] T091 [US9] 在 `apps/favorites/models.py` 建立 `Favorite`：`user`、`book`（FK）、`notify`（是否通知）；`UniqueConstraint(user, book)`（「同一使用者對同一書目只能收藏一次」）；以及 `Notification`：`recipient`（FK User）、`listing`（FK）、`content`、`created_at`、`is_read`；產生 migration
- [ ] T092 [US9] 在 `apps/favorites/receivers.py` 訂閱 `listing_published`，為收藏該書目且 `notify=True` 的使用者建立 `Notification`；在 `apps/favorites/apps.py` 的 `ready()` 載入
- [ ] T093 [US9] 在 `apps/favorites/views.py`、`apps/favorites/urls.py` 實作 `favorites/`（列表、切換通知、取消收藏）、收藏書目（從刊登詳情或書籍頁送出）、`notifications/`（列出並標為已讀）
- [ ] T094 [P] [US9] 在 `apps/favorites/context_processors.py` 提供未讀通知數，顯示在 `templates/base.html` 導覽列；建立範本 `templates/favorites/favorite_list.html`、`notification_list.html`

**Checkpoint**: T089、T090 通過；quickstart 情境 6 可完成

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: 文件、展示資料與整體驗收

- [ ] T095 [P] 撰寫 `README.md`：專案說明、依 quickstart 的啟動步驟、執行測試、期限處理指令、Email 驗證信的位置
- [ ] T096 [P] 在 `apps/backoffice/management/commands/seed_demo_data.py` 建立展示用假資料：測試買家A、測試賣家B、測試買家C（Email 皆為 `@example.com`、已驗證），數本虛構 ISBN 的書目與刊登
- [ ] T097 逐頁以手機寬度（375px）檢查所有範本可完成操作，修正 `static/css/site.css`（NFR-009）
- [ ] T098 確認 `DEBUG`、`SECRET_KEY` 只從 `.env` 讀取，repo 中沒有 `.env`、`db.sqlite3`、`media/`、`sent_emails/`（constitution 資料安全）
- [ ] T099 執行 `uv run python manage.py test`，全部通過
- [ ] T100 依 [quickstart.md](quickstart.md) 走完 6 個驗收情境，記錄結果

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup（Phase 1）**：沒有依賴
- **Foundational（Phase 2）**：依賴 Setup，完成前不能開始任何 User Story
- **US1 至 US9（Phase 3 至 11）**：依賴 Foundational
- **Polish（Phase 12）**：依賴所有 User Story

### User Story Dependencies

| Story | 依賴 | 原因 |
| --- | --- | --- |
| US1 帳號 | Foundational | — |
| US2 上架 | US1 | 需要已驗證的使用者 |
| US3 瀏覽 | US2 | 需要書目與刊登模型 |
| US4 交易 | US2 | 需要刊登模型；可與 US3 平行 |
| US5 評價 | US4 | 需要訂單完成 |
| US6 取消與爭議 | US4 | 需要訂單與轉換表；可與 US5 平行 |
| US7 後台 | US4、US6 | 裁決需要爭議；下架需要刊登 |
| US8 訊息 | US2 | 需要刊登；完成後補上 US7 爭議頁的訊息顯示 |
| US9 收藏與通知 | US2 | 訂閱 `listing_published` 訊號 |

### Within Each User Story

- 測試先寫，確認失敗後再實作
- 模型 → migration → 服務函式 → 頁面與網址 → 範本

### Parallel Opportunities

- Setup：T003、T004、T005
- Foundational：T010、T011、T012、T013、T014、T016、T017
- 每個 User Story 中標示 [P] 的測試可同時撰寫
- US2 完成後：US3、US4、US8、US9 可平行；US4 完成後：US5、US6 可平行

---

## Parallel Example: User Story 4

```bash
# 同時撰寫 US4 的測試：
Task: "apps/orders/tests/test_transitions.py"
Task: "apps/orders/tests/test_place_order.py"
Task: "apps/orders/tests/test_fulfilment.py"
Task: "apps/orders/tests/test_deadlines.py"
Task: "apps/orders/tests/test_recipient_info.py"
```

---

## Implementation Strategy

### MVP First

1. 完成 Phase 1、Phase 2
2. 完成 US1 至 US4：可以上架、搜尋、下單、出貨、收貨
3. **停下來驗收**：quickstart 情境 1 的步驟 1 至 6

### Incremental Delivery 與 PR 切分

依 constitution v2.0.0 原則 IV，Implement 階段分成多個 PR，每個 PR 由人類 review 程式碼後 merge：

| PR | 內容 | 驗收 |
| --- | --- | --- |
| Implement-1 | Phase 1、2 | Foundational 測試通過 |
| Implement-2 | US1 | US1 測試通過 |
| Implement-3 | US2、US3 | US2、US3 測試通過 |
| Implement-4 | US4 | US4 測試通過；情境 1 步驟 1 至 6 |
| Implement-5 | US5、US6 | US5、US6 測試通過 |
| Implement-6 | US7 | US7 測試通過；必做模組全部完成 |
| Implement-7 | US8、US9 | US8、US9 測試通過 |
| Implement-8 | Polish | 全部測試通過；quickstart 6 個情境 |

---

## 待確認事項與判定結果

產生 tasks 時發現兩處 spec 與 plan 沒有寫清楚的地方，由 agent 提出建議（AI 推測），人類於 2026-11-10 判定照建議採用，並已寫回 spec 與 data-model：

| 編號 | 問題 | 採用的做法 | 影響的工作 |
| --- | --- | --- | --- |
| Q-01 | 搜尋結果要包含哪些狀態的刊登？ | 只列出「上架中」 | T042、T044 |
| Q-02 | 管理員刪除帳號後，該使用者的歷史訂單、評價、訊息怎麼處理？ | 保留紀錄，使用者欄位設為空並顯示「已刪除的使用者」 | T080 |

---

## Notes

- [P] 表示不同檔案、沒有依賴，可平行進行
- [Story] 對應 spec 的 User Story
- 每個 User Story 完成後都可以單獨測試
- 實作不得超出已核准的 spec、plan 與 tasks（constitution v2.0.0 原則 I）

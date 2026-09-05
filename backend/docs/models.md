# Models 與資料庫 Migration

本專案使用 Flask-SQLAlchemy 定義資料模型，並透過 Flask-Migrate / Alembic 管理資料庫 schema 版本。Model 是應用程式看到的資料結構；migration 是把資料庫一步一步升級到相同結構的版本紀錄。兩者要一起維護，不能只改其中一邊。

目前開發主線是 `integration`。修改資料表前，先確認分支和遠端同步：

```powershell
git fetch origin
git status --short --branch
```

`integration...origin/integration` 沒有 `behind` 才是最新。若本地有別人的未提交修改，先不要順手一起 commit。

## 目前 Table 設計

### 使用者與配對

| Table | Model | 用途 |
|---|---|---|
| `users` | `User` | LINE 身分、角色、語言、onboarding 狀態，以及一對一雇主/看護配對 |
| `care_recipients` | `CareRecipient` | 被照顧者資料，由雇主建立，可指派給看護 |
| `invites` | `Invite` | 雇主產生給看護的邀請連結，連結可直接建立看護 session |

`users.role` 只有 `owner` 和 `nurse`。前端會顯示成雇主/看護，但後端和資料庫都用這兩個值。

`users.pair_user_id` 是 self foreign key，用來保存目前 MVP 的一對一配對。`owner.paired_user` 指向看護，`nurse.paired_user` 指向雇主。這不是多家庭成員設計；之後若要多人共享照護，需要新增關聯表，而不是塞更多欄位進 `users`。

`users.onboarded_at` 是登入流程的完成章。`NULL` 表示前端還要帶使用者走 onboarding；不是用 `name` 是否存在來判斷，因為 LINE Login 建帳號時可能已經帶入顯示名稱。

`invites.code` 是看護邀請連結的 credential，所以必須保持不可猜測。雇主目前只會拿到一個 active invite；重複建立會回傳原本那筆。看護打開 `/auth/invite/:code` 後，後端會把 invite 綁到 nurse，開 session，並與 owner 配對。

### 照護紀錄

| Table | Model | 用途 |
|---|---|---|
| `care_schedules` | `CareSchedule` | Tab 01 排程表，分 weekday/weekend |
| `vital_sign_logs` | `VitalSignLog` | Tab 01 生命徵象紀錄，單位由後端決定 |
| `diaries` | `Diary` | Tab 02 私密日記與分享日記 |
| `notes` | `StickyNote` | Tab 04 交流板便利貼 |

`care_schedules` 和 `vital_sign_logs` 都同時指向 `care_recipients.id` 與建立者 `users.id`。這讓資料能回答兩件事：這筆紀錄屬於哪位被照顧者，以及是誰建立的。

`diaries.is_private=true` 的日記才會進高壓偵測；分享出去的日記不呼叫模型。`diaries.ai_analysis` 是後台欄位，只記 `normal` / `emergency` 這類工程狀態，不在日記 API 回應中顯示給看護。

`notes.is_private` 表示便利貼是否只給自己看。`notes.images` 是 JSON array，存圖片 URL 或 metadata；圖片檔本身不進資料庫。

### Chat 與壓力事件

| Table | Model | 用途 |
|---|---|---|
| `care_agents` | `CareAgent` | 看護一次性建檔結果、baseline、guardrail、模型生成的照護摘要 |
| `chat_rooms` | `ChatRoom` | Tab 03 每個對話主題/房間 |
| `chat_messages` | `ChatMessage` | 單則使用者或 AI 訊息 |
| `stress_events` | `StressEvent` | 高壓事件計數與推播節流，不保存使用者原文 |

`care_agents.user_id` 指向看護，`care_agents.care_recipient_id` 指向被照顧者。這個欄位是必要的：AI 生成的照護 context、歡迎語、以及抽取後寫入排程/生命徵象都需要知道是哪位被照顧者。

`chat_rooms.care_agent_id` 指向對應 agent，`chat_messages.room_id` 指向房間。`chat_messages.sender` 只能是 `user` 或 `ai`。

`stress_events` 只記「有事件、來源、時間、是否已通知」，刻意不存日記或聊天室內容，也不外鍵回 `diaries` / `chat_messages`。這是隱私邊界：雇主收到的是異常筆數與建議行動，不是看護寫了什麼。

## Model 檔案位置

所有 model 都在 `backend/app/models/`，目前是扁平檔案：

| File | 主要 Models |
|---|---|
| `user.py` | `User`, `CareRecipient` |
| `invite.py` | `Invite` |
| `diary.py` | `Diary` |
| `sticky_note.py` | `StickyNote` |
| `care_schedule.py` | `CareSchedule` |
| `vital_sign_log.py` | `VitalSignLog` |
| `chat.py` | `CareAgent`, `ChatRoom`, `ChatMessage` |
| `stress_event.py` | `StressEvent` |

新增 model 後，必須在 `backend/app/models/__init__.py` 匯入並放進 `__all__`。Flask-Migrate 是從 SQLAlchemy metadata 偵測 schema，如果忘記匯入，`db migrate` 可能會顯示 `No changes in schema detected`。

## Migration 工作流程

### 1. 設定本機資料庫

第一次開發先建立 `.env`：

```powershell
Copy-Item .env.example .env
```

常見設定：

```env
DB_SERVER=127.0.0.1
DB_USER=root
DB_NAME=hackathon
DB_PASSWORD=your_password
```

`DB_SERVER` 可以包含 port，例如 `127.0.0.1:3307`。`.env` 不要 commit。

安裝依賴：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. 不要重新 init

`migrations/` 已經存在並且要提交到 Git。一般開發不要再跑：

```powershell
flask db init
```

只在全新專案、沒有 `migrations/` 目錄時才需要 init。

### 3. 先套到最新版

產生新 migration 前，先讓資料庫到目前 head：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
.\.venv\Scripts\python.exe -m flask --app main db current
.\.venv\Scripts\python.exe -m flask --app main db heads
```

如果 `db current` 不是 head，先不要 `db migrate`。否則 Alembic 很容易把別人的變更混進你的 migration。

### 4. 改 model 並產生 migration

修改 `backend/app/models/*.py` 後執行：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db migrate -m "describe schema change"
```

`db migrate` 只會產生 `backend/migrations/versions/*.py`，不會直接修改資料庫。

### 5. 人工檢查版本檔

Autogenerate 不是保證正確。每次都要打開新 migration 檢查：

- `down_revision` 是否接在目前 head 後面。
- `upgrade()` 是否只包含這次 feature 需要的 table/column/index/constraint。
- 是否誤把 rename 判斷成 drop + create。
- 是否新增 `nullable=False` 欄位但沒有 server default 或 backfill。
- foreign key、unique、index、check constraint 是否與 model 一致。
- `downgrade()` 是否能安全反向執行。
- 是否重複建立已存在的 table，例如 `invites`。


### 6. 套用並測試

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
python -m pytest
```

若只改前端，不需要新的 migration。若 API 行為依賴新欄位或新 table，model、migration、測試要在同一個 PR/commit 裡一起出現。

### 7. Commit 規則

只 stage 這次 schema 相關檔案：

```powershell
git add backend/app/models backend/migrations/versions backend/tests
git status --short
git commit -m "feat: describe schema change"
```

如果工作樹有別人的檔案，例如 `CLAUDE.md` 或其他未追蹤檔，不要順手加進去。

## 多人協作與多個 Heads

多人同時產生 migration 時，可能會出現多個 heads：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db heads
```

處理方式：

1. 先 `git fetch origin` 並 rebase/merge 最新 `integration`。
2. 確認兩邊 migration 都是必要且內容不重複。
3. 如果真的是兩條合法分支，建立 merge revision：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db merge heads -m "merge migration heads"
```

不要用刪 migration、改舊 revision id、或手動改資料庫版本表來硬解。這會讓其他人的資料庫更難升級。

## 常見問題

### `No changes in schema detected`

通常是新 model 沒有匯入 `backend/app/models/__init__.py`，或 app factory 沒有載入該 model。先檢查匯入，再重跑 `db migrate`。

### `Target database is not up to date`

資料庫尚未套到目前 head。先執行：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
```

### `Table already exists`

通常是 migration 重複 create table，或資料庫曾被手動建表。先檢查新 migration 是否包含不屬於這次的表。以目前專案來說，`invites` 已經有自己的 migration，新的 chat/stress migration 不該再碰它。

### MySQL `Access denied` 或 `Unknown database`

檢查 `.env` 的 `DB_SERVER`、`DB_USER`、`DB_PASSWORD`、`DB_NAME`。Flask-Migrate 不會自動建立 MySQL database，必要時先手動建立 DB，再跑 `db upgrade`。

### 需要回退 migration

```powershell
.\.venv\Scripts\python.exe -m flask --app main db downgrade -1
```

回退可能刪資料或欄位。共享資料庫、測試資料庫、正式資料庫操作前，先確認 `downgrade()` 內容並備份。

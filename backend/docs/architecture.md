# 系統架構與檔案規劃

這份文件補充 README 的架構圖，重點放在後端多檔案規劃、模組邊界、資料流與未來擴充方式。README 保持給評審快速閱讀；這份文件給開發者接手時看。

## 架構原則

後端採用 Flask App Factory + Blueprint + Service Layer。每個功能模組盡量維持同一種檔案形狀：

```text
app/<feature>/
├── __init__.py      # 建立 Blueprint
├── routes.py        # HTTP endpoint，只處理 request/response
├── schemas.py       # Marshmallow schema，處理輸入輸出格式
└── service.py       # 商業邏輯、資料庫操作、外部服務呼叫
```

Model 集中在 `app/models/`，不是每個 feature 各自放 model。這樣 Alembic 可以從單一 SQLAlchemy metadata 偵測 schema，也比較容易看出 table 之間的關聯。

共用邏輯放 `app/shared/`，例如錯誤類型與 API response envelope。不要讓 feature module 互相 import route；若需要跨功能協作，應該呼叫對方的 service function。

## 目錄設計

```text
backend/
├── app/
│   ├── __init__.py              # create_app(), blueprint 註冊, error handlers
│   ├── config.py                # 環境變數與 Flask 設定
│   ├── extensions.py            # db, migrate, session extension
│   ├── auth/                    # session、LINE Login、目前登入使用者
│   ├── users/                   # 使用者建立、onboarding、配對
│   ├── invites/                 # 雇主邀請看護連結
│   ├── care_recipients/         # 被照顧者
│   ├── care_schedules/          # Tab 01 排程
│   ├── vital_signs/             # Tab 01 生命徵象
│   ├── diaries/                 # Tab 02 日記
│   ├── chat/                    # Tab 03 Care Agent 與聊天室
│   ├── sticky_notes/            # Tab 04 交流板便利貼
│   ├── stress_signals/          # 壓力事件判定與紀錄
│   ├── line/                    # LINE webhook、rich menu、push notification
│   ├── uploads/                 # 圖片上傳
│   ├── models/                  # SQLAlchemy models
│   └── shared/                  # 共用錯誤、response helper
├── migrations/                  # Alembic migration chain
├── tests/                       # pytest
├── docs/
│   ├── api.md                   # API contract
│   ├── models.md                # table design 與 migration 流程
│   ├── module-map.md            # 開發交接與任務地圖
│   └── architecture.md          # 本文件
└── main.py                      # Flask entrypoint
```

## 模組邊界

| 模組 | 負責 | 不負責 |
| --- | --- | --- |
| `auth/` | session、LINE Login OAuth flow、讀取目前登入者 | 邀請碼綁定、使用者 onboarding 表單內容 |
| `users/` | 使用者資料、角色、配對、onboarding 完成章 | LINE webhook、邀請連結產生 |
| `invites/` | 雇主產生 invite、看護接受 invite、建立 owner/nurse 配對 | 一般 LINE Login、雇主 LINE 訊息互動 |
| `care_recipients/` | 被照顧者 CRUD 與 owner/nurse 權限 | 排程與生命徵象的細節邏輯 |
| `care_schedules/` | 排程 CRUD、weekday/weekend 規則 | AI 抽取文字 |
| `vital_signs/` | 生命徵象紀錄、單位決策、dashboard summary | 前端圖表渲染 |
| `diaries/` | 日記 CRUD、私密/分享判斷、觸發壓力偵測 | 直接推播 LINE 訊息內容 |
| `chat/` | Care Agent、baseline、聊天室、訊息回覆 | LINE webhook、長期通知排程 |
| `stress_signals/` | 高壓判定、`StressEvent` 紀錄、通知節流協調 | 保存使用者原文 |
| `line/` | LINE webhook、LINE push、雇主端訊息格式 | 看護端 session 與 app routing |
| `uploads/` | 檔案驗證、儲存、回傳 URL | 圖片分析或 OCR |

## 後端資料流

### 1. LINE Login

```text
Frontend RoleSelectView
  -> POST /api/auth/line/start
  -> LINE consent page
  -> GET /api/auth/line/callback
  -> backend opens session
  -> frontend /auth/callback loads /api/auth/session
  -> route to onboarding or dashboard
```

`auth/service.py` 只負責 LINE identity 與 session。是否需要 onboarding 由 `users.onboarded_at` 決定，前端不自行猜測。

### 2. Invite Flow

```text
Owner session
  -> POST /api/invites
  -> invite_url = /auth/invite/:code

Caregiver opens invite URL
  -> frontend AcceptInviteView
  -> POST /api/invites/<code>/enter
  -> backend creates/reuses nurse and pairs owner
  -> session opened
  -> route to caregiver onboarding or dashboard
```

邀請連結本身就是看護進入系統的 credential，因此 `Invite.code` 必須不可猜測，不能改回短碼。

### 3. Diary Stress Detection

```text
POST /api/diaries
  -> diaries/service.py saves Diary
  -> if is_private=True
       stress_signals/service.py analyzes text
       if high stress: create StressEvent
       line/notifications.py may push aggregate alert
  -> return diary response without ai_analysis
```

分享出去的日記不做 AI 壓力偵測。`StressEvent` 不保存日記內容，也不連回原始日記，避免雇主或後台流程反推出私密文字。

### 4. Chat Message Flow

```text
POST /api/chat/rooms
  -> create ChatRoom
  -> create first AI welcome message

POST /api/chat/rooms/<id>/messages
  -> save user ChatMessage
  -> call Gemini for AI reply
  -> save AI ChatMessage
  -> run stress signal analysis
  -> extract care facts into schedules/vital signs when applicable
```

聊天主流程不能因為壓力分析、照護資訊抽取或 LINE 推播失敗而整個失敗。這些附加流程應該記 log 並降級，讓看護端對話保持可用。

## Model 與 Table 規劃

資料表設計細節放在 [models.md](models.md)。這裡只列主要分群：

| 分群 | Tables |
| --- | --- |
| 身分與配對 | `users`, `care_recipients`, `invites` |
| 照護紀錄 | `care_schedules`, `vital_sign_logs` |
| 日記與交流板 | `diaries`, `notes` |
| Care Agent | `care_agents`, `chat_rooms`, `chat_messages` |
| 安全訊號 | `stress_events` |

新增 table 時要同時更新：

- `app/models/*.py`
- `app/models/__init__.py`
- `migrations/versions/*.py`
- 對應 service tests
- `docs/models.md`

## Migration 設計

Migration 的詳細流程放在 [models.md](models.md)。這裡記住三個設計規則：

1. Model 變更和 migration 要在同一個 commit 或 PR。
2. Autogenerate 後一定要人工檢查，避免重複建表、誤判 rename、或新增沒有 default 的 NOT NULL 欄位。
3. 多人同時產生 migration 時，用 Alembic merge revision 解多個 heads，不要手動改資料庫版本表。

目前重要注意事項：

- `invites` 已由 `d4e5f6a7b8c9_add_invites.py` 建立。
- `e46351fe0391_update_4_tables.py` 只負責 `stress_events`、`care_agents`、`chat_rooms`、`chat_messages`。
- `b2c3d4e5f6a7_align_diary_and_note_tables_with_models.py` 是 drift repair migration，已改成會先檢查 table/column/index 存在與否，避免乾淨 DB 從頭跑時失敗。

## 外部服務邊界

| 服務 | 封裝位置 | 原則 |
| --- | --- | --- |
| LINE Login | `app/auth/line_client.py` | 只處理 OAuth identity，不混入 invite 邏輯 |
| LINE Messaging API | `app/line/` | 雇主端通知通道，不接觸看護私密原文 |
| Google Gemini | `app/chat/client.py`, `app/stress_signals/` | 模型錯誤要可降級，不讓主要寫入流程崩潰 |
| MySQL | `app/models/`, `migrations/` | schema 變更必須經 migration |

## 新功能落點指南

| 想新增的功能 | 優先放置位置 |
| --- | --- |
| 新登入方式 | `app/auth/`，必要時搭配 `app/users/` |
| 新邀請規則 | `app/invites/` |
| 多家屬/多看護權限 | 新增關聯 model，不要硬塞 `users.pair_user_id` |
| 新 Care Agent prompt | `app/chat/prompts.py` |
| 新 AI 判定流程 | `app/stress_signals/` 或獨立 service，再由 feature service 呼叫 |
| 新 LINE rich menu action | `app/line/` |
| 新資料表 | `app/models/` + Alembic migration |

## 測試規劃

每個 feature 至少要有 route/service 層測試。建議測試分工如下：

| 測試檔 | 覆蓋重點 |
| --- | --- |
| `tests/test_auth*.py` | session、LINE Login callback、onboarding routing data |
| `tests/test_invites.py` | invite 建立、接受邀請、配對、session |
| `tests/test_diaries*.py` | 日記 CRUD、私密日記壓力偵測 |
| `tests/test_chat*.py` | Care Agent、baseline、聊天室、訊息流程 |
| `tests/test_line*.py` | webhook 驗證、通知格式 |
| `tests/test_*models.py` | model constraints 與 relationship |

外部 AI live test 預設應跳過，使用明確環境變數開啟，避免 CI 或本機測試不小心消耗 quota。

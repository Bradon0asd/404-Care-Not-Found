# 後端 API 功能清單

`backend` 分支目前實作的所有端點。本檔由程式碼實況整理，新增或修改 route 時請一併更新。

線上互動版：`GET /api/docs/swagger`（OpenAPI JSON 在 `GET /api/docs/openapi.json`）。

## 通用約定

- 所有 API 前綴 `/api`。
- 成功回應：`{"success": true, "data": ...}`，部分端點另有 `message` / `meta`。
- 失敗回應：`{"success": false, "error": {"code": "...", "message": "...", "details": ...}}`。
- 身分驗證兩種擇一（見 `app/auth/current_user.py`）：
  - **Session cookie**：Web App 走這條，登入後由 cookie 帶身分。
  - **`X-User-Id` header**：給 Swagger 與沒有 cookie jar 的腳本用，值為 user id。
- 下表「身分」欄：`session` = 需要登入身分；`公開` = 不需要；`LINE 簽章` = 驗 `X-Line-Signature`。

## 系統

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/health` | 健康檢查 | 公開 |
| GET | `/api/docs/swagger` | Swagger UI | 公開 |
| GET | `/api/docs/openapi.json` | OpenAPI 規格 | 公開 |
| GET | `/uploads/<filename>` | 取用已上傳的圖片 | 公開 |

## 帳號與登入

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| POST | `/api/auth/login` | 用 `line_id` 開 session（body：`line_id`） | 公開 |
| POST | `/api/auth/logout` | 結束 session | 公開 |
| GET | `/api/auth/session` | 讀目前 session 使用者 | session |
| POST | `/api/auth/line/start` | 依角色產生 LINE Login 授權網址（body：`role` = `owner` / `nurse`） | 公開 |
| GET | `/api/auth/line/callback` | LINE Login 導回，開 session 後 redirect 回前端 | 公開 |
| POST | `/api/users` | 建立使用者（body：`line_id`、`name`、`language`、`role`） | 公開 |
| GET | `/api/users/me` | 讀目前登入使用者 | session |
| POST | `/api/users/me/onboarding` | 完成一次性設定表單（body：`name`、`language`），蓋上 `onboarded_at` | session |
| GET | `/api/users/<user_id>` | 讀單一使用者 | 公開 |
| POST | `/api/users/<user_id>/pair` | 配對雇主與看護（body：`pair_user_id`） | 公開 |
| DELETE | `/api/users/<user_id>/pair` | 解除配對 | 公開 |

角色只有 `owner`（雇主）與 `nurse`（看護）。LINE 官方帳號來的使用者一律建成 `owner`，因為 LINE 是雇主端通道。

LINE Login callback 一律以 redirect 收尾（使用者的瀏覽器在那裡），成功導到 `LINE_LOGIN_SUCCESS_PATH`，失敗把錯誤碼放 query string 導到 `LINE_LOGIN_FAILURE_PATH`。

`/api/auth/session`、`/api/users/me` 與 `/api/users/me/onboarding` 都回一個 `needs_onboarding` 布林，由 `users.onboarded_at` 是否為 `NULL` 算出來。**前端不自行判斷是否註冊過**——LINE 登入建帳號時就會寫入顯示名稱，前端看得到的欄位沒有一個能代表新帳號。被邀請的看護填完 `/api/invites/<code>/profile` 也會蓋同一個章。

## 邀請連結（雇主邀看護，看護免註冊）

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| POST | `/api/invites` | 建立或取回雇主的邀請連結，回傳 `code` 與 `invite_url` | session（限 owner） |
| POST | `/api/invites/<code>/enter` | 看護開連結即取得身分，回傳 `needs_profile` | 公開 |
| POST | `/api/invites/<code>/profile` | 首次進入時補資料（body：`name`、`language`） | 公開 |

## 被照顧者

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/care-recipients` | 列出可存取的被照顧者 | session |
| POST | `/api/care-recipients` | 建立（body：`name`） | session |
| GET | `/api/care-recipients/<id>` | 讀單筆 | session |
| PATCH | `/api/care-recipients/<id>` | 更新（body：`name`） | session |

看護必須先與雇主配對才能建立被照顧者，否則回 `CARE_RECIPIENT_OWNER_REQUIRED`。

## Tab01 照護紀錄

### 排程表

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/care-recipients/<id>/schedules` | 列出排程（query：`schedule_type`） | session |
| POST | `/api/care-recipients/<id>/schedules` | 新增排程 | session |
| GET | `/api/schedules/<schedule_id>` | 讀單筆 | session |
| PATCH | `/api/schedules/<schedule_id>` | 更新 | session |
| DELETE | `/api/schedules/<schedule_id>` | 刪除 | session |

排程欄位：`schedule_type`（`weekday` / `weekend`）、`weekday`、`start_time`、`title`、`description`。

### 生命徵象與儀表板

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/care-recipients/<id>/vital-signs` | 列出紀錄（query：`vital_type`、`start_date`、`end_date`） | session |
| POST | `/api/care-recipients/<id>/vital-signs` | 新增一筆紀錄 | session |
| GET | `/api/care-recipients/<id>/dashboard` | 六項指標的儀表板摘要 | session |

`vital_type` 六種：`blood_pressure`、`blood_glucose`、`heart_rate`、`oxygen_saturation`、`temperature`、`respiratory_rate`（血壓用 `value` / `secondary_value` 收縮壓與舒張壓）。

Dashboard 每項指標回 `latest`、`current_average`、`previous_average`、`difference` 與 `change_text`。**只呈現變化，不做醫療判讀**，`change_text` 是「與過去一週相比」這類敘述，後端不回傳異常旗標。

## Tab02 秘密日記

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/diaries` | 列出自己的日記 | session |
| POST | `/api/diaries` | 新增（body：`title`、`content`、`image_url`、`is_private`） | session |
| GET | `/api/diaries/<diary_id>` | 讀單筆 | session |
| PATCH | `/api/diaries/<diary_id>` | 更新 | session |
| DELETE | `/api/diaries/<diary_id>` | 刪除 | session |

`is_private` 預設 `true`（僅自己），對應「日記預設全封閉」的鐵則。

## Tab03 跟我聊聊（樹洞）

### 建檔模式（一次性）

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/chat/agent` | 讀取已建立的 Care Agent | session |
| POST | `/api/chat/agent` | 建立或更新 Agent（body：`care_recipient_id`、`system_prompt`、`temperature`、`guardrail`） | session |
| GET | `/api/chat/agent/baseline` | 取得一次性的開場問句 | session |
| POST | `/api/chat/agent/baseline` | 儲存一次性作答（body：`answers`） | session |

`POST /api/chat/agent` 會呼叫模型生成照護 context／每日提醒／照護 tips／風險訊號四項，存進 `generated_profile` 之後每天複用，不重複生成。`temperature` 限 0–2。免費版一人一個 Agent，超過回 `CARE_AGENT_LIMIT_REACHED`。

`guardrail` 不是存起來就算，它每次對話都會併進 system instruction 一起送出。

baseline 問句由 AI 生成成聊天句（「最近有睡飽嗎？」），文案不得出現測驗／檢測字眼。完成後 `baseline_completed_at` 有值，Tab 03 從此走對話模式。

### 對話模式（每天）

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/chat/rooms` | 列出聊天室 | session |
| POST | `/api/chat/rooms` | 開聊天室（body：`title`、`mood_weather`） | session |
| GET | `/api/chat/rooms/<room_id>` | 讀聊天室與其訊息 | session |
| POST | `/api/chat/rooms/<room_id>/messages` | 送出訊息並取得回覆 | session |

`mood_weather` 四種：`sunny`、`cloudy`、`rainy`、`storm`。免費版一天一間，超過回 `CHAT_ROOM_QUOTA_REACHED`；未完成 baseline 就開房回 `BASELINE_REQUIRED`。

送出訊息時，後端在同一次請求裡做三件事，但**回應只含前者**：

1. 印尼語陪伴式回覆（回給看護）
2. 情緒分析 → 判定高壓則寫 `StressEvent` 並推播雇主 LINE
3. 抽取照護事實 → 中文寫入 `CareSchedule` / `VitalSignLog`

**回應永遠不含壓力分數、風險等級或觀察清單**，`ChatMessage` 的欄位只有 `id`、`room_id`、`sender`、`text`、`created_at`。第 2、3 步失敗時靜默略過並記 log，第 1 步失敗時回預先寫好的陪伴語句，**端點一律不因 AI 失敗而回 5xx**。

組 prompt 時只帶存檔的病患摘要加最近 6 則對話，不送完整歷史。

## Tab04 交流板便利貼

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| GET | `/api/notes` | 列出（query：`category`、`priority`、`is_reviewed`） | session |
| POST | `/api/notes` | 新增 | session |
| GET | `/api/notes/<note_id>` | 讀單筆 | session |
| PATCH | `/api/notes/<note_id>` | 更新 | session |
| DELETE | `/api/notes/<note_id>` | 刪除 | session |
| PATCH | `/api/notes/<note_id>/review` | 標記為已讀取 | session |

欄位：`title`、`content`、`category`（`leave` / `family` / `care` / `shopping` / `other`）、`priority`（`urgent` / `normal` / `low`，對應紅／黃／藍）、`images`、`is_private`。

## LINE（雇主端通道）

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| POST | `/api/line/webhook` | 接收 LINE 事件，選單點擊回照護摘要與便利貼 | LINE 簽章 |
| POST | `/api/line/stress-signals` | 推播壓力告知給配對的雇主（body：`abnormal_count`、`occurred_at`） | session |

壓力告知**只傳異常筆數、時間與建議關心方式，絕不含看護寫的任何內容**（`app/line/notifications.py`）。

## 檔案上傳

| 方法 | 路徑 | 說明 | 身分 |
| --- | --- | --- | --- |
| POST | `/api/uploads/image` | 上傳一張圖片（multipart，欄位 `file`），回傳可存取的 URL | session |

## 錯誤碼

| 代碼 | HTTP | 情境 |
| --- | --- | --- |
| `APP_ERROR` | 400 | 未分類的應用錯誤 |
| `VALIDATION_ERROR` | 422 | 請求欄位驗證失敗 |
| `AUTHENTICATION_REQUIRED` | 401 | 沒有有效身分 |
| `PERMISSION_DENIED` | 403 | 身分正確但無權存取該資源 |
| `USER_NOT_FOUND` | 404 | 找不到使用者 |
| `USER_ALREADY_EXISTS` | 409 | `line_id` 重複 |
| `USER_PAIRING_ERROR` | 400 | 配對條件不符 |
| `ROLE_MISMATCH` | 409 | 登入角色與既有帳號角色不符 |
| `INVITE_NOT_FOUND` | 404 | 邀請碼不存在 |
| `INVITE_REVOKED` | 410 | 邀請碼已失效 |
| `CARE_RECIPIENT_NOT_FOUND` | 404 | 找不到被照顧者 |
| `CARE_RECIPIENT_OWNER_REQUIRED` | 400 | 看護尚未與雇主配對 |
| `CARE_SCHEDULE_NOT_FOUND` | 404 | 找不到排程 |
| `DIARY_NOT_FOUND` | 404 | 找不到日記 |
| `STICKY_NOTE_NOT_FOUND` | 404 | 找不到便利貼 |
| `INVALID_UPLOAD` | 400 | 上傳檔案不合法 |
| `LINE_NOT_CONFIGURED` | 503 | 缺 Messaging API 環境變數 |
| `INVALID_LINE_SIGNATURE` | 400 | webhook 簽章驗證失敗 |
| `LINE_RECIPIENT_NOT_PAIRED` | 400 | 找不到可推播的雇主 |
| `LINE_LOGIN_NOT_CONFIGURED` | 503 | 缺 LINE Login 環境變數 |
| `LINE_LOGIN_FAILED` | 400 | LINE Login 流程失敗 |
| `GOOGLE_AI_NOT_CONFIGURED` | 503 | 缺 Gemini 金鑰 |
| `GOOGLE_AI_API_ERROR` | 502 | Gemini 呼叫失敗 |
| `CARE_AGENT_NOT_FOUND` | 404 | 尚未建立 Care Agent |
| `CARE_AGENT_LIMIT_REACHED` | 409 | 超過方案允許的 Agent 數 |
| `CHAT_ROOM_NOT_FOUND` | 404 | 找不到聊天室 |
| `CHAT_ROOM_QUOTA_REACHED` | 429 | 超過當日聊天室數上限 |
| `BASELINE_REQUIRED` | 409 | 尚未完成一次性建檔 |

## 尚未實作

- **Tab03 的 migration 還沒產出**：`care_agents`、`chat_rooms`、`chat_messages`、`stress_events` 四張表已在 model 與測試中，但因 `1b2c3d4e5f6a` 的 `down_revision` 指向不存在的 revision，Alembic 無法運作，尚未建到共用資料庫。
- **印尼語語音辨識（ASR）已擱置**，不在本次範圍；Tab03 的輸入為文字。
- 日記的 `ai_analysis` 欄位已在 model 與 migration 中，但 `DiarySchema` 還沒輸出。
- Tab05 訂閱方案、語音辨識、翻譯尚無端點。
- onboarding 目前只存得下 `name` 與 `language`；入境日期、第幾位被照顧者還沒有欄位，留在前端 store。

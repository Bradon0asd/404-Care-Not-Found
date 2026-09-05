# 後端模組對照表

這份文件用來對齊「每個功能一個資料夾」的後端結構，以及 AI 功能（Tab 03 樹洞、壓力告知）會動到哪些既有模組。

用途：AI 這條線的多數改動會踩到其他人已經寫好的模組，先把接觸點列清楚，避免兩人同時改同一支檔案。**「負責人」與「對應前端 Tab」兩欄留白，待各模組的擁有者補齊。**

AI 功能的編號（A1–A3、B1–B6）對應 `docs/AI_DEVELOPMENT_HANDOVER.md` 第 3 節。

開發分支：`integration`（已含前端，共用 DB 的 migration 版本與它一致）。

---

## 0. 目前的阻塞點

**共用資料庫的 alembic 版本是 `2c3d4e5f6a7b`，這支 revision 在 repo 的所有分支都不存在。** Alembic 找不到 DB 現在的位置，因此 `db current` / `db migrate` / `db upgrade` 全部失效。

推斷：有人在本機做了一支沒推上來的 migration（為 `diaries` 加 `entry_date`，該欄位在 DB 裡但不在 model 裡），並直接套用到共用 DB。

另一個併發問題：該 DB **沒有 `invites` 表**，雖然 `d4e5f6a7b8c9_add_invites.py` 就在 repo 裡、版本指標也宣稱走過它。邀請功能對共用 DB 是壞的。

**待該 migration 的作者推上來**。在那之前，Tab 02／Tab 03 的新資料表無法建到共用 DB，主動線只能在 SQLite 測試中驗證。

註：先前 `1b2c3d4e5f6a` 的 `down_revision` 指向不存在 revision 的問題，已由作者於 commit `3833767` 修復。

---

## 1. 現有模組一覽

每個資料夾是一個功能模組，內含 `__init__.py`（Blueprint）／`routes.py`／`schemas.py`／`service.py`。

| 資料夾 | 功能 | 對應前端 Tab | 負責人 |
|:---|:---|:---|:---|
| `app/auth/` | 登入／登出／session、LINE Login（`line_client.py`） | | |
| `app/invites/` | 雇主邀請連結，看護免註冊入場 | | |
| `app/users/` | 使用者、看護與雇主配對 | | |
| `app/care_recipients/` | 被照顧者 | | |
| `app/care_schedules/` | 每日排程表 | Tab 01 | |
| `app/vital_signs/` | 生命徵象與儀表板彙總 | Tab 01 | |
| `app/diaries/` | 秘密日記 | Tab 02 | |
| `app/chat/` | 樹洞對話與 Care Agent | Tab 03 | |
| `app/sticky_notes/` | 便利貼交流板 | Tab 04 | |
| `app/uploads/` | 圖片上傳與靜態檔服務 | 跨 Tab | |
| `app/line/` | LINE webhook、rich menu、推播 | 雇主端 | |
| `app/shared/` | 共用工具（錯誤、回應格式、權限），**非功能模組、無 Blueprint** | — | |
| `app/models/` | SQLAlchemy models，**扁平檔案不是模組資料夾** | — | |

---

## 2. AI 功能要新開幾個資料夾

**最多 1 個。** AI 工作有九成落在既有的 `app/chat/`。

| 資料夾 | 狀態 | 內容 |
|:---|:---|:---|
| `app/chat/` | **已完成** | `__init__.py`／`client.py`／`prompts.py`／`schemas.py`／`service.py`／`routes.py`，8 條端點。A2 降級、B2 分層觸發、B3 短 context、B4 guardrail、B5 baseline、B6 心情天氣都已實作並有測試 |
| `app/stress_signals/` | **已建立**，見第 5 節 | A3 按日彙總 ＋ B1 日記高壓偵測的共用落點。只有 `service.py`，**沒有 Blueprint** |

補充：

- **A1 印尼語 ASR 已擱置**，不需要資料夾。日後要做也是在 `app/chat/` 加一支端點，且交接文件明訂**不要走** `app/uploads/service.py`（那支會寫磁碟且只認圖片）。
- **Model 不是資料夾**：新增的是 `app/models/chat.py`（`CareAgent`／`ChatRoom`／`ChatMessage`）與 `app/models/stress_event.py`，放在既有的 `app/models/` 底下。`CareAgent` 需含 `care_recipient_id`（交接文件的欄位清單漏列）——沒有它，AI 抽取的紀錄無法寫進 `CareSchedule` / `VitalSignLog`，聊天室歡迎語也拿不到照顧者資訊。
- **chat 的四張表已經進 metadata**（`care_agents`、`chat_rooms`、`chat_messages`、`stress_events`），但**還沒有對應的 migration**。在阻塞點修好、我們產出自己的 migration 之前，其他人跑 `db migrate` 會把這四張表一起捲進他的版本檔 —— 產出後請照 `models.md` 的規定人工檢查，把不屬於你那次變更的表刪掉。

  （曾考慮先不匯入 `app/models/__init__.py` 來隔離，但那樣 pytest 的 `db.create_all()` 也看不到這些表，等於無法測試，因此改為正常匯入並用這則說明協調。）
- **測試不另開目錄**：`backend/tests/` 是扁平的 `test_*.py`。

---

## 3. 會改到既有行為的檔案（有 regression 風險，動前先講）

| 檔案 | 改什麼 | 出處 | 負責人 |
|:---|:---|:---|:---|
| `app/line/notifications.py` | `notify_stress_signal()` 目前是呼叫一次推一則，要改成按日彙總／節流，避免轟炸雇主 LINE | A3 | |
| `app/config.py` | 單一 `GEMINI_MODEL` 擴為 `GEMINI_MODEL_FAST` / `GEMINI_MODEL_DEEP` 兩組 | B2 | |
| `app/chat/client.py` | `model` property 正讀著 `GEMINI_MODEL`，必須與上一列同步改，否則分層觸發會拿到空值 | B2 | |
| `app/shared/errors.py` | 新增 Agent 與額度相關例外 | 三級表 | |
| `app/models/__init__.py`、`app/__init__.py` | 匯出新 model、註冊新 Blueprint | Step 2 | |
| `.env.example` | 補兩個模型變數，**只寫佔位值，不得填真實連線資訊** | B2 | |

---

## 4. 只新增呼叫、不改既有邏輯（風險低）

| 檔案 | 怎麼碰 | 負責人 |
|:---|:---|:---|
| `app/diaries/service.py` | **已接**。`create_diary()` 之後呼叫 `_detect_stress()`：`is_private=True`（僅自己）才送偵測並寫入 `Diary.ai_analysis`；分享出去的日記完全不呼叫模型（B1） | |
| `app/care_schedules/service.py` | **不用改。** `create_schedule()` 已是 `current_user=` 介面並內建權限檢查，AI 抽取的照護紀錄以看護身分直接呼叫即可 | |
| `app/vital_signs/service.py` | **不用改。** `create_vital_sign()` 同上，且 `unit` 由 server 依型別決定、不吃 client 輸入 | |

B1 的儲存位置**隊友已經開好，沒有另開一份**：`Diary.ai_analysis`（`DiaryAiAnalysis` 列舉，`normal` / `emergency`，見 `app/models/diary.py`）。

兩點要注意：

- 它只有二值、**沒有時間點**，所以 A3「異常筆數 ＋ 時間」的彙總仍需獨立的 `StressEvent`。兩者並存：`ai_analysis` 記單篇日記的判定，`StressEvent` 記可彙總的訊號。
- `DiarySchema` **沒有輸出** `ai_analysis`，且有測試斷言日記 API 的回應不含它。這符合「壓力是後台語言、不給看護看」的鐵則，不要加上去。

---

## 5. `app/stress_signals/`（已定案並建立）

A3（按日彙總）與 B1（日記偵測）的共用落點，獨立成模組。理由：`chat` 與 `diaries` 兩邊都要用它，塞進 `chat` 會讓 Tab 02 反過來依賴 Tab 03；塞進 `line` 則是把業務邏輯放進通訊通道模組。現在兩個呼叫端都只依賴它，而它不依賴任何一邊。

**沒有 Blueprint**，這是刻意的：壓力相關的東西不對看護開放任何端點，雇主端的手動推播已經在 `POST /api/line/stress-signals`。此模組只被其他 service 呼叫。

對外的函式：

| 函式 | 做什麼 |
|:---|:---|
| `analyze_and_record()` | 判定 → 高壓才寫 `StressEvent` → 觸發當日彙總推播。回傳布林值僅供記 log |
| `is_high_stress()` | 分層觸發：便宜模型先粗判，超過 `TRIAGE_THRESHOLD` 才呼叫貴模型 |
| `record_event()` | 只寫訊號 |
| `notify_daily_total()` | 推當日累計筆數，並把已涵蓋的事件標記 `notified_at`，同一筆不會被算進第二則通知 |

降級行為：模型呼叫失敗、回傳無法解析的 JSON、看護未配對雇主、LINE 未設定 —— 一律記 log 後安靜略過，不拋例外給呼叫端。看護的對話永遠不會因為背後的分析失敗而中斷（A2）。未推播成功的事件維持 `notified_at = NULL`，下一次推播會一併帶上。

---

## 6. 跨模組資料流（誰呼叫誰）

```
Tab 03 對話  →  app/chat/service.py
                  ├→ 陪伴回應      → ChatMessage（回看護）
                  ├→ 情緒分析      → 壓力訊號模組 → app/line/notifications.py（只傳筆數＋時間）
                  └→ 抽取照護事實  → app/care_schedules/service.py
                                     app/vital_signs/service.py

Tab 02 日記  →  app/diaries/service.py
                  └→ 僅 is_private=True  → 壓力訊號模組 → 同上
```

鐵則提醒：往 LINE 那條線**只傳「異常筆數 ＋ 時間 ＋ 建議行動」，絕不含對話或日記的任何文字**。壓力值與情緒分析屬後台語言，不回傳給看護端的任何 API。

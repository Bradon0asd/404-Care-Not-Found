# CLAUDE.md

隊名：**404: Care Not Found**｜BUILDMODE Hackathon 2026｜賽道 Social Impact（Track 05，無企業命題）

## 一句話定位

給移工看護一個記錄台灣生活與心情 的私人空間（樹洞），用遊戲化維持動力；雇主端不做 App，改走 LINE 官方帳號做低頻的「一眼看懂 + 收通知」。

## 協作規則（對 Claude）

- 不清楚就問我，不要自己猜。
- 不用 Emoji。
- 回答與程式碼都盡量簡短。
- 上線前一定先測試。

## 團隊約法三章（人 + AI 都要遵守）

1. **不可以把任何 API Key、帳號密碼、機敏性資訊上傳至公開的 GitHub。** 一律放 `.env`（已在 `.gitignore`），程式碼裡只讀環境變數，不寫死實際金鑰；commit 前若動到設定檔要再三檢查。

## 貫穿全專案的鐵則（不可違反）

- **站在看護那邊的樹洞，不是監控工具。** 對看護的 UI 文案永遠用陪伴語言（「有人站在你這邊」），絕不用監控語言（「AI 在監測你」）；核心對話頁永遠叫「跟我聊聊／今天的心情」，絕不叫「壓力檢測」。
- **輸入端一律印尼語**（至少「跟我聊聊」對話輸入、便利貼輸入需支援印尼文）。
- **care log ≠ medical record。** 只做照護生活紀錄，不做醫療診斷、不取代醫療判斷。遇到醫療判斷情境，AI 一律回「建議聯繫家屬／就醫」；生命徵象只呈現「變化」（如「與過去一週相比偏高」），不下醫療判讀。數值上升/下降可以用顏色（如紅/綠）簡單區分方向，這不算醫療判讀；但不能用顏色或文案暗示「異常」、「危險」等醫療診斷語氣。
- **壓力值／情緒分析是後台語言**，只用於觸發雇主端「告知義務」訊號，**絕不顯示給看護看**，且告知雇主的訊息**只傳「異常筆數 + 時間 + 建議行動」，絕不含看護寫了什麼**（對話或日記內容）。
- **看護對隱私分級有主控權**：日記預設「僅自己」（全封閉，只有這類內容進 AI 高壓偵測）；便利貼可指定給誰看。這個主控權是「對等」的具體實現。
- 不給雇主秘密日記——功能對稱 ≠ 權力對等，會稀釋「站在看護那邊」的核心立場；雇主的情感出口放 roadmap。

## 架構決策：雇主端退到 LINE，不做 App

- **看護端**：完整 Web App（RWD，App UI 語言，手機尺寸 demo），五個 Tab 齊全開發。
- **雇主端**：LINE 官方帳號，零安裝。LINE 上收三種訊息，對應原本雇主 4-Tab：
  1. **照護摘要推播**（原 Dashboard）：每日／異常時推播，可點連結看較完整 web 頁。
  2. **壓力告知**：見上方鐵則，只傳訊號不傳內容。
  3. **交流板便利貼**：看護發布、標了雇主可見的便利貼會推到 LINE；雇主可回，請假預告走這條。
- 理由：兩天多開發時間，把最複雜介面集中在真正高頻的看護端；雇主低頻，LINE 完全夠用。

## 看護端 Tab 結構（五個 Tab）

1. **Tab 01｜照護紀錄 Dashboard**：儀表板（生命徵象卡片：血壓/血糖/心跳/血氧/體溫/呼吸）與每日排程表兩個視圖切換，皆有平日/周末切換。時間表打勾＝同時完成「今日待辦」與「當日紀錄」。資料來源：排程表打勾 + Tab 03 對話 AI 抽取。
2. **Tab 02｜我的秘密日記**（看護專屬）：遊戲化破關地圖（Day N 氣泡），支援文字/語音/繪畫/圖片，AI 語音辨識（印尼語）。新增日記必須有「僅自己 / 分享給 LINE 好友」切換，預設「僅自己」。MVP 建議只做 streak + 里程碑，其餘放 roadmap。
3. **Tab 03｜跟我聊聊（樹洞）★核心頁**：分兩種模式，不能做成單一進度條。
   - **建檔模式**（一次性，Step 1-2）：Step1 輸入病患情境 System Prompt（含 Temperature 滑桿、Guardrail 欄位）；Step2 生成專屬 Care Agent + 建立心理基準線（baseline，僅首次，文案「一起聊聊你最近的狀態吧」/「完成一次性小任務」，不用「測驗/檢測」字眼）。免費版限制：最多 1 個 Agent。
   - **對話模式**（每天，Step 3-5）：Step3 一鍵「心情天氣」入口 → 印尼語語音/文字自然對話；Step4 AI 背後同時做三件事（看護無感）：①NLP 情緒分析→高壓則觸發告知雇主訊號（不傳內容）②抽取照護資訊寫進 Tab 01 ③陪伴式回應給看護（不是壓力分數）；Step5 歷程回顧（隨時可看，非流程步驟）。免費版一天最多開 1 個聊天室且對話有上限。
4. **Tab 04｜交流板（便利貼）**：三色分緩急（緊急=紅／普通=黃／不重要=藍）。看護可選擇每張便利貼給誰看。每張顯示雇主端狀態：已讀取/尚未讀取/未獲得瀏覽權限（雇主端走 LINE 後「已讀取」＝ LINE 已讀）。
5. **Tab 05｜帳戶管理**：變更系統模式、變更語言、綁定 LINE 帳號、訂閱方案（分級用「語音辨識次數／Agent 數／聊天室數／便利貼數」限制，呼應成本控制敘事）。

## 成本控制敘事（Token，工程成熟度加分點）

- **貴的只做一次**：Step 1-2 生成 persona/tips 耗 token 但一次性，存檔複用。
- **每日對話用便宜模型 + 短 context**：只帶病患摘要 + 當輪對話，不塞完整歷史。
- **分層觸發（tiered inference）**：便宜模型先粗判情緒，只有疑似高壓才呼叫貴模型深入分析。

## 賽制與時程（近三天，範圍已凍結對齊）

- 開發窗口：9/4 早上報到說明會後即可開工 + 9/5 整天到繳件。9/5 下午開放繳件、範圍凍結；9/6 10:00 繳件關閉，之後只能修 bug/補穩定性/補影片，不能加新功能。
- **核心目標：9/5 傍晚前主動線跑通 + 影片錄好初版。**
- 四項繳件（Day3 10:00 前，缺一不受理）：文字敘述（問題/使用者/核心功能/範圍）、2-3 分鐘 YouTube 影片（評分素材本體）、GitHub Repo（含 README：問題一句話、架構圖、安裝執行步驟、AI 用了什麼與限制說明、demo 連結）、Google Form。
- 兩輪評分標準不同：Round 1（初審，只看文字+影片+GitHub）我們的優勢在「問題定義 35%」；Round 2（Demo Day，Top 10 才有，5 分鐘現場）最高權重「使用者價值 30%」，開場第一句話：「這是一個站在看護那邊的出口」。
- 硬性提醒：每位成員需有效門票（現場收現金）；9/4/9/5/9/6 三天每天都要個人報到，缺一即失格；Day1 離場前鎖定 Social Impact 賽道；入選 Top10 未到場 = No-show 取消資格。

## Demo 核心主動線（唯一一條要演深、要跑通的路徑）

看護在 Tab 03 用印尼語講一段話（例：阿嬤跌倒、我很自責、心情不好）
→ AI 轉譯 + 情緒分析（後台判高壓）+ 抽取照護紀錄
→ ① 中文紀錄自動進 Tab 01 Dashboard
→ ② 觸發一則壓力告知推播到雇主 LINE（不含內容）
→ 看護端只看到溫暖的陪伴回應（無「觀察清單」字樣）

MVP 內做到能跑：Tab 01、Tab 03、LINE 壓力告知推播（若 LINE 串接來不及，demo 可用模擬推播畫面替代）。做得出 wireframe 但不強求 demo 跑通：Tab 02 破關地圖、Tab 04 完整權限、Tab 05、雇主 LINE 的照護摘要與交流板。全部放 roadmap：語言練習、照護知識庫、其他來源國語言、雇主情感出口、繪畫輸入、遊戲化完整機制。

## 技術棧與專案結構（後端，backend 分支）

Flask App Factory + Service Layer 骨架：

- `main.py` — 入口
- `app/__init__.py` — `create_app()`，註冊 blueprints（`/api`, `/api/auth`, `/api/line`）與統一錯誤處理（`AppError`、`ValidationError`）
- `app/config.py` — 讀 `.env`，組 `mysql+pymysql://` DB URI
- `app/extensions.py` — `db`（SQLAlchemy）、`migrate`（Flask-Migrate）
- `app/api/` — `routes.py` / `schemas.py`（marshmallow）/ `service.py`
- `app/auth/` — 同上結構
- `app/line/` — LINE Messaging API webhook 與 client（`line-bot-sdk`）
- `app/models/` — SQLAlchemy models（目前 `user.py`）
- `app/common/errors.py` — `AppError`
- `tests/` — pytest（`conftest.py`, `test_health.py`, `test_users.py`）

技術棧：Flask, Flask-SQLAlchemy, Flask-Migrate, marshmallow, webargs, PyMySQL, line-bot-sdk, python-dotenv, pytest。

### 常用指令

```bash
python -m venv .venv && source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
flask --app main db init
flask --app main db migrate -m "create users"
flask --app main db upgrade
flask --app main run --debug
pytest
```

已有 API：`GET /api/health`、`POST /api/users`、`GET /api/users/<id>`、`POST /api/line/webhook`。

正式部署前需設定 `DATABASE_URL`（或 `DB_SERVER`/`DB_NAME`/`DB_PASSWORD`）、`LINE_CHANNEL_ACCESS_TOKEN`、`LINE_CHANNEL_SECRET`，並關閉 debug mode。

## 待定技術選型（開工前拍板，資工/資管主導）

- 印尼語 ASR 用哪家（需實測準確率）
- 印尼語→中文翻譯用哪個
- Agent／NLP 情緒分析用哪個模型（呼應 tiered inference 成本控制）
- LINE 串接負責人與可行性（做不完 demo 用模擬推播畫面）
- 看護端介面語言：主張印尼文為主，demo 給中文評審看可雙語並陳

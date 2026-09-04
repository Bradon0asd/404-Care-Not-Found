# Frontend Overview

給後端／其他協作者快速掌握前端目前的架構與進度。程式碼本身的細節請直接看檔案，這份文件只講「東西在哪、為什麼這樣分」。

## 技術棧

Vue 3（`<script setup>` + TypeScript）、Vite、Vue Router、Pinia、Tailwind CSS v4。設計稿來自 Figma，色票已轉成 Tailwind theme tokens（見下方「樣式系統」）。

## 目前進度

**已完成（有實際畫面、可互動）：**

- 登入/邀請碼綁定流程（`views/auth/`）：選身分（看護/雇主）→ LINE 註冊（目前只是導頁，未接真的 LINE OAuth）→ 看護填基本資訊 / 雇主生成邀請碼
- Tab01 照護紀錄 Dashboard（`views/tab01-dashboard/`）：儀錶板（6 張生命徵象卡）＋ 每日排程表（平日/周末切換）＋ 新增排程表單
- Tab02 秘密日記（`views/tab02-diary/`）：破關地圖（Day 氣泡路徑，今日高亮）＋ 日記撰寫頁（標題/民國曆日期/內容/單張圖片/AI 語音辨識按鈕待接 ASR/僅自己或分享給 LINE 好友）
- Tab03 跟我聊聊（`views/tab03-chat/`）★核心頁，分兩種模式：
  - `/chat`（IntroView）是持久首頁，**兩支新聞影片永遠顯示在最上面**，下方內容依是否已建檔切換：
    - 未建檔：「建置你的第一個 Care Agent」5 步驟說明 + CTA
    - 已建檔：`DailyChatHome.vue`（心情天氣打卡 + 聊天室泡泡列表，浮動話題泡泡＝舊聊天室，中央大泡泡＝開新聊天）；頁面右上角有「模擬首次使用畫面」連結，點下去會把 `store.agent` 設回 `null`，方便demo/測試不用真的清資料庫
  - 建檔流程（僅未建檔時會走到）：`/chat/setup`（System Prompt + Temperature + Guardrail）→ `/chat/baseline` → `/chat/baseline/questions`（一次性 5 題心理基準線問卷，單選、選完自動跳下一題，第五題才是「生成」按鈕）→ 完成後寫入 `stores/careAgent.ts`，導回 `/chat` 就會看到已建檔的畫面
  - 點聊天室泡泡進 `/chat/room/:id`（文字輸入＋語音按鈕，AI 回覆目前是 stub，見下方「跟後端串接」）
- Tab04 便利貼牆（`views/tab04-board/`）：清單頁（狀態/層級篩選、點卡片彈出放大版便利貼，深色遮罩、點外部關閉）＋ 新增頁（三色層級選擇、標題/標籤類別 tap-to-edit、內容+語音+圖片、「設定便利貼權限➨發布便利貼」開權限彈窗，彈窗選完才真的送出）
- Tab05 帳戶管理（`views/tab05-account/`）：使用者卡片（樹的插圖是簡化版，實際插圖等 Figma 匯出素材）+ 變更語言（彈窗，共用 onboarding store 的語言狀態）/ 登出 / 訂閱方案三個入口，訂閱方案頁是免費/小資/進階三張方案卡（文案對應 CLAUDE.md 既有的定價表）

**五個 Tab 都有畫面了，全部路由可互動；目前所有資料都是前端本地假資料 / Pinia store，還沒接任何後端 API。**

## 路由總覽

| 路徑 | 頁面 | 說明 |
|---|---|---|
| `/` | — | redirect 到 `/auth/role`（正式入口，走登入流程） |
| `/auth/role` | RoleSelectView | 選身分，帶 `?invite=` 參數會自動選看護 |
| `/auth/caregiver/onboarding` | CaregiverOnboardingView | 看護：語言/入境日期/第幾位照護者 |
| `/auth/employer/setup` | EmployerSetupView | 雇主：設定看護資訊 + 生成邀請碼 |
| `/dashboard` | DashboardView | Tab01，儀錶板/排程表切換視圖 |
| `/dashboard/add-schedule` | AddScheduleView | 新增排程表單，寫回 schedule store |
| `/diary` | DiaryMapView | Tab02，破關地圖 |
| `/diary/:day` | DiaryEntryView | 單日日記撰寫/編輯頁 |
| `/chat` | IntroView | Tab03 持久首頁，影片固定顯示，下方依建檔狀態切換說明頁／DailyChatHome |
| `/chat/setup` | AgentSetupView | 建檔 Step1：System Prompt / Temperature / Guardrail |
| `/chat/baseline` | BaselineIntroView | 建檔 Step2 任務入口 |
| `/chat/baseline/questions` | BaselineQuestionsView | 5 題一次性基準線問卷 |
| `/chat/room/:id` | ChatRoomView | 單一聊天室對話畫面 |
| `/board` | BoardListView | Tab04，便利貼清單 + 篩選 |
| `/board/new` | AddNoteView | 新增便利貼表單 |
| `/account` | AccountView | Tab05，使用者資訊 + 變更語言/登出/訂閱方案入口 |
| `/account/plans` | PlansView | 訂閱方案一覽表 |
| `/:pathMatch(.*)*` | — | 任何不存在的路徑都 redirect 回 `/` |

## 目錄結構

```
src/
  components/
    common/       跨頁共用元件（Button、SegmentedToggle、免責聲明橫幅...）
    layout/       App 殼層（Header、底部 5-tab 導覽列、手機寬度容器）
    auth/         登入/邀請碼流程專用元件
    tab01-dashboard/  Tab01 專用元件（生命徵象卡、排程表格）
    tab02-diary/      Tab02 專用元件（日記氣泡、統計列、腳印裝飾）
    tab03-chat/       Tab03 專用元件（DailyChatHome 已建檔首頁內容、聊天泡泡、心情天氣、基準線問卷卡、Temperature/Guardrail 設定）
    tab04-board/      Tab04 專用元件（便利貼卡片、堆疊便利貼圖示、放大版便利貼彈窗、權限彈窗）
    tab05-account/    Tab05 專用元件（樹狀使用者卡片、分支導覽連結、方案卡片、語言彈窗）
  views/        每個路由對應一個 view，負責組裝 components + 串 store
  stores/       Pinia，一個 Tab/流程一個 store（onboarding.ts、schedule.ts、diary.ts、careAgent.ts、board.ts、account.ts）
  utils/        跨元件共用的純函式（目前只有 date.ts 的民國曆轉換）
  router/
  assets/       main.css（Tailwind 進入點 + 色票 tokens）
```

元件命名跟 Figma 圖層名對齊，方便比對設計稿。共用元件放 `common/`，跟特定 Tab 綁定的放對應的 `tabNN-*/` 資料夾。

## 樣式系統

Tailwind v4，色票定義在 `src/assets/main.css` 的 `@theme` block，對應 Figma 色票：

- `pink-100`～`pink-600`：粉色階（淺到深）
- `ink-100`～`ink-950`：黑/灰階（Figma 標 "Balck"，程式碼裡統一叫 `ink`）
- `accent`：唯一的黃色 `#FCD856`

## 跟後端串接（現在還沒做，但已知會需要什麼）

目前完全沒有呼叫任何 API，所有狀態都在瀏覽器記憶體（Pinia store）裡，重新整理就會消失。之後串接時，預期會需要對應到現有 API（見根目錄 `CLAUDE.md`）：

- `POST /api/users`：`EmployerSetupView` 生成邀請碼、`CaregiverOnboardingView` 完成 onboarding 時，應該要建立/更新使用者
- `POST /api/line/webhook`：目前「使用 LINE 註冊」按鈕只是前端導頁，之後要接真的 LINE Login/OAuth
- Tab01 的生命徵象卡、排程表（`stores/schedule.ts`）目前是寫死的假資料，之後要換成打 API 讀寫
- Tab02 日記（`stores/diary.ts`）目前只存在瀏覽器記憶體：需要一個存/讀日記的 API，以及印尼語 ASR 服務（`DiaryEntryView.vue` 的「AI 語音辨識」按鈕目前是空的 stub，見檔案內 TODO 註解）
- Tab03（`stores/careAgent.ts`）是目前缺口最大的地方：
  - System Prompt / Temperature / Guardrail 需要送到後端去實際生成 Care Agent persona（目前只是存在本地 store）
  - 5 題基準線問卷答案需要送出去建立心理基準線
  - 聊天室送出訊息後（`ChatInputBar.vue` → `store.sendMessage`），需要呼叫真正的 Care Agent API 拿到 AI 回覆；同一次呼叫也要做 CLAUDE.md 說的「情緒分析→高壓觸發雇主 LINE 告知（不傳內容）」＋「抽取照護資訊寫進 Tab01」，這兩件事前端完全看不到、也不應該看到
  - 聊天室語音輸入（`ChatInputBar.vue`）跟 System Prompt 語音輸入（`AgentSetupView.vue`）都是 stub，等印尼語 ASR
- Tab04 便利貼（`stores/board.ts`）目前只存在瀏覽器記憶體，且「已讀取/尚未讀取」狀態是寫死的假資料：實際上這個狀態要對應雇主端 LINE 的已讀狀態（見 CLAUDE.md「雇主端走 LINE 後『已讀取』＝ LINE 已讀」），需要後端/LINE webhook 才能是真的
- Tab05 訂閱方案（`stores/account.ts`）的「變更方案」按鈕是 stub（見 `PlansView.vue` TODO 註解），沒有實際付款流程，等付款方式決定後再接

**已知還沒解決/需要後續確認的地方：**
- Tab03 建檔流程有兩張新聞縮圖是 placeholder 灰色方塊（`NewsAwarenessBanner.vue`），還沒有 Figma 圖片素材
- 產品名稱曾經在不同 Figma 稿裡打成「Care Be Found」/「Care Not Found」/「Care Can Be Found」，目前統一用「404: Care Can Be Found」（文法正確版本），之後如果 Figma 又出現不同版本要再跟設計對齊
- Tab04 便利貼權限目前簡化成「只有自己／雇主」二選一（單一雇主帳號），功能規格文件裡原本想支援「指定給誰看」（多個家人聯絡人），等有多聯絡人資料模型再擴充
- Tab05 的樹狀插圖（`CareTreeHeader.vue`）用簡化幾何圖形逼近，頭像是 pravatar.cc 佔位照片，Figma 原稿是手繪風插畫，還沒有可匯出的素材檔
- **目前完全沒有路由守衛（route guard）**：`/` 會導去 `/auth/role`，但直接打 `/dashboard`、`/chat`、`/board`、`/account` 這些網址還是可以完全繞過登入流程直接進去，沒有任何「必須先登入/完成 onboarding」的攔截。MVP demo 階段這是刻意的（方便直接測任一頁），但正式串接後端後要補上

## 本機開發

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
npm run build       # 產出 dist/，型別檢查 + build
```

## 部署

- Vercel：`frontend/vercel.json` 已設定 root directory 對應與 SPA rewrite（Vue Router history mode 需要）
- Railway：`npm run start`（`serve -s dist`）撐靜態檔案，讀 Railway 注入的 `PORT`

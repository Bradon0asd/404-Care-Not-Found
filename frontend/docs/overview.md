# Frontend Overview

給後端／其他協作者快速掌握前端目前的架構與進度。程式碼細節請直接看檔案，這份文件只講「東西在哪、為什麼這樣分」。

## 技術棧

Vue 3（`<script setup>` + TypeScript）、Vite、Vue Router、Pinia、Tailwind CSS v4。設計稿來自 Figma，色票已轉成 Tailwind theme tokens（見「樣式系統」）。

## 專案結構

```
frontend/
├── docs/
│   └── overview.md          本文件
└── src/
    ├── main.ts               進入點：掛載 App、註冊 Pinia + Router
    ├── App.vue                只放 <RouterView />
    ├── router/
    │   └── index.ts           所有路由定義（見下方「路由總覽」）
    ├── stores/                Pinia，一個 Tab／流程一個 store
    │   ├── onboarding.ts      登入/邀請碼流程狀態（角色、語言、入境日期...）
    │   ├── schedule.ts        Tab01 排程表資料
    │   ├── diary.ts           Tab02 日記資料
    │   ├── careAgent.ts       Tab03 Care Agent + 聊天室資料
    │   ├── board.ts           Tab04 便利貼資料
    │   └── account.ts         Tab05 使用者/訂閱方案資料
    ├── utils/
    │   └── date.ts            民國曆日期格式化（toMinguoDate）
    ├── assets/
    │   └── main.css           Tailwind 進入點 + 色票 @theme tokens
    ├── views/                 每個路由對應一個 view，負責組裝 components + 串 store
    │   ├── auth/               登入/邀請碼綁定流程
    │   ├── tab01-dashboard/
    │   ├── tab02-diary/
    │   ├── tab03-chat/
    │   ├── tab04-board/
    │   └── tab05-account/
    └── components/
        ├── common/            跨頁共用元件（BaseButton、SegmentedToggle、免責聲明橫幅...）
        ├── layout/             App 殼層（AppHeader、BottomTabBar、PageContainer、SubPageHeader）
        ├── auth/               登入流程專用元件
        ├── tab01-dashboard/
        ├── tab02-diary/
        ├── tab03-chat/
        ├── tab04-board/
        └── tab05-account/
```

規則：元件命名跟 Figma 圖層名對齊，方便比對設計稿。共用元件放 `components/common/`，只有單一 Tab 會用到的放對應的 `tabNN-*/` 資料夾（views 跟 components 底下都有一份）。

## 目前進度

五個 Tab 都有畫面、全部路由可互動。**所有資料目前都是前端本地假資料／Pinia store，還沒接任何後端 API**（重新整理會消失）。

| Tab | 狀態 | 重點 |
|---|---|---|
| 登入/邀請碼 | 完成 | 選身分（看護/雇主）→ LINE 註冊（只是導頁，未接真的 OAuth）→ 看護填基本資訊 / 雇主生成邀請碼 |
| Tab01 照護紀錄 | 完成 | 儀錶板（6 張生命徵象卡）＋ 每日排程表（平日/周末）＋ 新增排程表單 |
| Tab02 秘密日記 | 完成 | 破關地圖（Day 氣泡路徑）＋ 日記撰寫頁（民國曆日期、AI 語音辨識為 stub、僅自己或分享給 LINE 好友） |
| Tab03 跟我聊聊 ★核心 | 完成 | 見下方「Tab03 細節」 |
| Tab04 便利貼牆 | 完成 | 清單頁（篩選、點卡片放大彈窗）＋ 新增頁（三色層級、設定權限彈窗、彈窗內才真的送出） |
| Tab05 帳戶管理 | 完成 | 樹狀使用者卡片（變更語言/登出/訂閱方案三分支）＋ 訂閱方案頁 |

### Tab03 細節（★核心頁，邏輯較複雜）

`/chat`（`IntroView`）是**持久首頁**：兩支新聞影片永遠顯示在最上面，下方內容依是否已建檔切換：

- **未建檔**：「建置你的第一個 Care Agent」5 步驟說明 + CTA
- **已建檔**：`DailyChatHome.vue`（心情天氣打卡 + 聊天室泡泡列表；浮動話題泡泡＝舊聊天室，中央大泡泡＝開新聊天）。頁面右上角有「模擬首次使用畫面」連結，點下去把 `store.agent` 設回 `null`，方便 demo/測試不用真的清資料庫

建檔流程（只有未建檔時才會走到）：

```
/chat/setup（System Prompt + Temperature + Guardrail）
  → /chat/baseline（任務入口）
  → /chat/baseline/questions（一次性 5 題心理基準線問卷，單選、選完自動跳下一題，第五題才是「生成」按鈕）
  → 寫入 stores/careAgent.ts，導回 /chat（此時會看到已建檔畫面）
```

點聊天室泡泡進 `/chat/room/:id`（文字輸入＋語音按鈕；AI 回覆目前是 stub，見「跟後端串接」）。

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
| `/chat` | IntroView | Tab03 持久首頁（見上方「Tab03 細節」） |
| `/chat/setup` | AgentSetupView | 建檔 Step1：System Prompt / Temperature / Guardrail |
| `/chat/baseline` | BaselineIntroView | 建檔 Step2 任務入口 |
| `/chat/baseline/questions` | BaselineQuestionsView | 5 題一次性基準線問卷 |
| `/chat/room/:id` | ChatRoomView | 單一聊天室對話畫面 |
| `/board` | BoardListView | Tab04，便利貼清單 + 篩選 |
| `/board/new` | AddNoteView | 新增便利貼表單 |
| `/account` | AccountView | Tab05，使用者資訊 + 變更語言/登出/訂閱方案入口 |
| `/account/plans` | PlansView | 訂閱方案一覽表 |
| `/:pathMatch(.*)*` | — | 任何不存在的路徑都 redirect 回 `/` |

## 樣式系統

Tailwind v4，色票定義在 `src/assets/main.css` 的 `@theme` block，對應 Figma 色票：

- `pink-100`～`pink-600`：粉色階（淺到深）
- `ink-100`～`ink-950`：黑/灰階（Figma 標 "Balck"，程式碼裡統一叫 `ink`）
- `accent`：唯一的黃色 `#FCD856`

## 跟後端串接（現在還沒做，但已知會需要什麼）

見根目錄 `CLAUDE.md` 的既有 API：

- `POST /api/users`：`EmployerSetupView` 生成邀請碼、`CaregiverOnboardingView` 完成 onboarding 時，應該要建立/更新使用者
- `POST /api/line/webhook`：目前「使用 LINE 註冊」按鈕只是前端導頁，之後要接真的 LINE Login/OAuth
- Tab01 生命徵象卡、排程表（`stores/schedule.ts`）是寫死的假資料，之後要換成打 API 讀寫
- Tab02 日記（`stores/diary.ts`）需要存/讀日記的 API，以及印尼語 ASR 服務（`DiaryEntryView.vue` 的「AI 語音辨識」是空的 stub，見檔案內 TODO）
- Tab03（`stores/careAgent.ts`）缺口最大：
  - System Prompt / Temperature / Guardrail 要送到後端實際生成 Care Agent persona
  - 5 題基準線問卷答案要送出去建立心理基準線
  - 聊天室送出訊息（`ChatInputBar.vue` → `store.sendMessage`）要呼叫真正的 Care Agent API 拿 AI 回覆；同一次呼叫也要做 CLAUDE.md 說的「情緒分析→高壓觸發雇主 LINE 告知（不傳內容）」＋「抽取照護資訊寫進 Tab01」，這兩件事前端完全看不到、也不應該看到
  - 聊天室與 System Prompt 的語音輸入都是 stub，等印尼語 ASR
- Tab04 便利貼（`stores/board.ts`）的「已讀取/尚未讀取」是寫死假資料，實際要對應雇主端 LINE 已讀狀態，需要後端/LINE webhook
- Tab05 訂閱方案（`stores/account.ts`）的「變更方案」是 stub，沒有實際付款流程

## 已知缺口

- **沒有路由守衛**：直接打 `/dashboard`、`/chat`、`/board`、`/account` 等網址可以完全繞過登入流程。MVP demo 階段刻意如此（方便直接測任一頁），正式串接後端後要補上
- Tab03 建檔流程的兩張新聞縮圖是灰色 placeholder（`NewsAwarenessBanner.vue`），還沒有 Figma 圖片素材
- Tab04 便利貼權限簡化成「只有自己／雇主」二選一（單一雇主帳號），規格文件原本想支援指定多個家人聯絡人，等有多聯絡人資料模型再擴充
- Tab05 樹狀插圖（`CareTreeHeader.vue`）用簡化幾何圖形逼近，頭像是 pravatar.cc 佔位照片，Figma 原稿是手繪風插畫，還沒有可匯出的素材檔
- 產品名稱曾在不同 Figma 稿打成三種寫法，目前統一用「404: Care Can Be Found」（文法正確版本），之後 Figma 若又有新版本要再對齊

## 開發與部署

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
npm run build    # 型別檢查 + build，產出 dist/
```

部署走 **Railway**（CLI 直接部署本機資料夾，沒有接 GitHub 自動部署）：

```bash
cd frontend
railway up
```

`npm run start`（`serve -s dist`）在 Railway 上撐靜態檔案，會讀 Railway 注入的 `PORT`。

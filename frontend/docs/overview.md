# Frontend Overview

給後端／其他協作者快速掌握前端目前的架構與進度。程式碼本身的細節請直接看檔案，這份文件只講「東西在哪、為什麼這樣分」。

## 技術棧

Vue 3（`<script setup>` + TypeScript）、Vite、Vue Router、Pinia、Tailwind CSS v4。設計稿來自 Figma，色票已轉成 Tailwind theme tokens（見下方「樣式系統」）。

## 目前進度

**已完成（有實際畫面、可互動）：**

- 登入/邀請碼綁定流程（`views/auth/`）：選身分（看護/雇主）→ LINE 註冊（目前只是導頁，未接真的 LINE OAuth）→ 看護填基本資訊 / 雇主生成邀請碼
- Tab01 照護紀錄 Dashboard（`views/tab01-dashboard/`）：儀錶板（6 張生命徵象卡）＋ 每日排程表（平日/周末切換）＋ 新增排程表單
- Tab02 秘密日記（`views/tab02-diary/`）：破關地圖（Day 氣泡路徑，今日高亮）＋ 日記撰寫頁（標題/民國曆日期/內容/單張圖片/AI 語音辨識按鈕待接 ASR/僅自己或分享給 LINE 好友）

**只有路由 stub、還沒做畫面：** Tab03 跟我聊聊、Tab04 便利貼牆、Tab05 帳戶管理（`/chat`、`/board`、`/account`，目前都顯示「開發中」佔位頁）

**目前所有資料都是前端本地假資料 / Pinia store，還沒接任何後端 API。**

## 路由總覽

| 路徑 | 頁面 | 說明 |
|---|---|---|
| `/` | — | redirect 到 `/dashboard`（開發階段先跳過 auth，方便直接測 Tab） |
| `/auth/role` | RoleSelectView | 選身分，帶 `?invite=` 參數會自動選看護 |
| `/auth/caregiver/onboarding` | CaregiverOnboardingView | 看護：語言/入境日期/第幾位照護者 |
| `/auth/employer/setup` | EmployerSetupView | 雇主：設定看護資訊 + 生成邀請碼 |
| `/dashboard` | DashboardView | Tab01，儀錶板/排程表切換視圖 |
| `/dashboard/add-schedule` | AddScheduleView | 新增排程表單，寫回 schedule store |
| `/diary` | DiaryMapView | Tab02，破關地圖 |
| `/diary/:day` | DiaryEntryView | 單日日記撰寫/編輯頁 |
| `/chat` `/board` `/account` | PlaceholderView | Tab03-05 佔位頁 |

## 目錄結構

```
src/
  components/
    common/       跨頁共用元件（Button、SegmentedToggle、免責聲明橫幅...）
    layout/       App 殼層（Header、底部 5-tab 導覽列、手機寬度容器）
    auth/         登入/邀請碼流程專用元件
    tab01-dashboard/  Tab01 專用元件（生命徵象卡、排程表格）
    tab02-diary/      Tab02 專用元件（日記氣泡、統計列、腳印裝飾）
    tab03-chat/ tab04-board/ tab05-account/  預留給後續 Tab，目前是空的
  views/        每個路由對應一個 view，負責組裝 components + 串 store
  stores/       Pinia，一個 Tab/流程一個 store（onboarding.ts、schedule.ts、diary.ts）
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

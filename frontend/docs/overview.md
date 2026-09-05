# Frontend Overview

給後端／其他協作者快速掌握前端目前的架構與進度。程式碼細節請直接看檔案，這份文件只講「東西在哪、為什麼這樣分」。

## 技術棧

Vue 3（`<script setup>` + TypeScript）、Vite、Vue Router、Pinia、Tailwind CSS v4、vue3-carousel（Tab03 新聞影片滑動用）。設計稿來自 Figma，色票已轉成 Tailwind theme tokens（見「樣式系統」）。

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
    ├── i18n/                  中／印尼文介面切換（見下方「多語系」）
    │   ├── id.ts              中文原文 → 印尼文對照表
    │   ├── index.ts           註冊全域 $t()，同步 html lang / 頁面標題
    │   └── README.md          維護規則
    ├── stores/                Pinia，一個 Tab／流程一個 store
    │   ├── onboarding.ts      登入/邀請碼流程狀態（角色、語言、入境日期...）
    │   ├── schedule.ts        Tab01 排程表資料
    │   ├── diary.ts           Tab02 日記資料
    │   ├── careAgent.ts       Tab03 Care Agent + 聊天室資料
    │   ├── board.ts           Tab04 便利貼資料
    │   └── account.ts         使用者/照顧對象/Care Agent 名稱/訂閱方案資料——現在是跨 Tab 共用的資料來源（見下方）
    ├── utils/
    │   ├── date.ts            民國曆日期格式化（toMinguoDate）
    │   └── schedule.ts        Tab01 時間表小時清單（scheduleHours，07:00–23:00）
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
        ├── common/            跨頁共用元件（BaseButton、SegmentedToggle、免責聲明橫幅、BackgroundBlobs 裝飾背景...）
        ├── layout/             App 殼層（AppHeader、BottomTabBar、PageContainer（含 #header/#fab/#footer slot）、SubPageHeader）
        ├── auth/               登入流程專用元件
        ├── tab01-dashboard/
        ├── tab02-diary/
        ├── tab03-chat/
        ├── tab04-board/       含 NoteCard、NoteMetaIcon（卡片欄位小圖示）、AddNoteButton（新增鈕，獨立於共用 FloatingAddButton）
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

### 近期 UI 精緻度修正（跟 Figma 原稿逐項比對後的調整）

分工：Claude 負責邏輯正確性/跟 Figma 細節比對，Codex 負責排版精緻度。以下按負責人記錄，避免之後又被改回舊版或搞混誰動過什麼。

**Claude 改的：**

- **AppHeader**：底色改 `bg-pink-500`（`#FFB2C7`，設計稿命名 "Primary 05"），副標題文字改白色（不是灰色 — 灰色是之前對比度 bug 的錯誤修法），icon 換成乾淨版本（Codex 後續又重畫成現在的火把/手電筒造型，見下方 Codex 段落，這裡的「乾淨版本」只是指當時那一輪改動，不是描述現在的圖案）
- **MedicalDisclaimerBanner**：整個重做，從刺眼的深紅色長條改成淺灰卡片（`bg-ink-200`）+ 紅色圓形 i icon + 只有「不」字紅色加粗 + 灰色方形關閉鈕；props 從單一 `message` 改成 `before`/`highlight`/`after` 三段式，方便只標紅中間那個字
- **VitalSignCard（Tab01）**：改成雙層卡片效果（`border-pink-400` 框住白底），標題置中加底線。原本刻意保留中性顏色（不加紅/綠），但後續 Codex 加回 `trendTone` 紅綠標示，見下方「CLAUDE.md 規則變動」
- **FloatingAddButton（Tab01 新增鈕）**：改用 `PageContainer` 新的 `#fab` slot，固定在整個手機畫面右下角，不會再跟著內容捲動跑掉
- **NewsAwarenessBanner（Tab03）**：從灰色 placeholder 換成 `vue3-carousel` 滑動容器 + 真的 YouTube 縮圖（`img.youtube.com/vi/{id}/hqdefault.jpg`），點縮圖開新分頁到 YouTube；底色改 `bg-ink-200`（縮圖圓角後續被 Codex 加回來了，見下方「第六輪」）
- **IntroView（Tab03）**：「你的 Care Agent 已經準備好了」從常駐文字改成可關閉的提示卡（`bg-ink-200` 灰底，非粉色，+ X 按鈕），開發用的「模擬首次使用畫面」連結獨立一行、不受提示卡開關影響
- **WeatherMoodPicker + 5 個天氣 icon（Tab03）**：選中的天氣圖示現在會從外框變實心（`filled` prop 切換 `fill: none → currentColor`），不再只是變色，跟未選取的區別更明顯
- **NoteDetailModal（Tab04）**：「普通」（黃色）層級原本用 `bg-accent/30`（30% 透明度），疊在深色遮罩上完全看不清楚文字；改成跟緊急/不重要一樣不透明的 `bg-accent`

**Codex 改的：**

- **BottomTabBar**：重做成膠囊型浮動列，中間「跟我聊聊」用絕對定位的正圓（非圓角矩形）做出突出剪影，選中分頁用膠囊蓋住圖示+文字
- **PageContainer**：寬度上限微調（`max-w-sm` → `max-w-[402px]`，對齊 Figma 手機尺寸）
- **BackgroundBlobs**：4 個裝飾 blob 顏色/形狀調整
- **Tab01**：`ScheduleTable`／`SegmentedToggle` 改用 accent 黃色系配色重新設計；`AddScheduleView` 表單版面重排；新增 `utils/schedule.ts` 統一時間表小時範圍（07:00–23:00）
- **Tab02 破關地圖**：`DiaryDayBubble`／`FootprintDots`／`IconFootprint` 重畫（雙層描邊圓圈、真的腳印形狀、依前後泡泡位置動態算角度的連接線）。這一輪的 flex 版面在可視高度 ≲740px 的裝置上會溢出到底部導覽列下方看不見（Day101/Day100 這類後面的項目），根因是 flex 容器缺少 `min-h-0` 導致撐高不會自動收縮，且泡泡本身尺寸偏大、7 顆+6 個腳印的最小總高度超過矮螢幕能給的空間。**此問題已在下方「第三輪」的絕對定位版面修復**，見該段落
- **Tab04**：`NoteCard` 改用新的 `NoteMetaIcon`（標題/權限/層級小圖示）取代文字前綴 emoji；新增 `AddNoteButton.vue`（獨立的新增鈕樣式，不是共用 `FloatingAddButton`）
- **Tab05**：`CareTreeHeader` 大幅重畫（更細緻的樹冠/樹枝/葉子 SVG 路徑）；`AccountView` 版面調整；`PlanCard`／`PlansView` 訂閱方案卡片配色與陰影調整
- **根目錄 `README.md`**：整份重寫，含專案定位、功能對照表、本機啟動、建置指令、Railway 部署步驟、目錄結構——內容比這份 `overview.md` 更適合給第一次接觸專案的人看，建議先看那份再看這份的細節

**CLAUDE.md 規則變動：**「不用紅色標示異常」改成「數值上升/下降可以用顏色簡單區分方向，但不能暗示醫療異常/危險」——因為 `VitalSignCard` 現在有 `trendTone`（positive/negative）紅綠標示變化方向，使用者確認這不算醫療判讀，鐵則已同步更新。

**Codex 改的（第三輪，內容重複比對後合併紀錄）：**

- **`stores/account.ts` 變成跨 Tab 共用的資料中心**：新增 `careRecipient`（`name`/`nickname`/`condition`）跟 `agentName` 兩個欄位。原本 Tab01/Tab03 到處寫死的 `{{照顧者}}`、`{{看護名稱}}` 這類佔位字串，現在都改成從這個 store 讀真的值：
  - `stores/careAgent.ts` 的 `welcomeMessage()` 用 `agentName`／`careRecipient` 組出真的歡迎詞
  - `AddScheduleView.vue`、`DashboardView.vue`（傳給 `ScheduleTable`）的照顧者名稱都改讀 `account.careRecipient.name`
  - 之後接後端時，這個 store 大概就是「使用者/照顧者基本資料」API 要對應的形狀
- **`DiaryEntryView.vue`**：日記日期從純顯示改成真的可以點開瀏覽器原生日期選擇器修改（`showPicker()`），「分享給 LINE 朋友」按鈕文案跟版面微調
- **Tab02 破關地圖再改版**：`DiaryMapView.vue` 從 flex 版面整個換成絕對定位＋百分比座標的路徑版面（`dayPositions` + `pathTop()` 算出每個泡泡在容器內的相對位置），腳印角度一樣動態算。**這是全新的版面邏輯，跟上一輪 flex 版面是不同做法**——Claude 已用 Playwright 在 402×568～402×812 共 6 種視窗高度重新測試（`/diary` 頁面，比較每個 Day 泡泡的 `getBoundingClientRect().bottom` 跟底部導覽列 `top`），**矮螢幕溢出問題已確認修復，全部高度都沒有溢出**。下方「已知缺口」的那條舊紀錄已移除
- `AppHeader`、`CareTreeHeader`、`DiaryStatsBar`、`FloatingAddButton`（新增鈕放大 12→14）、`UpgradeLimitBanner`（改成跟 `MedicalDisclaimerBanner` 同款的 `bg-ink-200` 灰底卡片＋方形關閉鈕）、`PageContainer` 陸續有小幅樣式微調（icon、間距、陰影、slot 判斷條件等），細節請直接看檔案

**Claude 改的（文件修正）：**

- **`frontend/README.md`**：原本還是 `create-vue` 產生的預設模板內容，跟專案完全無關；改成簡短說明 + 指到根目錄 `README.md` 和這份 `overview.md`

**Codex 改的（第四輪，中／印尼文介面切換，58 個檔案）：**

- 新增 `src/i18n/`（`id.ts`／`index.ts`／`README.md`），架構跟預設值變動細節見上方「多語系」；`main.ts` 註冊 `installI18n(app)`
- 幾乎所有 view／component 的固定文案改包 `$t()`，純機械式替換，邏輯行為沒變
- `NewsAwarenessBanner`（Tab03）新增可收合／展開功能（右上角箭頭按鈕），**跟上面「Tab03 細節」原本寫的「兩支新聞影片永遠顯示在最上面」不同，已在下方段落更新**
- `DiaryEntryView`（日記標題）／`AddNoteView`（便利貼標題、標籤）拿掉原本「顯示文字 + 編輯按鈕才能改」的切換邏輯（`editingTitle`/`editingTag` ref），改成欄位本身就一直可以直接輸入，行為更單純
- `stores/board.ts`／`stores/careAgent.ts` 種子資料標上 `demo: true`（詳見「多語系」段落說明目前這個 flag 還沒有實際的翻譯判斷邏輯在用它）
- 根目錄 `README.md` 補充一段語言切換說明，連結到 `frontend/src/i18n/README.md`

**Codex 改的（第五輪，小幅視覺/多語系適配）：**

- **`FamilyIllustration`（登入流程共用插圖）**：從單一 emoji 佔位圖換成真的手繪風 SVG 插畫（兩人並肩站立），只用在 `RoleSelectView`／`EmployerSetupView`／`CaregiverOnboardingView` 這三個 auth 頁面；**Tab03 `IntroView` 已移除這張插圖**（原本建檔說明畫面上方會放）
- **`IconLine`**：LINE icon 重畫，改成白底＋綠色線稿的版本
- **`RoleSelectView`**：標題「歡迎使用照見」拆成兩個字級不同的 `<span>`，印尼文版本字級縮小，避免譯文較長被截斷
- **`IntroView`**：「建置你的第一個 Care Agent」按鈕加寬、固定高度/字級，同樣是為了容納較長的印尼文按鈕文字

**Codex 改的（第六輪）：**

- **`stores/account.ts` 新增 `employer`（`id`/`name`）欄位**：Tab04 的 `NoteCard`／`NoteDetailModal`／`NotePermissionModal` 原本寫死的「雇主」文字，改成讀 `account.employer.name` 帶真名字（例如「雇主：林小姐」、「林小姐已讀取」），套用第三輪就開始的模式（account.ts 是跨 Tab 佔位字串的資料來源）
- **`frontend/index.html`**：`favicon.ico`（Vite 預設圖示）換成真的品牌 `favicon.svg`；順手清了 HTML 格式（自closing tag 加 `/>`）
- **`NewsAwarenessBanner`（Tab03）**：影片縮圖從 `h-24` 加高到 `h-36`，並把圓角加回來（`rounded-lg`）——**跟上面「Claude 改的」那條「縮圖拿掉圓角，跟 Figma 對齊」的記錄不同，目前實際樣式是有圓角的，那條舊紀錄已經過期**
- **`PlanCard`（Tab05 訂閱方案）**：卡片內容改成 `flex-wrap` 版面避免長文案擠爆，費用數字字級加大（`text-lg` → `text-3xl`）
- `AddScheduleView` 表單 textarea padding 微調

**Codex 改的（第七輪）：**

- **`DailyChatHome`（Tab03 已建檔首頁）**：打卡心情天氣後，畫面上方新增一個 3 秒後自動消失的提示卡「心情已送出，謝謝你分享今天的感受！」（`Teleport` 到 `body`、`role="status"`／`aria-live="polite"`，並尊重 `prefers-reduced-motion`）
- **`CareTreeHeader`／`AccountView`（Tab05）**：樹狀插圖改用 CSS container query（`container-type: size` + `cqw`/`cqh` 單位）依可用空間縮放，不再是固定 `max-w-[402px]`；頭像跟文字間距同步縮小配合新比例。插圖本身仍是簡化幾何圖形＋`pravatar.cc` 佔位照片，這點沒變（見「已知缺口」）
- `AddNoteView` 便利貼內容 textarea 字級微調（14px→13px）

**Codex 改的（第八輪）：**

- **`BaselineQuestionsView`（Tab03 心理基準線問卷）修正選項邏輯錯誤**：原本 5 題基準線問卷裡「心情如何」「壓力有多大」這兩題都套用同一組頻率選項（完全沒有/很少/有時候/常常/幾乎每天），語意對不上（心情、壓力程度不該用「頻率」問法）；改成各自專屬選項——心情題用「很好/還不錯/普通/不太好/非常不好」，壓力題用「完全沒有/有一點/普通/很大/非常大」，並在 `id.ts` 補上對應印尼文譯文

### Tab03 細節（★核心頁，邏輯較複雜）

`/chat`（`IntroView`）是**持久首頁**：兩支新聞影片區塊永遠顯示在最上面（可收合/展開，右上角箭頭按鈕，收合後只留一行提示文字），下方內容依是否已建檔切換：

- **未建檔**：「建置你的第一個 Care Agent」5 步驟說明 + CTA
- **已建檔**：`DailyChatHome.vue`（心情天氣打卡 + 聊天室泡泡列表；浮動話題泡泡＝舊聊天室，中央大泡泡＝開新聊天）。打卡後畫面上方會跳出一個 3 秒消失的「心情已送出」提示卡。頁面右上角有「模擬首次使用畫面」連結，點下去把 `store.agent` 設回 `null`，方便 demo/測試不用真的清資料庫

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

## 多語系（中／印尼文介面切換，Codex 建）

**純前端本地對照表，不呼叫任何翻譯 API／模型**：

- `src/i18n/id.ts`：中文原文（原封不動當 key）對應印尼文譯文的固定表，共 276 行；譯文尚未經印尼語母語者審校
- `src/i18n/index.ts`：`installI18n(app)` 在 `main.ts` 掛載時註冊全域 `$t()`；讀 `stores/onboarding.ts` 的 `language` 欄位（`'zh' | 'id'`），比對成功就回傳 `id.ts` 的譯文，否則原樣輸出中文；同時同步 `<html lang>` 跟頁面 `<title>`
- 語言偏好存在 `localStorage`（key: `care-ui-language`），重新整理後會記得；**未選擇過的預設值現在是中文 `zh`**（`onboarding.ts` 舊版預設是 `id`，這輪改成先讀 localStorage、讀不到才 fallback 中文）。這點跟 `CLAUDE.md`「看護端介面語言：主張印尼文為主」字面上不同，但使用者已確認可以接受——理由是介面本來就能隨時切換語言，預設值不是唯一入口
- 語言切換入口：`CaregiverOnboardingView`（onboarding 一次性設定）跟 Tab05 `LanguageModal`
- 幾乎全部 view/component 的固定 UI 文案都已包上 `$t('原文')`（含變數用 `$t('...{name}...', { name })`）；只有**使用者自己輸入的內容**（日記內容、聊天訊息、便利貼內容等）維持原文不翻譯
- `stores/board.ts`、`stores/careAgent.ts` 的種子資料現在都標了 `demo: true`（`StickyNote.demo`、`ChatRoom.demo`、`ChatMessage.demo`），用來跟使用者之後自己新增的內容區分——**目前這個 flag 前端還沒有實際拿來做「只翻譯 demo 內容」的判斷邏輯，看起來是先標記、翻譯邏輯本身其實對所有字串一視同仁（因為 `$t()` 是包在模板寫死的文案上，使用者輸入的欄位模板裡本來就沒被包 `$t()`）**，這個 flag 目前主要功能是文件用途（跟 `i18n/README.md` 的說明對應），之後有真的動態內容判斷需求時可以重新利用
- 日記日期顯示：語言為印尼文時改用 `Intl.DateTimeFormat('id-ID', { dateStyle: 'full' })`，中文時維持原本的民國曆 `toMinguoDate()`

## 跟後端串接（現在還沒做，但已知會需要什麼）

見根目錄 `CLAUDE.md` 的既有 API：

- `POST /api/users`：`EmployerSetupView` 生成邀請碼、`CaregiverOnboardingView` 完成 onboarding 時，應該要建立/更新使用者
- 「使用 LINE 註冊」按鈕目前只是前端導頁，還沒接真的 LINE Login/OAuth——**這需要新的登入用端點，跟現有 `POST /api/line/webhook` 是兩件事**：`/api/line/webhook` 是 LINE Messaging API 的 webhook，用來接收 LINE OA 收到的事件（雇主端交流板回覆、之類），不是給使用者登入用的 OAuth callback
- Tab01 生命徵象卡、排程表（`stores/schedule.ts`）是寫死的假資料，之後要換成打 API 讀寫
- Tab02 日記（`stores/diary.ts`）需要存/讀日記的 API，以及印尼語 ASR 服務（`DiaryEntryView.vue` 的「AI 語音辨識」是空的 stub，見檔案內 TODO）
- Tab03（`stores/careAgent.ts`）缺口最大：
  - System Prompt / Temperature / Guardrail 要送到後端實際生成 Care Agent persona
  - 5 題基準線問卷答案要送出去建立心理基準線
  - 聊天室送出訊息（`ChatInputBar.vue` → `store.sendMessage`）要呼叫真正的 Care Agent API 拿 AI 回覆；同一次呼叫也要做 CLAUDE.md 說的「情緒分析→高壓觸發雇主 LINE 告知（不傳內容）」＋「抽取照護資訊寫進 Tab01」，這兩件事前端完全看不到、也不應該看到
  - 聊天室與 System Prompt 的語音輸入都是 stub，等印尼語 ASR
- Tab04 便利貼（`stores/board.ts`）的「已讀取/尚未讀取」是寫死假資料，實際要對應雇主端 LINE 已讀狀態——**待確認可行性**：LINE Messaging API 目前沒有提供「使用者是否已讀某則推播訊息」的事件或查詢，一般作法是退而求其次用「雇主是否點擊過訊息裡的連結」之類的替代訊號來模擬已讀，需要後端這邊評估怎麼做，不是單純接 webhook 就能拿到
- Tab05 訂閱方案（`stores/account.ts`）的「變更方案」是 stub，沒有實際付款流程
- `stores/account.ts` 現在也存了 `careRecipient`／`agentName`／`employer`，跨 Tab01/Tab03/Tab04 共用，之後應該對應到「使用者基本資料 + 照顧對象資料 + 雇主資料」的 API
- **前後端角色命名不一致**：前端（`stores/onboarding.ts`、`RoleSelectView` 等）用 `caregiver`／`employer`；後端（`backend/app/models/user.py` 的 `UserRole`）用 `nurse`／`owner`。接 API 時要在某一層做映射（`caregiver` ↔ `nurse`、`employer` ↔ `owner`），目前兩邊都還沒有人統一或轉換
- **UI 介面文字的中/印尼文切換是純前端靜態對照表**（`src/i18n/`），不需要後端翻譯 API。後端真正需要處理的翻譯只有「使用者實際輸入內容」的印尼語→中文（CLAUDE.md 待定技術選型那條），跟這組介面切換是兩回事，不要搞混

## 已知缺口

- **沒有路由守衛**：直接打 `/dashboard`、`/chat`、`/board`、`/account` 等網址可以完全繞過登入流程。MVP demo 階段刻意如此（方便直接測任一頁），正式串接後端後要補上
- Tab03 新聞影片是寫死的兩個 YouTube 影片 ID（`NewsAwarenessBanner.vue` 的 `videos` 陣列），影片下架或要換片要手動改
- Tab04 便利貼權限簡化成「只有自己／雇主」二選一（單一雇主帳號），規格文件原本想支援指定多個家人聯絡人，等有多聯絡人資料模型再擴充
- Tab05 樹狀插圖（`CareTreeHeader.vue`）用簡化幾何圖形逼近，頭像是 pravatar.cc 佔位照片，Figma 原稿是手繪風插畫，還沒有可匯出的素材檔
- 產品名稱曾在不同 Figma 稿打成三種寫法，目前統一用「404: Care Can Be Found」（文法正確版本），之後 Figma 若又有新版本要再對齊

## 開發與部署

```bash
cd frontend
npm ci           # 或 npm install
npm run dev      # http://localhost:5173
npm run build    # 型別檢查 + build，產出 dist/
```

部署走 **Railway**（CLI 直接上傳本機資料夾，沒有接 GitHub 自動部署，執行者需要目標 Railway 專案的部署權限）：

```bash
cd frontend
railway login
railway link       # 選正確的 project / environment / service
railway status      # 確認部署目標對不對
railway up . --path-as-root --service <前端服務名稱>
```

Service 設定：Root Directory 用預設根目錄、Build Command 設 `npm run build`、Start Command 設 `npm run start`（內部是 `serve -s dist`，會讀 Railway 注入的 `PORT`）。部署後到該 Service 的 Networking 設定產生公開網域即可瀏覽。詳細版本另見根目錄 `README.md`。

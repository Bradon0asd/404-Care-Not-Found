# 404: Care Can Be Found

給移工看護一個記錄照護生活、書寫心情與獲得陪伴的私人空間。

本專案由 **404: Care Not Found** 團隊於 **BUILDMODE Hackathon 2026 · Social Impact** 開發。本頁說明 `frontend` 分支的前端應用與操作方式。

## 專案定位

看護端以手機版 Web App 提供照護紀錄、秘密日記、心情對話與便利貼交流。雇主端規劃透過 LINE 官方帳號接收照護摘要與分享訊息。

- **看護的私人空間**：秘密日記預設僅自己可見，便利貼可選擇是否分享給雇主。
- **照護生活紀錄**：呈現紀錄與數值變化，不提供醫療診斷。
- **陪伴式對話**：Care Agent 的目標是協助看護表達心情、整理生活經驗。

## 目前功能

目前為可操作的前端展示版本，資料由 Pinia store 與示範資料提供。**尚未串接後端 API，重新整理頁面後，本次新增或修改的資料會重設。**

| 頁面 | 路徑 | 可體驗內容 |
| --- | --- | --- |
| 登入與建檔 | `/auth/role` | 角色選擇、看護基本資料、雇主邀請碼流程 |
| Tab01 照護紀錄 | `/dashboard` | 生命徵象卡片、平日／周末排程、07:00–23:00 時間表與新增排程 |
| Tab02 秘密日記 | `/diary` | 日期地圖、撰寫日記與分享設定 |
| Tab03 跟我聊聊 | `/chat` | Care Agent 建檔、一次性問卷、心情天氣、聊天室列表與文字輸入 |
| Tab04 便利貼牆 | `/board` | 狀態／層級篩選、便利貼詳情、新增與分享權限設定 |
| Tab05 我的帳戶 | `/account` | 帳戶資訊、語言選項、登出與訂閱方案展示 |

LINE 登入／推播、語音辨識、翻譯、AI 即時回覆與付款仍待串接；畫面中的既有 AI 對話與便利貼已讀狀態為示範資料。登入流程尚未提供正式身分驗證與路由保護。

## 技術棧

Vue 3、TypeScript、Vite、Vue Router、Pinia、Tailwind CSS v4。

## 本機啟動

環境需求：Node.js `^22.18.0 || >=24.12.0` 與 npm。

從 Repo 根目錄執行：

```bash
cd frontend
npm ci
npm run dev
```

開啟終端機顯示的網址，預設為 `http://localhost:5173`。首頁會進入角色選擇頁，也可直接使用上方路徑預覽各分頁。

## 建置與檢查

以下指令皆在 `frontend/` 執行：

| 指令 | 用途 |
| --- | --- |
| `npm run build` | TypeScript 型別檢查與正式建置，輸出至 `dist/` |
| `npm run preview` | 本機預覽建置結果 |
| `npm run type-check` | 單獨執行型別檢查 |
| `npm run lint` | 執行 Oxlint 與 ESLint，包含自動修正 |
| `npm run format` | 格式化 `src/`，會修改檔案 |
| `npm run start` | 使用 `serve -s dist` 提供建置後的 SPA |

## Railway 部署

目前採用 **Railway CLI 上傳本機前端資料夾**。此流程不依賴 GitHub 自動部署；執行者需要有目標 Railway 專案的部署權限。

1. 在 Railway 專案建立或選擇前端 Service。
2. 在該 Service 設定 Build Command 為 `npm run build`、Start Command 為 `npm run start`。
3. 在本機 `frontend/` 目錄執行：

```bash
railway login
railway link
railway status
railway up . --path-as-root --service <前端服務名稱>
```

將 `<前端服務名稱>` 替換為實際名稱。`railway link` 時選擇正確的專案、環境與前端 Service，並用 `railway status` 確認部署目標。

此指令將 `frontend/` 當作上傳根目錄，Service 的 Root Directory 應使用預設根目錄。部署後，在 Service 的 Networking 設定產生公開網域，即可瀏覽網站。

後端請使用同專案內的獨立 Service，分別管理啟動指令與環境變數。

## 目錄與協作文件

```text
.
├── README.md                專案介紹與前端使用入口
├── frontend/
│   ├── src/
│   │   ├── components/      共用元件與各分頁元件
│   │   ├── views/           登入流程與五個分頁
│   │   ├── stores/          Pinia 狀態與示範資料
│   │   ├── router/          路由設定
│   │   ├── assets/          樣式與色票
│   │   └── utils/           共用工具
│   ├── docs/                前端架構與協作說明
│   └── package.json         套件與執行指令
└── backend/                 Flask 後端程式
```

- [前端架構與串接說明](frontend/docs/overview.md)
- [專案定位與協作規則](CLAUDE.md)
- [後端程式目錄](backend/)

前端功能與串接細節請參閱前端文件；後端開發與執行方式請依後端團隊文件為準。

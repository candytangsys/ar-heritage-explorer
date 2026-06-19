# AR Heritage Explorer

**淡江大學校園 AR 歷史地標探索系統 / Tamkang University Campus AR Heritage Explorer**

🌐 **語言 / Language：** [繁體中文](#繁體中文) ｜ [English](#english)

開發者 / Author：candytangsys ｜ 最後更新 / Last updated：2026-06-19

---

<a id="繁體中文"></a>
## 繁體中文

---

## 一、專案概述

### 1.1 專案背景

本專案結合擴增實境（AR）與地理資訊系統（GPS），打造一套以手機瀏覽器為主要載體的校園歷史地標互動探索平台。使用者無需安裝 App，掃描 QR Code 或直接輸入網址即可使用。

### 1.2 專案目標

- 讓學生與訪客透過 AR 技術認識淡江大學的歷史建築與文化地景
- 結合遊戲化機制（Gamification）提升教育內容的吸引力
- 建立可擴充的地標資料管理系統，供管理員維護內容

### 1.3 設計靈感

- Pokémon GO 的 GPS 定點觸發與集點機制
- 創作者 MaiAZhen 的 XR 現實疊加概念
- 台灣文化部古蹟數位化推廣方向

---

## 二、系統架構

### 2.1 技術棧

| 層級 | 技術 | 說明 |
|------|------|------|
| 前端 | HTML5 / CSS3 / JavaScript | 介面與互動邏輯 |
| AR 鏡頭 | 原生 `getUserMedia` | 免標記鏡頭實景，無需安裝 App、無需印標記 |
| 定位導覽 | Geolocation + Device Orientation | GPS 距離判定與指南針雷達導覽 |
| 地圖 | Leaflet.js 1.9.4 | 互動地圖與地標標記 |
| 後端 | Python Flask 3.1.3 | API 路由與伺服器邏輯 |
| 認證 | Flask-Login 0.6.3 | 管理員登入與 Session 管理 |
| 資料庫 | SQLite | 輕量本地資料庫 |
| 部署 | Render.com（Free Tier） | 雲端 HTTPS 部署 |
| 版本控制 | Git + GitHub | 原始碼管理 |

### 2.2 系統架構圖

```
使用者裝置（手機瀏覽器）
        │
        │ HTTPS
        ▼
  Render.com 伺服器
        │
   Python Flask
   ┌────┴────┐
   │         │
前端路由   API 路由
HTML/CSS/JS  /api/landmarks
AR.js        /api/game/*
Leaflet.js   │
             │
          SQLite DB
          ┌──┴──────────┐
          │             │
       landmarks     players
       admins        player_progress
```

### 2.3 專案資料夾結構

```
ar-heritage-explorer/
├── app.py                  ← Flask 主程式、所有路由
├── database.py             ← 資料庫初始化、Schema、8 個地標種子資料
├── requirements.txt        ← Python 套件清單
├── render.yaml             ← Render 部署設定
├── heritage.db             ← SQLite 資料庫（自動生成）
├── LANDMARKS_DATA.md       ← 地標原始資料文件
├── images/                 ← 地標原始照片（開發用）
├── .gitignore
├── static/
│   └── uploads/            ← 地標圖片（landmark_N_M.jpg 命名規則）
└── templates/
    ├── index.html          ← 地圖瀏覽頁（現由 /game 替代為首頁入口）
    ├── landmark.html       ← 地標詳細資訊頁 + 遊戲解鎖整合
    ├── ar_marker.html      ← AR Marker 掃描頁
    ├── ar_gps.html         ← GPS AR 探索頁
    ├── admin_login.html    ← 管理員登入
    ├── admin_dashboard.html← 後台地標列表
    ├── admin_form.html     ← 新增/編輯地標表單
    ├── game_start.html     ← 遊戲開始/暱稱輸入（網站入口首頁）✅
    ├── game_map.html       ← 遊戲地圖 ✅
    ├── game_unlock.html    ← 解鎖慶祝動畫頁 ✅
    └── game_profile.html   ← 玩家成就頁 ✅
```

---

## 三、使用者角色

| 角色 | 說明 | 權限 |
|------|------|------|
| 一般訪客 | 學生、訪客、新生 | 瀏覽地圖、查看地標、AR 體驗、玩探索遊戲 |
| 管理員 | 系統管理者 | 登入後台、新增/編輯/刪除地標、管理所有資料 |

---

## 四、功能規格

### 4.1 遊戲入口首頁（game_start.html）← 網站入口

- 路由 `/` 直接導向 `/game`（game_start.html）
- 輸入暱稱後產生 device_id 儲存至 localStorage
- 呼叫 `/api/game/register` 後跳轉至遊戲地圖

### 4.2 遊戲地圖（game_map.html，主畫面）

- Leaflet.js 互動地圖，聚焦淡江大學校園
- 已解鎖地標顯示藍色發光標記，未解鎖顯示灰色
- 點擊任一標記（含未解鎖）彈窗 →「前往介紹頁」直接進地標詳細頁
- **左下角常駐兩顆同色入口按鈕**（灰底藍字）：
  - 📷 AR 掃描：用 GPS 自動找最近地標，直接進該地標鏡頭頁
  - 📡 GPS 定位：進 GPS 雷達導覽頁
- 右上角顯示點數，底部顯示解鎖進度條，右下角為成就頁入口

### 4.3 地標詳細頁（landmark.html）

- 顯示封面圖片（無圖時顯示預設 emoji 佔位）
- 地標名稱（中英文）、地址、歷史介紹（中英文）、歷史人物小故事
- 頁面上方提供 📷 AR 掃描 / 📡 GPS 定位 入口
- **未解鎖時**：隱藏測驗，顯示「🔒 尚未解鎖」提示與前往現場解鎖的按鈕
- **已解鎖後**：開放歷史小測驗（四選一），答對呼叫 `/api/game/quiz` 加 +10 分（每地標限一次）

### 4.4 解鎖慶祝頁（game_unlock.html）

- 「📍 抵達現場，解鎖成功！」動畫與點數顯示
- 達成全蒐集時觸發 +100 pts 特別獎勵提示
- 主按鈕「📖 看介紹並答題 +10」導向該地標介紹頁；另有「繼續探索地圖」

### 4.5 玩家成就頁（game_profile.html）

- 顯示玩家暱稱、稱號、總點數
- 5 個成就徽章（已解鎖/未解鎖狀態）
- 「繼續探索」按鈕

### 4.6 地圖瀏覽頁（index.html）

- 獨立的純覽地圖（無遊戲系統）
- Leaflet.js 互動地圖
- 地標以藍色發光圓點標記，點擊彈出 Popup 卡片（含封面圖）
- 地標資料透過 `/api/landmarks` 動態載入
- 目前不作為入口，可由導覽列補充連結

### 4.7 AR 鏡頭（ar_marker.html）

- **免標記（markerless）**：直接呼叫後鏡頭作為實景背景，不需列印或顯示 Hiro Marker
- 鏡頭正常開啟時畫面乾淨無浮動提示，可直接掃描；**僅在開不了鏡頭時**才顯示紅色提示與地標資訊卡
- 背景持續以 GPS 計算與本地標距離：≤ 50 公尺時出現「✅ 解鎖此地標」按鈕，呼叫 `/api/game/unlock` 解鎖
- 左上角「← 返回地圖」直接回主畫面（不會進入介紹頁）
- 需要 HTTPS 環境 + 相機 / 定位權限

### 4.8 GPS 導覽（ar_gps.html）

- **無鏡頭**：以指南針式雷達 + 距離清單導引使用者走向地標
- 取得 GPS 座標，計算各地標的距離與方位角
- 雷達光點與清單箭頭會隨手機朝向即時旋轉（指向目標方向）
- 走近 50 公尺內且未解鎖的地標，點擊該列即可解鎖；已解鎖則連往介紹頁答題加分
- iOS 13+ 會請求「方向感應」權限以啟用羅盤
- 需要 HTTPS 環境 + 定位（與方向感應）權限

### 4.9 管理員後台

- **登入**：帳號密碼驗證（Werkzeug hash 加密）
- **地標列表**：統計、縮圖表格、查看/編輯/刪除操作
- **新增/編輯**：中英文名稱、地址、GPS 座標、介紹、圖片上傳、測驗設定

---

## 五、資料庫規格

### 5.1 landmarks 表（地標資料）

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| id | INTEGER PK | 自動遞增主鍵 |
| name_zh | TEXT | 地標中文名稱 |
| name_en | TEXT | 地標英文名稱 |
| lat | REAL | GPS 緯度 |
| lng | REAL | GPS 經度 |
| address | TEXT | 地址描述 |
| description_zh | TEXT | 中文歷史介紹 |
| description_en | TEXT | 英文歷史介紹 |
| history_story | TEXT | 歷史人物小故事 |
| image_path | TEXT | 封面圖片路徑（uploads/landmark_N_1.jpg） |
| quiz_question | TEXT | 測驗題目 |
| quiz_a | TEXT | 選項 A |
| quiz_b | TEXT | 選項 B |
| quiz_c | TEXT | 選項 C |
| quiz_d | TEXT | 選項 D |
| quiz_answer | TEXT | 正確答案（A/B/C/D） |
| created_at | TIMESTAMP | 建立時間 |

### 5.2 admins 表（管理員帳號）

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| id | INTEGER PK | 自動遞增主鍵 |
| username | TEXT UNIQUE | 帳號 |
| password_hash | TEXT | Werkzeug 雜湊密碼 |

### 5.3 players 表（玩家資料）

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| id | INTEGER PK | 自動遞增主鍵 |
| nickname | TEXT | 玩家暱稱 |
| device_id | TEXT UNIQUE | 瀏覽器裝置識別碼 |
| total_points | INTEGER | 累積總點數 |
| created_at | TIMESTAMP | 建立時間 |

### 5.4 player_progress 表（遊戲進度）

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| id | INTEGER PK | 自動遞增主鍵 |
| device_id | TEXT | 對應玩家裝置 ID |
| landmark_id | INTEGER | 對應地標 ID |
| unlocked_at | TIMESTAMP | 解鎖時間 |
| quiz_correct | BOOLEAN | 測驗是否答對 |
| points_earned | INTEGER | 本次獲得點數 |

---

## 六、遊戲系統規格【Phase 3 ✅ 完成】

### 6.1 遊戲名稱

**淡江探索者 / TKU Explorer**

### 6.2 核心玩法

玩家輸入暱稱後進入遊戲地圖（主畫面），實際走訪 8 個校園地標。**到現場用 AR 鏡頭掃描或 GPS 定位（距離 ≤ 50m）即可解鎖**（+30），解鎖後進地標介紹頁作答歷史小測驗額外加分（答對 +10）。累積點數並解鎖成就稱號。

**流程：** 地圖主畫面 →（📷 AR 掃描 / 📡 GPS 定位）→ 到現場解鎖（+30）→ 解鎖慶祝頁 → 介紹頁答題加分（+10）。

### 6.3 點數規則

| 行為 | 點數 |
|------|------|
| 到現場解鎖地標（AR 鏡頭掃描 / GPS 定位，距離 ≤ 50m） | +30 pts |
| 歷史小測驗答對（解鎖後才能作答，每地標限一次） | +10 pts |
| 蒐集全部 8 個地標 | +100 pts（特別獎勵） |

> **解鎖機制（重要）：** 解鎖改為「實際走到現場」——用 AR 鏡頭掃描或 GPS 定位，當裝置距地標 50 公尺內即可解鎖（伺服器端以 Haversine 距離驗證）。歷史小測驗改為**解鎖後的額外加分**，不再是解鎖條件。

### 6.4 成就稱號

| 稱號 | 解鎖條件 |
|------|---------|
| 🐣 淡江新鮮人 | 解鎖第 1 個地標 |
| 🗺️ 校園探索者 | 解鎖 3 個地標 |
| 📚 淡江學者 | 累積答對 5 題 |
| 🏆 淡江通 | 解鎖全部地標 |
| ⭐ 淡江達人 | 全部地標滿分通關 |

### 6.5 遊戲頁面

| 頁面 | 路由 | 狀態 |
|------|------|------|
| game_start.html | /game | ✅ 完成（網站入口） |
| game_map.html | /game/map | ✅ 完成 |
| game_unlock.html | /game/unlock | ✅ 完成 |
| game_profile.html | /game/profile | ✅ 完成 |

---

## 七、API 路由規格

### 頁面路由

| 方法 | 路由 | 說明 |
|------|------|------|
| GET | / | 重定向至 /game |
| GET | /game | 遊戲入口（暱稱輸入）← 網站首頁 |
| GET | /game/map | 遊戲地圖 |
| GET | /game/profile | 玩家成就頁 |
| GET | /game/unlock | 解鎖慶祝頁 |
| GET | /landmark/<id> | 地標詳細頁 |
| GET | /ar/marker/<id> | AR Marker 掃描頁 |
| GET | /ar/gps | GPS AR 探索頁 |
| GET | /admin/login | 管理員登入頁 |
| POST | /admin/login | 登入驗證 |
| GET | /admin/logout | 登出 |
| GET | /admin | 後台地標列表 |
| GET | /admin/landmark/new | 新增地標頁 |
| POST | /admin/landmark/new | 儲存新地標 |
| GET | /admin/landmark/<id>/edit | 編輯地標頁 |
| POST | /admin/landmark/<id>/edit | 更新地標 |
| POST | /admin/landmark/<id>/delete | 刪除地標 |

### API 路由

| 方法 | 路由 | 說明 |
|------|------|------|
| GET | /api/landmarks | 取得所有地標 JSON |
| POST | /api/game/register | 玩家註冊（輸入暱稱） |
| GET | /api/game/progress | 取得玩家進度 |
| POST | /api/game/unlock | 定位解鎖（傳 lat/lng，伺服器驗證 ≤ 50m，+30 pts） |
| POST | /api/game/quiz | 歷史測驗加分（須已解鎖，答對 +10 pts，限一次） |

---

## 八、部署資訊

| 項目 | 內容 |
|------|------|
| 平台 | Render.com Free Tier |
| 網址 | https://ar-heritage-explorer.onrender.com |
| GitHub | https://github.com/candytangsys/ar-heritage-explorer |
| Build Command | pip install -r requirements.txt && python database.py |
| Start Command | gunicorn app:app |
| 注意事項 | 免費方案閒置後休眠，首次載入可能等待 30–50 秒 |

---

## 九、開發進度

| Phase | 內容 | 狀態 |
|-------|------|------|
| Phase 1 | 地圖 + 地標詳細頁 + 後台 CRUD + 小測驗 | ✅ 完成 |
| Phase 2 | AR Marker 掃描 + GPS AR 探索 | ✅ 完成 |
| Phase 3 | 遊戲系統 + 8 個淡江校園地標資料 + 實景照片 | ✅ 完成 |
| Phase 4 | 排行榜 + 分享功能 + UI 優化 | 📋 規劃中 |

### Phase 3 完成清單

- [x] 遊戲入口 (game_start.html)：暱稱輸入、device_id 生成、網站入口重定向
- [x] 遊戲地圖 (game_map.html)：Leaflet 互動地圖、進度追蹤、發光標記
- [x] 解鎖慶祝頁 (game_unlock.html)：解鎖動畫、點數顯示、全蒐集獎勵
- [x] 玩家成就頁 (game_profile.html)：5 個徽章系統、點數顯示、稱號
- [x] 遊戲 API：register / unlock / progress 完整實作
- [x] 點數系統：解鎖 +10、答對 +20、答錯 +5、全蒐集 +100
- [x] 成就系統：5 個稱號
- [x] landmark.html 遊戲整合：答題後自動呼叫解鎖 API
- [x] 8 個淡江大學校園地標（精確 GPS 座標、中英文介紹、歷史故事、測驗題）
- [x] 各地標封面照片（landmark_N_1.jpg，每個地標 1–3 張）

---

## 十、Phase 4 規格【規劃中】

### 10.1 目標

提升使用者留存率與社群傳播，讓探索遊戲更具競爭性與分享動機。

### 10.2 功能項目

#### 排行榜（Leaderboard）
- 顯示前 10 名玩家（暱稱 + 點數 + 蒐集數）
- 路由：`/game/leaderboard`
- API：`GET /api/game/leaderboard`
- 資料來源：players 表，依 total_points DESC 排序

#### 探索紀錄（個人時間軸）
- 在 game_profile.html 新增已解鎖地標清單
- 顯示解鎖時間、答題結果、獲得點數

#### 分享功能
- 地標詳細頁新增「分享此地標」按鈕
- 使用 Web Share API（手機原生分享）
- Fallback：複製連結到剪貼簿

#### UI 全面優化
- 統一深色主題（`#0f1923` 底色、`#4fc3f7` 主色）
- game_map.html 加入動畫過場與載入 spinner
- landmark.html 圖片 gallery（多張照片左右滑動）
- 手機底部導覽列固定顯示（地圖 / 成就 / 排行榜）

#### 地標圖片 Gallery
- landmark.html 支援多張照片（landmark_N_1.jpg ~ landmark_N_3.jpg）
- 左右滑動切換（touch swipe）

### 10.3 新增 API

| 方法 | 路由 | 說明 |
|------|------|------|
| GET | /game/leaderboard | 排行榜頁面 |
| GET | /api/game/leaderboard | 取得前 10 名玩家 JSON |

### 10.4 預計新增/修改檔案

| 檔案 | 變更類型 | 說明 |
|------|---------|------|
| templates/game_leaderboard.html | 新增 | 排行榜頁面 |
| templates/game_profile.html | 修改 | 加入解鎖地標時間軸 |
| templates/landmark.html | 修改 | 圖片 gallery + 分享按鈕 |
| templates/game_map.html | 修改 | 底部導覽列加入排行榜入口 |
| app.py | 修改 | 新增 leaderboard 路由 |

---

## 十一、校園地標清單

系統共 8 個淡江大學校園地標：

| # | 地標名稱 | GPS 緯度 | GPS 經度 | 照片數 |
|---|---------|---------|---------|-------|
| 1 | 驚聲紀念大樓 | 25.17550007 | 121.45133989 | 1 張 |
| 2 | 覺生紀念圖書館 | 25.17477507 | 121.45107288 | 2 張 |
| 3 | 海事博物館暨黑天鵝展示廳 | 25.17620523 | 121.45042453 | 3 張 |
| 4 | 書卷廣場 | 25.17554047 | 121.45062699 | 3 張 |
| 5 | 文錙藝術中心 | 25.17507179 | 121.45219130 | 3 張 |
| 6 | 學生活動中心 | 25.17475595 | 121.45033093 | 3 張 |
| 7 | 五虎崗綜合球場 | 25.17560869 | 121.45386137 | 2 張 |
| 8 | 覺生綜合大樓 | 25.17443460 | 121.45083835 | 2 張 |

所有地標均包含：中英文名稱、精確 GPS 座標（實地確認）、中英文歷史介紹、歷史故事、4 選 1 測驗、封面照片。

---

## 十二、快速開始

### 本地開發

```bash
# 1. 進入專案目錄
cd ar-heritage-explorer

# 2. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 初始化資料庫（自動建立 8 個地標）
python database.py

# 5. 執行應用
python app.py
```

訪問 `http://localhost:5000`（自動跳轉至遊戲入口）

### 管理員後台

- 路由：`http://localhost:5000/admin/login`
- 帳號：admin / 密碼：admin123

### 重置資料庫

```bash
rm heritage.db
python database.py
```

---

## 十三、技術支援

- **GitHub**: https://github.com/candytangsys/ar-heritage-explorer
- **開發者**: candytangsys
- **最後更新**: 2026年6月19日

[⬆ 回到語言選單 / Back to top](#ar-heritage-explorer)

---

<a id="english"></a>
## English

**Tamkang University Campus AR Historical Landmark Exploration System**
Author: candytangsys · Last updated: June 19, 2026

### 1. Overview

This project combines Augmented Reality (AR) and GPS to build an interactive campus heritage exploration platform delivered through the mobile browser. No app install is required — users scan a QR code or open a URL.

**Goals:** help students and visitors discover Tamkang University's historical buildings through AR; increase engagement with gamification; provide an extensible content-management system for administrators.

### 2. Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | HTML5 / CSS3 / JavaScript | UI and interaction logic |
| AR Camera | Native `getUserMedia` | Markerless camera overlay (no app, no printed marker) |
| Navigation | Geolocation + Device Orientation | Radar / bearing guide to landmarks |
| Maps | Leaflet.js 1.9.4 | Interactive map and markers |
| Backend | Python Flask 3.1.3 | API routing and server logic |
| Auth | Flask-Login 0.6.3 | Admin login and session management |
| Database | SQLite | Lightweight local database |
| Deployment | Render.com (Free Tier) | Cloud HTTPS hosting |

### 3. User Roles

| Role | Permissions |
|------|-------------|
| Visitor | Browse map, view landmarks, AR camera, GPS guide, play the game |
| Admin | Log in, create/edit/delete landmarks, manage all data |

### 4. Features

- **Game Entry (`game_start.html`)** — site entry. `/` redirects to `/game`; enter a nickname → a `device_id` is stored in localStorage → `/api/game/register` → game map.
- **Game Map (`game_map.html`, main screen)** — Leaflet map centered on campus; unlocked landmarks glow blue, locked ones are gray. Tapping any marker opens its detail page. Two always-on entry buttons (bottom-left): 📷 AR Scan (GPS picks the nearest landmark and opens its camera page) and 📡 GPS Locate (opens the radar guide).
- **Landmark Detail (`landmark.html`)** — bilingual name, address, history, a historical-figure story. While locked, the quiz is hidden and an unlock prompt is shown; once unlocked, the 4-option quiz opens and a correct answer calls `/api/game/quiz` for +10 bonus (once per landmark).
- **Unlock Celebration (`game_unlock.html`)** — "arrived on-site" animation, points, and a +100 bonus when all landmarks are collected. Primary button leads to the detail page to take the quiz.
- **Player Achievements (`game_profile.html`)** — nickname, title, total points, and 5 badges.
- **AR Camera (`ar_marker.html`)** — markerless: opens the rear camera as a live backdrop. Clean view when the camera works; the info card/error only appears if the camera can't open. Background GPS shows distance and an "Unlock" button appears within 50 m. Back button returns to the map.
- **GPS Guide (`ar_gps.html`)** — no camera; a compass-style radar plus a list of landmarks with direction arrows and live distances. Tap a nearby (≤ 50 m) locked landmark to unlock it. Requests iOS device-orientation permission for the compass.
- **Admin Panel** — Werkzeug-hashed login; landmark list with stats and thumbnails; create/edit form with bilingual fields, GPS, image upload, and quiz settings.

### 5. Database Schema

- **`landmarks`** — `id`, `name_zh`, `name_en`, `lat`, `lng`, `address`, `description_zh`, `description_en`, `history_story`, `image_path`, `quiz_question`, `quiz_a`–`quiz_d`, `quiz_answer`, `created_at`.
- **`admins`** — `id`, `username` (UNIQUE), `password_hash`.
- **`players`** — `id`, `nickname`, `device_id` (UNIQUE), `total_points`, `created_at`.
- **`player_progress`** — `id`, `device_id`, `landmark_id`, `unlocked_at`, `quiz_correct`, `points_earned`.

### 6. Game System (淡江探索者 / TKU Explorer)

Enter a nickname → physically travel to each of the 8 landmarks → unlock by being on-site (AR camera scan or GPS, within 50 m) → optionally answer the history quiz for bonus points → accumulate points and earn titles.

| Action | Points |
|--------|--------|
| Unlock on-site (AR scan / GPS, distance ≤ 50 m) | +30 |
| History quiz correct (only after unlock, once per landmark) | +10 |
| Collect all 8 landmarks | +100 (bonus) |

> **Unlock mechanic:** unlocking now requires actually visiting the site — the device must be within 50 m of the landmark (verified server-side with the Haversine formula via AR camera or GPS). The quiz is a post-unlock bonus, no longer the unlock gate.

**Titles:** 🐣 TKU Freshman (1 unlocked) · 🗺️ Campus Explorer (3 unlocked) · 📚 TKU Scholar (5 correct) · 🏆 TKU Master (all unlocked) · ⭐ TKU Legend (perfect score on all).

### 7. API Routes

**Pages:** `GET /` → `/game`, `/game`, `/game/map`, `/game/profile`, `/game/unlock`, `/landmark/<id>`, `/ar/marker/<id>` (AR camera), `/ar/gps` (GPS guide), `/admin/login`, `/admin/logout`, `/admin`, `/admin/landmark/new`, `/admin/landmark/<id>/edit`, `/admin/landmark/<id>/delete`.

**API:** `GET /api/landmarks` · `POST /api/game/register` · `GET /api/game/progress` · `POST /api/game/unlock` (location-based, ≤ 50 m, +30) · `POST /api/game/quiz` (post-unlock bonus, +10).

### 8. Deployment

| Item | Value |
|------|-------|
| Platform | Render.com Free Tier |
| URL | https://ar-heritage-explorer.onrender.com |
| Build | `pip install -r requirements.txt && python database.py` |
| Start | `gunicorn app:app` |
| Note | Free tier sleeps when idle; first load may take 30–50 s |

### 9. Progress

| Phase | Content | Status |
|-------|---------|--------|
| Phase 1 | Map + detail + admin CRUD + quiz | ✅ Done |
| Phase 2 | AR camera + GPS guide | ✅ Done |
| Phase 3 | Game system + 8 TKU landmarks + real photos | ✅ Done |
| Phase 4 | Leaderboard + sharing + UI polish | 📋 Planned |

### 10. Campus Landmarks (8)

Each landmark has a bilingual name, verified GPS coordinates, bilingual history, a story, a 4-option quiz, and cover photos:

| # | Landmark | Lat | Lng |
|---|----------|-----|-----|
| 1 | Ching-Sheng Memorial Building | 25.17550007 | 121.45133989 |
| 2 | Chueh-Sheng Memorial Library | 25.17477507 | 121.45107288 |
| 3 | Maritime Museum & Black Swan Hall | 25.17620523 | 121.45042453 |
| 4 | Scroll Plaza | 25.17554047 | 121.45062699 |
| 5 | Wen-Tzao Arts Center | 25.17507179 | 121.45219130 |
| 6 | Student Activity Center | 25.17475595 | 121.45033093 |
| 7 | Wuhukang Sports Court | 25.17560869 | 121.45386137 |
| 8 | Chueh-Sheng Complex Building | 25.17443460 | 121.45083835 |

### 11. Quick Start

```bash
cd ar-heritage-explorer
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python database.py         # creates 8 landmarks
python app.py
```

Open `http://localhost:5000` (auto-redirects to the game entry).
Admin panel: `http://localhost:5000/admin/login` — username `admin`, password `admin123`.
Reset DB: `rm heritage.db && python database.py`.

> Note: the AR camera and GPS compass require **HTTPS** (or `localhost`) and camera/location permissions to work on a phone.

[⬆ Back to top / 回到語言選單](#ar-heritage-explorer)

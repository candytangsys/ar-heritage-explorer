# AR Heritage Explorer

**淡江大學校園 AR 歷史地標探索系統**
撰寫日期：2026年6月
開發者：candytangsys

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
| AR 引擎 | AR.js + A-Frame 1.4.2 | Web-based AR，無需安裝 App |
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
├── database.py             ← 資料庫初始化與 Schema
├── requirements.txt        ← Python 套件清單
├── render.yaml             ← Render 部署設定
├── heritage.db             ← SQLite 資料庫（自動生成）
├── .gitignore
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── map.js
│   └── uploads/            ← 地標圖片上傳目錄
└── templates/
    ├── index.html          ← 使用者地圖首頁
    ├── landmark.html       ← 地標詳細資訊頁
    ├── ar_marker.html      ← AR 圖片掃描頁
    ├── ar_gps.html         ← GPS AR 探索頁
    ├── admin_login.html    ← 管理員登入
    ├── admin_dashboard.html← 後台地標列表
    ├── admin_form.html     ← 新增/編輯地標表單
    ├── game_start.html     ← 遊戲開始/暱稱輸入 ✅
    ├── game_map.html       ← 遊戲地圖 ✅
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

### 4.1 地圖首頁（index.html）

- Leaflet.js 互動地圖，預設顯示淡江大學校園範圍
- 地標以自訂藍色發光圓點標記顯示
- 點擊標記彈出 Popup 卡片，顯示地標名稱與「探索此地標」按鈕
- Popup 卡片顯示地標封面圖（如有上傳）
- 地標資料透過 `/api/landmarks` 動態載入

### 4.2 地標詳細頁（landmark.html）

- 顯示封面圖片（無圖時顯示預設 emoji 佔位）
- 地標名稱（中文 + 英文雙語）
- 地址資訊
- 歷史介紹（中文 + 英文）
- 歷史人物小故事（獨立區塊）
- 歷史小測驗（單選四選一，答對/答錯即時回饋）
- AR 功能入口按鈕：
  - 📷 AR Marker 掃描
  - 📡 GPS AR 探索

### 4.3 AR Marker 掃描（ar_marker.html）

- 使用 AR.js + A-Frame，無需安裝 App
- 手機鏡頭對準 Hiro Marker 圖片觸發
- AR 疊加內容：
  - 地標中文名稱（藍色大標題）
  - 英文名稱
  - 地址
  - 歷史介紹前 40 字預覽
  - 小測驗提示（如有設定）
  - 裝飾性 3D 元素（發光橫條）
- 右下角顯示 Marker 參考圖
- 需要 HTTPS 環境（Render 部署後可用）

### 4.4 GPS AR 探索（ar_gps.html）

- 使用 AR.js Location-Based，手機走動時自動偵測
- 取得使用者 GPS 座標，顯示於底部狀態列
- 右側顯示最近 5 個地標及距離（公尺/公里）
- 3D 場景中顯示地標方向標記：
  - 藍色發光浮動圓球
  - 垂直光柱
  - 地標名稱文字
- 點擊跳轉至地標詳細頁
- 需要 HTTPS 環境（Render 部署後可用）

### 4.5 管理員後台

#### 登入（admin_login.html）

- 帳號密碼驗證（Werkzeug hash 加密儲存）
- 預設帳號：admin / admin123（上線後請更改）
- 錯誤時顯示提示訊息

#### 地標列表（admin_dashboard.html）

- 顯示地標總數統計
- 表格列出所有地標：縮圖、中英文名稱、地址、座標
- 每筆提供：查看、編輯、刪除操作
- 刪除前有確認提示

#### 新增/編輯地標（admin_form.html）

- 基本資訊：中英文名稱、地址、GPS 座標（緯度/經度）
- 介紹內容：中英文歷史介紹、歷史人物小故事
- 圖片上傳：支援 jpg/png/webp/gif，儲存於 static/uploads/
- 歷史小測驗：題目、四個選項、正確答案

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
| image_path | TEXT | 封面圖片路徑 |
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

### 5.3 players 表（玩家資料）✅ 已實現

| 欄位名稱 | 型別 | 說明 |
|---------|------|------|
| id | INTEGER PK | 自動遞增主鍵 |
| nickname | TEXT | 玩家暱稱 |
| device_id | TEXT UNIQUE | 瀏覽器裝置識別碼 |
| total_points | INTEGER | 累積總點數 |
| created_at | TIMESTAMP | 建立時間 |

### 5.4 player_progress 表（遊戲進度）✅ 已實現

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

玩家透過遊戲系統在校園內探索 9 個地標，作答歷史測驗後自動解鎖，累積點數並達成成就。

### 6.3 點數規則

| 行為 | 點數 |
|------|------|
| 解鎖新地標 | +10 pts |
| 歷史問題答對 | +20 pts |
| 歷史問題答錯但完成 | +5 pts |
| 蒐集全部地標 | +100 pts（特別獎勵） |

### 6.4 成就稱號

| 稱號 | 解鎖條件 |
|------|---------|
| 🐣 淡江新鮮人 | 解鎖第 1 個地標 |
| 🗺️ 校園探索者 | 解鎖 3 個地標 |
| 📚 淡江學者 | 累積答對 5 題 |
| 🏆 淡江通 | 解鎖全部地標 |
| ⭐ 淡江達人 | 全部地標滿分通關 |

### 6.5 遊戲頁面（已實現）

| 頁面 | 功能 | 狀態 |
|------|------|------|
| game_start.html | 輸入暱稱、產生 device_id、開始遊戲 | ✅ |
| game_map.html | 校園地圖，已解鎖地標發光顯示，未解鎖灰色 | ✅ |
| game_profile.html | 個人成就、點數、蒐集進度、稱號顯示 | ✅ |
| game_unlock.html | 解鎖動畫頁面（規劃但未實現） | 📋 |

---

## 七、API 路由規格

### 現有路由（✅ 已實現）

| 方法 | 路由 | 說明 |
|------|------|------|
| GET | / | 地圖首頁 |
| GET | /landmark/<id> | 地標詳細頁 |
| GET | /api/landmarks | 取得所有地標 JSON |
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

### 遊戲系統 API（✅ 已實現）

| 方法 | 路由 | 說明 |
|------|------|------|
| POST | /api/game/register | 玩家註冊（輸入暱稱） |
| GET | /api/game/progress | 取得玩家進度 |
| POST | /api/game/unlock | 解鎖地標 + 提交答題結果 |
| GET | /game | 遊戲地圖首頁 |
| GET | /game/map | 遊戲地圖（Leaflet） |
| GET | /game/profile | 玩家成就頁 |

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
| Phase 3 | 遊戲系統 + 校園地標資料 | ✅ 完成 |
| Phase 4 | 自訂 AR Marker + 3D 模型疊加 | 📋 規劃中 |

### Phase 3 最終實現狀態

#### ✅ 已實現項目
- 遊戲入口 (game_start.html) - 暱稱輸入、device_id 生成
- 遊戲地圖 (game_map.html) - Leaflet 互動地圖、進度追蹤、發光標記
- 玩家成就頁 (game_profile.html) - 5 個徽章系統、點數顯示、稱號
- 5 個遊戲 API 路由 - 完整的註冊、解鎖、進度查詢功能
- 完整的點數系統 - 解鎖 +10 pts、答對 +20 pts、答錯 +5 pts
- 成就系統 - 5 個稱號（新鮮人、探索者、學者、淡江通、達人）
- 資料表 - players 和 player_progress 完整建立
- 地標詳情頁遊戲集成 - landmark.html 答題後自動呼叫 /api/game/unlock
- 校園地標資料 - 9 個淡江大學校園地標（包含中英文介紹、GPS座標、歷史故事、測驗題目）

---

## 十、待辦事項

### ✅ 已完成
- [x] 實作 Phase 3 遊戲系統
- [x] 更改 secret_key (已設定為 'tku-ar-heritage-2026-candy')
- [x] 建立 players 和 player_progress 資料表
- [x] 實現 5 個遊戲 API 路由
- [x] 建立 3 個遊戲頁面 (game_start, game_map, game_profile)
- [x] 在 landmark.html 集成遊戲解鎖功能（答題後自動呼叫 /api/game/unlock）
- [x] 新增 8 個淡江大學校園地標資料（含中英文介紹、歷史故事、測驗題目）

### 🔄 進行中 / 待完成
- [ ] 為地標上傳封面照片
- [ ] 驗證 GPS 座標準確性（實地測試）
- [ ] 建立 game_unlock.html（解鎖動畫頁面）【規劃但未實現】
- [ ] 部署到 Render.com

### 📋 Phase 4 規劃中
- [ ] 自訂 AR Marker 設計
- [ ] 3D 模型疊加功能
- [ ] AR 實景錄影功能
- [ ] 離線模式支援

---

## 十一、校園地標清單

系統已包含以下 9 個淡江大學校園地標：

1. ✅ 淡水紅毛城（示例地標）
2. ✅ 驚聲紀念大樓
3. ✅ 覺生紀念圖書館
4. ✅ 海事博物館暨黑天鵝展示廳
5. ✅ 書卷廣場（蛋捲廣場）
6. ✅ 文錙藝術中心
7. ✅ 學生活動中心
8. ✅ 五虎崗綜合球場
9. ✅ 覺生綜合大樓

所有地標均包含：
- 中英文名稱與詳細介紹
- GPS 座標（緯度/經度）
- 歷史故事敘述
- 4 選 1 歷史小測驗

---

## 十二、快速開始

### 本地開發
```bash
# 1. 進入專案目錄
cd ar-heritage-explorer

# 2. 建立虛擬環境
python -m venv venv
source venv/Scripts/activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 初始化資料庫
python database.py

# 5. 執行應用
python app.py
```

訪問 `http://localhost:5000`

### 管理員後台
- 路由：`http://localhost:5000/admin/login`
- 帳號：admin
- 密碼：admin123

### 遊戲系統
- 路由：`http://localhost:5000/game`
- 輸入暱稱開始探索

---

## 十三、技術支援

- **GitHub**: https://github.com/candytangsys/ar-heritage-explorer
- **開發者**: candytangsys
- **最後更新**: 2026年6月15日

# 建築辨識模型（Teachable Machine）

AR 鏡頭頁（`/ar/marker/<id>`）會載入這個資料夾裡的模型來辨識建築。
**把訓練好的三個檔案放進這個資料夾即可：**

```
static/tm-model/
├── model.json
├── metadata.json
└── weights.bin
```

放好後，鏡頭對準建築、信心度 ≥ 85% 連續數幀就會解鎖。
（在還沒放模型前，鏡頭頁會自動退回用 GPS 距離解鎖，App 仍可運作。）

---

## 一、訓練步驟（Google Teachable Machine，免費）

1. 開 https://teachablemachine.withgoogle.com → **Get Started** → **Image Project** → **Standard image model**
2. 為 **每一棟建築建立一個 class**，class 名稱請包含該地標的 **id 數字**：

   | Class 名稱 | 對應地標 |
   |-----------|---------|
   | `lm1` | 驚聲紀念大樓 |
   | `lm2` | 覺生紀念圖書館 |
   | `lm3` | 海事博物館暨黑天鵝展示廳 |
   | `lm4` | 書卷廣場 |
   | `lm5` | 文錙藝術中心 |
   | `lm6` | 學生活動中心 |
   | `lm7` | 五虎崗綜合球場 |
   | `lm8` | 覺生綜合大樓 |

   > 程式是用 class 名稱裡的數字對應地標 id，所以 `lm3`、`landmark_3`、`3` 都可以，重點是數字要對。

3. 再加一個 `unknown` class，放天空、地面、路面、其他不相關畫面，避免亂解鎖。
4. 每個 class 上傳 **30~50 張照片**，務必涵蓋：
   - 不同**角度**（正面、側面、斜角）
   - 不同**距離**（遠景、中景、近景）
   - 不同**光線**（晴天、陰天、上午、下午）
   - 有人/沒人、有遮擋/無遮擋
   - 用「Webcam」直接連拍最快，或上傳手機拍的照片
5. 按 **Train Model**（瀏覽器分頁不要關）。
6. 訓練完點 **Export Model** → 切到 **TensorFlow.js** 分頁 → **Download** →
   下載得到一個 zip，解壓出 `model.json`、`metadata.json`、`weights.bin`。
7. 把這三個檔案丟進 `static/tm-model/`，重新整理鏡頭頁即可測試。

## 二、調整辨識靈敏度

在 `templates/ar_marker.html` 最上方的 script：
- `CONF_THRESHOLD`（預設 0.85）：調高更嚴格、調低更容易解鎖
- `HOLD_FRAMES`（預設 8）：需連續達標的幀數，調高更穩、調低更快

## 三、提高準確率的訣竅

- 淡江很多建築外觀相似（一樣的磁磚/灰牆），**訓練照片的多樣性**是準度關鍵。
- 認錯時：補拍會混淆的角度照片重新訓練。
- 想更防作弊：之後可把解鎖改成「辨識成功 **且** GPS 在 50m 內」（後端已支援，把前端 `scanned` 與距離一起判斷即可）。

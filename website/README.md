# Ask-Then-Do-It 宇宙巡航介紹網站

以 Vite、Three.js 與原生 JavaScript 製作的純前端產品介紹網站。使用者隨捲動穿越五個目的地，從需求混亂、釐清、規格規劃、實作驗證，抵達提供安裝方式的 Aegis Station。網站不需要 API 伺服器、資料庫、帳號或環境變數。

## 本機開發

建議使用 Node.js 22 LTS 或更新版本。

```sh
npm install
npm run dev
```

Vite 會在終端顯示實際網址，預設為 `http://127.0.0.1:5173`。開發連接埠被占用時會自動改用下一個可用連接埠。

```sh
npm test
npm run build
npm run preview
```

`npm test` 使用 Node.js 內建測試執行器；`npm run build` 輸出至 `dist/`；`npm run preview` 可在本機檢查正式建置。

## 靜態部署

將 `dist/` 的全部內容上傳至任何支援 HTTPS 的靜態網站空間即可。正式環境不需要執行 Node.js；GitHub 儲存庫與文件連結仍需網際網路連線。

目前設定以網域根目錄部署，例如 `https://example.com/`。地球表面貼圖使用 `/textures/earth.jpg` 根路徑，若要部署在 `/project/` 等子路徑，需同步調整 Vite 的 `base` 與該資源路徑。不要直接以 `file://` 開啟原始碼或建置輸出，請透過 HTTP 靜態伺服器提供檔案。

剪貼簿使用瀏覽器 Clipboard API，正式環境需 HTTPS；`localhost` 與 `127.0.0.1` 可供本機開發。權限遭拒時，介面顯示失敗訊息並選取指令，使用者仍可手動複製。

## 模組配置

| 路徑 | 職責 |
| --- | --- |
| `src/main.js` | HUD 組裝、導覽、捲動同步、語言選單與安裝終端互動 |
| `src/style.css` | 響應式配置、太空 HUD、玻璃終端與減少動態樣式 |
| `src/scene/universe.js` | Three.js 場景、攝影機曲線、PBR 星體、Fresnel 大氣、星環、星空與 Bloom |
| `src/data/planets.js` | 行星座標、尺寸、材質參數、相機構圖參數與效能設定 |
| `src/data/product.js` | 專案連結、安裝指令與導覽目的地 |
| `src/data/i18n/` | 繁體中文、英文、日文文案與語言索引 |
| `src/lib/i18n.js` | DOM 與 ARIA 翻譯、metadata 更新、語言偏好保存 |
| `src/lib/journey.js` | 正規化捲動進度與目的地切換邊界 |
| `public/textures/` | 本機提供的地球表面貼圖；其他星體材質由程式生成 |
| `public/fonts/` | 本機提供的 DM Sans、IBM Plex Mono 與其 SIL Open Font License |
| `tests/core.test.js` | 語言切換、儲存失敗、航程邊界與跨模組資料一致性測試 |

## 操作與行為

- 捲動推進航程，沿著平滑軌跡依序拜訪各站。
- 五個目的地依序為混亂深空、Aeris、Kronos、Solis 與 Aegis Station。
- 攝影機以 `CatmullRomCurve3` 串聯星體，使用時間差平滑插值，並加入滑鼠視差。
- 預設語言為繁體中文；切換英文或日文會立即更新文字、頁面標題、說明與無障礙標籤，偏好保存在 `localStorage`。儲存不可用時仍可正常切換。
- 安裝終端提供 Codex、Claude Code 與 Git clone 分頁、一鍵複製、GitHub 儲存庫及對應語言文件連結。
- 暫停按鈕與系統 `prefers-reduced-motion` 設定可減少動態；WebGL 不可用時保留靜態背景、內容與安裝功能。
- 手機降低星空粒子數與像素比；分頁在背景時停止渲染工作；模組卸載時釋放 Three.js 資源。
- 提供跳至安裝連結、鍵盤可操作語言選單與安裝分頁、複製狀態提示。

網站只呈現工作流程的介紹與安裝方式，不會在瀏覽器執行安裝指令。產品文案以適當驗證與審查描述交付階段，保留 Full、Lite 與 Direct 實作選項的差異，不宣稱每次工作都會新增測試。

## 原始專案與素材

產品網址與安裝資訊依 2026-09-11 查閱的公開專案文件整理：

- [Ask-Then-Do-It 原始專案](https://github.com/Mysterio1001/Ask-Then-Do-It)
- [繁體中文開始文件](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.zh-TW.md)
- [English getting started](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.en.md)
- [日本語の開始ガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/START-HERE.ja.md)

表面貼圖取自 Three.js examples，已隨站點存放於 `public/textures/`，執行時不向素材來源請求檔案：

- `earth.jpg`：[earth_atmos_2048.jpg](https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg)
- [Three.js 原始碼與授權](https://github.com/mrdoob/three.js)
- Kronos 等星體表面、星環、雲層、星雲與太陽能板紋理由程式生成；空間站使用 Three.js 幾何模型；圖示使用 [Lucide](https://lucide.dev/)。

品牌標誌 `public/logo.png` 取自 Ask-Then-Do-It 原始專案的 Codex 外掛資產：

- [logo.png](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/main/adapters/codex/plugin/ask-then-do-it/assets/logo.png)

字型已隨站點存放於 `public/fonts/`，執行時不向 Google Fonts 發出請求。DM Sans 使用拉丁字元可變字型，IBM Plex Mono 用於等寬 HUD；中文與日文使用裝置系統字型。兩套字型採 [SIL Open Font License 1.1](https://openfontlicense.org/)，完整授權分別存於 `public/fonts/DM-Sans-LICENSE.txt` 與 `public/fonts/IBM-Plex-Mono-LICENSE.txt`。字型來源為 [DM Sans](https://github.com/google/fonts/tree/main/ofl/dmsans) 與 [IBM Plex Mono](https://github.com/google/fonts/tree/main/ofl/ibmplexmono)。

## 驗證範圍

自動測試涵蓋三語文案完整性、首次與再次造訪的語言、切換時 DOM / ARIA / metadata 更新、localStorage 失敗、缺少翻譯的回退、捲動超界，以及 HUD 導覽、曲線控制點、貼圖檔案之間的一致性。

已在本機瀏覽器檢查 1440×900、1366×768、390×844 與 320×740 視窗，包含五站畫面、WebGL 實際渲染、貼圖載入、語言切換及複製成功回饋。驗證截圖保存在被 Git 忽略的 `artifacts/`。

WebGL context loss、Clipboard 權限拒絕與作業系統動態偏好切換保留防護處理，但未在真實裝置中強制觸發。不同 GPU 的實際 FPS 仍需部署後量測。Three.js 延遲載入區塊約 530 KB（gzip 約 135 KB），Vite 會提出超過 500 KB 的提示；HUD 主程式獨立載入，不等待 3D 初始化。

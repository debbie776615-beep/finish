# 元盾資安 完工確認書產生器

## 檔案結構（放進 GitHub repo 時）
```
your-repo/
├── app.py
├── requirements.txt
├── assets/
│   └── logo.png              ← 公司LOGO放這裡（記得是 assets 資料夾內，不是根目錄）
└── fonts/
    └── NotoSansTC-Regular.ttf  ← 中文字型檔，一定要一起上傳，否則中文會顯示不出來
```

⚠️ **`fonts/NotoSansTC-Regular.ttf` 這個檔案（約7MB）務必要 commit 進 repo**，
不要因為檔案比較大就漏傳，少了它 PDF 裡的中文字會整段顯示不出來或亂碼。

## 部署到 Streamlit Community Cloud
1. 把 `app.py`、`requirements.txt`、`assets/logo.png` 一起 push 到 GitHub repo
2. 到 https://share.streamlit.io 用同一個 GitHub 帳號登入
3. 選擇該 repo，Main file path 填 `app.py`，按 Deploy

## 欄位說明
- **客戶資訊**：客戶名稱、完工日期（自動轉民國年）、電話、手機、Email、地址、產品服務名稱、窗口聯絡人 → 都是輸入框，直接填
- **核對完工項目**：下方表格可直接點「+」新增列，或選取列後刪除，項次會自動從1開始編號
- **服務電話**：預設 (02) 5562-5888，可修改
- **簽名區**：客戶名稱會自動帶入，客戶聯絡人簽名／元盾資安主管簽名與日期維持空白，供列印後手寫簽名

## 字型
改用內嵌的 **Noto Sans TC**（Google開源繁體中文字型，`fonts/NotoSansTC-Regular.ttf`）。

原本想用 reportlab 內建的 `MSung-Light`（號稱不用另外傳字型檔），
但實測發現它其實不含真正的字型外框，只是指向系統的 Adobe-CNS1 語言包，
在 Streamlit Cloud、多數瀏覽器內建PDF檢視器上都會找不到而整段中文顯示不出來或亂碼。
所以改成內嵌真正的 TTF 字型檔，字型資料直接包進產生出來的PDF裡，不依賴對方裝置裝了什麼字型，
這樣才能保證任何人打開都正常顯示。

## 之後可以再調整的方向（先列出來，需要再說）
- LOGO 大小/位置微調
- 增加「核對」欄位下拉選單（例如 V / X / N/A）
- 服務電話等公司固定資訊改成程式碼內寫死，介面上不顯示編輯欄位

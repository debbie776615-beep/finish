# 元盾資安 完工確認書產生器

## 檔案結構（放進 GitHub repo 時）
```
your-repo/
├── app.py
├── requirements.txt
└── assets/
    └── logo.png      ← 公司LOGO放這裡（記得是 assets 資料夾內，不是根目錄）
```

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
中文字型用 reportlab 內建的 `MSung-Light`（繁體中文 Big5 CID 字型），
不需要額外上傳 .ttf 字型檔到 repo，這點跟報價單那支程式不太一樣，可以省掉字型檔案處理的麻煩。

## 之後可以再調整的方向（先列出來，需要再說）
- LOGO 大小/位置微調
- 增加「核對」欄位下拉選單（例如 V / X / N/A）
- 服務電話等公司固定資訊改成程式碼內寫死，介面上不顯示編輯欄位

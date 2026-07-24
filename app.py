import io
import os
from datetime import date

import streamlit as st
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ---------- 字型設定 ----------
# 之前用的 reportlab 內建 CID 字型「MSung-Light」不會內嵌實際字型外框，
# 只是指向 Adobe-CNS1 語言包，很多環境（Streamlit Cloud、瀏覽器內建PDF檢視器、
# 手機等）沒有這個語言包就會整段中文顯示不出來或亂碼。
# 改用內嵌的 Noto Sans TC TTF 字型，字型資料直接包進PDF，任何裝置都能正確顯示。
FONT_NAME = "NotoSansTC"
FONT_PATH = "fonts/NotoSansTC-Regular.ttf"
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

LOGO_PATH = "assets/logo.png"


def ad_to_minguo(d: date) -> str:
    """西元日期轉民國日期字串"""
    return f"民國 {d.year - 1911} 年 {d.month} 月 {d.day} 日"


def build_pdf(data: dict, items_df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
    )

    styles = {
        "title": ParagraphStyle(
            "title", fontName=FONT_NAME, fontSize=18, leading=24,
            alignment=TA_CENTER, spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", fontName=FONT_NAME, fontSize=16, leading=22,
            alignment=TA_CENTER, spaceAfter=10,
        ),
        "cell": ParagraphStyle(
            "cell", fontName=FONT_NAME, fontSize=10.5, leading=15,
            alignment=TA_LEFT,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold", fontName=FONT_NAME, fontSize=10.5, leading=15,
            alignment=TA_CENTER,
        ),
        "note": ParagraphStyle(
            "note", fontName=FONT_NAME, fontSize=10.5, leading=18,
        ),
        "sign": ParagraphStyle(
            "sign", fontName=FONT_NAME, fontSize=10.5, leading=20,
        ),
    }

    story = []

    # ---------- 頁首：LOGO（右上角）＋ 標題 ----------
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=32 * mm, height=12 * mm)
        logo.hAlign = "RIGHT"
        story.append(logo)
        story.append(Spacer(1, 2 * mm))

    story.append(Paragraph("元盾資安股份有限公司", styles["title"]))
    story.append(Paragraph("完 工 確 認 書", styles["subtitle"]))

    # ---------- 客戶資訊表格 ----------
    def P(text):
        return Paragraph(str(text) if text is not None else "", styles["cell"])

    def PB(text):
        return Paragraph(str(text) if text is not None else "", styles["cell_bold"])

    info_rows = [
        [PB("客戶資訊"), "", "", ""],
        [PB("客戶名稱"), P(data["customer_name"]), PB("完工日期"), P(data["complete_date"])],
        [PB("電話"), P(data["phone"]), PB("手機"), P(data["mobile"])],
        [PB("Email"), P(data["email"]), PB("地址"), P(data["address"])],
        [PB("產品服務名稱"), P(data["service_name"]), PB("窗口聯絡人"), P(data["contact_person"])],
    ]

    info_table = Table(
        info_rows,
        colWidths=[30 * mm, 65 * mm, 30 * mm, 55 * mm],
        rowHeights=[8 * mm, 10 * mm, 10 * mm, 10 * mm, 10 * mm],
    )
    info_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("SPAN", (0, 0), (-1, 0)),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),
        ("BACKGROUND", (2, 1), (2, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 4 * mm))

    # ---------- 核對完工項目表格 ----------
    item_header = [PB("項次"), PB("項目"), PB("內容"), PB("核對"), PB("備註")]
    item_rows = [[PB("核對完工項目"), "", "", "", ""], item_header]

    for idx, row in items_df.reset_index(drop=True).iterrows():
        item_rows.append([
            PB(idx + 1),
            P(row.get("項目", "")),
            P(row.get("內容", "")),
            PB(row.get("核對", "")),
            P(row.get("備註", "")),
        ])

    item_rows.append([PB("以下空白"), "", "", "", ""])

    items_table = Table(
        item_rows,
        colWidths=[15 * mm, 30 * mm, 75 * mm, 15 * mm, 45 * mm],
    )
    style_cmds = [
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("SPAN", (0, 0), (-1, 0)),
        ("SPAN", (0, -1), (-1, -1)),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, -1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    items_table.setStyle(TableStyle(style_cmds))
    story.append(items_table)
    story.append(Spacer(1, 8 * mm))

    # ---------- 底下說明文字 ----------
    story.append(Paragraph(
        "各項目貴公司核對無誤後，請在下方「客戶名稱、客戶聯絡人」確認簽名處簽名。謝謝！",
        styles["note"],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(f"服務電話：{data['service_phone']}", styles["note"]))
    story.append(Spacer(1, 6 * mm))

    sign_table = Table(
        [
            [
                Paragraph(f"客戶名稱：{data['customer_name']}", styles["sign"]),
                Paragraph("元盾資安主管確認簽名：__________________", styles["sign"]),
            ],
            [
                Paragraph("客戶聯絡人確認簽名：__________________", styles["sign"]),
                Paragraph("元盾資安主管確認日期：____年____月____日", styles["sign"]),
            ],
        ],
        colWidths=[85 * mm, 95 * mm],
    )
    sign_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sign_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


# ================= Streamlit 介面 =================
st.set_page_config(page_title="元盾資安 完工確認書產生器", page_icon="📄", layout="centered")

st.title("📄 完工確認書產生器")
st.caption("元盾資安股份有限公司")

st.subheader("客戶資訊")
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("客戶名稱", "")
    phone = st.text_input("電話", "")
    email = st.text_input("Email", "")
    service_name = st.text_input("產品服務名稱", "")
with col2:
    complete_date = st.date_input("完工日期", value=date.today())
    mobile = st.text_input("手機", "")
    address = st.text_input("地址", "")
    contact_person = st.text_input("窗口聯絡人", "")

st.subheader("核對完工項目")
st.caption("可直接在下方表格中新增／刪除列，項次會自動編號")

default_items = pd.DataFrame(
    [
        {"項目": "網站弱掃", "內容": "網站弱掃報告交付（初測）", "核對": "V", "備註": ""},
        {"項目": "網站弱掃", "內容": "網站弱掃報告交付（複測）", "核對": "V", "備註": ""},
    ]
)

items_df = st.data_editor(
    default_items,
    num_rows="dynamic",
    width="stretch",
    column_config={
        "核對": st.column_config.TextColumn(help="通常填 V，也可留空"),
    },
)

st.subheader("其他")
service_phone = st.text_input("服務電話", "(02) 5562-5888")

st.divider()

if st.button("產生完工確認書 PDF", type="primary"):
    if not customer_name:
        st.error("請先填寫客戶名稱")
    else:
        data = {
            "customer_name": customer_name,
            "complete_date": ad_to_minguo(complete_date),
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "address": address,
            "service_name": service_name,
            "contact_person": contact_person,
            "service_phone": service_phone,
        }
        pdf_bytes = build_pdf(data, items_df)
        st.success("PDF 已產生完成！")
        st.download_button(
            label="下載完工確認書 PDF",
            data=pdf_bytes,
            file_name=f"{customer_name}_完工確認書.pdf",
            mime="application/pdf",
        )

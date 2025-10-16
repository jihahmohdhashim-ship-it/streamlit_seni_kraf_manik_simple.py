# streamlit_seni_kraf_manik_simple.py
# Versi ringkas paparan produk Seni Kraf Manik PPKI SMK Sultan Muzafar Shah 1
# Jalankan dengan: streamlit run streamlit_seni_kraf_manik_simple.py

import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import uuid

# --- Konfigurasi ---
st.set_page_config(page_title="Seni Kraf Manik PPKI", layout="wide")
DATA_DIR = Path("./seni_kraf_data")
IMG_DIR = DATA_DIR / "images"
CSV_FILE = DATA_DIR / "produk.csv"
DATA_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

# --- Fungsi bantu ---
def load_products():
    if CSV_FILE.exists():
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["id", "nama", "harga", "gambar_path"])

def save_products(df):
    df.to_csv(CSV_FILE, index=False)

def save_image(uploaded_file):
    ext = Path(uploaded_file.name).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    path = IMG_DIR / filename
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(path)

# --- Header ---
st.title("🪡 Seni Kraf Manik")
st.subheader("PPKI SMK Sultan Muzafar Shah 1 (Kefungsian Rendah)")
st.markdown("Paparan hasil kraf manik — brooch, keychain, cincin, tasbih dan banyak lagi.")

# --- Borang tambah produk ---
with st.expander("➕ Tambah Produk Baru"):
    with st.form("form_produk", clear_on_submit=True):
        nama = st.text_input("Nama Produk")
        harga = st.number_input("Harga (RM)", min_value=0.0, step=0.5, format="%.2f")
        gambar = st.file_uploader("Muat naik gambar produk", type=["png", "jpg", "jpeg"])
        submit = st.form_submit_button("Simpan")

        if submit:
            if not nama:
                st.error("Sila masukkan nama produk.")
            else:
                df = load_products()
                img_path = save_image(gambar) if gambar else ""
                new = {"id": uuid.uuid4().hex, "nama": nama, "harga": harga, "gambar_path": img_path}
                df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                save_products(df)
                st.success(f"Produk '{nama}' disimpan.")

# --- Senarai produk ---
df = load_products()

st.markdown("## 🛍️ Senarai Produk")
if df.empty:
    st.info("Tiada produk ditambah lagi.")
else:
    for i in range(0, len(df), 3):
        row = df.iloc[i:i+3]
        cols = st.columns(len(row))
        for c, (_, item) in zip(cols, row.iterrows()):
            c.markdown(f"**{item['nama']}**")
            if item["gambar_path"] and Path(item["gambar_path"]).exists():
                img = Image.open(item["gambar]()

# Proyek Analisis Data: E-Commerce Public Dataset

## Deskripsi
Proyek ini menganalisis performa bisnis ritel Olist E-Commerce Brasil (2016–2018), berfokus pada pendapatan per kategori produk, dampak keterlambatan pengiriman terhadap kepuasan pelanggan, dan pemetaan demografi geospasial.

## Struktur Direktori
- `dashboard/`: Berisi kode antarmuka Streamlit (`dashboard.py`) dan dataset bersih (`main_data.csv`).
- `data/`: Dataset mentah yang digunakan untuk analisis.
- `notebook.ipynb`: Dokumentasi lengkap Data Wrangling, EDA, visualisasi, dan kesimpulan.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.

# Instalasi dan Setup Lingkungan Kerja (Visual Studio Code)

1. Buka folder proyek ini menggunakan **Visual Studio Code (VS Code)**.
2. Buka terminal terintegrasi di VS Code dengan menekan tombol `` Ctrl + ` `` (atau melalui menu **Terminal > New Terminal** di bagian atas).
3. Buat *virtual environment* baru (opsional namun sangat disarankan) dengan menjalankan perintah berikut di terminal:
   ```bash
   python -m venv venv
   ```
4. Aktifkan Virtual Environment tersebut:
   untuk windows
   ```bash
   .\venv\Scripts\activate
   ```
5. Pasang semua library yang dibutuhkan dengan menjalankan perintah:
   ```
   pip install -r requirements.txt
   ```

# Cara menjalankan dashboard streamlit (Visual Studio Code):
Setelah semua library berhasil diinstal dan virtual environment dalam keadaan aktif (ditandai dengan awalan (venv) di terminal Anda), jalankan perintah berikut untuk meluncurkan dashboard ke browser:
```
streamlit run dashboard/dashboard.py
```
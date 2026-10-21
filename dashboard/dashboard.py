import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

# 1. Page layout & CSS Styling

st.set_page_config(
    page_title="E-Commerce Performance Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* hide sidebar */
    [data-testid="collapsedControl"] { display: none; }
    
    /* main bg */
    .stApp {
        background-color: #0B131B;
        color: #E2E8F0;
    }

    /* containere padding */
    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    /* container styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0F172A !important;
        border: 1px solid #1E2D3D !important;
        border-radius: 6px;
        padding: 4px;
        box-shadow: none;
        height: 100%;
    }
    
    /* columns height */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
    }

    /* --- dropdown styling --- */
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="base-input"]:focus-within {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 1px #38BDF8 !important;
        outline: none !important;
    }
    /* tag styling */
    span[data-baseweb="tag"] {
        background-color: rgba(56, 189, 248, 0.15) !important;
        border: 1px solid #38BDF8 !important;
        color: #38BDF8 !important;
    }

    /* typography */
    .main-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.35rem;
        letter-spacing: 0.5px;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        max-width: 1150px;
    }

    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1E2D3D;
    }

    .card-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 0.2rem;
    }
    .card-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 1rem;
    }
    
    /* insight panel */
    .insight-panel {
        background-color: #0F172A;
        border: 1px solid #1E2D3D;
        padding: 1.5rem;
        border-radius: 6px;
        height: 100%;
        display: flex;
        flex-direction: column;
        color: #94A3B8;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .insight-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 1.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1E2D3D;
    }
    .insight-panel ul {
        margin-top: 0.5rem;
        padding-left: 1.2rem;
        flex-grow: 1;
    }
    .insight-panel li {
        margin-bottom: 0.6rem;
    }
    .insight-panel strong {
        color: #F8FAFC;
        font-weight: 600;
    }

    /* utility classes */
    .text-blue { color: #38BDF8 !important; font-weight: 700; }
    .text-red { color: #F87171 !important; font-weight: 700; }
    .text-white { color: #F8FAFC !important; font-weight: 700; }
    
    /* KPI components */
    .kpi-wrapper {
        padding: 0.5rem 0.8rem;
    }
    .kpi-title {
        font-size: 0.88rem;
        color: #94A3B8;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .kpi-val {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# matplotlib global settings
FIG_SIZE = (7.0, 4.3)
FIG_DPI = 180

plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "axes.edgecolor": "#233547",
    "axes.labelcolor": "#94A3B8",
    "text.color": "#E2E8F0",
    "xtick.color": "#94A3B8",
    "ytick.color": "#E2E8F0",
    "grid.color": "#1E2D3D",
    "font.sans-serif": ["Inter", "Segoe UI", "Arial", "sans-serif"],
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLOR_PRIMARY = "#38BDF8"
COLOR_DANGER = "#F87171"
COLOR_MUTED = "#1E2D3D"

def lock_canvas(fig):
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure, fill=False, edgecolor="none", linewidth=0))

def shorten_label(text, max_len=25):
    text_str = str(text)
    return text_str if len(text_str) <= max_len else text_str[:max_len - 3] + "..."

def format_currency(val):
    if val >= 1_000_000:
        return f"R$ {val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"R$ {val / 1_000:.1f}K"
    return f"R$ {val:,.0f}"

# 2. Data Loading & Preprocessing

@st.cache_data
def load_main_data():
    current_dir = Path(__file__).resolve().parent
    data_path = current_dir / "main_data.csv"
    if not data_path.exists():
        data_path = Path.cwd() / "dashboard" / "main_data.csv"
    df = pd.read_csv(data_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

def create_category_rev_df(df):
    # filter hanya baris item (bukan review)
    df = df[df["is_item_row"]]
    return df.groupby("product_category_name_english", as_index=False)["price"].sum().rename(columns={"price": "total_revenue"}).sort_values(by="total_revenue", ascending=False)

def create_delivery_stats(df):
    # hitung jumlah pesanan unik per status pengiriman
    counts = df.drop_duplicates(subset="order_id").groupby("delivery_status", as_index=False).agg(order_count=("order_id", "count"))
    # hitung rata-rata skor ulasan per status pengiriman (hanya baris review)
    scores = df[df["is_review_row"]].groupby("delivery_status", as_index=False).agg(avg_score=("review_score", "mean"))
    summary = counts.merge(scores, on="delivery_status", how="left")
    order_map = {"Tepat Waktu": 0, "Terlambat": 1}
    summary["sort_key"] = summary["delivery_status"].map(lambda x: order_map.get(x, 2))
    return summary.sort_values("sort_key").drop(columns="sort_key")

def create_bystate_df(df):
    return df.groupby("customer_state", as_index=False)["customer_id"].nunique().rename(columns={"customer_id": "customer_count"}).sort_values(by="customer_count", ascending=False)

main_df = load_main_data()
min_date_global, max_date_global = main_df["order_purchase_timestamp"].min().date(), main_df["order_purchase_timestamp"].max().date()

# Mapping negara bagian Brasil ke nama lengkap untuk tampilan
state_mapping = {
    "AC": "Acre (AC)", "AL": "Alagoas (AL)", "AP": "Amapá (AP)", "AM": "Amazonas (AM)",
    "BA": "Bahia (BA)", "CE": "Ceará (CE)", "DF": "Distrito Federal (DF)", "ES": "Espírito Santo (ES)",
    "GO": "Goiás (GO)", "MA": "Maranhão (MA)", "MT": "Mato Grosso (MT)", "MS": "Mato Grosso do Sul (MS)",
    "MG": "Minas Gerais (MG)", "PA": "Pará (PA)", "PB": "Paraíba (PB)", "PR": "Paraná (PR)",
    "PE": "Pernambuco (PE)", "PI": "Piauí (PI)", "RJ": "Rio de Janeiro (RJ)", "RN": "Rio Grande do Norte (RN)",
    "RS": "Rio Grande do Sul (RS)", "RO": "Rondônia (RO)", "RR": "Roraima (RR)", "SC": "Santa Catarina (SC)",
    "SP": "São Paulo (SP)", "SE": "Sergipe (SE)", "TO": "Tocantins (TO)"
}


# 3. Header

st.markdown(
    '<div class="main-title">E-Commerce Performance Analysis: Category Revenue, Delivery Impact, and Customer Distribution</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="main-subtitle">'
    'Evaluasi komprehensif performa bisnis ritel berdasarkan riwayat data transaksi Olist E-Commerce, '
    'mencakup pemetaan kontribusi omzet per kategori produk, korelasi ketepatan waktu logistik terhadap tingkat '
    'kepuasan pelanggan, serta konsentrasi demografi pasar di wilayah Brasil.'
    '</div>',
    unsafe_allow_html=True
)

# 4. Filter Controls

kpi_container = st.empty()
st.write("")
filter_container = st.container(border=True)

with filter_container:
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.1, 1.1, 1.2, 1.0])
    
    with f_col1:
        preset_period = st.selectbox(
            "Cakupan Waktu", 
            ["Keseluruhan (2016 - 2018)", "Fokus 2016", "Fokus 2017", "Fokus 2018", "Kustom"], 
            index=0
        )
    with f_col2:
        delivery_options = ["Semua Status"] + sorted(main_df["delivery_status"].dropna().unique().tolist())
        selected_delivery = st.selectbox("Status Pengiriman", delivery_options, index=0)
    with f_col3:
        all_states_raw = sorted(main_df["customer_state"].dropna().unique().tolist())
        all_states_display = [state_mapping.get(s, s) for s in all_states_raw]
        
        selected_states_display = st.multiselect(
            "Negara Bagian (State)", 
            options=all_states_display, 
            default=[], 
            placeholder="Semua wilayah"
        )
        selected_states = [s.split(" ")[-1].replace("(", "").replace(")", "") for s in selected_states_display]
        
    with f_col4:
        if preset_period == "Kustom":
            date_range = st.date_input("Rentang Kustom", [min_date_global, max_date_global], min_value=min_date_global, max_value=max_date_global)
            start_date, end_date = date_range if len(date_range) == 2 else (min_date_global, max_date_global)
            top_n = 8
        else:
            top_n_label = st.selectbox(
                "Jumlah Kategori Visual",
                options=[f"{i} Kategori" for i in range(3, 11)],
                index=5  # Default index 5 = "8 Kategori"
            )
            top_n = int(top_n_label.split()[0])

# Penentuan Filter Tanggal Berdasarkan Preset
if preset_period != "Kustom":
    if preset_period == "Fokus 2016":
        start_date, end_date = pd.to_datetime("2016-01-01").date(), pd.to_datetime("2016-12-31").date()
    elif preset_period == "Fokus 2017":
        start_date, end_date = pd.to_datetime("2017-01-01").date(), pd.to_datetime("2017-12-31").date()
    elif preset_period == "Fokus 2018":
        start_date, end_date = pd.to_datetime("2018-01-01").date(), pd.to_datetime("2018-12-31").date()
    else:
        start_date, end_date = min_date_global, max_date_global

# Terapkan Filter
filtered_df = main_df[(main_df["order_purchase_timestamp"].dt.date >= start_date) & (main_df["order_purchase_timestamp"].dt.date <= end_date)].copy()
if selected_delivery != "Semua Status":
    filtered_df = filtered_df[filtered_df["delivery_status"] == selected_delivery]
if selected_states:
    filtered_df = filtered_df[filtered_df["customer_state"].isin(selected_states)]

category_rev_df = create_category_rev_df(filtered_df)
delivery_stats_df = create_delivery_stats(filtered_df)
bystate_df = create_bystate_df(filtered_df)

# 5. KPI Metrics

unique_orders_df = filtered_df.drop_duplicates(subset="order_id")
total_orders = len(unique_orders_df)
total_revenue = filtered_df.loc[filtered_df["is_item_row"], "price"].sum()
avg_rating = filtered_df.loc[filtered_df["is_review_row"], "review_score"].mean()
on_time_rate = (unique_orders_df["delivery_status"] == "Tepat Waktu").mean() * 100 if len(unique_orders_df) > 0 else 0

with kpi_container:
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        with st.container(border=True):
            st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Total Pesanan Unik</div><div class="kpi-val text-white">{total_orders:,}</div></div>', unsafe_allow_html=True)
    with k2:
        with st.container(border=True):
            st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Total Pendapatan Aktual</div><div class="kpi-val text-blue">{format_currency(total_revenue)}</div></div>', unsafe_allow_html=True)
    with k3:
        with st.container(border=True):
            st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Ketepatan Pengiriman</div><div class="kpi-val text-blue">{on_time_rate:.1f}%</div></div>', unsafe_allow_html=True)
    with k4:
        with st.container(border=True):
            val_str = f"{avg_rating:.2f} <span style='font-size:1.1rem; color:#94A3B8;'>/ 5.00</span>" if pd.notna(avg_rating) else "N/A"
            st.markdown(f'<div class="kpi-wrapper"><div class="kpi-title">Rata-rata Skor Ulasan</div><div class="kpi-val text-blue">{val_str}</div></div>', unsafe_allow_html=True)

# 6. PERFORMA PENDAPATAN KATEGORI PRODUK

st.markdown('<div class="section-header">1. Performa Pendapatan Kategori Produk</div>', unsafe_allow_html=True)

# --- 1a: TOP N ---
col1_chart, col1_desc = st.columns([1.5, 1])
with col1_chart:
    with st.container(border=True):
        st.markdown(f'<div class="card-header">1a. Top {top_n} Kategori Pendapatan Tertinggi</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Akumulasi penjualan kotor (BRL) berdasarkan kategori</div>', unsafe_allow_html=True)
        top_df = category_rev_df.head(top_n).sort_values(by="total_revenue", ascending=True)
        fig1, ax1 = plt.subplots(figsize=FIG_SIZE, dpi=FIG_DPI)
        lock_canvas(fig1)
        fig1.subplots_adjust(left=0.35, right=0.85, top=0.92, bottom=0.08)
        if not top_df.empty:
            colors1 = [COLOR_MUTED] * (len(top_df) - 1) + [COLOR_PRIMARY]
            bars1 = ax1.barh([shorten_label(c) for c in top_df["product_category_name_english"]], top_df["total_revenue"], color=colors1, height=0.6)
            ax1.spines["bottom"].set_visible(False)
            ax1.xaxis.set_visible(False)
            ax1.tick_params(axis="y", labelsize=9.5, length=0)
            max_val = top_df["total_revenue"].max()
            ax1.set_xlim(0, max_val * 1.25)
            for bar in bars1:
                w = bar.get_width()
                ax1.text(w + (max_val * 0.02), bar.get_y() + bar.get_height()/2, format_currency(w), va="center", ha="left", fontsize=9, color="#F8FAFC" if w == max_val else "#94A3B8", fontweight="bold" if w == max_val else "normal")
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)

with col1_desc:
    lead_c = top_df.iloc[-1]["product_category_name_english"] if not top_df.empty else "-"
    lead_v = top_df.iloc[-1]["total_revenue"] if not top_df.empty else 0
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Segmen Pasar Utama</div>
            <div>Kategori <span class="text-blue">{lead_c}</span> memimpin mutlak sebagai penyumbang omzet tertinggi dengan perolehan kumulatif mencapai <span class="text-white">{lead_v:,.2f} BRL</span>.</div>
            <ul>
                <li><strong>Acuan Historis:</strong> Analisis spesifik pada data tahun 2017 memperlihatkan pola serupa, dengan kategori <span class="text-blue">bed_bath_table</span> merajai pasar.</li>
                <li><strong>Pola Konsumsi:</strong> Basis konsumen platform memiliki kecenderungan transaksi yang kuat pada segmen perlengkapan rumah tangga, gaya hidup (<em>watches_gifts</em>), dan perawatan diri.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Stabilitas volume pesanan pada kategori unggulan ini krusial untuk menjaga arus kas. Penambahan alokasi promosi disarankan difokuskan pada sektor ini.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

st.write("")

# --- 1b: BOTTOM N ---
col2_chart, col2_desc = st.columns([1.5, 1])
with col2_chart:
    with st.container(border=True):
        st.markdown(f'<div class="card-header">1b. Bottom {top_n} Kategori Pendapatan Terendah</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Kategori dengan kontribusi penjualan paling minimum</div>', unsafe_allow_html=True)
        bot_df = category_rev_df.tail(top_n).sort_values(by="total_revenue", ascending=False)
        fig2, ax2 = plt.subplots(figsize=FIG_SIZE, dpi=FIG_DPI)
        lock_canvas(fig2)
        fig2.subplots_adjust(left=0.35, right=0.85, top=0.92, bottom=0.08)
        if not bot_df.empty:
            colors2 = [COLOR_MUTED] * (len(bot_df) - 1) + [COLOR_DANGER]
            bars2 = ax2.barh([shorten_label(c) for c in bot_df["product_category_name_english"]], bot_df["total_revenue"], color=colors2, height=0.6)
            ax2.spines["bottom"].set_visible(False)
            ax2.xaxis.set_visible(False)
            ax2.tick_params(axis="y", labelsize=9.5, length=0)
            max_bot = bot_df["total_revenue"].max() if bot_df["total_revenue"].max() > 0 else 1
            min_bot = bot_df["total_revenue"].min()
            ax2.set_xlim(0, max_bot * 1.25)
            for bar in bars2:
                w = bar.get_width()
                ax2.text(w + (max_bot * 0.02), bar.get_y() + bar.get_height()/2, f"R$ {w:,.0f}", va="center", ha="left", fontsize=9, color="#F8FAFC" if w == min_bot else "#94A3B8", fontweight="bold" if w == min_bot else "normal")
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

with col2_desc:
    low_c = bot_df.iloc[-1]["product_category_name_english"] if not bot_df.empty else "-"
    low_v = bot_df.iloc[-1]["total_revenue"] if not bot_df.empty else 0
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Evaluasi Segmen Mikro</div>
            <div>Sebagai penyeimbang, kategori <span class="text-red">{low_c}</span> menempati posisi paling dasar dengan kontribusi omzet hanya <span class="text-white">{low_v:,.2f} BRL</span> sepanjang periode terpilih.</div>
            <ul>
                <li><strong>Acuan Historis:</strong> Kategori <span class="text-red">diapers_and_hygiene</span> sebelumnya mencatat titik terendah pada tahun 2017.</li>
                <li><strong>Penyebab Mendasar:</strong> Kategori jasa atau kebutuhan yang mengandalkan kecepatan pakai tidak selaras dengan rantai pasok pengiriman reguler yang memakan waktu berhari-hari.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Lakukan audit beban operasional terhadap katalog ini. Penghapusan kategori berpotensi mengefisienkan infrastruktur platform.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# 7. DAMPAK LOGISTIK TERHADAP KEPUASAN

st.markdown('<div class="section-header">2. Dampak Keterlambatan Logistik Terhadap Reputasi</div>', unsafe_allow_html=True)

col3_chart, col3_desc = st.columns([1.5, 1])
with col3_chart:
    sub_colA, sub_colB = st.columns(2)
    
    with sub_colA:
        with st.container(border=True):
            st.markdown('<div class="card-header">2a. Ketepatan Waktu Logistik</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Volume pesanan tiba vs batas estimasi</div>', unsafe_allow_html=True)
            fig3, ax3 = plt.subplots(figsize=(4.5, 4.3), dpi=FIG_DPI)
            lock_canvas(fig3)
            fig3.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
            if not delivery_stats_df.empty:
                d_colors = [{"Tepat Waktu": COLOR_PRIMARY, "Terlambat": COLOR_DANGER}.get(s, COLOR_MUTED) for s in delivery_stats_df["delivery_status"]]
                wedges, texts, autotexts = ax3.pie(delivery_stats_df["order_count"], labels=delivery_stats_df["delivery_status"], autopct="%1.1f%%", startangle=90, colors=d_colors, pctdistance=0.75, wedgeprops=dict(width=0.4, edgecolor="#0F172A", linewidth=2), textprops=dict(color="#E2E8F0", fontsize=9.5))
                for autotext in autotexts:
                    autotext.set_fontweight("bold")
                ax3.text(0, -0.1, f"{total_orders / 1000:.1f}K" if total_orders >= 1000 else str(total_orders), ha="center", va="center", fontsize=15, fontweight="bold", color="#F8FAFC")
            st.pyplot(fig3, use_container_width=True)
            plt.close(fig3)

    with sub_colB:
        with st.container(border=True):
            st.markdown('<div class="card-header">2b. Fluktuasi Kepuasan Pelanggan</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Rata-rata skor ulasan (Skala 1 - 5)</div>', unsafe_allow_html=True)
            fig4, ax4 = plt.subplots(figsize=(4.5, 4.3), dpi=FIG_DPI)
            lock_canvas(fig4)
            fig4.subplots_adjust(left=0.15, right=0.9, top=0.88, bottom=0.15)
            if not delivery_stats_df.empty:
                b_colors = [{"Tepat Waktu": COLOR_PRIMARY, "Terlambat": COLOR_DANGER}.get(s, COLOR_MUTED) for s in delivery_stats_df["delivery_status"]]
                bars4 = ax4.bar(delivery_stats_df["delivery_status"], delivery_stats_df["avg_score"], color=b_colors, width=0.5)
                ax4.set_ylim(0, 5.5)
                ax4.yaxis.grid(True, linestyle="--", alpha=0.3)
                ax4.set_axisbelow(True)
                ax4.tick_params(axis="both", labelsize=9)
                for bar in bars4:
                    h = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2, h + 0.15, f"{h:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold", color="#F8FAFC")
            st.pyplot(fig4, use_container_width=True)
            plt.close(fig4)

with col3_desc:
    late_orders = int(delivery_stats_df.loc[delivery_stats_df["delivery_status"] == "Terlambat", "order_count"].sum()) if not delivery_stats_df.empty else 0

    # Skor ulasan dinamis mengikuti filter (bukan angka tetap)
    def _score(status):
        row = delivery_stats_df.loc[delivery_stats_df["delivery_status"] == status, "avg_score"]
        return f"{row.iloc[0]:.2f}" if not row.empty and pd.notna(row.iloc[0]) else "-"

    on_time_score = _score("Tepat Waktu")
    late_score = _score("Terlambat")
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Kolerasi Waktu & Reputasi</div>
            <div>Tingkat keberhasilan pemenuhan logistik berdampak mutlak terhadap nilai reputasi yang diberikan oleh konsumen (Sesuai dengan Pertanyaan 2).</div>
            <ul>
                <li><strong>Stabilitas Kepuasan:</strong> Pesanan yang diselesaikan sesuai batas estimasi mampu mengamankan tingkat kepuasan yang sangat solid, menetap di rata-rata <span class="text-blue">{on_time_score}</span> dari skala 5.</li>
                <li><strong>Penalti Reputasi:</strong> Tercatat ada <span class="text-red">{late_orders:,} pesanan</span> yang mengalami keterlambatan. Keterlambatan ini seketika menekan skor ulasan anjlok ke angka <span class="text-red">{late_score}</span>.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Keterlambatan adalah titik kritis kegagalan layanan. Manajemen perlu mengkalibrasi ulang parameter algoritma estimasi kedatangan, serta merevisi SLA dengan ekspedisi bermasalah.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# 8. DISTRIBUSI GEOSPASIAL & DEMOGRAFI

st.markdown('<div class="section-header">3. Demografi Geospasial dan Konsentrasi Wilayah</div>', unsafe_allow_html=True)

# --- 3a: TOP 10 STATES ---
col4a_chart, col4a_desc = st.columns([1.5, 1])
with col4a_chart:
    with st.container(border=True):
        st.markdown('<div class="card-header">3a. Peta Kepadatan Pelanggan (Top 10 States)</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Volume konsumen unik berdasarkan negara bagian administratif</div>', unsafe_allow_html=True)
        top_st = bystate_df.head(10).sort_values(by="customer_count", ascending=True)
        fig5, ax5 = plt.subplots(figsize=FIG_SIZE, dpi=FIG_DPI)
        lock_canvas(fig5)
        fig5.subplots_adjust(left=0.15, right=0.85, top=0.92, bottom=0.08)
        if not top_st.empty:
            colors5 = [COLOR_MUTED] * (len(top_st) - 1) + [COLOR_PRIMARY]
            bars5 = ax5.barh(top_st["customer_state"], top_st["customer_count"], color=colors5, height=0.65)
            ax5.spines["bottom"].set_visible(False)
            ax5.xaxis.set_visible(False)
            ax5.tick_params(axis="y", labelsize=9.5, length=0)
            max_st = top_st["customer_count"].max()
            ax5.set_xlim(0, max_st * 1.25)
            for bar in bars5:
                w = int(bar.get_width())
                ax5.text(w + (max_st * 0.02), bar.get_y() + bar.get_height()/2, f"{w:,}", va="center", ha="left", fontsize=9, color="#F8FAFC" if w == max_st else "#94A3B8", fontweight="bold" if w == max_st else "normal")
        st.pyplot(fig5, use_container_width=True)
        plt.close(fig5)

with col4a_desc:
    st_lead = top_st.iloc[-1]["customer_state"] if not top_st.empty else "-"
    st_lead_val = top_st.iloc[-1]["customer_count"] if not top_st.empty else 0
    st_lead_name = state_mapping.get(st_lead, st_lead)
    _runners = [state_mapping.get(x, x) for x in bystate_df["customer_state"].iloc[1:3]]
    runner_txt = f", disusul oleh {' dan '.join(_runners)}" if _runners else ""
    st.markdown(
        f"""
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Polarisasi Demografi</div>
            <div>Analisis demografis memperlihatkan struktur pembagian pasar yang tidak merata di wilayah daratan Brasil.</div>
            <ul>
                <li><strong>Dominasi Pesisir:</strong> Negara bagian <span class="text-blue">{st_lead_name}</span> menguasai pangsa pasar secara absolut dengan volume <span class="text-white">{st_lead_val:,} pelanggan</span>{runner_txt}.</li>
                <li><strong>Efisiensi Logistik:</strong> Ketiga wilayah ini secara ekonomi memang merupakan klaster paling maju dengan jaringan logistik darat yang paling efisien.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Penempatan Pusat Gudang Distribusi (<em>Fulfillment Center</em>) di dalam irisan area SP-RJ-MG sangat diwajibkan untuk menekan biaya logistik <em>last-mile</em>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

st.write("")

# 3b: PEMETAAN GEOSPASIAL
# Batas koordinat geografis Brasil (latitude dan longitude) untuk memfilter titik pelanggan
BR_LAT = (-33.751169, 5.274388)
BR_LNG = (-73.982830, -34.793147)

def customer_points(df):
    pts = df.drop_duplicates("customer_id").dropna(subset=["customer_geo_lat", "customer_geo_lng"])
    return pts[pts["customer_geo_lat"].between(*BR_LAT) & pts["customer_geo_lng"].between(*BR_LNG)]

base_map_df = customer_points(main_df)   # seluruh pelanggan (lapisan acuan, abu-abu)
map_df = customer_points(filtered_df)    # pelanggan sesuai filter (biru)

col4b_chart, col4b_desc = st.columns([1.5, 1])
with col4b_chart:
    with st.container(border=True):
        st.markdown('<div class="card-header">3b. Pemetaan Distribusi Koordinat Spasial</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Titik biru: pelanggan sesuai filter. Titik abu-abu: seluruh pelanggan sebagai acuan posisi wilayah</div>', unsafe_allow_html=True)
        fig6, ax6 = plt.subplots(figsize=(7.0, 5.8), dpi=FIG_DPI)
        lock_canvas(fig6)
        fig6.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.10)
        if not base_map_df.empty:
            ax6.scatter(base_map_df["customer_geo_lng"], base_map_df["customer_geo_lat"], alpha=0.25, s=1.0, c="#475569", edgecolors="none")
            if not map_df.empty:
                ax6.scatter(map_df["customer_geo_lng"], map_df["customer_geo_lat"], alpha=0.45, s=1.5, c=COLOR_PRIMARY, edgecolors="none")
            # kunci tampilan ke seluruh Brasil agar peta tidak ter-zoom saat filter dipakai
            ax6.set_xlim(BR_LNG[0], BR_LNG[1])
            ax6.set_ylim(BR_LAT[0], BR_LAT[1])
            ax6.set_aspect("equal", adjustable="box")
            ax6.xaxis.grid(True, linestyle="--", alpha=0.15)
            ax6.yaxis.grid(True, linestyle="--", alpha=0.15)
            ax6.set_xlabel("Garis Bujur (Longitude)", fontsize=9)
            ax6.set_ylabel("Garis Lintang (Latitude)", fontsize=9)
            ax6.tick_params(axis="both", labelsize=8.5)
        st.pyplot(fig6, use_container_width=True)
        plt.close(fig6)

with col4b_desc:
    if selected_states:
        map_panel = f"""
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Sebaran Wilayah Terpilih</div>
            <div>Peta menampilkan <span class="text-white">{len(map_df):,} pelanggan</span> pada {len(selected_states)} negara bagian terpilih sesuai filter aktif.</div>
            <ul>
                <li><strong>Cara Membaca:</strong> Titik biru adalah pelanggan pada wilayah terpilih, sedangkan abu-abu adalah seluruh pelanggan sebagai acuan posisi. Titik yang rapat menandakan konsentrasi pelanggan yang tinggi.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Hapus filter negara bagian untuk melihat perbandingan konsentrasi pelanggan di seluruh Brasil dan menentukan prioritas wilayah logistik.</li>
            </ul>
        </div>
        """
    else:
        map_panel = """
        <div class="insight-panel">
            <div class="insight-title">Insight Analisis: Tantangan Topografi</div>
            <div>Pemetaan plot titik berfungsi sebagai verifikasi spasial atas data distribusi administratif sebelumnya.</div>
            <ul>
                <li><strong>Konfirmasi Kepadatan:</strong> Ekosistem transaksi terpusat menyerupai gumpalan solid <span class="text-blue">di lajur pesisir timur</span> hingga ke ujung selatan negara.</li>
                <li><strong>Area Hampa Logistik:</strong> Area pedalaman yang membentang di bagian utara dan barat mencerminkan bentang alam Amazon. Persebaran di zona ini <span class="text-blue">sangat renggang dan menantang secara logistik</span>.</li>
                <li><strong>Rekomendasi Bisnis:</strong> Mengirim paket ke area utara terpencil berisiko tinggi gagal memenuhi ekspektasi pelanggan. Kemitraan strategis dengan ekspedisi lokal rute perintis mutlak diperlukan.</li>
            </ul>
        </div>
        """
    st.markdown(map_panel, unsafe_allow_html=True)
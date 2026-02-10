import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Gizli Tamlar Fabrikası",
    page_icon="🏭",
    layout="centered"
)

# --- CSS STİLLERİ (FABRİKA TEMASI) ---
st.markdown("""
<style>
    .stApp {
        background-color: #f1f2f6;
    }
    h1 { color: #2d3436; text-align: center; font-family: 'Courier New', monospace; font-weight: bold; }
    
    /* SİPARİŞ KARTI */
    .order-card {
        background-color: #fff;
        border: 4px dashed #fab1a0;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .order-title { font-size: 1.2rem; color: #636e72; text-transform: uppercase; letter-spacing: 2px; }
    .fraction-big { font-size: 3rem; font-weight: bold; color: #e17055; margin: 10px 0; }

    /* FABRİKA BANDI */
    .conveyor-belt {
        background-color: #dfe6e9;
        border-top: 5px solid #636e72;
        border-bottom: 5px solid #636e72;
        padding: 20px;
        overflow-x: auto;
        white-space: nowrap;
        border-radius: 5px;
        margin: 20px 0;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 10px;
    }

    /* BİRİM KESİR BLOKLARI (HAM MADDE) */
    .raw-block {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        background-color: #0984e3;
        color: white;
        border-radius: 5px;
        font-weight: bold;
        font-size: 1.2rem;
        border: 2px solid #74b9ff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }

    /* PAKETLENMİŞ KUTU (TAM) */
    .package-box {
        display: inline-flex;
        flex-direction: row; /* Yan yana diz */
        background-color: #fdcb6e;
        border: 3px solid #e17055;
        border-radius: 10px;
        padding: 5px;
        margin-right: 15px;
        position: relative;
    }
    
    /* Kutunun üzerindeki "1 TAM" etiketi */
    .package-label {
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        background: #e17055;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
    }

    /* Kutu içindeki bloklar */
    .packed-block {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background-color: #0984e3;
        color: white;
        border: 1px solid white;
        font-size: 0.9rem;
    }

    .btn-factory {
        width: 100%;
        background-color: #00b894;
        color: white;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        font-size: 1.2rem;
    }
    .btn-factory:hover { background-color: #55efc4; }

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (DURUM YÖNETİMİ) ---
if 'numerator' not in st.session_state:
    st.session_state.numerator = 7
if 'denominator' not in st.session_state:
    st.session_state.denominator = 3
if 'status' not in st.session_state:
    st.session_state.status = 'raw' # 'raw' (ham) veya 'packed' (paketlenmiş)

# --- FONKSİYONLAR ---
def new_order():
    """Yeni bir sipariş oluşturur."""
    denominators = [2, 3, 4, 5, 6]
    denom = random.choice(denominators)
    # Bileşik kesir olması için pay > payda olmalı
    num = random.randint(denom + 1, denom * 3 + denom - 1)
    
    st.session_state.numerator = num
    st.session_state.denominator = denom
    st.session_state.status = 'raw'

def pack_items():
    """Paketleme işlemini başlatır."""
    st.session_state.status = 'packed'

# --- ARAYÜZ (UI) ---
st.title("🏭 Gizli Tamlar Fabrikası")

# 1. Kontrol Paneli
col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    if st.button("🔄 Yeni Sipariş"):
        new_order()
        st.rerun()

# 2. Sipariş Kartı
st.markdown(f"""
<div class="order-card">
    <div class="order-title">📝 GÜNLÜK SİPARİŞ KARTI</div>
    <div class="fraction-big">{st.session_state.numerator} / {st.session_state.denominator}</div>
    <div style="color: #636e72;">
        Fabrika Şefi diyor ki:<br>
        <i>"Elimizde <b>{st.session_state.numerator}</b> tane <b>1/{st.session_state.denominator}</b>'lik parça var.<br>
        Bunları {st.session_state.denominator}'li gruplar halinde paketle!"</i>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Fabrika Bandı (Görselleştirme)
st.write("### ⚙️ Üretim Bandı")

if st.session_state.status == 'raw':
    # HAM MADDE GÖRÜNÜMÜ
    blocks_html = ""
    for _ in range(st.session_state.numerator):
        blocks_html += f'<div class="raw-block">1/{st.session_state.denominator}</div>'
    
    st.markdown(f'<div class="conveyor-belt">{blocks_html}</div>', unsafe_allow_html=True)
    
    # Paketleme Butonu
    if st.button("📦 MAKİNEYİ ÇALIŞTIR VE PAKETLE", type="primary", use_container_width=True):
        pack_items()
        st.rerun()

else:
    # PAKETLENMİŞ GÖRÜNÜM
    num = st.session_state.numerator
    denom = st.session_state.denominator
    
    whole_count = num // denom
    remainder = num % denom
    
    html_output = ""
    
    # Tam Paketleri Çiz
    for i in range(whole_count):
        pack_content = ""
        for _ in range(denom):
            pack_content += f'<div class="packed-block">1/{denom}</div>'
            
        html_output += f"""
        <div class="package-box">
            <div class="package-label">1 TAM</div>
            {pack_content}
        </div>
        """
    
    # Kalan Parçaları Çiz (Paketlenmemiş)
    for _ in range(remainder):
        html_output += f'<div class="raw-block" style="margin-left:10px; background-color: #fab1a0; border-color: #e17055;">1/{denom}</div>'
        
    st.markdown(f'<div class="conveyor-belt" style="background-color: #81ecec;">{html_output}</div>', unsafe_allow_html=True)
    
    # Sonuç Kartı
    st.success("✅ Paketleme Tamamlandı!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Toplam Parça", f"{num} adet")
    with col2:
        st.metric("Oluşan Tam Paket", f"{whole_count} TAM")
    with col3:
        st.metric("Artan Parça", f"{remainder} adet")
        
    st.info(f"**Matematiksel Dönüşüm:** {num}/{denom} = **{whole_count} Tam {remainder}/{denom}**")

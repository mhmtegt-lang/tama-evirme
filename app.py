import streamlit as st
import streamlit.components.v1 as components
import random

# --- KODLAMA STANDARTLARI: KONFİGÜRASYON ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası - Birikimli Mod", layout="wide")

# --- SİPARİŞ KARTLARI ---
if 'order_num' not in st.session_state:
    st.session_state.order_num = 7
    st.session_state.order_den = 3

# --- SIDEBAR: KONTROL PANELİ ---
with st.sidebar:
    st.header("📋 Fabrika Yönetimi")
    if st.button("🚀 Yeni Rastgele Sipariş"):
        st.session_state.order_den = random.choice([2, 3, 4, 5])
        st.session_state.order_num = random.randint(st.session_state.order_den + 1, 12)
        st.rerun()
    st.info("İpucu: Makinedeki sayaç parçalar paketlense bile artmaya devam eder, böylece toplam miktarı korur.")

# --- HTML/JS/CSS MOTORU ---
# Not: f-string içinde CSS/JS parantezleri için {{ }} kullanılmıştır.
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --primary: #0984e3;
            --accent: #ff7675;
            --shipping: #e8f8f5;
            --text: #2d3436;
        }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #fdfdfd; padding: 10px; display: flex; flex-direction: column; align-items: center; }}
        
        /* SİPARİŞ KARTI (image_2b925a tabanlı) */
        .order-card {{
            background: white; border: 3px dashed var(--accent); border-radius: 15px;
            padding: 10px; width: 280px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        .order-num {{ font-size: 40px; font-weight: bold; color: var(--accent); margin: 0; line-height: 1; }}
        .order-line {{ border-bottom: 4px solid var(--accent); width: 40px; margin: 5px auto; }}
        .order-den {{ font-size: 30px; font-weight: bold; color: var(--accent); margin: 0; line-height: 1; }}

        /* FABRİKA DÜZENİ */
        .factory-grid {{
            display: grid; grid-template-columns: 1fr 220px 1.5fr;
            gap: 15px; width: 100%; max-width: 1100px; align-items: stretch;
        }}

        .section-box {{
            background: white; border: 2px solid #eee; border-radius: 15px; padding: 15px;
            display: flex; flex-direction: column; min-height: 350px; position: relative;
        }}
        
        /* BAŞLIKLAR (image_2b925a'daki gibi yukarıda) */
        .section-title {{ 
            font-size: 12px; color: #999; font-weight: bold; text-align: center; 
            text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;
        }}

        /* DEPO VE PARÇALAR */
        .warehouse {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }}
        .piece {{
            width: 50px; height: 50px; background: var(--primary); color: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 13px;
            transition: 0.2s; border: 1px solid rgba(255,255,255,0.2);
        }}
        .piece:hover {{ transform: scale(1.1); background: #74b9ff; }}

        /* MAKİNE (Sıfırlanmayan Sayaçlı) */
        .machine-container {{
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            border: 2px solid #fab1a0; background: #fffcfb; border-radius: 12px; padding: 10px; height: 100%;
        }}
        #counter-display {{
            font-size: 22px; font-weight: bold; color: var(--primary); 
            background: #e1f5fe; padding: 8px 20px; border-radius: 25px; margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .bin-area {{
            width: 100%; border: 2px dashed #ddd; border-radius: 10px; 
            min-height: 80px; display: flex; flex-wrap: wrap; align-items: center; 
            justify-content: center; gap: 4px; padding: 5px;
        }}

        /* SEVKİYAT (SAĞ) */
        .shipping {{ background: var(--shipping); border-color: #00b894; }}
        .shipping-items {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; }}
        
        .box {{
            display: flex; border: 2px solid #e17055; background: #ffeaa7;
            border-radius: 8px; position: relative; padding: 4px; height: 60px; align-items: center;
            animation: popIn 0.3s ease-out;
        }}
        .box::after {{
            content: "1 TAM"; position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
            background: #e17055; color: white; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;
        }}
        
        .artan-box {{
            background: #a29bfe; border: 2px solid #6c5ce7; border-radius: 8px; 
            padding: 4px; height: 60px; display: flex; align-items: center; position: relative;
        }}
        .artan-box::after {{
            content: "ARTAN"; position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
            background: #6c5ce7; color: white; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;
        }}

        .packed-piece {{ width: 45px; height: 45px; background: var(--primary); border: 1px solid white; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold; }}

        @keyframes popIn {{ from {{ transform: scale(0.8); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
    </style>
</head>
<body>

    <div class="order-card">
        <div style="font-size: 10px; color: #999; margin-bottom: 5px;">GÜNLÜK SİPARİŞ KARTI</div>
        <p class="order-num">{st.session_state.order_num}</p>
        <div class="order-line"></div>
        <p class="order-den">{st.session_state.order_den}</p>
    </div>

    <div class="factory-grid">
        <div class="section-box">
            <div class="section-title">1. Ham Madde Deposu</div>
            <div class="warehouse" id="warehouse"></div>
        </div>

        <div class="section-box">
            <div class="section-title">2. Makine</div>
            <div class="machine-container">
                <div id="counter-display">0 / {st.session_state.order_den}</div>
                <div class="bin-area" id="bin"></div>
            </div>
        </div>

        <div class="section-box shipping">
            <div class="section-title">3. Sevkiyat Alanı (Ürünler)</div>
            <div class="shipping-items" id="shipping"></div>
        </div>
    </div>

    <script>
        const den = {st.session_state.order_den};
        const totalNum = {st.session_state.order_num};
        let globalProcessed = 0; // Birikimli Sayaç
        let currentInMachine = 0; // O anki paket içindeki parça

        const warehouseDiv = document.getElementById('warehouse');
        const binDiv = document.getElementById('bin');
        const shippingDiv = document.getElementById('shipping');
        const counterDisplay = document.getElementById('counter-display');

        function init() {{
            for(let i=0; i < totalNum; i++) {{
                let p = document.createElement('div');
                p.className = 'piece';
                p.innerText = '1/' + den;
                p.onclick = () => process(p);
                warehouseDiv.appendChild(p);
            }}
        }}

        function process(el) {{
            warehouseDiv.removeChild(el);
            
            // Sayacı Güncelle (Sıfırlanmaz!)
            globalProcessed++;
            counterDisplay.innerText = globalProcessed + " / " + den;

            // Makineye görsel parça ekle
            currentInMachine++;
            let packed = document.createElement('div');
            packed.className = 'packed-piece';
            packed.innerText = '1/' + den;
            binDiv.appendChild(packed);

            // Paketleme kontrolü
            if (currentInMachine === den) {{
                setTimeout(sendToShipping, 400);
            }} else if (globalProcessed === totalNum) {{
                // Son parçalar paketlenemedi (Artan)
                setTimeout(sendRemainderToShipping, 600);
            }}
        }}

        function sendToShipping() {{
            let box = document.createElement('div');
            box.className = 'box';
            for(let i=0; i < den; i++) {{
                let p = document.createElement('div');
                p.className = 'packed-piece';
                p.innerText = '1/' + den;
                box.appendChild(p);
            }}
            shippingDiv.appendChild(box);
            
            // Makine içindeki görseli temizle ama sayacı elleyemezsin!
            binDiv.innerHTML = '';
            currentInMachine = 0;
            
            confetti({{ particleCount: 60, spread: 50, origin: {{ x: 0.7, y: 0.6 }} }});
        }}

        function sendRemainderToShipping() {{
            if (currentInMachine > 0) {{
                let artanBox = document.createElement('div');
                artanBox.className = 'artan-box';
                for(let i=0; i < currentInMachine; i++) {{
                    let p = document.createElement('div');
                    p.className = 'packed-piece';
                    p.innerText = '1/' + den;
                    artanBox.appendChild(p);
                }}
                shippingDiv.appendChild(artanBox);
                binDiv.innerHTML = '';
                currentInMachine = 0;
            }}
        }}

        init();
    </script>
</body>
</html>
"""

try:
    components.html(html_code, height=750)
except Exception as e:
    st.error(f"Fabrika sisteminde bir hata oluştu: {e}")

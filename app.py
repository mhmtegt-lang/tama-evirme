import streamlit as st
import streamlit.components.v1 as components

# --- KODLAMA STANDARTLARI: KONFİGÜRASYON ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası v2", layout="wide")

# --- SİPARİŞ LİSTESİ (Çoklu Seçenekler) ---
ORDERS = [
    {"num": 7, "den": 3, "label": "7/3 (Standart)"},
    {"num": 13, "den": 6, "label": "13/6 (Orta Seviye)"},
    {"num": 14, "den": 11, "label": "14/11 (Zor)"},
    {"num": 5, "den": 2, "label": "5/2 (Başlangıç)"}
]

# --- SESSION STATE ---
if 'current_order' not in st.session_state:
    st.session_state.current_order = ORDERS[0]

# --- SIDEBAR: SİPARİŞ SEÇİMİ ---
with st.sidebar:
    st.header("📋 Sipariş Yönetimi")
    choice = st.selectbox(
        "Yeni bir Sipariş Kartı seçin:",
        options=range(len(ORDERS)),
        format_func=lambda x: ORDERS[x]["label"]
    )
    
    if st.button("🚀 Siparişi Fabrikaya Gönder"):
        st.session_state.current_order = ORDERS[choice]
        st.rerun()

# --- HTML/JS/CSS MOTORU ---
order_num = st.session_state.current_order["num"]
order_den = st.session_state.current_order["den"]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --primary: #0984e3;
            --accent: #ff7675;
            --shipping-bg: #e8f8f5;
        }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f8f9fa; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
        
        /* SİPARİŞ KARTI DÜZENLEMELERİ */
        .order-card {{
            background: white; border: 3px dashed var(--accent); border-radius: 15px;
            padding: 15px; width: 320px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        .order-num {{ font-size: 42px; font-weight: bold; color: var(--accent); margin: 0; line-height: 1; }} /* 7 Yazısı küçültüldü */
        .order-line {{ border-bottom: 4px solid var(--accent); width: 40px; margin: 5px auto; }}
        .order-den {{ font-size: 32px; font-weight: bold; color: var(--accent); margin: 0; line-height: 1; }}

        /* FABRİKA ALANI */
        .factory-grid {{
            display: grid; grid-template-columns: 1fr 220px 1.5fr;
            gap: 20px; width: 100%; max-width: 1100px; align-items: stretch;
        }}

        .section-box {{
            background: white; border: 2px solid #ddd; border-radius: 12px; padding: 15px;
            display: flex; flex-direction: column; min-height: 280px; position: relative;
        }}
        
        /* BAŞLIK HİZALAMASI (Yukarı çekildi) */
        .section-title {{ 
            font-size: 11px; color: #888; font-weight: bold; text-align: center; 
            position: absolute; top: 10px; width: calc(100% - 30px);
            text-transform: uppercase; letter-spacing: 1px;
        }}

        .content-area {{ margin-top: 30px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }}

        /* PARÇA VE MAKİNE */
        .piece {{
            width: 48px; height: 48px; background: var(--primary); color: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 12px;
            transition: 0.2s; border: 1px solid rgba(255,255,255,0.2);
        }}
        .piece:hover {{ transform: translateY(-3px); background: #74b9ff; }}

        .machine-bin {{
            margin-top: 40px; border: 3px solid #fab1a0; background: #fffcfb; 
            border-radius: 12px; padding: 10px; display: flex; flex-direction: column; align-items: center;
        }}
        
        /* GERÇEK ZAMANLI KESİR GÖSTERGESİ */
        #fraction-display {{
            font-size: 18px; font-weight: bold; color: var(--primary); margin-bottom: 10px;
            background: #e1f5fe; padding: 5px 15px; border-radius: 20px;
        }}

        .bin-slots {{ display: flex; gap: 4px; min-height: 50px; align-items: center; justify-content: center; }}

        /* SEVKİYAT VE PAKETLER */
        .box {{
            display: flex; border: 2px solid #e17055; background: #ffeaa7;
            border-radius: 8px; position: relative; padding: 4px; height: 55px; align-items: center;
        }}
        .box::after {{
            content: "1 TAM"; position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
            background: #e17055; color: white; padding: 1px 6px; border-radius: 10px; font-size: 9px; font-weight: bold;
        }}
        
        .art-label {{
            background: #6c5ce7; color: white; padding: 1px 6px; border-radius: 10px; font-size: 9px; font-weight: bold;
            position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
        }}

        .packed-piece {{ width: 40px; height: 40px; background: var(--primary); border: 1px solid white; display: flex; align-items: center; justify-content: center; color: white; font-size: 10px; font-weight: bold; }}

    </style>
</head>
<body>

    <div class="order-card">
        <div style="font-size: 9px; margin-bottom: 5px; color: #999;">📝 GÜNLÜK SİPARİŞ KARTI</div>
        <p class="order-num">{order_num}</p>
        <div class="order-line"></div>
        <p class="order-den">{order_den}</p>
    </div>

    <div class="factory-grid">
        <div class="section-box">
            <div class="section-title">1. HAM MADDE DEPOSU</div>
            <div class="content-area" id="warehouse"></div>
        </div>

        <div class="section-box" style="border-color: #fab1a0;">
            <div class="section-title">2. MAKİNE</div>
            <div class="machine-bin">
                <div id="fraction-display">0 / {order_den}</div>
                <div class="bin-slots" id="bin"></div>
            </div>
        </div>

        <div class="section-box" style="background: var(--shipping-bg); border-color: #00b894;">
            <div class="section-title">3. SEVKİYAT ALANI (ÜRÜNLER)</div>
            <div class="content-area" id="shipping"></div>
        </div>
    </div>

    <script>
        const den = {order_den};
        const total = {order_num};
        let warehouseCount = total;
        let binCount = 0;

        const warehouseDiv = document.getElementById('warehouse');
        const binDiv = document.getElementById('bin');
        const shippingDiv = document.getElementById('shipping');
        const fracDisplay = document.getElementById('fraction-display');

        function init() {{
            for(let i=0; i < total; i++) {{
                let p = document.createElement('div');
                p.className = 'piece';
                p.innerText = '1/' + den;
                p.onclick = () => move(p);
                warehouseDiv.appendChild(p);
            }}
        }}

        function move(el) {{
            warehouseDiv.removeChild(el);
            warehouseCount--;

            binCount++;
            fracDisplay.innerText = binCount + " / " + den;

            let p = document.createElement('div');
            p.className = 'packed-piece';
            p.innerText = '1/' + den;
            binDiv.appendChild(p);

            if(binCount === den) {{
                setTimeout(packageBox, 400);
            }} else if (warehouseCount === 0) {{
                setTimeout(moveRemainder, 600);
            }}
        }}

        function packageBox() {{
            let b = document.createElement('div');
            b.className = 'box';
            for(let i=0; i<den; i++) {{
                let p = document.createElement('div');
                p.className = 'packed-piece';
                p.innerText = '1/' + den;
                b.appendChild(p);
            }}
            shippingDiv.appendChild(b);
            binDiv.innerHTML = '';
            binCount = 0;
            fracDisplay.innerText = "0 / " + den;
            confetti({{ particleCount: 50, spread: 40, origin: {{ x: 0.7, y: 0.5 }} }});
        }}

        function moveRemainder() {{
            if(binCount > 0) {{
                const items = binDiv.querySelectorAll('.packed-piece');
                items.forEach(item => {{
                    let r = document.createElement('div');
                    r.className = 'piece';
                    r.style.position = 'relative';
                    r.innerHTML = '<div class="art-label">ARTAN</div>1/' + den;
                    shippingDiv.appendChild(r);
                }});
                binDiv.innerHTML = '';
                fracDisplay.innerText = "Bitti!";
            }}
        }}

        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=750)

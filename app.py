import streamlit as st
import streamlit.components.v1 as components
import random

# --- KODLAMA STANDARTLARI: KONFİGÜRASYON ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası", layout="wide")

# --- OYUN DURUMU ---
if 'order_num' not in st.session_state:
    # Başlangıç siparişi: 7/3
    st.session_state.order_num = 7
    st.session_state.order_den = 3

# --- HTML/JS/CSS OYUN MOTORU ---
# Piaget'nin korunum ilkesini destekleyen, parçaların sağa sevkiyatını sağlayan motor.
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --bg: #f8f9fa;
            --primary: #0984e3;
            --accent: #ff7675;
            --shipping-bg: #e8f8f5;
        }}
        body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); padding: 20px; display: flex; flex-direction: column; align-items: center; }}
        
        /* SİPARİŞ KARTI */
        .order-card {{
            background: white; border: 3px dashed var(--accent); border-radius: 15px;
            padding: 20px; width: 350px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        .order-num {{ font-size: 50px; font-weight: bold; color: var(--accent); margin: 0; }}
        .order-line {{ border-bottom: 4px solid var(--accent); width: 50px; margin: 2px auto; }}
        .order-den {{ font-size: 35px; font-weight: bold; color: var(--accent); margin: 0; }}

        /* FABRİKA ALANI */
        .factory-grid {{
            display: grid; grid-template-columns: 1fr 200px 1.5fr;
            gap: 20px; width: 100%; max-width: 1000px; align-items: stretch;
        }}

        .section-box {{
            background: white; border: 2px solid #ddd; border-radius: 12px; padding: 15px;
            display: flex; flex-direction: column; min-height: 250px;
        }}
        .title {{ font-size: 12px; color: #aaa; font-weight: bold; text-align: center; margin-bottom: 10px; }}

        /* DEPODAKİ PARÇALAR */
        .warehouse {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }}
        .piece {{
            width: 50px; height: 50px; background: var(--primary); color: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 13px;
            transition: transform 0.2s; border: 1px solid rgba(255,255,255,0.2);
        }}
        .piece:hover {{ transform: translateY(-3px); background: #74b9ff; }}

        /* MAKİNE ÜRETİM BANDI */
        .machine {{
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            border: 3px solid #fab1a0; background: #fffcfb; border-radius: 12px; gap: 5px;
        }}
        .bin {{
            width: 160px; height: 60px; border: 2px solid #ddd; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; gap: 3px;
            background: #fdfdfd; padding: 4px;
        }}

        /* SEVKİYAT ALANI (SAĞ TARAF) */
        .shipping {{ background: var(--shipping-bg); border-color: #00b894; }}
        .shipping-items {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; }}
        
        .box {{
            display: flex; border: 2px solid #e17055; background: #ffeaa7;
            border-radius: 8px; position: relative; padding: 4px; height: 60px; align-items: center;
            animation: slideIn 0.4s ease-out;
        }}
        .box::after {{
            content: "1 TAM"; position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
            background: #e17055; color: white; padding: 1px 6px; border-radius: 10px; font-size: 10px; font-weight: bold;
        }}
        
        .remaining-piece {{
            background: #a29bfe; border-color: #6c5ce7; position: relative;
        }}
        .remaining-piece::after {{
            content: "ARTAN"; position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
            background: #6c5ce7; color: white; padding: 1px 6px; border-radius: 10px; font-size: 10px; font-weight: bold;
        }}

        .packed-piece {{ width: 42px; height: 42px; background: var(--primary); border: 1px solid white; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold; }}

        @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
    </style>
</head>
<body>

    <div class="order-card">
        <div style="font-size: 10px; letter-spacing: 1px;">📝 GÜNLÜK SİPARİŞ KARTI</div>
        <p class="order-num">{st.session_state.order_num}</p>
        <div class="order-line"></div>
        <p class="order-den">{st.session_state.order_den}</p>
    </div>

    <div class="factory-grid">
        <div class="section-box">
            <div class="title">1. HAM MADDE DEPOSU</div>
            <div class="warehouse" id="warehouse"></div>
        </div>

        <div class="section-box machine">
            <div class="title">2. MAKİNE</div>
            <div class="bin" id="bin">
                <span style="color:#ccc; font-size:11px;">Parçayı Buraya Tıkla</span>
            </div>
        </div>

        <div class="section-box shipping">
            <div class="title">3. SEVKİYAT ALANI (ÜRÜNLER)</div>
            <div class="shipping-items" id="shipping"></div>
        </div>
    </div>

    <script>
        const den = {st.session_state.order_den};
        const total = {st.session_state.order_num};
        let warehouseCount = total;
        let binCount = 0;

        const warehouseDiv = document.getElementById('warehouse');
        const binDiv = document.getElementById('bin');
        const shippingDiv = document.getElementById('shipping');

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
            if(binCount === 0) binDiv.innerHTML = '';
            
            warehouseDiv.removeChild(el);
            warehouseCount--;

            let p = document.createElement('div');
            p.className = 'packed-piece';
            p.innerText = '1/' + den;
            binDiv.appendChild(p);
            binCount++;

            if(binCount === den) {{
                setTimeout(packageBox, 300);
            }} else if (warehouseCount === 0) {{
                // Kalan artan parça için kontrol
                setTimeout(moveRemainderToShipping, 500);
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
            binDiv.innerHTML = '<span style="color:#ccc; font-size:11px;">Paketlendi!</span>';
            binCount = 0;
            confetti({{ particleCount: 40, spread: 40, origin: {{ x: 0.7, y: 0.5 }} }});
            
            if(warehouseCount > 0 && warehouseCount < den) {{
                 // Eğer depoda kalanlar bir tam etmiyorsa otomatik bitirilemez, kullanıcının tıklaması beklenir.
            }}
        }}

        function moveRemainderToShipping() {{
            if(binCount > 0) {{
                // Makinede kalan (tamamlanamayan) parçaları tek tek sağa at
                const items = binDiv.querySelectorAll('.packed-piece');
                items.forEach(item => {{
                    let r = document.createElement('div');
                    r.className = 'piece remaining-piece';
                    r.innerText = '1/' + den;
                    shippingDiv.appendChild(r);
                }});
                binDiv.innerHTML = '<span style="color:#ccc; font-size:11px;">Bitti!</span>';
                binCount = 0;
            }}
        }}

        init();
    </script>
</body>
</html>
"""

components.html(html_code, height=700)

# --- ALT PANEL: SONUÇ VE YENİ SİPARİŞ ---
st.markdown("---")
if st.button("🔄 Fabrikayı Sıfırla ve Yeni Sipariş Al"):
    st.session_state.order_den = random.choice([2, 3, 4, 5, 6])
    st.session_state.order_num = random.randint(st.session_state.order_den + 1, 15)
    st.rerun()

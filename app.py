import streamlit as st
import streamlit.components.v1 as components

# --- KODLAMA STANDARTLARI ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası", layout="wide")

# --- OYUN DURUMU (SESSION STATE) ---
if 'order_num' not in st.session_state:
    st.session_state.order_num = 7
if 'order_den' not in st.session_state:
    st.session_state.order_den = 3

# --- HTML/JS/CSS (OYUN MOTORU) ---
# Piaget'nin korunum ilkesini desteklemek için parçaların kutuya girmesi simüle edildi.
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background-color: #f1f2f6; display: flex; flex-direction: column; align-items: center; padding: 20px; }}
        
        /* SİPARİŞ KARTI */
        .order-card {{
            background: white; border: 4px dashed #ff7675; border-radius: 20px;
            padding: 30px; width: 400px; text-align: center; margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }}
        .order-num {{ font-size: 60px; font-weight: bold; color: #ff7675; margin: 0; }}
        .order-line {{ border-bottom: 5px solid #ff7675; width: 60px; margin: 5px auto; }}
        .order-den {{ font-size: 40px; font-weight: bold; color: #ff7675; margin: 0; }}

        /* PAKETLEME ALANI */
        .factory-floor {{
            display: flex; gap: 50px; align-items: flex-start; width: 100%; max-width: 1000px;
        }}

        /* SOL: HAM MADDE (DEPO) */
        .warehouse {{ flex: 1; display: flex; flex-wrap: wrap; gap: 10px; border: 2px solid #ddd; padding: 20px; border-radius: 15px; background: white; }}
        .unit-piece {{
            width: 60px; height: 60px; background: #0984e3; color: white; display: flex;
            align-items: center; justify-content: center; font-weight: bold; cursor: pointer;
            border-radius: 8px; transition: 0.2s;
        }}
        .unit-piece:hover {{ transform: scale(1.1); background: #74b9ff; }}

        /* SAĞ: SEVKİYAT (PAKETLENMİŞ ÜRÜNLER) */
        .shipping {{ flex: 1.5; display: flex; flex-wrap: wrap; gap: 20px; border: 2px solid #00b894; padding: 20px; border-radius: 15px; background: #e8f8f5; min-height: 200px; }}
        
        .box {{
            display: flex; border: 3px solid #e17055; background: #ffeaa7; border-radius: 10px;
            position: relative; padding: 5px; height: 70px; align-items: center;
        }}
        .box::after {{
            content: "1 TAM"; position: absolute; top: -25px; left: 50%; transform: translateX(-50%);
            background: #e17055; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold;
        }}
        .packed-piece {{ width: 50px; height: 50px; background: #0984e3; border: 1px solid white; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; }}

        /* AKTİF KUTU (MAKİNE) */
        .machine {{ width: 100%; text-align: center; margin-bottom: 20px; }}
        .machine-bin {{
            width: 250px; height: 80px; border: 4px solid #fab1a0; margin: auto;
            display: flex; align-items: center; justify-content: center; gap: 5px;
            background: #fff; border-radius: 15px; position: relative;
        }}
        .machine-bin::before {{ content: "MAKİNE (Giriş)"; position: absolute; top: -20px; font-size: 12px; color: #aaa; }}

    </style>
</head>
<body>

    <div class="order-card">
        <div style="font-size: 12px; color: #aaa;">GÜNLÜK SİPARİŞ KARTI</div>
        <p class="order-num">{st.session_state.order_num}</p>
        <div class="order-line"></div>
        <p class="order-den">{st.session_state.order_den}</p>
        <div style="margin-top:15px; font-style: italic; font-size: 14px; color: #636e72;">
            "Elimizde {st.session_state.order_num} adet 1/{st.session_state.order_den} parça var. <br>
            Bunları {st.session_state.order_den}'li paketler yap!"
        </div>
    </div>

    <div class="machine">
        <div class="machine-bin" id="machine-bin">
            <span style="color: #ccc;">Parçaları buraya tıkla!</span>
        </div>
    </div>

    <div class="factory-floor">
        <div class="warehouse" id="warehouse">
            </div>
        <div class="shipping" id="shipping">
            </div>
    </div>

    <script>
        const den = {st.session_state.order_den};
        const totalNum = {st.session_state.order_num};
        let warehouseCount = totalNum;
        let machineCount = 0;

        const warehouse = document.getElementById('warehouse');
        const machine = document.getElementById('machine-bin');
        const shipping = document.getElementById('shipping');

        // Depoyu Doldur
        function initWarehouse() {{
            warehouse.innerHTML = '';
            for(let i=0; i < warehouseCount; i++) {{
                let p = document.createElement('div');
                p.className = 'unit-piece';
                p.innerText = '1/' + den;
                p.onclick = () => moveToMachine(p);
                warehouse.appendChild(p);
            }}
        }}

        function moveToMachine(element) {{
            if (machineCount === 0) machine.innerHTML = '';
            
            warehouse.removeChild(element);
            warehouseCount--;

            let packed = document.createElement('div');
            packed.className = 'packed-piece';
            packed.innerText = '1/' + den;
            machine.appendChild(packed);
            machineCount++;

            // Paket Doldu mu?
            if (machineCount === den) {{
                setTimeout(finalizePackage, 300);
            }}
        }}

        function finalizePackage() {{
            let box = document.createElement('div');
            box.className = 'box';
            for(let i=0; i < den; i++) {{
                let p = document.createElement('div');
                p.className = 'packed-piece';
                p.innerText = '1/' + den;
                box.appendChild(p);
            }}
            shipping.appendChild(box);
            
            machine.innerHTML = '<span style="color: #ccc;">Yeni paket hazır!</span>';
            machineCount = 0;
            
            confetti({{ particleCount: 50, spread: 30, origin: {{ y: 0.8 }} }});

            checkGameOver();
        }}

        function checkGameOver() {{
            if (warehouseCount < den) {{
                // Kalanlar depoda kalır, paketleme biter.
                if(warehouseCount === 0) {{
                    alert("Tüm sipariş paketlendi!");
                }}
            }}
        }}

        initWarehouse();
    </script>
</body>
</html>
"""

components.html(html_code, height=800)

# --- ALT KONTROLLER (STREAMLIT) ---
st.markdown("---")
if st.button("🔄 Yeni Rastgele Sipariş Al"):
    import random
    st.session_state.order_den = random.choice([2, 3, 4, 5])
    st.session_state.order_num = random.randint(st.session_state.order_den + 1, 15)
    st.rerun()

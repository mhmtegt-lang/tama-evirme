import streamlit as st
import streamlit.components.v1 as components

# --- KODLAMA STANDARTLARI: GÜVENLİK VE YAPILANDIRMA ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası", layout="wide")

# --- CSS STİLLERİ (Görsel 1 ile Birebir Uyumlu) ---
STYLE = """
<style>
    body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; }
    .factory-container { max-width: 800px; margin: auto; padding: 20px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    
    /* SAYI DOĞRUSU */
    .number-line { position: relative; width: 100%; height: 100px; margin: 40px 0; border-bottom: 3px solid #00a8ff; }
    .tick { position: absolute; bottom: -10px; width: 4px; height: 20px; background: #00a8ff; transform: translateX(-50%); }
    .tick-label { position: absolute; top: 25px; transform: translateX(-50%); font-weight: bold; font-size: 1.2rem; }
    .point { position: absolute; bottom: -8px; width: 16px; height: 16px; background: #00a8ff; border-radius: 50%; transform: translateX(-50%); }

    /* BLOKLAR */
    .blocks-row { display: flex; position: absolute; bottom: 5px; width: 100%; transition: all 0.5s; }
    .block { display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; border: 1px solid white; height: 50px; border-radius: 4px 4px 0 0; }
    
    /* Görseldeki Renkler */
    .purple { background-color: #9b59b6; } /* 1/3 */
    .pink { background-color: #ff9ff3; color: #2d3436; border-radius: 0 0 8px 8px !important; border-top: none !important; } /* 1 TAM */

    .mixed-row { display: flex; position: absolute; top: 105px; width: 100%; }
</style>
"""

# --- OYUN MANTIĞI (Logic) ---
def main():
    st.title("🏭 Gizli Tamlar Fabrikası")
    st.write("Görseldeki adımları takip ederek bileşik kesirleri paketleyelim.")

    # Durum Yönetimi (Step 1 to Step 4)
    if 'step' not in st.session_state:
        st.session_state.step = 1

    # Kontrol Butonları
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("⬅️ Önceki Adım") and st.session_state.step > 1:
            st.session_state.step -= 1
    with col2:
        if st.button("Sonraki Adım ➡️") and st.session_state.step < 4:
            st.session_state.step += 1
    with col3:
        if st.button("🔄 Fabrikayı Sıfırla"):
            st.session_state.step = 1

    st.subheader(f"📍 {st.session_state.step}. Adım")

    # --- DİNAMİK HTML OLUŞTURMA ---
    # Adım 4'te 4 tane 1/3 var. Her adımda bir tane artıyor.
    num_blocks = st.session_state.step
    block_width = 33.33  # 1/3 olduğu için (100% / 3)
    
    # Üstteki 1/3 Blokları
    upper_blocks = "".join([f'<div class="block purple" style="width:{block_width}%">1/3</div>' for _ in range(num_blocks)])
    
    # Alttaki Paketleme (Sadece Adım 3 ve 4'te görünür)
    lower_content = ""
    if st.session_state.step >= 3:
        # 3 tane 1/3 = 1 TAM
        lower_content += f'<div class="block pink" style="width:100%">1</div>'
        if st.session_state.step == 4:
            # 1/3 artan parça
            lower_content += f'<div class="block purple" style="width:{block_width}%">1/3</div>'

    html_content = f"""
    {STYLE}
    <div class="factory-container">
        <div class="number-line">
            <div class="blocks-row">{upper_blocks}</div>
            
            <div class="point" style="left: 0%"></div><div class="tick-label" style="left: 0%">0</div>
            <div class="tick" style="left: 16.66%"></div>
            <div class="tick" style="left: 33.33%"></div>
            <div class="point" style="left: 50%"></div><div class="tick-label" style="left: 50%">1</div>
            <div class="tick" style="left: 66.66%"></div>
            <div class="tick" style="left: 83.33%"></div>
            <div class="point" style="left: 100%"></div><div class="tick-label" style="left: 100%">2</div>

            <div class="mixed-row">{lower_content}</div>
        </div>
    </div>
    """
    
    components.html(html_content, height=300)

    # --- GÖRSEL 2: SORULAR (image_1f6946.png) ---
    if st.session_state.step == 4:
        st.markdown("---")
        st.write("### 🧠 Fabrika Şefi'nin Soruları")
        
        q1 = st.text_input("a) 4. Adım'daki iki farklı modelin kesir gösterimi nedir?")
        q2 = st.text_area("b) Bu iki gösterim arasındaki ilişkiyi nasıl ifade edersiniz?")
        
        if st.button("Cevapları Gönder"):
            if "4/3" in q1 and "1 tam 1/3" in q1.lower():
                st.balloons()
                st.success("Tebrikler! Piaget'nin korunum ilkesini kanıtladın: Parçalar paketlense de miktar değişmez!")
            else:
                st.info("İpucu: Üstteki model 4 tane 1/3, alttaki model 1 tam ve 1/3.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Fabrika hattında teknik bir arıza oluştu: {e}")

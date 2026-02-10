import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# --- KODLAMA STANDARTLARI: KONFİGÜRASYON ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası", layout="wide")

class FractionFactory:
    """Bileşik kesirleri tam sayılı kesirlere dönüştüren iş mantığı sınıfı."""
    
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ValueError("Payda sıfır olamaz.")
        self.num = numerator
        self.den = denominator

    def get_step_info(self, step):
        """Her adımda tam ve artan bilgisini hesaplar."""
        whole = step // self.den
        remainder = step % self.den
        return whole, remainder

class FactoryVisualizer:
    """Görseldeki (image_1f6657.png) stilinde çizim yapan motor."""
    
    @staticmethod
    def draw_step(current_step, denominator, target_num):
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Sayı doğrusu ayarları
        limit = 2.5 if target_num/denominator <= 2 else (target_num/denominator) + 0.5
        ax.set_xlim(-0.2, limit)
        ax.set_ylim(-1.5, 2)
        ax.axis('off')

        # 1. Sayı Doğrusu Çizgisi
        ax.axhline(y=0, color='#3498db', linewidth=2, zorder=1)
        
        # Tam sayı işaretleri ve ara bölmeler
        ticks = int(limit) + 1
        for i in range(ticks):
            ax.plot(i, 0, 'o', color='#2980b9', markersize=8, zorder=2)
            ax.text(i, -0.4, str(i), ha='center', fontsize=12, fontweight='bold')
            
            # Ara bölmeler (Payda kadar)
            if i < ticks - 1:
                for j in range(1, denominator):
                    ax.plot(i + j/denominator, 0, '.', color='#3498db', markersize=4)

        # 2. ÜST KATMAN: Birim Kesir Blokları (Bileşik Gösterim)
        # Görseldeki mor renk: #9b59b6
        for s in range(current_step):
            x_pos = s * (1/denominator)
            rect = patches.Rectangle(
                (x_pos, 0.2), 1/denominator, 0.6,
                edgecolor='white', facecolor='#9b59b6', linewidth=1
            )
            ax.add_patch(rect)
            ax.text(x_pos + 0.5/denominator, 0.5, f"1/{denominator}", 
                    ha='center', va='center', color='white', fontsize=8)

        # 3. ALT KATMAN: Paketleme (Tam Sayılı Gösterim)
        # Görseldeki pembe renk: #ff9ff3
        whole = current_step // denominator
        remainder = current_step % denominator
        
        # Tamları Çiz
        for w in range(whole):
            rect = patches.Rectangle(
                (w, -1.2), 1, 0.6,
                edgecolor='white', facecolor='#ff9ff3', linewidth=2
            )
            ax.add_patch(rect)
            ax.text(w + 0.5, -0.9, "1 TAM", ha='center', va='center', color='black', fontweight='bold')

        # Kalanı Çiz
        if remainder > 0:
            for r in range(remainder):
                x_rem = whole + (r * (1/denominator))
                rect = patches.Rectangle(
                    (x_rem, -1.2), 1/denominator, 0.6,
                    edgecolor='white', facecolor='#9b59b6', linewidth=1
                )
                ax.add_patch(rect)
                ax.text(x_rem + 0.5/denominator, -0.9, f"1/{denominator}", 
                        ha='center', va='center', color='white', fontsize=8)

        return fig

def main():
    st.title("🏭 Gizli Tamlar Fabrikası: Adım Adım Üretim")
    st.markdown("---")

    # --- DURUM YÖNETİMİ (Session State) ---
    if 'game_num' not in st.session_state:
        st.session_state.game_den = random.choice([3, 4, 5])
        st.session_state.game_num = random.randint(st.session_state.game_den + 1, 8)
        st.session_state.step = 0

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("📦 Sipariş Kartı")
        st.info(f"Hedef Kesir: **{st.session_state.game_num}/{st.session_state.game_den}**")
        st.write(f"Fabrikaya **{st.session_state.game_num}** tane **1/{st.session_state.game_den}** parçası geldi.")
        
        # Adım Butonları
        if st.button("➕ Bir Parça Daha Ekle", disabled=(st.session_state.step >= st.session_state.game_num)):
            st.session_state.step += 1
            st.rerun()
            
        if st.button("🔄 Yeni Sipariş Al"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    with col2:
        st.subheader(f"Adım {st.session_state.step}: Üretim Hattı")
        
        # Görselleştirme
        try:
            fig = FactoryVisualizer.draw_step(
                st.session_state.step, 
                st.session_state.game_den, 
                st.session_state.game_num
            )
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Görselleştirme hatası: {e}")

        # Bilgi Notları
        whole, rem = divmod(st.session_state.step, st.session_state.game_den)
        if st.session_state.step > 0:
            st.write(f"**Şu anki Durum:** {st.session_state.step} tane birim kesir toplandı.")
            if whole > 0:
                st.success(f"🎊 {whole} tane TAM paket oluştu!")
            if rem > 0:
                st.warning(f"⚠️ {rem} tane parça henüz paketlenemedi (Artan).")

    # --- GÖRSEL 2 SORULARI (Interaktif) ---
    if st.session_state.step == st.session_state.game_num:
        st.markdown("---")
        st.subheader("🧠 Fabrika Şefi Soruyor")
        ans_a = st.text_input("Siparişin tam sayılı kesir karşılığı nedir? (Örn: 2 tam 1/3)")
        if ans_a:
            correct_ans = f"{whole} tam {rem}/{st.session_state.game_den}" if rem > 0 else f"{whole}"
            if ans_a.lower().strip() == correct_ans.lower():
                st.balloons()
                st.success("Harika! Siparişi doğru etiketledin.")
            else:
                st.error(f"Tekrar dene! İpucu: {whole} tam ve artan parça...")

if __name__ == "__main__":
    main()

import streamlit as st

# 1. SAYFA AYARLARI (Mobil cihazlarda tam ekran ve şık görünmesi için)
st.set_page_config(
    page_title="Kalori Sihirbazı", 
    page_icon="🏃", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. GÖRSEL BAŞLIK VE GİRİŞ
st.title("🏃 Koşu Bandı Kalori Sihirbazı")
st.markdown("##### *Laboratuvar tipi gelişmiş kalori hesaplama sistemi*")
st.write("Bilgilerini girip 'Kaloriyi Hesapla' butonuna basman yeterli kral. Boş bıraktığın profil alanları senin standart değerlerine göre hesaplanır.")
st.markdown("---")

# 3. KULLANICI PROFİL ALANI (Biyometrik Veriler)
st.subheader("👤 Profil Bilgileri")
col1, col2 = st.columns(2)

with col1:
    cinsiyet = st.radio("Cinsiyet", ("Erkek", "Kadın"), index=0)
with col2:
    yas = st.number_input("Yaşınız", min_value=1, max_value=120, value=23, step=1)

# Yan yana iki kolon daha açarak kilo ve eğimi yerleştiriyoruz
col3, col4 = st.columns(2)
with col3:
    kilo = st.number_input("Kilonuz (kg)", min_value=10.0, max_value=300.0, value=76.0, step=0.1)
with col4:
    egim = st.number_input("Koşu Bandı Eğimi (%)", min_value=0.0, max_value=30.0, value=5.7, step=0.1)

st.markdown("---")

# 4. ANTRENMAN VERİLERİ ALANI (Mesafe ve Süre)
st.subheader("📊 Antrenman Değerleri")
col5, col6 = st.columns(2)

with col5:
    mesafe_km = st.number_input("Yürünen / Koşulan Mesafe (km)", min_value=0.01, max_value=100.0, value=5.0, step=0.01)
with col6:
    sure_dakika = st.number_input("Toplam Süre (Dakika)", min_value=1.0, max_value=480.0, value=30.0, step=1.0)

st.markdown("---")

# 5. HESAPLAMA VE ÇIKTI MOTORU
if st.button("🔥 KALORİYİ HESAPLA", type="primary", use_container_width=True):
    
    # Arka plan veri dönüşümleri
    cinsiyet_kod = 'e' if cinsiyet == "Erkek" else 'k'
    egim_ondalik = egim / 100
    
    # Hız Hesaplamaları (km/saat ve metre/dakika)
    hiz_km_sa = mesafe_km / (sure_dakika / 60)
    hiz_m_dk = hiz_km_sa * 16.6667
    
    # Hıza Göre Akıllı Formül Seçimi (ACSM Standartları)
    if hiz_km_sa < 8.0:
        aktivite_turu = "Yürüyüş (Walking)"
        vo2 = (0.1 * hiz_m_dk) + (1.8 * hiz_m_dk * egim_ondalik) + 3.5
    else:
        aktivite_turu = "Koşu (Running)"
        vo2 = (0.2 * hiz_m_dk) + (0.9 * hiz_m_dk * egim_ondalik) + 3.5
    
    # Aktivite anındaki brüt oksijen tüketimi kalorisi
    brut_kalori = ((vo2 * kilo) / 200) * sure_dakika
    
    # Biyometrik Harris-Benedict Düzeltmesi (Yağ/Kas ve Metabolizma Yaşı Dengesi)
    if cinsiyet_kod == 'e':
        bazal_metabolizma = 66.47 + (13.75 * kilo) + (5.0 * 170) - (6.75 * yas)
        yas_faktoru = max(0.90, 1.0 - ((yas - 20) * 0.002))
    else:
        bazal_metabolizma = 655.1 + (9.56 * kilo) + (1.85 * 170) - (4.68 * yas)
        yas_faktoru = max(0.85, 0.92 - ((yas - 20) * 0.002))
        
    dakikalik_bazal = bazal_metabolizma / 1440
    antrenman_bazal = dakikalik_bazal * sure_dakika
    
    # Net harcanan kalori ve gerçekçi sapma aralığı (+- %2)
    net_kalori = (brut_kalori - antrenman_bazal) * yas_faktoru + antrenman_bazal
    alt_sinir = round(net_kalori * 0.98)
    ust_sinir = round(net_kalori * 1.02)
    
    # EKRAA ŞIK SONUÇ KARTLARI BASMA
    st.success(f"### 🎉 Tahmini Yakılan Kalori: {alt_sinir} - {ust_sinir} kcal")
    
    # İstatistikleri yan yana gösteren şık kutular (Metrics)
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="Hesaplanan Hız", value=f"{hiz_km_sa:.2f} km/s")
    with res_col2:
        st.metric(label="Aktivite Türü", value=aktivite_turu)
    with res_col3:
        st.metric(label="Efor Süresi", value=f"{int(sure_dakika)} dk")
        
    st.balloons() # Hesaplama bitince ekrandan yukarı balonlar uçuran tatlı bir kutlama efekti
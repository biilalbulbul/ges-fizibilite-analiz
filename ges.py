import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon
import requests
import pandas as pd
import os
from fpdf import FPDF
import tempfile
from geopy.geocoders import Nominatim

st.set_page_config(page_title="GES-Pro | Profesyonel Analiz", layout="wide")

# CSS - Arayüz Tasarımı
st.markdown("""<style>
    .stApp { background-color: #0E1117; }
    h1 { color: #F4D03F !important; }
</style>""", unsafe_allow_html=True)

# Yan Menü
if os.path.exists("banner.png"): st.sidebar.image("banner.png", use_container_width=True)
st.sidebar.header("⚙️ Parametreler")
panel_verimi = 0.22 if "Premium" in st.sidebar.selectbox("Panel Verimliliği", ("Standart (%20)", "Premium (%22)")) else 0.20
maliyet = st.sidebar.number_input("Kurulum Maliyeti ($/kWp)", value=800)
fiyat = st.sidebar.number_input("Elektrik Birim Fiyatı ($/kWh)", value=0.10)

st.title("GES-Pro: Profesyonel Solar Raporlama")

# --- YENİ EKLENEN: ADRES VE KOORDİNAT ARAMA SİSTEMİ ---
col_map_top1, col_map_top2 = st.columns([1, 1])
with col_map_top1:
    search_type = st.radio("Konum Seçim Yöntemi", ["Adres ile Bul", "Koordinat Gir"])
    lat, lon = 40.9, 29.2 # Varsayılan değerler
    
    if search_type == "Adres ile Bul":
        adres = st.text_input("Adres:", placeholder="Örn: Kadıköy, İstanbul")
        if adres:
            try:
                geolocator = Nominatim(user_agent="ges_pro_app")
                loc = geolocator.geocode(adres)
                if loc: lat, lon = loc.latitude, loc.longitude
            except: st.error("Adres bulunamadı.")
    else:
        lat = st.number_input("Enlem:", value=40.9, format="%.6f")
        lon = st.number_input("Boylam:", value=29.2, format="%.6f")

# --- PDF OLUŞTURMA FONKSİYONU ---
def create_pdf(alan, y_uretim, t_maliyet, y_tasarruf, fixed):
    panel_sayisi = int(alan * 0.45) 
    co2_tasarruf = (y_uretim * 0.5) / 1000
    amortisman = t_maliyet / y_tasarruf
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 15, "GES PROJESI TEKLIF VE FIZIBILITE RAPORU", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "1. Teknik Proje Ozeti", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"- Toplam Cati Alani: {alan:,.0f} m2", ln=True)
    pdf.cell(200, 8, f"- Tahmini Panel Sayisi: {panel_sayisi} Adet", ln=True)
    pdf.cell(200, 8, f"- Yillik Tahmini Uretim: {y_uretim:,.0f} kWh", ln=True)
    pdf.cell(200, 8, f"- Yillik Bolgesel Isinim: {fixed['H(i)_y']:.1f} kWh/m2", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "2. Finansal Verimlilik", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"- Toplam Yatirim Maliyeti: ${t_maliyet:,.0f}", ln=True)
    pdf.cell(200, 8, f"- Yillik Tasarruf: ${y_tasarruf:,.0f}", ln=True)
    pdf.cell(200, 8, f"- Amortisman Suresi: {amortisman:.1f} Yil", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "3. Cevresel Etki", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"- Yillik Karbon Salinimi Onleme: {co2_tasarruf:.2f} Ton CO2", ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- ANA HARİTA VE ANALİZ ---
col1, col2 = st.columns([3, 2])

with col1:
    m = folium.Map(location=[lat, lon], zoom_start=18, max_zoom=22)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                     attr='Esri', max_zoom=22, max_native_zoom=19).add_to(m)
    draw = Draw(export=False, draw_options={'polygon': True, 'polyline': False, 'rectangle': False, 'circle': False, 'marker': False})
    m.add_child(draw)
    st_data = st_folium(m, width=900, height=600)

with col2:
    if st_data["last_active_drawing"]:
        coords = st_data["last_active_drawing"]["geometry"]["coordinates"][0]
        poly = Polygon(coords)
        alan = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[poly]).to_crs("EPSG:32635").area.values[0]
        
        url = f"https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat={round(poly.centroid.y, 4)}&lon={round(poly.centroid.x, 4)}&peakpower=1&loss=14&outputformat=json"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()['outputs']
                fixed = data['totals']['fixed']
                
                tab1, tab2, tab3 = st.tabs(["💼 Finansal", "📊 Üretim", "🌍 Teknik"])
                
                with tab1:
                    y_uretim = alan * panel_verimi * fixed['H(i)_y'] * 0.86
                    t_maliyet = (alan * panel_verimi) * maliyet
                    y_tasarruf = y_uretim * fiyat
                    panel_sayisi = int(alan * 0.45)
                    co2_tasarruf = (y_uretim * 0.5) / 1000
                    amortisman = t_maliyet / y_tasarruf if y_tasarruf > 0 else 0
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Maliyet", f"${t_maliyet:,.0f}")
                    c2.metric("Tasarruf", f"${y_tasarruf:,.0f}")
                    c3.metric("Amortisman", f"{amortisman:.1f} Yıl")
                    
                    st.divider()
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.subheader("📋 Teknik Detaylar")
                        st.markdown(f"- **Çatı Alanı:** {alan:,.0f} m²")
                        st.markdown(f"- **Panel Sayısı:** {panel_sayisi} Adet")
                        st.markdown(f"- **Yıllık Üretim:** {y_uretim:,.0f} kWh")
                    
                    with col_right:
                        st.subheader("🌱 Stratejik Kazanımlar")
                        st.write(f"- **Karbon Önleme:** {co2_tasarruf:.2f} Ton CO2")
                        st.write("- **Garanti:** 25 Yıl Performans")
                        st.write("- **Sürdürülebilirlik:** A+ Sınıfı")
                    
                    st.divider()
                    pdf_path = create_pdf(alan, y_uretim, t_maliyet, y_tasarruf, fixed)
                    with open(pdf_path, "rb") as f:
                        st.download_button("📄 Profesyonel PDF Raporu İndir", f, "GES_Teklif.pdf")

                with tab2:
                    st.subheader("Aylık PV Enerji Çıkışı")
                    # Grafik verisine birim ismini ekledik
                    chart_data = pd.DataFrame(data['monthly']['fixed']).set_index('month')[['E_m']]
                    chart_data.columns = ['Enerji (kWh)']
                    st.bar_chart(chart_data, color="#F4D03F")
                    
                with tab3:
                    st.table(pd.DataFrame({
                        "Parametre": ["Sistem Kaybı", "Yıllık Işınım"], 
                        "Değer": ["%14", f"{fixed['H(i)_y']} kWh/m²"]
                    }))
            else:
                st.error("API verisi alınamadı.")
        except:
            st.error("Hesaplama hatası.")
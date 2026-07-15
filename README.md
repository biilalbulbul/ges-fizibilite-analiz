# GES Fizibilite ve Analiz Aracı

Harita mühendisliği prensipleriyle geliştirilmiş, çatı tipi GES (Güneş Enerjisi Santralleri) için otomatik teknik ve finansal fizibilite raporlama aracı. Python dilinde Folium, Shapely, Geopandas, Geopy gibi GIS kütüphaneleri kullanılarak tasarlanmıştır.

## Proje Hakkında
Bu yazılım, çatı tipi güneş enerjisi projelerinde manuel ölçüm ve hesaplama süreçlerini dijitalleştirmek için geliştirilmiştir. Kullanıcılar harita üzerinde istedikleri çatıyı seçerek, sistemin sunduğu mekansal analiz sayesinde anlık olarak teknik ve finansal verimlilik raporlarına ulaşabilmektedir.

##  Kullanılan Teknolojiler
- **Python**: Temel programlama dili.
- **Streamlit**: Web arayüzü ve uygulama çerçevesi.
- **Folium & Leafmap**: Mekansal veri görselleştirme ve etkileşimli haritalar.
- **GeoPandas & Shapely**: CBS tabanlı alan hesaplamaları ve mekansal analizler.
- **Geopy**: Konum ve adres çözümleme.
- **JRC PVGIS API**: Güneş enerjisi üretim tahmini için küresel veri entegrasyonu.

## Temel Özellikler
- **Adres/Koordinat Tabanlı Arama**: İstenilen bölgeye hızlı odaklanma.
- **Otomatik Alan Hesaplama**: Çatı sınırlarını çizerek anında metrekare ($m^2$) hesabı.
- **Finansal Analiz**: Kurulum maliyeti, yıllık tasarruf ve amortisman süresi hesaplamaları.
- **Profesyonel PDF Raporu**: Tüm analizlerin kurum kimliğine uygun, anlık PDF çıktısı.
- **Karbon Salınım Analizi**: Yatırımın çevresel etkisinin raporlanması.

## İletişim ve İş Birliği
Bu yazılımın mekansal analiz metodolojisi ve teknik altyapısı özgün bir çalışma olup, GES sektöründeki firmalar için teklif süreçlerini optimize etmeyi hedeflemektedir. İş birliği, demo talepleri veya teknik detaylar için iletişime geçebilirsiniz.

## Gelecek Planları ve Geliştirme Süreci
Bu proje, enerji sektöründeki dijital dönüşümü desteklemek amacıyla sürekli olarak güncellenmektedir. Yakın dönem yol haritamda şu geliştirmeler bulunmaktadır:
- **Ada Parsel Bazlı Sorgu Sistemi**: Projede yer alan mevcut Adres ve Coğrafi Koordinatlara dayalı olan sorgu sistemine ek olarak sonraki aşamalarda, Ada Parsel üzerinden de sorgu yapılıp arsa, binalara kolaylıkla ulaşılabilmesini sağlayacağım.
- **Arazi Tipi** : Çatı analizlerine ek olarak, geniş arazilerde (tarla/arsa) kurulum potansiyelini belirlemek için; eğim analizi, şebeke bağlantı noktasına mesafe hesaplama ve tarım arazisi vasfı gözetmeksizin saha verimliliği optimizasyonu modüllerinin sisteme entegre edilmesi.
- **Gölge Analizi**: Çatı üzerindeki elektrik direkleri, ağaçlar, binalar gibi çevresel engelleri analiz ederek daha hassas verimlilik hesaplamaları eklemek.
- **Veri Tabanı Entegrasyonu**: Hazırlanan tüm tekliflerin kaydedilebileceği ve geçmişe dönük analizlerin yapılabileceği bir kullanıcı paneli.
- **Gelişmiş Panel Modülleri**: Farklı markaların teknik verilerini seçebileceğiniz dinamik bir marka kütüphanesi.
- **3D Modelleme**: Çatı eğimini ve yönünü dikkate alan daha kapsamlı 3D görselleştirme desteği.

**Bilal Bülbül**
https://www.linkedin.com/in/bilal-bülbül-4099b5333/

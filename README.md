# 📥 YouTube Video ve MP3 İndirici Web Uygulaması

Temiz, modern ve şık bir arayüze sahip **YouTube Video ve MP3 İndirici** web uygulaması.

---

## 🚀 Özellikler

- **🎨 Ultra Modern & Glassmorphism UI:** Özel koyu tema (Dark Mode), yumuşak geçişler, YouTube enerjisini yansıtan neon detaylar ve şık kart tasarımları.
- **⚡ yt-dlp & FFmpeg Entegrasyonu:** En son YouTube şifreleme ve akış protokolleriyle tam uyumlu indirme motoru.
- **🎯 İki Temel Format Seçeneği:**
  1. **🎵 Sadece Ses (En Yüksek Kalite MP3):** En yüksek ses kalitesi ayıklanır, FFmpeg ile 320 kbps MP3 formatına dönüştürülür ve ID3 meta etiketleri eklenir.
  2. **🎬 Video (En Yüksek Kalite MP4):** En yüksek çözünürlükteki video (1080p, 2K, 4K) ile ses akışı birleştirilerek saf MP4 formatında sunulur.
- **✂️ Belirli Bir Aralığı İndirme (Zaman Kırpma):**
  - "Belirli Bir Aralığı İndir" onay kutusu ile video içinden sadece istenen zaman dilimini (Örn: `00:01:15` veya `75` saniye) indirme imkanı.
  - FFmpeg keyframe (`force_keyframes_at_cuts`) desteği sayesinde milisaniyelik, kayıpsız ve hassas kesim.
  - Hem MP3 hem de MP4 formatlarında tam uyumlu.
- **📊 Canlı İndirme & Dönüştürme Göstergeleri:**
  - Anlık ilerleme çubuğu (%)
  - İndirme hızı (MB/s veya KB/s)
  - İndirilen ve toplam boyut
  - Tahmini kalan süre (ETA)
- **🎧 Dahili Oynatıcı & Tek Tıkla Tarayıcı İndirmesi:**
  - İndirilen MP3 veya MP4 dosyasını doğrudan sayfada dinleyin veya izleyin.
  - `st.download_button` ile tek tıkla bilgisayarınıza kaydedin.
  - İstenirse yerel indirme klasörünü doğrudan açma imkanı.
- **📜 İndirme Geçmişi:** Aynı oturumda indirilen medyaları listeleyip kolayca tekrar indirebilme.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. 📦 Bağımsız Masaüstü Programı (.EXE - Kuruluma Gerek Yok)
Herhangi bir bilgisayarda Python veya FFmpeg olmadan çalıştırmak için:
1. `dist/YouTubeIndirici/YouTubeIndirici.exe` dosyasına çift tıklayın (veya `dist/YouTubeIndirici-Windows.zip` arşivini hedef bilgisayarda açıp çalıştırın).
2. Otomatik olarak tarayıcınızda açılır ve kullanıma hazır hale gelir.
3. Klasör içindeki `Masaüstü_Kısayolu_Oluştur.bat` dosyasına tıklayarak Windows masaüstünüze doğrudan kısayol ekleyebilirsiniz.

### 2. Geliştirici Modunda Başlatma
Proje dizinindeki [baslat.bat](file:///c:/Users/izgem/Desktop/youtube-in/baslat.bat) dosyasına çift tıklayarak tarayıcınızda otomatik olarak açabilirsiniz.

### 3. Terminal Üzerinden Manuel Çalıştırma
```powershell
# Sanal ortamı aktive edin veya doğrudan sanal ortamdaki streamlit ile çalıştırın:
.\.venv\Scripts\streamlit.exe run app.py
```

Uygulama yerel adres: `http://localhost:8501`

---

## 📁 Proje Yapısı

- [YouTubeIndirici.exe](file:///c:/Users/izgem/Desktop/youtube-in/dist/YouTubeIndirici/YouTubeIndirici.exe): Kurulumsuz tek tıkla çalışan Windows masaüstü programı.
- [app.py](file:///c:/Users/izgem/Desktop/youtube-in/app.py): Modern Streamlit kullanıcı arayüzü ve akış yönetimi.
- [downloader.py](file:///c:/Users/izgem/Desktop/youtube-in/downloader.py): `yt-dlp` ve `FFmpeg` ile medya çıkarma, dönüştürme ve ilerleme takip modülü.
- [main.py](file:///c:/Users/izgem/Desktop/youtube-in/main.py): Bağımsız .exe paketleyici başlatıcı modülü.
- [bin/](file:///c:/Users/izgem/Desktop/youtube-in/bin/): Yerleşik `ffmpeg.exe` ve `ffprobe.exe` araçları.
- [requirements.txt](file:///c:/Users/izgem/Desktop/youtube-in/requirements.txt): Gerekli Python bağımlılıkları.
- [baslat.bat](file:///c:/Users/izgem/Desktop/youtube-in/baslat.bat): Tek tıkla uygulamayı başlatan geliştirici scripti.
- `downloads/`: İndirilen medya dosyalarının saklandığı klasör.

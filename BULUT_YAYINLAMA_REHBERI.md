# 🌐 YouTube İndirici - Ücretsiz Web Sitesi Olarak Yayınlama Rehberi

Bu rehber, uygulamanızı **%100 ÜCRETSİZ** olarak tüm dünyadan ve tüm cihazlardan (telefon, tablet, bilgisayar) erişilebilecek bir web sitesi haline getirmeniz için hazırlanmıştır.

En ideal ve tamamen ücretsiz platform: **Streamlit Community Cloud** (Resmi Streamlit bulut sunucusu).

---

## 📋 Projede Yapılan Otomatik Hazırlıklar (Tamamlandı ✅)
1. **`packages.txt` oluşturuldu:** Linux bulut sunucusunda `ffmpeg` aracının otomatik kurulması sağlandı.
2. **`requirements.txt` hazırlandı:** Gerekli tüm kütüphaneler tanımlandı.
3. **`app.py` buluta uyarlandı:** Bulut ortamında çalışırken yerel klasör açma hataları önlendi, doğrudan tarayıcıdan indirme optimize edildi.
4. **`.gitignore` güncellendi:** Ağır dosyaların (Windows `.exe`, `bin/`, `dist/`) GitHub'a yüklenip limit hatası vermesi engellendi.
5. **Yerel Git arşivi (`main` dalı) oluşturuldu:** Tüm kodlar ilk commit ile paketlendi.

---

## 🚀 3 Basit Adımda Yayınlama:

### Adım 1: GitHub'da Yeni Bir Repo Oluşturun (1 Dakika)
1. [github.com](https://github.com) adresine gidin ve giriş yapın (Hesabınız yoksa ücretsiz kaydolun).
2. Sağ üstteki **"+"** ikonuna tıklayıp **"New repository"** seçin.
3. **Repository name:** `youtube-indirici` (veya dilediğiniz bir isim) yazın.
4. **Public** (Herkese Açık) seçeneğini işaretleyin.
5. *"Add a README"*, *"Add .gitignore"* seçeneklerini **İŞARETLEMEYİN** (çünkü projemizde zaten var).
6. Yeşil **"Create repository"** butonuna tıklayın.

---

### Adım 2: Kodları GitHub'a Gönderin (Terminalden)
GitHub sayfasında size verilen linki (`https://github.com/KULLANICI_ADINIZ/youtube-indirici.git`) kopyalayın ve proje klasörünüzde terminal açarak şu komutları çalıştırın:

```powershell
# GitHub linkinizi ekleyin (Kendi linkinizi yazın):
git remote add origin https://github.com/KULLANICI_ADINIZ/youtube-indirici.git

# Kodları gönderin:
git push -u origin main
```

*(Alternatif olarak: GitHub web sayfasında "uploading an existing file" seçeneğiyle `app.py`, `downloader.py`, `requirements.txt`, `packages.txt` ve `.streamlit/` klasörünü sürükleyip bırakabilirsiniz.)*

---

### Adım 3: Streamlit Cloud ile Yayına Alın (Ücretsiz)
1. **[share.streamlit.io](https://share.streamlit.io)** adresine gidin.
2. **"Continue with GitHub"** diyerek GitHub hesabınızla tek tıkla giriş yapın.
3. **"Create app"** veya **"New app"** butonuna tıklayın.
4. Açılan formda:
   - **Repository:** `KULLANICI_ADINIZ/youtube-indirici`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Dilediğiniz özel bir isim belirleyebilirsiniz (Örn: `benim-youtube-indiricim`).
5. **"Deploy!"** butonuna basın.

🎉 **Tebrikler!** Yaklaşık 1-2 dakika içinde uygulamanız:
`https://benim-youtube-indiricim.streamlit.app`
gibi kalıcı, SSL sertifikalı (https) ve tamamen ücretsiz bir web sitesi olarak 7/24 yayında olacaktır!

---

## 💡 Önemli İpuçları
- **Mobil Uyumlu:** Web sitesi yayınlandıktan sonra linki telefonunuza gönderip telefonunuzdan da YouTube videosu/MP3'ü indirebilirsiniz.
- **Otomatik Güncelleme:** Projede bir değişiklik yapıp `git push` yaptığınızda, web siteniz otomatik olarak güncellenir.

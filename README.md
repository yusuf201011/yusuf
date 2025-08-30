# 🏆 Spor Sitesi

Modern ve kullanıcı dostu bir spor haberleri ve maç sonuçları web sitesi. Flask framework'ü kullanılarak geliştirilmiştir.

## ✨ Özellikler

- 📰 **Spor Haberleri**: Kategorilere ayrılmış güncel spor haberleri
- ⚽ **Maç Sonuçları**: Canlı ve tamamlanmış maç sonuçları
- 👥 **Kullanıcı Yönetimi**: Kayıt olma ve giriş yapma sistemi
- 🔧 **Admin Paneli**: Haber ve maç ekleme yönetimi
- 📱 **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- 🎨 **Modern UI**: Bootstrap 5 ile güzel arayüz

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd spor-sitesi
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı çalıştırın:**
```bash
python app.py
```

5. **Tarayıcınızda açın:**
```
http://localhost:5000
```

## 📋 Kullanım

### Normal Kullanıcı
- Ana sayfada güncel haberleri ve maçları görüntüleyin
- Haberler sayfasından kategorilere göre filtreleme yapın
- Maçlar sayfasından spor türü ve duruma göre filtreleme yapın
- Kayıt olun ve giriş yapın

### Admin Kullanıcı
- **Giriş bilgileri:**
  - Kullanıcı adı: `admin`
  - Şifre: `admin123`
- Admin panelinden haber ekleyin
- Maç programları ve sonuçları ekleyin
- Site istatistiklerini görüntüleyin

## 🏗️ Proje Yapısı

```
spor-sitesi/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── templates/            # HTML şablonları
│   ├── base.html         # Ana şablon
│   ├── index.html        # Ana sayfa
│   ├── news.html         # Haberler sayfası
│   ├── news_detail.html  # Haber detayı
│   ├── matches.html      # Maçlar sayfası
│   ├── login.html        # Giriş sayfası
│   ├── register.html     # Kayıt sayfası
│   ├── admin.html        # Admin paneli
│   ├── admin_add_news.html    # Haber ekleme
│   └── admin_add_match.html   # Maç ekleme
└── static/               # Statik dosyalar
    ├── css/              # CSS dosyaları
    ├── js/               # JavaScript dosyaları
    └── images/           # Resim dosyaları
```

## 🗄️ Veritabanı Modelleri

### User (Kullanıcı)
- id, username, email, password_hash, created_at, is_admin

### News (Haber)
- id, title, content, image_url, category, created_at, author_id

### Match (Maç)
- id, home_team, away_team, home_score, away_score, match_date, status, sport_type

## 🎨 Teknolojiler

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome
- **Veritabanı**: SQLite
- **Dil**: Python 3.8+

## 📱 Özellikler Detayı

### Haberler
- Kategori bazlı filtreleme (Futbol, Basketbol, Voleybol, Tenis, Diğer)
- Sayfalama sistemi
- Haber detay sayfaları
- İlgili haberler önerisi

### Maçlar
- Spor türü filtreleme
- Durum filtreleme (Programlanmış, Canlı, Tamamlanmış)
- Canlı maç göstergeleri
- Maç tarih ve saat bilgileri

### Admin Paneli
- Haber ekleme formu
- Maç ekleme formu
- Site istatistikleri
- Hızlı erişim linkleri

## 🔧 Geliştirme

### Yeni özellik eklemek için:
1. `app.py` dosyasında yeni route'lar ekleyin
2. Gerekli template dosyalarını oluşturun
3. Veritabanı modellerini güncelleyin
4. CSS/JS dosyalarını ekleyin

### Veritabanı değişiklikleri:
```bash
# Veritabanını sıfırlamak için
rm spor_sitesi.db
python app.py
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📞 İletişim

- Email: info@sporsitesi.com
- Telefon: +90 555 123 4567

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir. Gerçek bir spor sitesi için ek güvenlik önlemleri ve optimizasyonlar gerekebilir.

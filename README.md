🧠 Projenin Amacı
Geliştirdiğim bu yazılım, kameradan veya klasörden alınan görüntülerdeki plakaları:

Otomatik olarak algılar

OCR (optik karakter tanıma) ile plakadaki harf ve rakamları okur

Okunan plakaları tekrar kontrol eder ve gereksiz kopyaları engeller

Her tanınan plakayı bir dosyaya kaydeder ve sayısını takip eder.

🔧 Kullanılan Teknolojiler
OpenCV: Görüntü işleme ve kontur analizi

imutils: Görüntüleri yeniden boyutlandırma ve kontur alma

EasyOCR: Plaka karakterlerini tanıma (Türkçe destekli)

NumPy: Görsel işlemler

datetime & os: Dosya yönetimi ve zaman damgası

🧪 Sistemin İşleyişi
Görüntü Girişi:

Kameradan canlı görüntü alınıyor.

Alternatif olarak klasördeki fotoğraflar taranıyor (plates_to_read).

Plaka Tespiti:

Görüntü griye çevriliyor, bulanıklaştırılıyor ve kenarları bulunuyor.

Belirli oranda dörtgen benzeri konturlar plaka olarak varsayılıyor.

Plaka Okuma:

EasyOCR ile plaka karakterleri okunuyor.

Sadece geçerli plakalar (harf + sayı oranı yeterli) kaydediliyor.

Tekrar Algılama Engeli:

Aynı plaka daha önce tanındıysa sadece sayacı artırılıyor.
![Ekran görüntüsü 2025-05-26 001607](https://github.com/user-attachments/assets/298d0cbb-92d0-41b6-904b-9f3587420dc4)


Her plakanın bir adet küçük görseli ve sayacı ekranda gösteriliyor.

💡 Neden Bu Sistem Etkili?
❌ Aynı plaka tekrar tekrar analiz edilmez (verimlilik artar)

✅ Sadece geçerli plaka formatları tanınır (hatalı veriler elenir)

📁 Her okunan plaka dosyaya kaydedilir (otomatik kayıt)

👁️ Görsel olarak da önizleme penceresi oluşturuluyor (anlık takip)

🚀 Gelecek Geliştirmeler
YOLOv5 gibi daha sağlam bir modelle araç ve plaka tespiti

Web arayüzü veya mobil entegrasyon

Plaka geçmişini veri tabanında tutma ve sorgulama

Hatalı OCR çıktıları için manuel düzeltme paneli

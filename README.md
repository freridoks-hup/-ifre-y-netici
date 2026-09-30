# Güvenli Şifre Yöneticisi & Analiz Aracı

Python ile sıfırdan geliştirilmiş, üçüncü taraf hazır araçlara bağımlı olmayan, modern kırma yazılımlarına (John the Ripper, Hashcat vb.) karşı dirençli kişisel şifre yöneticisi ve üreticisi.

# Öne Çıkan Özellikler

* **Kriptografik Rastgelelik (`secrets`):** Standart ve tahmin edilebilir `random` kütüphanesi yerine, donanımsal düzeyde güvenli rastgele karakter seçimi.
* **Askeri Düzeyde Şifreleme (`Fernet`):** Kayıtlarınız disk üzerinde açık metin (plain-text) olarak değil, belirlediğiniz **Master Password (Ana Şifre)** ile türetilen anahtarla şifrelenmiş (`.enc`) olarak saklanır.
* **Brute-Force Dayanıklılık Analizi:** Üretilen şifrenin kombinasyon uzayını hesaplayarak modern sistemlere karşı tahmini kırılma süresini raporlar.
* **Güvenlik Puanlama Sistemi:** Şifrenizin uzunluk ve karakter çeşitliliğine göre 100 üzerinden güvenlik puanı verir.
* **Sıfır Bağımlılık Tuzağı:** Tamamen kendi kontrolünüzde, şeffaf ve özelleştirilebilir Python mantığı.

# Kurulum ve Çalıştırma

Projeyi yerel ortamınıza klonlayın ve gerekli kriptografi kütüphanesini yükleyin:

```bash
# Depoyu klonlayın
git clone [https://github.com/freridoks-hup/python-port-tarayici-beta.git](https://github.com/freridoks-hup/python-port-tarayici-beta.git)
cd python-port-tarayici-beta

# Gerekli kütüphaneyi yükleyin
pip install cryptography

# Şifre yöneticisini çalıştırın
python sifre_yoneticisi.py

import string
import secrets
import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DOSYA_ADI = "kasam.enc"
ANAHTAR_DOSYASI = "anahtar.key"

def anahtar_olustur_veya_yukle():
    
    master_sifre = input("🔒 Kasayı açmak / oluşturmak için Master Şifre girin: ").encode()
    
    
    salt = b'guvenli_salt_degeri_123' 
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_sifre))
    return key

def sifre_analiz_et(sifre, karakter_kumesi_boyutu):
    uzunluk = len(sifre)
    puan = 0
    if uzunluk >= 16: puan += 50
    elif uzunluk >= 12: puan += 35
    elif uzunluk >= 8: puan += 20
    else: puan += 5
    
    if any(c in string.ascii_lowercase for c in sifre): puan += 10
    if any(c in string.ascii_uppercase for c in sifre): puan += 15
    if any(c in string.digits for c in sifre): puan += 15
    if any(c in string.punctuation for c in sifre): puan += 10
    
    if puan > 100: puan = 100
    
    toplam_kombinasyon = karakter_kumesi_boyutu ** uzunluk
    saniye = toplam_kombinasyon / 10_000_000_000
    
    if saniye < 1: sure = "Anında (< 1 saniye - Çok Zayıf!)"
    elif saniye < 60: sure = f"{int(saniye)} saniye"
    elif saniye < 3600: sure = f"{int(saniye / 60)} dakika"
    elif saniye < 86400: sure = f"{int(saniye / 3600)} saat"
    elif saniye < 31536000: sure = f"{int(saniye / 86400)} gün"
    elif saniye < 31536000 * 1000: sure = f"{int(saniye / 31536000)} yıl"
    else: sure = "Milyarlarca yıl (Kırılması imkansıza yakın!)"
        
    return puan, sure

def sifreleri_oku(key):
    if not os.path.exists(DOSYA_ADI):
        return {}
    try:
        f = Fernet(key)
        with open(DOSYA_ADI, "rb") as dosya:
            sifreli_veri = dosya.read()
        cozulmus_veri = f.decrypt(sifreli_veri)
        return json.loads(cozulmus_veri.decode())
    except Exception:
        print("❌ Hatalı Master Şifre veya bozulmuş dosya!")
        return None

def sifreleri_kaydet(key, veri):
    f = Fernet(key)
    sifrelenmis_veri = f.encrypt(json.dumps(veri).encode())
    with open(DOSYA_ADI, "wb") as dosya:
        dosya.write(sifrelenmis_veri)

def ana_menu():
    print("=" * 50)
    print("🛡️ GÜVENLİ ŞİFRE YÖNETİCİSİ (BRUTE-FORCE DİRENÇLİ)")
    print("=" * 50)
    
    key = anahtar_olustur_veya_yukle()
    
    
    mevcut_veriler = sifreleri_oku(key)
    if mevcut_veriler is None:
        return

    while True:
        print("\n--- İŞLEM MENÜSÜ ---")
        print("1. Yeni Güvenli Şifre Üret ve Kaydet")
        print("2. Kayıtlı Şifreleri Listele")
        print("3. Çıkış ('q')")
        
        secim = input("Seçiminiz (1/2/3): ").lower()
        if secim == '3' or secim == 'q':
            print("Kasa kilitlendi. Güvenle kalın!")
            break
            
        elif secim == '1':
            site = input("Hangi site/uygulama için? (Örn: github.com): ")
            kadi = input("Kullanıcı adınız / E-postanız: ")
            
            try:
                uzunluk_input = input("Şifre uzunluğu kaç olsun? [Varsayılan: 16]: ")
                uzunluk = int(uzunluk_input) if uzunluk_input else 16
            except ValueError:
                uzunluk = 16
                
            kullanilacak_karakterler = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
            sifre = "".join(secrets.choice(kullanilacak_karakterler) for _ in range(uzunluk))
            
            puan, sure = sifre_analiz_et(sifre, len(kullanilacak_karakterler))
            
            print("\n" + "-" * 40)
            print(f"🔑 Üretilen Şifre     : {sifre}")
            print(f"📊 Güvenlik Puanı     : {puan} / 100")
            print(f"⏱️ Tahmini Kırılma Süresi: {sure}")
            print("-" * 40)
            
            kayit_onayi = input("Bu şifreyi kasaya kaydetmek istiyor musun? (e/h): ").lower()
            if kayit_onayi == 'e':
                mevcut_veriler[site] = {"kullanici_adi": kadi, "sifre": sifre}
                sifreleri_kaydet(key, mevcut_veriler)
                print("✅ Başarıyla şifrelenerek kasaya kaydedildi!")
                
        elif secim == '2':
            if not mevcut_veriler:
                print("📭 Kasanız henüz boş.")
            else:
                print("\n--- 📂 KASADAKİ GÜVENLİ KAYITLAR ---")
                for site, bilgiler in mevcut_veriler.items():
                    print(f"Site : {site}")
                    print(f"K.Adı: {bilgiler['kullanici_adi']}")
                    print(f"Şifre: {bilgiler['sifre']}")
                    print("-" * 30)
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    ana_menu()

import pandas as pd
import sqlite3


vt = sqlite3.connect("veritabani.db")
imlec = vt.cursor()
imlec.execute('''CREATE TABLE IF NOT EXISTS admin (kullanici_adi , sifre )''')
imlec.execute('''CREATE TABLE IF NOT EXISTS pilot (ad , soyad , lisans )''')
imlec.execute('''CREATE TABLE IF NOT EXISTS veri_tablosu (Şehir , Havalimanı , Kodadı )''')
imlec.execute('''CREATE TABLE IF NOT EXISTS ucak_bilgileri (ucak_kuyruk_numarasi , ucak_varis_yeri , ucak_yolcu_kapasitesi , havaalani_bekleme_suresi )''')
def admin_girisi():
    while True:
        print("1 - Kayıt Ol")
        print("2 - Giriş Yap")
        print("3 - Çıkış Yap")
        admin_secim = input("Seçiminizi yapın: ")

        if admin_secim == "1":
            kullanici_adi = input("Kullanıcı adınızı girin: ")
            sifre = input("Şifrenizi girin: ")
            imlec.execute("INSERT INTO admin VALUES (?, ?)", (kullanici_adi, sifre))
            vt.commit()
            print("Kayıt başarılı!")
        elif admin_secim == "2":
            kullanici_adi = input("Kullanıcı adınızı girin: ")
            sifre = input("Şifrenizi girin: ")
            imlec.execute("SELECT * FROM admin WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
            kullanici = imlec.fetchone()
            if kullanici:
                print("Giriş başarılı!")
                havaalani_verileri_girisi()
            else:
                print("Hatalı kullanıcı adı veya şifre!")
        elif admin_secim == "3":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz bir seçim yaptınız!")

def pilot_girisi():
    while True:
        print("Pilot İşlemleri")
        print("1 - Yeni Pilot Kaydı")
        print("2 - Pilot Giriş Ekranı")
        print("3 - Geri")
        pilot_secim = input("Seçiminizi yapın: ")

        if pilot_secim == "1":
            pilot_adi = input("Pilot adını girin: ")
            pilot_soyadi = input("Pilot soyadını girin: ")
            pilot_lisans = input("Pilot lisansını girin: ")
            imlec.execute("INSERT INTO pilot (ad, soyad, lisans) VALUES (?, ?, ?)", (pilot_adi, pilot_soyadi, pilot_lisans))
            vt.commit()
            print("Yeni pilot kaydı başarılı!")
        elif pilot_secim == "2":
            pilot_adi = input("Pilot adınızı girin: ")
            pilot_soyadi = input("Pilot soyadınızı girin: ")
            pilot_lisans = input("Pilot lisansınızı girin: ")
            imlec.execute("SELECT * FROM pilot WHERE ad=? AND soyad=? AND lisans=?", (pilot_adi, pilot_soyadi, pilot_lisans))
            pilot = imlec.fetchone()
            if pilot:
                print("Pilot girişi başarılı!")
                UcakBilgileri()
            else:
                print("Pilot bulunamadı veya bilgiler hatalı!")
        elif pilot_secim == "3":
            print("Geri dönülüyor...")
            break
        else:
            print("Geçersiz bir seçim yaptınız!")


def havaalani_verileri_girisi():

    havaalani_ucak_kapasitesi = []
    with open('dosya.csv', 'r', encoding='utf-8-sig') as csv_file:
        for line in csv_file:
            data = line.strip().split(';')
            havaalani_ucak_kapasitesi.append(data)    
    df = pd.DataFrame(havaalani_ucak_kapasitesi, columns=['Şehir', 'Havalimanı', 'Kodadı'])
    for index,row in df.iterrows():
        imlec.execute("INSERT INTO veri_tablosu (Şehir, Havalimanı, Kodadı) VALUES (?, ?, ?)",
                      (row['Şehir'], row['Havalimanı'], row['Kodadı'] ))
    
    imlec.execute("PRAGMA table_info(veri_tablosu)")
    columns = [column[1] for column in imlec.fetchall()]
    
    if 'Havalimanı Uçak Kapasitesi' not in columns:
        imlec.execute("ALTER TABLE veri_tablosu ADD COLUMN 'Havalimanı Uçak Kapasitesi' INTEGER")
    
    if 'Bekleyen Yolcu Sayısı' not in columns:
        imlec.execute("ALTER TABLE veri_tablosu ADD COLUMN 'Bekleyen Yolcu Sayısı' INTEGER")
    
    havalimani_adi = input("Havalimanı adını giriniz: ")
    ucak_kapasitesi = input("Havalimanı uçak kapasitesini giriniz: ")
    yolcu_sayisi = input("Bekleyen yolcu sayısını giriniz: ")
    
    imlec.execute("UPDATE veri_tablosu SET 'Havalimanı Uçak Kapasitesi' = ?, 'Bekleyen Yolcu Sayısı' = ? WHERE Havalimanı = ?", (ucak_kapasitesi, yolcu_sayisi, havalimani_adi))
    vt.commit()

def UcakBilgileri():
    ucak_kuyruk_numarasi = input("Uçak kuyruk numarasını girin: ")
    ucak_varis_yeri = input("İnmek istediğiniz havaalanını yazın: ")
    ucak_yolcu_kapasitesi = int(input("Uçak yolcu kapasitesini girin: "))
    havaalani_bekleme_suresi = int(input("Havaalanında kaç dakika kalacaksınız: "))
    imlec.execute("INSERT INTO ucak_bilgileri VALUES (?, ?, ?, ?)", (ucak_kuyruk_numarasi,ucak_varis_yeri,ucak_yolcu_kapasitesi, havaalani_bekleme_suresi))
    # Pilotun inmek istediği havalimanını kontrol et
    imlec.execute("SELECT * FROM veri_tablosu WHERE Havalimanı=?", (ucak_varis_yeri,))
    havalimani = imlec.fetchone()
    print(havalimani)
    if havalimani:
        # Havalimanı bulundu
        # Havalimanı uçak kapasitesini kontrol et
        if havalimani[3] > 0:
            # Uçak kapasitesi var
                # Havalimanı uçak kapasitesini güncelle
                imlec.execute("""UPDATE veri_tablosu SET 'Havalimanı Uçak Kapasitesi' = 'Havalimanı Uçak Kapasitesi' - 1 WHERE Havalimanı=?""", (ucak_varis_yeri,))
                vt.commit()
                # Bekleyen yolcu sayısını güncelle
                imlec.execute("UPDATE veri_tablosu SET 'Bekleyen Yolcu Sayısı' = 'Bekleyen Yolcu Sayısı' - ? WHERE Havalimanı=?", (ucak_yolcu_kapasitesi, ucak_varis_yeri))
                vt.commit()
                # Bekleyen yolcu sayısını kontrol et
                imlec.execute("SELECT * FROM veri_tablosu WHERE Havalimanı=?", (ucak_varis_yeri,))
                havalimani = imlec.fetchone()
                if havalimani[4] == 0:
                    # Bekleyen yolcu kalmadı
                    print("Bekleyen yolcu kalmadı!")

        else:
            # Uçak kapasitesi yok
            print("Bu havaalanına inemezsiniz. Başka bir havaalanı seçin.")
    else:
        # Havalimanı bulunamadı
        print("Hatalı bir havaalanı adı girdiniz. Lütfen tekrar deneyin.")

    
    vt.commit()
    vt.close()

def cikis():
    print("Çıkış yapılıyor...")





















"""class UcakBilgileri:
     def __init__(self):

         self.ucak_kuyruk_numarasi = ""
         self.ucak_varis_yeri = ""
         self.ucak_kapasitesi = 0
         self.havaalani_bekleme_suresi = 0
     def veri_al(self):
         self.ucak_kuyruk_numarasi = input("Uçak kuyruk numarasını girin: ")
         self.ucak_varis_yeri = input("İnmek istediğiniz havaalanını yazın: ")
         self.ucak_kapasitesi = int(input("Uçak kapasitesini girin: "))
         self.havaalani_bekleme_suresi = int(input("Havaalanında kaç dakika kalacaksınız: "))"""  
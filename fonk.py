import giris_ekrani

while True:
    print("1. Admin Girişi")
    print("2. Pilot Girişi")

    print("3. çıkıs")
    ana_menu_secimi = int(input("Lütfen bir işlem seçiniz: "))

    if ana_menu_secimi == 1:
        giris_ekrani.admin_girisi()

    elif ana_menu_secimi == 2:
        giris_ekrani.pilot_girisi()
       
    elif ana_menu_secimi == 3:    
        giris_ekrani.cikis()  
        break
    else:
        print("Geçersiz bir seçim yaptınız! ")



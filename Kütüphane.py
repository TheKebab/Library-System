import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3 as sql
baglanti = sql.connect("kutuphaneSistemi.db")
kalem = baglanti.cursor()
if baglanti:
    print("Bağlantı başarılı")

butonFont = QFont("Times",25)

def ustBolum(mevcutPencere):
    
    
    geriButon = QPushButton("<-",mevcutPencere)
    geriButon.setFont(butonFont)
    geriButon.setGeometry(1550, 20, 40, 40)
    
    geriButon.clicked.connect(mevcutPencere.close)
    
    
class YeniKitap(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Kitap Ekle")
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        baslik = QLabel("Yeni Kitap Ekle")
        baslik.setFont(butonFont)
        self.basarili = QLabel("Ekleme Başarılı...")
        self.basarili.hide()
        self.basarisiz = QLabel("Ekleme Başarısız...")
        self.basarisiz.hide()
        self.eklenecekKitapAdi=QLineEdit()
        self.eklenecekKitapAdi.setPlaceholderText("Kitap Adını Giriniz...")
        kaydet= QPushButton("Kitabı Ekle")
        kaydet.clicked.connect(self.kitapKaydet)
        
        dikey.addWidget(baslik)
        dikey.addWidget(self.eklenecekKitapAdi)
        dikey.addWidget(kaydet)
        dikey.addWidget(self.basarili)
        dikey.addWidget(self.basarisiz)
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    
    def kitapKaydet(self):
        
        isim = self.eklenecekKitapAdi.text()
        kalem.execute("INSERT INTO kitaplar (kitap_ad) VALUES (?)",(isim,))
        
        baglanti.commit()
        
        if baglanti:
            self.basarili.show()
        else:
            self.basarisiz.show()
            
class KitapSil(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Sil")
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        silBaslik = QLabel("Listeden Kitap Sil")
        silBaslik.setFont(butonFont)
        self.silmeBasarili = QLabel("Silme Başarılı...")
        self.silmeBasarisiz = QLabel("Silme Başarısız...")
        self.silmeBasarili.hide()
        self.silmeBasarisiz.hide()
        self.silinecekKitapAdi = QLineEdit()
        self.silinecekKitapAdi.setPlaceholderText("Kitap Adını Giriniz...")
        silmeButon=QPushButton("Kitabı Listeden Sil")
        silmeButon.clicked.connect(self.kitabiSil)
        dikey.addWidget(silBaslik)
        dikey.addWidget(self.silinecekKitapAdi)
        dikey.addWidget(silmeButon)
        dikey.addWidget(self.silmeBasarili)
        dikey.addWidget(self.silmeBasarisiz)
        
        
        
        
        
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    def kitabiSil(self):
        silinecekKitap = self.silinecekKitapAdi.text()
        kalem.execute("DELETE FROM kitaplar WHERE kitap_ad = ?",(silinecekKitap,))
        baglanti.commit()
        if baglanti:
            self.silmeBasarili.show()
        else:
            self.silmeBasarisiz.show()
            
class KitapListesi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Listesi")
        ustBolum(self)
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        baslik = QLabel("Kitap Listesi")
        baslik.setFont(butonFont)
        aciklama = QLabel("Müsaitlik durumunu görmek istediğiniz kitaba tıklayın")
        liste = QListWidget()
        kitapEkle = QPushButton("Yeni Kitap Ekle")
        kitapEkle.setFont(butonFont)
        kitapEkle.clicked.connect(self.yeniEkle)
        kitapSil = QPushButton("Kitap Sil")
        kitapSil.setFont(butonFont)
        kitapSil.clicked.connect(self.kitapSil)
        kitaplar = kalem.execute("SELECT * FROM kitaplar")
        for i in kitaplar.fetchall():
            liste.addItem(i[1])
        liste.itemClicked.connect(self.kitapBilgi)
            
        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addWidget(liste)
        dikey.addWidget(kitapEkle)
        dikey.addWidget(kitapSil)
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
        
    
    def kitapBilgi(self,item):
        kitapİsmi = item.text()
        kontrol = kalem.execute("SELECT * FROM kitaplar WHERE kitap_ad = ?",(kitapİsmi,))
        mevcutDurum = kontrol.fetchall()[0][2]
        if mevcutDurum ==0:
            kitapKimde= kalem.execute("SELECT * FROM odunc WHERE kitap_ad = ?",(kitapİsmi,))
            ogrenci = kitapKimde.fetchall()[0][1]
            QMessageBox.information(self,"Müsaitlik Durumu",kitapİsmi +" kitabı şuan "+ ogrenci + " isimli öğrencide")
        elif mevcutDurum == 1:
           
            QMessageBox.information(self,"Müsaitlik Durumu",kitapİsmi + " kitabı elimizde mevcut.")
    def yeniEkle(self):
        self.yeni = YeniKitap()
        
        self.yeni.show()
    
    def kitapSil(self):
        self.silici = KitapSil()
        self.silici.show()
        
class OgrenciEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Öğrenci Ekle")
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        self.eklenecekOgrenciAdi= QLineEdit()
        self.eklenecekOgrenciAdi.setPlaceholderText("Öğrenci Adı Giriniz")
        self.basarili = QLabel("Kayıt Başarılı...")
        self.basarili.hide()
        baslik = QLabel("Yeni Öğrenci Kayıt")
        baslik.setFont(butonFont)
        kayit = QPushButton("Kaydet")
        kayit.setFont(butonFont)
        kayit.clicked.connect(self.ogrenciKayit)
        dikey.addWidget(baslik)
        dikey.addWidget(self.eklenecekOgrenciAdi)
        
        dikey.addWidget(kayit)
        dikey.addWidget(self.basarili)
        
        
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    def ogrenciKayit(self):
        isim = self.eklenecekOgrenciAdi.text()
        
        kalem.execute("INSERT INTO ogrenci (ogrenci_ad) VALUES (?)",(isim,))
        self.basarili.show()
        baglanti.commit()

class OduncEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Ödünç İşlemi")
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        self.kaydetmeYazi = QLabel("Kaydetme Başarılı")
        self.kaydetmeYazi.hide()
        self.eklenecekOgrenciAdi= QLineEdit()
        self.eklenecekOgrenciAdi.setPlaceholderText("Öğrenci Adı Giriniz")
        self.eklenecekKitapAdi = QLineEdit()
        self.eklenecekKitapAdi.setPlaceholderText("Kitap Adı Giriniz")
        
        oduncKaydet = QPushButton("Kaydet")
        oduncKaydet.setFont(butonFont)
        oduncKaydet.clicked.connect(self.kaydet)
        
        
       
        
        dikey.addWidget(self.eklenecekOgrenciAdi)
        dikey.addWidget(self.eklenecekKitapAdi)
        
        dikey.addWidget(oduncKaydet)
        dikey.addWidget(self.kaydetmeYazi)
        
        
        
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    
    def kaydet(self):
        ogrenciIsim = self.eklenecekOgrenciAdi.text()
        kitapIsim = self.eklenecekKitapAdi.text()
        kitapKontrol = kalem.execute("SELECT * FROM kitaplar WHERE kitap_ad = (?)",(kitapIsim,))
        kitapUzunluk = kitapKontrol.fetchall()
        ogrenciKontrol = kalem.execute("SELECT * FROM ogrenci WHERE ogrenci_ad = ?",(ogrenciIsim,))
        ogrenciFetchKontrol = ogrenciKontrol.fetchall()
        
        if len(kitapUzunluk) == 0   :
            QMessageBox.information(self,"Kitap Mevcut Değil", kitapIsim + " isimli kitap mevcut değil")
            
            
        if kitapUzunluk[0][2] == 0:
            QMessageBox.information(self,"Kitap Müsait Değil", kitapIsim + " isimli kitap şimdilik başkasının elinde")
        if len(ogrenciFetchKontrol) == 0:
            QMessageBox.information(self, "Kayıtsız Öğrenci", ogrenciIsim + " adlı öğrenci sistemimizde kayıtlı değildir")
        else:
              kalem.execute("INSERT INTO odunc (ogrenci_ad,kitap_ad) VALUES (?,?)",(ogrenciIsim,kitapIsim,))
              kalem.execute("UPDATE kitaplar SET kitap_durum =0 WHERE kitap_ad = ?",(kitapIsim,))
              self.kaydetmeYazi.show()
            
        
       
        baglanti.commit()
    
class OduncSil(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ödünç İşlemi Sil")
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        self.silinecekOgrenciAdi= QLineEdit()
        self.silinecekOgrenciAdi.setPlaceholderText("Öğrenci Adı Giriniz")
        self.silinecekKitapAdi = QLineEdit()
        self.silinecekKitapAdi.setPlaceholderText("Kitap Adı Giriniz")
        sil = QPushButton("Kaydı Sil")
        sil.setFont(butonFont)
        sil.clicked.connect(self.silmeIslemi)
        self.silmeBasari = QLabel("İade İşlemi Başarılı")
        self.silmeBasari.hide()
        dikey.addWidget(self.silinecekOgrenciAdi)
        dikey.addWidget(self.silinecekKitapAdi)
        dikey.addWidget(sil)
        dikey.addWidget(self.silmeBasari)
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    def silmeIslemi(self):
        ogrenciIsim = self.silinecekOgrenciAdi.text()
        kitapIsim = self.silinecekKitapAdi.text()
        kontrol = kalem.execute("SELECT * FROM odunc WHERE ogrenci_ad = ? AND kitap_ad = ? ",(ogrenciIsim,kitapIsim,))
        silmeKontrol = kontrol.fetchall()
        
        
        
        if (len(silmeKontrol) ==0 )    :
            QMessageBox.information(self, "Hata ", " Hatalı Kitap Adı ve/veya Öğrenci Adı ")
        
        
        
            
        
        else:
            kalem.execute("DELETE FROM odunc WHERE ogrenci_ad = ? AND kitap_ad = ? ",(ogrenciIsim, kitapIsim,))
            kalem.execute("UPDATE kitaplar SET kitap_durum = 1 WHERE  kitap_ad = ?",(kitapIsim,))
            self.silmeBasari.show()
        baglanti.commit()
    
class OgrenciListesi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Öğrenci Listesi")
        
        ustBolum(self)
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        baslik = QLabel("Öğrenci Listesi")
        aciklama = QLabel("Kitap ödünç alıp almadığını görmek istediğiniz öğrencinin üstüne tıklayın")
        ogrenciEkle = QPushButton("Yeni Öğrenci Ekle")
        ogrenciEkle.setFont(butonFont)
        ogrenciEkle.clicked.connect(self.yeniOgrenciEkle)
        ogrenciListe = kalem.execute("SELECT * FROM ogrenci")
        liste = QListWidget()
        
        for i in ogrenciListe.fetchall():
            liste.addItem(i[1])
        liste.itemClicked.connect(self.ogrenciBilgileri)
            
        baslik.setFont(butonFont)
        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addWidget(liste)
        dikey.addWidget(ogrenciEkle)
        
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    
    def yeniOgrenciEkle(self):
        self.yeniOgrenci = OgrenciEkle()
        self.yeniOgrenci.show()
    
    def ogrenciBilgileri(self,item):
        ogrenciAdi = item.text()
        self.ogr = OgrenciBilgi(ogrenciAdi)
        self.ogr.show()
        
class OgrenciBilgi(QWidget):
    def __init__(self,ogrenciAdi):
        super().__init__()
        self.setWindowTitle("Öğrencinin Sahip Olduğu Kitaplar")
        self.setGeometry(100, 100, 250, 250)
        ustBolum(self)
        liste = QListWidget()
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        kontrol = kalem.execute("SELECT * FROM odunc WHERE ogrenci_ad = ?",(ogrenciAdi,))
        for i in kontrol.fetchall():
            eklenecekler = i[1] + " - " + i[2]
            liste.addItem(eklenecekler)
        
        dikey.addWidget(liste)
        yatay.addLayout(dikey)
        self.setLayout(yatay)
        
class OduncListesi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ödünç Listesi")
        
        ustBolum(self)
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        baslik = QLabel("Ödünç işlemleri")
        liste= QListWidget()
        oduncEkle = QPushButton("Yeni Ödünç Alma İşlemi")
        oduncEkle.setFont(butonFont)
        oduncEkle.clicked.connect(self.oduncKayit)
        
        
        iadeEkle = QPushButton("Yeni İade İşlemi")
        iadeEkle.setFont(butonFont)
        iadeEkle.clicked.connect(self.oduncSil)
        
        baslik.setFont(butonFont)
        oduncler = kalem.execute("SELECT * FROM odunc")
        for i in oduncler.fetchall():
            eklenecek = i[1] + " - " + i[2]
            liste.addItem(eklenecek)
        
        dikey.addWidget(baslik)
        dikey.addWidget(liste)
        dikey.addWidget(oduncEkle)
        dikey.addWidget(iadeEkle)
        
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
                     
    def oduncKayit(self):
        self.yeniOduncEkle = OduncEkle()
        self.yeniOduncEkle.show()
    
    def oduncSil(self):
        self.yeniOduncSil = OduncSil()
        self.yeniOduncSil.show()
        
class YardimSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Yardım ve Hakkında")
        ustBolum(self)
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        font = QFont("Times",15)
        baslik = QLabel("Yardım ve Hakkımızda")
        satir1= QLabel("Bu uygulama Ataman Kunbuk tarafından yazılmıştır.")
        satir2 = QLabel("Uygulamanın kullanımıyla ilgili rehber aşağıdadır:")
        satir3 = QLabel("Uygulamayı kullanabilmek için önce Kitap Listesi-> Yeni Kitap Ekle kısmından yeni kitap ekleyiniz.")
        satir4 = QLabel("Ardından Öğrenci Listesi -> Yeni Öğrenci Ekle kısmından yeni öğrenci ekleyiniz.")
        satir5 = QLabel("Bu ilk iki işlemi yapmadığınız takdirde programı kullanırken hata alacaksınız")
        satir6 = QLabel("Öğrenci Listesinde öğrencinin adının üzerine bir kez tıklayarak öğrencinin ödünç aldığı kitapları görebilirsiniz.")
        satir7 = QLabel("Kitap Listesinde kitap ismine tıklayarak o kitabın şuan kütüphane sisteminde mevcut olup olmadığını görebilirsiniz.")
        satir9 = QLabel("Uygulamanın işinize yaramasını temenni ederim.")
        
        satir1.setFont(font)
        satir2.setFont(font)
        satir3.setFont(font)
        satir4.setFont(font)
        satir5.setFont(font)
        satir6.setFont(font)
        satir7.setFont(font)
        satir9.setFont(font)
        
        baslik.setFont(butonFont)
        dikey.addWidget(baslik)
        dikey.addWidget(satir1)
        dikey.addWidget(satir2)
        dikey.addWidget(satir3)
        dikey.addWidget(satir4)
        dikey.addWidget(satir5)
        dikey.addWidget(satir6)
        dikey.addWidget(satir7)
        dikey.addWidget(satir9)
        
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
        
class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        
        kapatButon = QPushButton("X",self)
        kapatButon.setFont(butonFont)
        kapatButon.setGeometry(1600, 20, 40, 40)
        kapatButon.clicked.connect(self.kapat)
        
        self.setGeometry(250, 250, 500, 500)
        self.setWindowTitle("Kütüphane Sistemi")
        yazi = QLabel("Kütüphane Takip Sistemine Hoşgeldiniz...")
        yazi.setFont(butonFont)
        dugme1= QPushButton("Kitap Listesi")
        dugme1.setFont(butonFont)
        dugme1.clicked.connect(self.kitapAc)
        dugme2 = QPushButton("Öğrenci Listesi")
        dugme2.setFont(butonFont)
        dugme2.clicked.connect(self.ogrenciAc)
        dugme3 = QPushButton("Ödünç İşlemleri")
        dugme3.setFont(butonFont)
        dugme3.clicked.connect(self.oduncAc)
        yardim = QPushButton("Yardım - Hakkımızda")
        yardim.setFont(butonFont)
        yardim.clicked.connect(self.yardimAc)
        
        
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        
        dikey.addWidget(yazi)
        dikey.addStretch()
        dikey.addWidget(dugme1)
        dikey.addStretch()
        dikey.addWidget(dugme2)
        dikey.addStretch()
        dikey.addWidget(dugme3)
        dikey.addStretch()
        dikey.addWidget(yardim)
        dikey.addStretch()
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
        
        
        
        
        self.showMaximized()
    
    def kitapAc(self):
        self.kitap = KitapListesi()
        self.kitap.showMaximized()
    
    def kapat(self):
        qApp.closeAllWindows()
        qApp.quit()
    
    def ogrenciAc(self):
        self.ogrenci = OgrenciListesi()
        self.ogrenci.showMaximized()
    def oduncAc(self):
        self.odunc = OduncListesi()
        self.odunc.showMaximized()
    def yardimAc(self):
        self.yardimHakkinda = YardimSayfasi()
        self.yardimHakkinda.showMaximized()
    
    
        
    


        
       
        
       
        
       
        
       
        
       
        
       
        
       
        
       
        





uygulama = QApplication(sys.argv)
pencere1 = AnaPencere()
sys.exit(uygulama.exec_())
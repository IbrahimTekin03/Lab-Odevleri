import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('gemiler.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Gemiler (
                GemilerID INTEGER PRIMARY KEY AUTOINCREMENT,
                SeriNo TEXT,
                Ad TEXT,
                Agirlik REAL,
                YapimYili INTEGER,
                Tip TEXT,
                Kapasite REAL,
                Litre REAL,
                KonteynerSayisi INTEGER,
                MaxAgirlik REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Seferler (
                SeferID INTEGER PRIMARY KEY AUTOINCREMENT,
                GemiID INTEGER,
                KaptanID1 INTEGER,
                KaptanID2 INTEGER,
                MurettabatID INTEGER,
                YolaCikisTarihi TEXT,
                DonusTarihi TEXT,
                LimanID INTEGER,
                FOREIGN KEY(GemiID) REFERENCES Gemiler(GemilerID),
                FOREIGN KEY(KaptanID1) REFERENCES Kaptanlar(KaptanID),
                FOREIGN KEY(KaptanID2) REFERENCES Kaptanlar(KaptanID),
                FOREIGN KEY(MurettabatID) REFERENCES Murettabat(MurettabatID),
                FOREIGN KEY(LimanID) REFERENCES Limanlar(LimanID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Limanlar (
                LimanID INTEGER PRIMARY KEY AUTOINCREMENT,
                LimanAdi TEXT,
                Ulke TEXT,
                Nufus INTEGER,
                PasaportIstiyorMu TEXT,
                DemirlemeUcreti REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Kaptanlar (
                KaptanID INTEGER PRIMARY KEY AUTOINCREMENT,
                Ad TEXT,
                Soyad TEXT,
                Adres TEXT,
                Vatandaslik TEXT,
                DogumTarihi TEXT,
                IseGirisTarihi TEXT,
                Lisans TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Murettabat (
                MurettabatID INTEGER PRIMARY KEY AUTOINCREMENT,
                Ad TEXT,
                Soyad TEXT,
                Adres TEXT,
                Vatandaslik TEXT,
                DogumTarihi TEXT,
                IseGirisTarihi TEXT,
                Gorev TEXT)''')

class Gemiler:
    def __init__(self, seri_no, ad, agirlik, yapim_yili, tip, kapasite=None, max_agirlik=None, litre=None,
                 konteyner_sayisi=None):
        self.seri_no = seri_no
        self.ad = ad
        self.agirlik = agirlik
        self.yapim_yili = yapim_yili
        self.tip = tip
        self.kapasite = kapasite
        self.max_agirlik = max_agirlik
        self.litre = litre
        self.konteyner_sayisi = konteyner_sayisi

    def ekle(self):
        if self.tip == "Yolcu Gemisi":
            cursor.execute('''INSERT INTO Gemiler (SeriNo, Ad, Agirlik, YapimYili, Tip, Kapasite)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (self.seri_no, self.ad, self.agirlik, self.yapim_yili, self.tip, self.kapasite))
        elif self.tip == "Petrol Tankeri":
            cursor.execute('''INSERT INTO Gemiler (SeriNo, Ad, Agirlik, YapimYili, Tip, Litre)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (self.seri_no, self.ad, self.agirlik, self.yapim_yili, self.tip, self.litre))
        elif self.tip == "Konteyner Gemisi":
            cursor.execute('''INSERT INTO Gemiler (SeriNo, Ad, Agirlik, YapimYili, Tip, KonteynerSayisi, MaxAgirlik)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (self.seri_no, self.ad, self.agirlik, self.yapim_yili, self.tip, self.konteyner_sayisi,
                            self.max_agirlik))
        conn.commit()


class Seferler:
    def __init__(self, gemi_id, kaptan_id, kaptan_id2, murettabat_id, yola_cikis_tarihi, donus_tarihi, liman_id):
        self.gemi_id = gemi_id
        self.kaptan_id = kaptan_id
        self.kaptan_id2 = kaptan_id2
        self.murettabat_id = murettabat_id
        self.yola_cikis_tarihi = yola_cikis_tarihi
        self.donus_tarihi = donus_tarihi
        self.liman_id = liman_id

    def ekle(self):
        cursor.execute('''INSERT INTO Seferler (GemiID, KaptanID1,KaptanID2, MurettabatID, YolaCikisTarihi, DonusTarihi, LimanID)
                          VALUES (?, ?, ?,?, ?, ?, ?)''',
                       (self.gemi_id, self.kaptan_id, self.kaptan_id2, self.murettabat_id, self.yola_cikis_tarihi,
                        self.donus_tarihi, self.liman_id))
        conn.commit()

class Limanlar:
    def __init__(self, liman_adi, ulke, nufus, pasaport_istiyor_mu, demirleme_ucreti):
        self.liman_adi = liman_adi
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport_istiyor_mu = pasaport_istiyor_mu
        self.demirleme_ucreti = demirleme_ucreti

    def ekle(self):
        cursor.execute('''INSERT INTO Limanlar (LimanAdi, Ulke, Nufus, PasaportIstiyorMu, DemirlemeUcreti)
                          VALUES (?, ?, ?, ?, ?)''',
                       (self.liman_adi, self.ulke, self.nufus, self.pasaport_istiyor_mu, self.demirleme_ucreti))
        conn.commit()

        messagebox.showinfo("Başarılı", "Liman başarıyla eklendi.")


class Kaptanlar:
    def __init__(self, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans):
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.lisans = lisans

    def ekle(self):
        cursor.execute('''INSERT INTO Kaptanlar (Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IseGirisTarihi, Lisans)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (self.ad, self.soyad, self.adres, self.vatandaslik, self.dogum_tarihi, self.ise_giris_tarihi,
                        self.lisans))
        conn.commit()


class Murettabat:
    def __init__(self, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev):
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.gorev = gorev

    def ekle(self):
        cursor.execute('''INSERT INTO Murettabat (Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IseGirisTarihi, Gorev)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (self.ad, self.soyad, self.adres, self.vatandaslik, self.dogum_tarihi, self.ise_giris_tarihi,
                        self.gorev))
        conn.commit()

class SelectIslem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.button_veri_ekle=tk.Button(self,text="Veri Ekle", command=self.open_add_form)
        self.button_veri_ekle.pack()

        self.button_veri_sil=tk.Button(self,text="Veri Sil-Düzenle",command=self.open_del_form)
        self.button_veri_sil.pack()

    def open_del_form(self):
        form=DeleteEditForm()
        form.mainloop()

    def open_add_form(self):
        form=SelectForm()
        form.mainloop()



class SelectForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Veri Ekleme Formu")

        self.button_gemiler = tk.Button(self, text="Gemiler", command=self.open_gemiler_form)
        self.button_gemiler.pack()

        self.button_seferler = tk.Button(self, text="Seferler", command=self.open_seferler_form)
        self.button_seferler.pack()

        self.button_limanlar = tk.Button(self, text="Limanlar", command=self.open_limanlar_form)
        self.button_limanlar.pack()

        self.button_kaptanlar = tk.Button(self, text="Kaptanlar", command=self.open_kaptanlar_form)
        self.button_kaptanlar.pack()

        self.button_murettabat = tk.Button(self, text="Murettabat", command=self.open_murettabat_form)
        self.button_murettabat.pack()

    def open_gemiler_form(self):
        form = GemilerForm()
        form.mainloop()

    def open_seferler_form(self):
        form = SeferlerForm()
        form.mainloop()

    def open_limanlar_form(self):
        form = LimanlarForm()
        form.mainloop()

    def open_kaptanlar_form(self):
        form = KaptanlarForm()
        form.mainloop()

    def open_murettabat_form(self):
        form = MurettabatForm()
        form.mainloop()

    def open_delete_edit_form(self):
        form = DeleteEditForm()
        form.mainloop()


class GemilerForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Gemi Ekleme Formu")

        self.label_seri_no = tk.Label(self, text="Seri No:")
        self.label_seri_no.pack()
        self.entry_seri_no = tk.Entry(self)
        self.entry_seri_no.pack()

        self.label_ad = tk.Label(self, text="Ad:")
        self.label_ad.pack()
        self.entry_ad = tk.Entry(self)
        self.entry_ad.pack()

        self.label_agirlik = tk.Label(self, text="Ağırlık:")
        self.label_agirlik.pack()
        self.entry_agirlik = tk.Entry(self)
        self.entry_agirlik.pack()

        self.label_yapim_yili = tk.Label(self, text="Yapım Yılı:")
        self.label_yapim_yili.pack()
        self.entry_yapim_yili = tk.Entry(self)
        self.entry_yapim_yili.pack()

        self.label_tip = tk.Label(self, text="Tip:")
        self.label_tip.pack()
        self.tip_options = ["Yolcu Gemisi", "Petrol Tankeri", "Konteyner Gemisi"]
        self.selected_tip = tk.StringVar(self)
        self.selected_tip.set(self.tip_options[0])
        self.tip_menu = tk.OptionMenu(self, self.selected_tip, *self.tip_options, command=self.show_capacity_entry)
        self.tip_menu.pack()

        self.capacity_frame = tk.Frame(self)

        self.label_capacity = tk.Label(self.capacity_frame, text="Kapasite:")
        self.label_capacity.pack()
        self.entry_capacity = tk.Entry(self.capacity_frame)
        self.entry_capacity.pack()

        self.label_max_agirlik = tk.Label(self.capacity_frame, text="Maksimum Ağırlık:")
        self.entry_max_agirlik = tk.Entry(self.capacity_frame)

        self.capacity_frame.pack()

        self.button_ekle = tk.Button(self, text="Ekle", command=self.gemi_ekle)
        self.button_ekle.pack(side="top")

    def show_capacity_entry(self, selected_tip):

        self.label_capacity.pack_forget()
        self.entry_capacity.pack_forget()
        self.label_max_agirlik.pack_forget()
        self.entry_max_agirlik.pack_forget()

        if selected_tip == "Yolcu Gemisi":
            self.label_capacity.config(text="Yolcu Kapasitesi:")
            self.label_capacity.pack()
            self.entry_capacity.pack()
        elif selected_tip == "Petrol Tankeri":
            self.label_capacity.config(text="Petrol Kapasitesi (Litre):")
            self.label_capacity.pack()
            self.entry_capacity.pack()
        elif selected_tip == "Konteyner Gemisi":
            self.label_capacity.config(text="Konteyner Sayısı:")
            self.label_capacity.pack()
            self.entry_capacity.pack()
            self.label_max_agirlik.pack()
            self.entry_max_agirlik.pack()

    def gemi_ekle(self):
        try:
            seri_no = self.entry_seri_no.get()
            ad = self.entry_ad.get()
            agirlik = float(self.entry_agirlik.get())
            yapim_yili = int(self.entry_yapim_yili.get())
            tip = self.selected_tip.get()
            kapasite = float(self.entry_capacity.get())
            max_agirlik = float(
                self.entry_max_agirlik.get()) if tip == "Konteyner Gemisi" else None

            gemi = Gemiler(seri_no, ad, agirlik, yapim_yili, tip, kapasite,
                           max_agirlik)
            gemi.ekle()

            messagebox.showinfo("Başarılı", "Gemi başarıyla eklendi.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Gemi eklenirken bir hata oluştu: {str(e)}")


class SeferlerForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Sefer Ekleme Formu")

        self.label_gemi_seri_no = tk.Label(self, text="Gemi Seri No:")
        self.label_gemi_seri_no.pack()

        gemiler = cursor.execute("SELECT SeriNo, GemilerID FROM Gemiler").fetchall()
        self.gemi_options = {seri_no: gemi_id for seri_no, gemi_id in gemiler}
        self.selected_gemi_seri_no = tk.StringVar(self)
        self.selected_gemi_seri_no.set(gemiler[0][0])
        self.gemi_seri_menu = tk.OptionMenu(self, self.selected_gemi_seri_no, *self.gemi_options.keys())
        self.gemi_seri_menu.pack()

        self.label_kaptan_ad = tk.Label(self, text="Kaptan Adı:")
        self.label_kaptan_ad.pack()
        kaptanlar = cursor.execute("SELECT Ad, Soyad FROM Kaptanlar").fetchall()
        self.kaptan_options = {f"{ad} {soyad}": (ad, soyad) for ad, soyad in kaptanlar}
        self.selected_kaptan = tk.StringVar(self)
        self.selected_kaptan.set(list(self.kaptan_options.keys())[0])
        self.kaptan_menu = tk.OptionMenu(self, self.selected_kaptan, *self.kaptan_options.keys())
        self.kaptan_menu.pack()

        self.label_kaptan_ad2 = tk.Label(self, text="İkinci Kaptan Adı:")
        self.label_kaptan_ad2.pack()
        self.selected_kaptan2 = tk.StringVar(self)
        self.selected_kaptan2.set(list(self.kaptan_options.keys())[0])
        self.kaptan_menu2 = tk.OptionMenu(self, self.selected_kaptan2, *self.kaptan_options.keys())
        self.kaptan_menu2.pack()

        self.label_murettabat_ad = tk.Label(self, text="Mürettebat Adı:")
        self.label_murettabat_ad.pack()

        murettabatlar = cursor.execute("SELECT Ad, Soyad FROM Murettabat").fetchall()
        self.murettabat_options = {f"{ad} {soyad}": (ad, soyad) for ad, soyad in murettabatlar}
        self.selected_murettabat = tk.StringVar(self)
        self.selected_murettabat.set(
            list(self.murettabat_options.keys())[0])
        self.murettabat_menu = tk.OptionMenu(self, self.selected_murettabat, *self.murettabat_options.keys())
        self.murettabat_menu.pack()

        self.label_yola_cikis_tarihi = tk.Label(self, text="Yola Çıkış Tarihi:")
        self.label_yola_cikis_tarihi.pack()
        self.entry_yola_cikis_tarihi = tk.Entry(self)
        self.entry_yola_cikis_tarihi.pack()

        self.label_donus_tarihi = tk.Label(self, text="Dönüş Tarihi:")
        self.label_donus_tarihi.pack()
        self.entry_donus_tarihi = tk.Entry(self)
        self.entry_donus_tarihi.pack()

        self.label_liman = tk.Label(self, text="Yola Çıkış Limanı:")
        self.label_liman.pack()

        limanlar = cursor.execute("SELECT LimanAdi FROM Limanlar").fetchall()
        self.liman_options = [liman_adi[0] for liman_adi in limanlar]
        self.selected_liman = tk.StringVar(self)
        self.selected_liman.set(self.liman_options[0])
        self.liman_menu = tk.OptionMenu(self, self.selected_liman, *self.liman_options)
        self.liman_menu.pack()

        self.button_ekle = tk.Button(self, text="Ekle", command=self.sefer_ekle)
        self.button_ekle.pack()

    def sefer_ekle(self):
        gemi_seri_no = self.selected_gemi_seri_no.get()
        kaptan_ad, kaptan_soyad = self.kaptan_options[self.selected_kaptan.get()]
        kaptan_ad2, kaptan_soyad2 = self.kaptan_options[self.selected_kaptan2.get()]
        murettabat_ad, murettabat_soyad = self.murettabat_options[self.selected_murettabat.get()]
        yola_cikis_tarihi = self.entry_yola_cikis_tarihi.get()
        donus_tarihi = self.entry_donus_tarihi.get()
        liman = self.selected_liman.get()
        seferler = cursor.execute(
            "SELECT * FROM Seferler WHERE (KaptanID1=? OR KaptanID2=?) AND (YolaCikisTarihi <= ? AND DonusTarihi >= ?)",
            (kaptan_ad, kaptan_ad2, donus_tarihi, yola_cikis_tarihi)).fetchall()
        if seferler:
            messagebox.showerror("Hata",
                                 "Seçilen kaptanlardan en az biri belirtilen tarih aralığında başka bir sefere atanmış.")
            return

        sefer = Seferler(gemi_seri_no, kaptan_ad, kaptan_ad2, murettabat_ad, yola_cikis_tarihi, donus_tarihi, liman)
        sefer.ekle()
        messagebox.showinfo("Başarılı", "Sefer başarıyla eklendi.")
        self.destroy()

    def validate_sefer(self, gemi_seri_no, kaptan_ad, murettabat_ad):

        gemi_exists = cursor.execute("SELECT * FROM Gemiler WHERE SeriNo=?", (gemi_seri_no,)).fetchone() is not None
        kaptan_exists = cursor.execute("SELECT * FROM Kaptanlar WHERE Ad=? AND Soyad=?",
                                       kaptan_ad.split()).fetchone() is not None
        murettabat_exists = cursor.execute("SELECT * FROM Murettabat WHERE Ad=? AND Soyad=?",
                                           murettabat_ad.split()).fetchone() is not None

        kaptan_count = cursor.execute("SELECT COUNT(*) FROM Kaptanlar").fetchone()[0]
        murettabat_count = cursor.execute("SELECT COUNT(*) FROM Murettabat").fetchone()[0]

        if not (gemi_exists and kaptan_exists and murettabat_exists):
            messagebox.showerror("Hata", "Geçersiz gemi, kaptan veya mürettebat bilgisi.")
            return False
        elif kaptan_count < 2 or murettabat_count < 1:
            messagebox.showerror("Hata", "En az 2 kaptan ve 1 mürettebat olmalıdır.")
            return False
        else:
            return True


class LimanlarForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Liman Ekleme Formu")

        self.label_liman_adi = tk.Label(self, text="Liman Adı:")
        self.label_liman_adi.pack()
        self.entry_liman_adi = tk.Entry(self)
        self.entry_liman_adi.pack()

        self.label_ulke = tk.Label(self, text="Ülke:")
        self.label_ulke.pack()
        self.entry_ulke = tk.Entry(self)
        self.entry_ulke.pack()

        self.label_nufus = tk.Label(self, text="Nüfus:")
        self.label_nufus.pack()
        self.entry_nufus = tk.Entry(self)
        self.entry_nufus.pack()

        self.label_pasaport_istiyor_mu = tk.Label(self, text="Pasaport İstiyor mu:")
        self.label_pasaport_istiyor_mu.pack()
        self.entry_pasaport_istiyor_mu = tk.Entry(self)
        self.entry_pasaport_istiyor_mu.pack()

        self.label_demirleme_ucreti = tk.Label(self, text="Demirleme Ücreti:")
        self.label_demirleme_ucreti.pack()
        self.entry_demirleme_ucreti = tk.Entry(self)
        self.entry_demirleme_ucreti.pack()

        self.button_ekle = tk.Button(self, text="Ekle", command=self.liman_ekle)
        self.button_ekle.pack()

    def liman_ekle(self):
        liman_adi = self.entry_liman_adi.get()
        ulke = self.entry_ulke.get()
        nufus = int(self.entry_nufus.get())
        pasaport_istiyor_mu = self.entry_pasaport_istiyor_mu.get()
        demirleme_ucreti = float(self.entry_demirleme_ucreti.get())

        limanlar = cursor.execute("SELECT * FROM Limanlar WHERE LimanAdi=? AND Ulke=?", (liman_adi, ulke)).fetchall()
        if limanlar:
            messagebox.showerror("Hata", "Bu liman zaten mevcut.")
            return

        liman = Limanlar(liman_adi, ulke, nufus, pasaport_istiyor_mu, demirleme_ucreti)
        liman.ekle()


class KaptanlarForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kaptan Ekleme Formu")

        self.label_ad = tk.Label(self, text="Ad:")
        self.label_ad.pack()
        self.entry_ad = tk.Entry(self)
        self.entry_ad.pack()

        self.label_soyad = tk.Label(self, text="Soyad:")
        self.label_soyad.pack()
        self.entry_soyad = tk.Entry(self)
        self.entry_soyad.pack()

        self.label_adres = tk.Label(self, text="Adres:")
        self.label_adres.pack()
        self.entry_adres = tk.Entry(self)
        self.entry_adres.pack()

        self.label_vatandaslik = tk.Label(self, text="Vatandaşlık:")
        self.label_vatandaslik.pack()
        self.entry_vatandaslik = tk.Entry(self)
        self.entry_vatandaslik.pack()

        self.label_dogum_tarihi = tk.Label(self, text="Doğum Tarihi:")
        self.label_dogum_tarihi.pack()
        self.entry_dogum_tarihi = tk.Entry(self)
        self.entry_dogum_tarihi.pack()

        self.label_ise_giris_tarihi = tk.Label(self, text="İşe Giriş Tarihi:")
        self.label_ise_giris_tarihi.pack()
        self.entry_ise_giris_tarihi = tk.Entry(self)
        self.entry_ise_giris_tarihi.pack()

        self.label_lisans = tk.Label(self, text="Lisans:")
        self.label_lisans.pack()
        self.entry_lisans = tk.Entry(self)
        self.entry_lisans.pack()

        self.button_ekle = tk.Button(self, text="Ekle", command=self.kaptan_ekle)
        self.button_ekle.pack()

    def kaptan_ekle(self):
        ad = self.entry_ad.get()
        soyad = self.entry_soyad.get()
        adres = self.entry_adres.get()
        vatandaslik = self.entry_vatandaslik.get()
        dogum_tarihi = self.entry_dogum_tarihi.get()
        ise_giris_tarihi = self.entry_ise_giris_tarihi.get()
        lisans = self.entry_lisans.get()

        kaptan = Kaptanlar(ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans)
        kaptan.ekle()

        messagebox.showinfo("Başarılı", "Kaptan başarıyla eklendi.")
        self.destroy()


class MurettabatForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Mürettebat Ekleme Formu")

        self.label_ad = tk.Label(self, text="Ad:")
        self.label_ad.pack()
        self.entry_ad = tk.Entry(self)
        self.entry_ad.pack()

        self.label_soyad = tk.Label(self, text="Soyad:")
        self.label_soyad.pack()
        self.entry_soyad = tk.Entry(self)
        self.entry_soyad.pack()

        self.label_adres = tk.Label(self, text="Adres:")
        self.label_adres.pack()
        self.entry_adres = tk.Entry(self)
        self.entry_adres.pack()

        self.label_vatandaslik = tk.Label(self, text="Vatandaşlık:")
        self.label_vatandaslik.pack()
        self.entry_vatandaslik = tk.Entry(self)
        self.entry_vatandaslik.pack()

        self.label_dogum_tarihi = tk.Label(self, text="Doğum Tarihi:")
        self.label_dogum_tarihi.pack()
        self.entry_dogum_tarihi = tk.Entry(self)
        self.entry_dogum_tarihi.pack()

        self.label_ise_giris_tarihi = tk.Label(self, text="İşe Giriş Tarihi:")
        self.label_ise_giris_tarihi.pack()
        self.entry_ise_giris_tarihi = tk.Entry(self)
        self.entry_ise_giris_tarihi.pack()

        self.label_gorev = tk.Label(self, text="Görev:")
        self.label_gorev.pack()
        self.entry_gorev = tk.Entry(self)
        self.entry_gorev.pack()

        self.button_ekle = tk.Button(self, text="Ekle", command=self.murettabat_ekle)
        self.button_ekle.pack()

    def murettabat_ekle(self):
        ad = self.entry_ad.get()
        soyad = self.entry_soyad.get()
        adres = self.entry_adres.get()
        vatandaslik = self.entry_vatandaslik.get()
        dogum_tarihi = self.entry_dogum_tarihi.get()
        ise_giris_tarihi = self.entry_ise_giris_tarihi.get()
        gorev = self.entry_gorev.get()

        murettabat = Murettabat(ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev)
        murettabat.ekle()

        messagebox.showinfo("Başarılı", "Mürettebat başarıyla eklendi.")
        self.destroy()


class DeleteEditForm(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Veri Silme ve Düzenleme Formu")

        self.label_table = tk.Label(self, text="Tablo Seç:")
        self.label_table.pack()
        self.table_options = ["Gemiler", "Seferler", "Limanlar", "Kaptanlar", "Murettabat"]
        self.selected_table = tk.StringVar(self)
        self.selected_table.set(self.table_options[0])
        self.table_menu = tk.OptionMenu(self, self.selected_table, *self.table_options)
        self.table_menu.pack()

        self.label_action = tk.Label(self, text="İşlem Seç:")
        self.label_action.pack()
        self.action_options = ["Sil", "Düzenle"]
        self.selected_action = tk.StringVar(self)
        self.selected_action.set(self.action_options[0])
        self.action_menu = tk.OptionMenu(self, self.selected_action, *self.action_options)
        self.action_menu.pack()

        self.button_select = tk.Button(self, text="Seç", command=self.select_action)
        self.button_select.pack()

    def select_action(self):
        selected_table = self.selected_table.get()
        selected_action = self.selected_action.get()
        form = None

        if selected_action == "Sil":
            form = DeleteForm(selected_table)
        elif selected_action == "Düzenle":
            form = EditForm(selected_table)

        if form:
            form.mainloop()


class DeleteForm(tk.Toplevel):
    def __init__(self, table):
        super().__init__()
        self.title(f"{table} Silme Formu")

        self.label_id = tk.Label(self, text=f"{table} ID:")
        self.label_id.pack()
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.button_delete = tk.Button(self, text="Sil", command=lambda: self.delete_record(table))
        self.button_delete.pack()

    def delete_record(self, table):
        record_id = self.entry_id.get()
        confirm = messagebox.askyesno("Emin misiniz?", "Bu kaydı silmek istediğinizden emin misiniz?")
        if confirm:
            if table == "Gemiler":
                cursor.execute(f"DELETE FROM {table} WHERE GemiID=?", (record_id,))
            elif table == "Seferler":
                cursor.execute(f"DELETE FROM {table} WHERE SeferID=?", (record_id,))
            elif table == "Limanlar":
                cursor.execute(f"DELETE FROM {table} WHERE LimanID=?", (record_id,))
            elif table == "Kaptanlar":
                cursor.execute(f"DELETE FROM {table} WHERE KaptanID=?", (record_id,))
            elif table == "Murettabat":
                cursor.execute(f"DELETE FROM {table} WHERE MurettabatID=?", (record_id,))

            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla silindi.")
            self.destroy()


class EditForm(tk.Toplevel):
    def __init__(self, table):
        super().__init__()
        self.title(f"{table} Düzenleme Formu")

        self.label_id = tk.Label(self, text=f"{table} ID:")
        self.label_id.pack()
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.label_field = tk.Label(self, text="Düzenlenecek Alan:")
        self.label_field.pack()
        self.entry_field = tk.Entry(self)
        self.entry_field.pack()

        self.label_new_value = tk.Label(self, text="Yeni Değer:")
        self.label_new_value.pack()
        self.entry_new_value = tk.Entry(self)
        self.entry_new_value.pack()

        self.button_edit = tk.Button(self, text="Düzenle", command=lambda: self.edit_record(table))
        self.button_edit.pack()

    def edit_record(self, table):
        record_id = self.entry_id.get()
        field = self.entry_field.get()
        new_value = self.entry_new_value.get()

        confirm = messagebox.askyesno("Emin misiniz?", "Bu kaydı düzenlemek istediğinizden emin misiniz?")
        if confirm:
            if table == "Gemiler":
                cursor.execute(f"UPDATE {table} SET {field}=? WHERE GemiID=?", (new_value, record_id))
            elif table == "Seferler":
                cursor.execute(f"UPDATE {table} SET {field}=? WHERE SeferID=?", (new_value, record_id))
            elif table == "Limanlar":
                cursor.execute(f"UPDATE {table} SET {field}=? WHERE LimanID=?", (new_value, record_id))
            elif table == "Kaptanlar":
                cursor.execute(f"UPDATE {table} SET {field}=? WHERE KaptanID=?", (new_value, record_id))
            elif table == "Murettabat":
                cursor.execute(f"UPDATE {table} SET {field}=? WHERE MurettabatID=?", (new_value, record_id))

            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla güncellendi.")
            self.destroy()


if __name__ == "__main__":
    app = SelectIslem()
    app.mainloop()

conn.commit()
conn.close()

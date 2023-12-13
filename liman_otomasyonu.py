import csv


class TIR:
    def __init__(self, plaka, tonaj, ulke):
        self.plaka = plaka
        self.tonaj = tonaj
        self.ulke = ulke

    def __str__(self):
        return f"TIR - Plaka: {self.plaka}, Tonaj: {self.tonaj}, Ülke: {self.ulke}"


class Gemi:
    def __init__(self, gemi_numarasi, kapasite, gidecek_ulke):
        self.gemi_numarasi = gemi_numarasi
        self.kapasite = kapasite
        self.yuk_bilgisi = []
        self.gidecek_ulke = gidecek_ulke

    def __str__(self):
        return f"Gemi - Numara: {self.gemi_numarasi}, Kapasite: {self.kapasite}, Gidecek Ülke: {self.gidecek_ulke}"


class Liman:
    def __init__(self):
        self.istif_alani = [0, 750]
        self.gemiler = {}
        self.tirlar = {}

    def tir_indir(self, t):
        if t in self.tirlar:
            sorted_tirler = sorted(self.tirlar[t], key=lambda tir: tir.plaka[-3:])
            for tir in sorted_tirler:
                if tir.tonaj == 20 and self.istif_alani[0] < 750:
                    self.istif_alani[0] += 20
                    print(f"{t} - {tir} yükü indirildi. İstif Alanı: {self.istif_alani}")
                if tir.tonaj == 30 and self.istif_alani[0] < 750:
                    self.istif_alani[0] += 30
                    print(f"{t} - {tir} yükü indirildi. İstif Alanı: {self.istif_alani}")
                if self.istif_alani[0] == 750:
                    print("İstif alanı doldu!")
                elif self.istif_alani[0] == 0:
                    print("İstif alanı boşaldı!")



    def gemilere_yukle(self, t):
        if self.istif_alani[0] > 0:
            for gemi in sorted(self.gemiler.values(), key=lambda g: g.gemi_numarasi):
                kapasite_yuzdesi = sum(yuk['miktar'] for yuk in gemi.yuk_bilgisi) / gemi.kapasite

                if self.istif_alani[0] > 0:
                    kalan_kapasite = gemi.kapasite - sum(yuk['miktar'] for yuk in gemi.yuk_bilgisi)

                    yuk_miktari = min(self.istif_alani[0], kalan_kapasite)

                    parca_tonaj = min(yuk_miktari, gemi.kapasite * 0.95)

                    if kapasite_yuzdesi + parca_tonaj / gemi.kapasite > 1:
                        if parca_tonaj > 0:
                            print(f"{t} - {gemi} kapasitesi aşıldığı için son yük geri indirildi.")
                            self.istif_alani[0] += parca_tonaj
                            break

                    if parca_tonaj > 0:
                        yuk_ulke = self.tirlar[t][0].ulke
                        if yuk_ulke == gemi.gidecek_ulke:
                            gemi.yuk_bilgisi.append({'miktar': parca_tonaj, 'ulke': yuk_ulke})
                            self.istif_alani[0] -= parca_tonaj
                            print(f"{t} - {gemi} 'a doğru yola çıkıyor! İstif Alanı: {self.istif_alani}")
                            break
                        else:
                            print(f"{t} - {gemi} Gemi dolmadığı için limanda bekliyor.")
                            break

    def limani_calistir(self):
        for t in sorted(self.tirlar.keys()):
            print(f"\nGeliş Zamanı: {t}")
            self.tir_indir(t)
            self.gemilere_yukle(t)


def main():
    liman = Liman()

    with open("olaylar.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            g_zaman = int(row[0])
            plaka = row[1]
            tonaj = int(row[5])
            ulke = row[2]
            tir = TIR(plaka, tonaj, ulke)
            if g_zaman not in liman.tirlar:
                liman.tirlar[g_zaman] = []
            liman.tirlar[g_zaman].append(tir)

    with open("gemiler.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            gemi_numarasi = row[1]
            kapasite = int(row[2])
            gidecek_ulke = row[3]
            gemi = Gemi(gemi_numarasi, kapasite, gidecek_ulke)
            liman.gemiler[gemi_numarasi] = gemi

    liman.limani_calistir()


if __name__ == "__main__":
    main()

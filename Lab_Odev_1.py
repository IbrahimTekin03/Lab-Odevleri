print("Hoşgeldiniz")
print("Bu Program 10 Farklı Seçeneğe Sahip Bir Konsol Menüsüdür")
print("Her Seçenek Farklı Bir Fonksiyon Gerçekleştirmektedir")
print("1. k'nıncı En Küçük Elemanı Bulma\n2. En Yakın Çifti Bulma\n3. Bir Listenin Tekrar Eden Elemanlarını Bulma\n4. Matris Çarpımı\n5. Bir Text Dosyasındaki Kelimelerin frekansını Bulma\n6. Liste İçinde En Küçük Değeri Bulma\n7. Karekök Fonksiyonu\n8. En Büyük Ortak Bölen\n9. Asallık Testi\n10. Daha Hızlı Fibonacci Hesabı")

soru_no = int(input("Kaç Numaraya Gitmek İstiyorsunuz: "))

if soru_no == 1:
    def k_kucuk(k, liste):
        if k <= 0 or k > len(liste):
            return "Değer Hatası!"

        sirali_liste = sorted(liste)
        k_kucuk_eleman = sirali_liste[k - 1]

        return k_kucuk_eleman


    k = int(input("K değerini girin: "))

    liste = input("Liste elemanlarını virgülle ayırarak girin: ")
    liste = [int(x) for x in liste.split(",")]

    k_kucuk_sonuc = k_kucuk(k, liste)
    print(f"{k}. en küçük eleman: {k_kucuk_sonuc}")

    pass
elif soru_no == 2:
    def en_yakin_cift():
        try:
            hedef_sayi = int(input("Hedef sayıyı girin: "))
            liste = [int(x) for x in input("Bir liste girin (sayıları boşluklarla ayırın): ").split()]

            if len(liste) < 2:
                print("Listede en az iki sayı olmalıdır.")
                return

            en_yakin_cift = (liste[0], liste[1])
            en_kucuk_fark = abs(en_yakin_cift[0] + en_yakin_cift[1] - hedef_sayi)

            for i in range(len(liste)):
                for j in range(i + 1, len(liste)):
                    toplam = liste[i] + liste[j]
                    fark = abs(toplam - hedef_sayi)
                    if fark < en_kucuk_fark:
                        en_kucuk_fark = fark
                        en_yakin_cift = (liste[i], liste[j])

            print(f"En yakın çift: {en_yakin_cift[0]} ve {en_yakin_cift[1]}")

        except ValueError:
            print("Geçersiz giriş! Lütfen sayıları doğru bir şekilde girin.")


    en_yakin_cift()
    pass
elif soru_no == 3:
    def tekrar_eden_elemanlar(liste):
        tekrarlar = [x for x in liste if liste.count(x) > 1]
        return list(set(tekrarlar))


    liste = input("Liste elemanlarını virgülle ayırarak girin: ")
    liste = [int(x) for x in liste.split(",")]

    tekrar_eden_elemanlar_sonuc = tekrar_eden_elemanlar(liste)
    print("Tekrar eden elemanlar:", tekrar_eden_elemanlar_sonuc)

    pass
elif soru_no == 4:
    def matris_carpimi_veya_zip(matris1, matris2):
        try:

            if all(isinstance(ele, (int, float)) for satir in matris1 for ele in satir) and all(
                    isinstance(ele, (int, float)) for satir in matris2 for ele in satir):
                satir1, sutun1 = len(matris1), len(matris1[0])
                satir2, sutun2 = len(matris2), len(matris2[0])
                if sutun1 != satir2:
                    print(
                        "Matris boyutları uyumsuz. İlk matrisin sütun sayısı ikinci matrisin satır sayısına eşit olmalıdır.")
                    return

                sonuc = [[sum(matris1[i][k] * matris2[k][j] for k in range(sutun1)) for j in range(sutun2)] for i in
                         range(satir1)]
            else:

                zip1 = zip(matris1, matris2)
                sonuc = list(zip1)

            for satir in sonuc:
                print(satir)

        except (ValueError, TypeError, IndexError):
            print("Geçersiz giriş! Lütfen matrisleri doğru bir şekilde girin.")


    A = []
    satir1 = int(input("Matris A'nın satır sayısını girin: "))
    sutun1 = int(input("Matris A'nın sütun sayısını girin: "))
    for i in range(satir1):
        satir = [float(x) for x in input(f"Matris A, {i + 1}. satırı girin (sayıları boşluklarla ayırın): ").split()]
        if len(satir) != sutun1:
            print("Hatalı giriş! Her satırın aynı sayıda elemana sahip olması gerekir.")
            exit()
        A.append(satir)

    B = []
    satir2 = int(input("Matris B'nin satır sayısını girin: "))
    sutun2 = int(input("Matris B'nin sütun sayısını girin: "))
    for i in range(satir2):
        satir = [float(x) for x in input(f"Matris B, {i + 1}. satırı girin (sayıları boşluklarla ayırın): ").split()]
        if len(satir) != sutun2:
            print("Hatalı giriş! Her satırın aynı sayıda elemana sahip olması gerekir.")
            exit()
        B.append(satir)

    matris_carpimi_veya_zip(A, B)
    pass
elif soru_no == 5:
    from functools import reduce


    def kelime_frekansi(dosya_yolu):
        with open(dosya_yolu, 'r') as dosya:
            metin = dosya.read()
            kelimeler = metin.split()

            def kelimeleri_ayir(kelime):
                return kelime

            def frekanslar(frekanslar, kelime):
                if kelime in frekanslar:
                    frekanslar[kelime] += 1
                else:
                    frekanslar[kelime] = 1
                return frekanslar

            frekanslar = reduce(frekanslar, map(kelimeleri_ayir, kelimeler), {})
            return frekanslar


    dosya_yolu = input("Dosya yolunu girin: ")

    frekanslar = kelime_frekansi(dosya_yolu)
    print(frekanslar)

    pass
elif soru_no == 6:
    def en_kucuk_deger(liste):
        if len(liste) == 1:
            return liste[0]
        else:
            min_geriye_kalan = en_kucuk_deger(liste[1:])
            return min(liste[0], min_geriye_kalan)

    liste = [int(x) for x in input("Bir liste girin (sayıları boşluklarla ayırın): ").split()]


    en_kucuk = en_kucuk_deger(liste)


    print(f"Listenin en küçük değeri: {en_kucuk}")
    pass
elif soru_no == 7:
    def karekok(N, x0, tol=1e-10, maxiter=10, iterasyon=0):
        iterasyon += 1
        x1 = 0.5 * (x0 + N / x0)

        hata = abs(x1 ** 2 - N)

        if hata < tol or iterasyon >= maxiter:
            if iterasyon >= maxiter:
                print(f"{maxiter} iterasyonda sonuca ulaşılamadı. Maximum iterasyon sayısına ulaşıldı.")
            return x1

        return karekok(N, x1, tol, maxiter, iterasyon)


    N = int(input("N değerini girin: "))
    x0 = float(input("x0 değerini girin: "))

    sonuc = karekok(N, x0)
    print(sonuc)

    pass
elif soru_no == 8:
    def eb_ortak_bolen(a, b):
        if b == 0:
            return a
        else:
            return eb_ortak_bolen(b, a % b)


    sayi1 = int(input("Birinci tam sayıyı girin: "))
    sayi2 = int(input("İkinci tam sayıyı girin: "))

    ebob = eb_ortak_bolen(sayi1, sayi2)

    print(f"{sayi1} ve {sayi2} sayılarının en büyük ortak böleni: {ebob}")
    pass
elif soru_no == 9:
    def asal_veya_degil(sayi):
        if sayi <= 1:
            return False
        if sayi <= 3:
            return True
        if sayi % 2 == 0:
            return False

        for i in range(3, int(sayi ** 0.5) + 1, 2):
            if sayi % i == 0:
                return False

        return True


    sayi = int(input("Sayıyı girin: "))
    print(asal_veya_degil(sayi))

    pass
elif soru_no == 10:
    def hizlandirici(n, k, fib_k, fib_k1):
        if n == k:
            return fib_k
        else:
            return hizlandirici(n, k + 1, fib_k + fib_k1, fib_k)


    def fibonacci(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return hizlandirici(n, 2, 1, 1)


    n = int(input("Fibonacci dizisinin kaçıncı elemanını hesaplamak istersiniz? "))

    result = fibonacci(n)
    print(f"Fibonacci({n}) = {result}")
    pass
else:
    print("Geçersiz seçenek. Lütfen 1 ile 10 arasında bir sayı girin.")

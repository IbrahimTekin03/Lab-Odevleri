#include "Ucgen.h"
#include "DogruParcasi.h"
#include <cmath>

Ucgen::Ucgen(const Nokta& p1, const Nokta& p2, const Nokta& p3)
    : nokta1(p1), nokta2(p2), nokta3(p3) {}


const Nokta& Ucgen::getP1() const {
    return nokta1;
}

void Ucgen::setP1(const Nokta& p1) {
    nokta1 = p1;
}

const Nokta& Ucgen::getP2() const {
    return nokta2;
}

void Ucgen::setP2(const Nokta& p2) {
    nokta2 = p2;
}

const Nokta& Ucgen::getP3() const {
    return nokta3;
}

void Ucgen::setP3(const Nokta& p3) {
    nokta3 = p3;
}


std::string Ucgen::toString() const {
    return "üçgen; " + nokta1.toString() + ", " + nokta2.toString() + ", " + nokta3.toString();
}

double Ucgen::alan() const {
    DogruParcasi kenar1(nokta1, nokta2);
    DogruParcasi kenar2(nokta2, nokta3);
    DogruParcasi kenar3(nokta3, nokta1);

    double uzunluk1 = kenar1.uzunluk();
    double uzunluk2 = kenar2.uzunluk();
    double uzunluk3 = kenar3.uzunluk();

    double s = (uzunluk1 + uzunluk2 + uzunluk3) / 2.0;
    double alan = sqrt(s * (s - uzunluk1) * (s - uzunluk2) * (s - uzunluk3));

    return alan;
}


double Ucgen::cevre() const {
    DogruParcasi kenar1(nokta1, nokta2);
    DogruParcasi kenar2(nokta2, nokta3);
    DogruParcasi kenar3(nokta3, nokta1);

    double uzunluk1 = kenar1.uzunluk();
    double uzunluk2 = kenar2.uzunluk();
    double uzunluk3 = kenar3.uzunluk();

    double cevre = uzunluk1 + uzunluk2 + uzunluk3;

    return cevre;
}



double* Ucgen::acilar() const {

    double* aciDizisi = new double[3];

    DogruParcasi kenar1(nokta1, nokta2);
    DogruParcasi kenar2(nokta2, nokta3);
    DogruParcasi kenar3(nokta3, nokta1);

    double uzunluk1 = kenar1.uzunluk();
    double uzunluk2 = kenar2.uzunluk();
    double uzunluk3 = kenar3.uzunluk();

    aciDizisi[0] = acos((uzunluk1 * uzunluk1 + uzunluk3 * uzunluk3 - uzunluk2 * uzunluk2) / (2 * uzunluk1 * uzunluk3));
    aciDizisi[1] = acos((uzunluk1 * uzunluk1 + uzunluk2 * uzunluk2 - uzunluk3 * uzunluk3) / (2 * uzunluk1 * uzunluk2));
    aciDizisi[2] = acos((uzunluk2 * uzunluk2 + uzunluk3 * uzunluk3 - uzunluk1 * uzunluk1) / (2 * uzunluk2 * uzunluk3));

    return aciDizisi;
}


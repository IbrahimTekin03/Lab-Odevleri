#include "Daire.h"

Daire::Daire(const Nokta& center, double radius)
    : merkez(center), yaricap(radius) {}


Daire::Daire(const Daire& other)
    : merkez(other.merkez), yaricap(other.yaricap) {}


Daire::Daire(const Daire& other, double scale)
    : merkez(other.merkez), yaricap(other.yaricap* scale) {}


double Daire::alan() const {
    return 3.14 * yaricap * yaricap;
}

double Daire::cevre() const {
    return 2 * 3.14 * yaricap;
}

int Daire::kesisim(const Daire& other) const {

    double uzaklik = sqrt(pow(merkez.getX() - other.merkez.getX(), 2) + pow(merkez.getY() - other.merkez.getY(), 2));


    double toplamYaricap = yaricap + other.yaricap;

    if (uzaklik < toplamYaricap) {
 
        return 0;
    }
    else if (uzaklik == toplamYaricap) {

        return 1;
    }
    else {
        return 2;
    }
}


std::string Daire::toString() const {
    return "Merkez: " + merkez.toString() + ", Yarýçap: " + std::to_string(yaricap);
}


void Daire::yazdir() const {
    std::cout << toString() << std::endl;
}

#include "DogruParcasi.h"

DogruParcasi::DogruParcasi(const Nokta& point1, const Nokta& point2)
    : p1(point1), p2(point2) {}


DogruParcasi::DogruParcasi(const DogruParcasi& other)
    : p1(other.p1), p2(other.p2) {}


double uzaklik(const Nokta& p1, const Nokta& p2) {
    double deltaX = p2.getX() - p1.getX();
    double deltaY = p2.getY() - p1.getY();
    return sqrt(deltaX * deltaX + deltaY * deltaY);
}

DogruParcasi::DogruParcasi(const Nokta& center, double length, double slope) {

    double x1 = center.getX();
    double y1 = center.getY();

  
    double deltaX = length / (std::sqrt(1 + slope * slope));
    double deltaY = slope * deltaX;

    double x2 = x1 + deltaX;
    double y2 = y1 + deltaY;

    p2.set(x2, y2);
}

const Nokta& DogruParcasi::getP1() const {
    return p1;
}

void DogruParcasi::setP1(const Nokta& point) {
    p1 = point;
}

const Nokta& DogruParcasi::getP2() const {
    return p2;
}

void DogruParcasi::setP2(const Nokta& point) {
    p2 = point;
}


double DogruParcasi::uzunluk() const {
    return uzaklik(p1, p2);
}


Nokta DogruParcasi::kesisimNoktasi(const Nokta& point) const {

    double x1 = p1.getX();
    double y1 = p1.getY();
    double x2 = p2.getX();
    double y2 = p2.getY();


    double x = point.getX();
    double y = point.getY();


    double m = (y2 - y1) / (x2 - x1);


    double b = y1 - m * x1;


    double kesisimX = (y - b) / m;
    double kesisimY = m * kesisimX + b;

    return Nokta(kesisimX, kesisimY);
}


Nokta DogruParcasi::ortaNokta() const {
    double ortaX = (p1.getX() + p2.getX()) / 2.0;
    double ortaY = (p1.getY() + p2.getY()) / 2.0;
    return Nokta(ortaX, ortaY);
}

std::string DogruParcasi::toString() const {
    return "P1: " + p1.toString() + ", P2: " + p2.toString();
}

void DogruParcasi::yazdir() const {
    std::cout << toString() << std::endl;
}

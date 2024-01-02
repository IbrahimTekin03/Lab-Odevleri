#include "Nokta.h"

Nokta::Nokta() : x(0.0), y(0.0) {}

Nokta::Nokta(double xy) : x(xy), y(xy) {}

Nokta::Nokta(double x_, double y_) : x(x_), y(y_) {}

Nokta::Nokta(const Nokta& other) : x(other.x), y(other.y) {}

Nokta::Nokta(const Nokta& other, double ofset_x, double ofset_y) : x(other.x + ofset_x), y(other.y + ofset_y) {}


double Nokta::getX() const {
    return x;
}

void Nokta::setX(double value) {
    x = value;
}

double Nokta::getY() const {
    return y;
}

void Nokta::setY(double value) {
    y = value;
}


void Nokta::set(double xCoord, double yCoord) {
    x = xCoord;
    y = yCoord;
}

std::string Nokta::toString() const {
    return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
}

void Nokta::yazdir() const {
    std::cout << toString() << std::endl;
}

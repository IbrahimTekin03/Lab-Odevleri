#ifndef DAIRE_H
#define DAIRE_H

#include "Nokta.h"
#include <cmath>
#include <iostream>

class Daire {
private:
    Nokta merkez;
    double yaricap;

public:

    Daire(const Nokta& center, double radius);

    Daire(const Daire& other);

    Daire(const Daire& other, double scale);

    double alan() const;

    double cevre() const;

    int kesisim(const Daire& other) const;

    std::string toString() const;

    void yazdir() const;
};

#endif // DAIRE_H

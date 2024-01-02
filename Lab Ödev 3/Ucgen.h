#ifndef UCGEN_H
#define UCGEN_H

#include "Nokta.h"
#include "DogruParcasi.h"

class Ucgen {
private:
    Nokta nokta1;
    Nokta nokta2;
    Nokta nokta3;

public:

    Ucgen(const Nokta& p1, const Nokta& p2, const Nokta& p3);


    const Nokta& getP1() const;
    void setP1(const Nokta& p1);

    const Nokta& getP2() const;
    void setP2(const Nokta& p2);

    const Nokta& getP3() const;
    void setP3(const Nokta& p3);

    std::string toString() const;

    double alan() const;

    double cevre() const;

    double* acilar() const;
};

#endif // UCGEN_H

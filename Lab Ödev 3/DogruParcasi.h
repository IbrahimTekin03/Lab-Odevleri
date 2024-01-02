#ifndef DOGRUPARCASI_H
#define DOGRUPARCASI_H

#include "Nokta.h"
#include <cmath>
#include <iostream>

class DogruParcasi {
private:
    Nokta p1;
    Nokta p2;

public:
    
    DogruParcasi(const Nokta& point1, const Nokta& point2); 

    DogruParcasi(const DogruParcasi& other);   
 
    DogruParcasi(const Nokta& center, double length, double slope); 

    
    const Nokta& getP1() const;
    void setP1(const Nokta& point);
                                      
    const Nokta& getP2() const;
    void setP2(const Nokta& point);

    
    double uzunluk() const;     

  
    Nokta kesisimNoktasi(const Nokta& point) const; 
    Nokta ortaNokta() const;

   
    std::string toString() const;

   
    void yazdir() const;
};

#endif // DOGRUPARCASI_H

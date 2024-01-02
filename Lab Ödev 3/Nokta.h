#ifndef NOKTA_H
#define NOKTA_H

#include <iostream>
#include <string>

class Nokta {
private:
    double x;
    double y;

public:

    Nokta();

    Nokta(double value);

    Nokta(double xCoord, double yCoord);

    Nokta(const Nokta& other);

    Nokta(const Nokta& other, double offset_x, double offset_y);

    double getX() const;
    void setX(double value);
    double getY() const;
    void setY(double value);

    void set(double xCoord, double yCoord);

    std::string toString() const;

    void yazdir() const;
};

#endif // NOKTA_H

#include <iostream>

struct Point {
    double x, y;
};

bool checkParallelism(Point p1, Point p2, Point p3, Point p4);
bool checkEquality(Point p1, Point p2, Point p3, Point p4);

void firstSide(double a, double b, double x0, double y0, Point p1, Point p2);
void secondSide(double a, double b, double x0, double y0, Point p2, Point p3);
void thirdSide(double a, double b, double x0, double y0, Point p3, Point p4);
void fourthSide(double a, double b, double x0, double y0, Point p1, Point p4);

#include "Header.h"

bool checkParallelism(Point p1, Point p2, Point p3, Point p4) {
    if (((p2.x - p1.x) != 0) && ((p3.x - p2.x) != 0) && ((p4.x - p3.x) != 0) && ((p4.x - p1.x) != 0)) {
        double k1 = (p2.y - p1.y) / (p2.x - p1.x);
        double k2 = (p3.y - p2.y) / (p3.x - p2.x);
        double k3 = (p4.y - p3.y) / (p4.x - p3.x);
        double k4 = (p4.y - p1.y) / (p4.x - p1.x);

        if ((k1 == k3) && (k2 == k4)) {
            return true;
        }
        else {
            return false;
        }
    }
    else if ((p1.x == p2.x) && (p3.x == p4.x)) {
        return true;
    }
    else {
        return false;
    }
}

bool checkEquality(Point p1, Point p2, Point p3, Point p4) {

    double a1 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
    double b1 = sqrt((p4.x - p3.x) * (p4.x - p3.x) + (p4.y - p3.y) * (p4.y - p3.y));
    double c = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y));
    double d = sqrt((p4.x - p1.x) * (p4.x - p1.x) + (p4.y - p1.y) * (p4.y - p1.y));

    if ((a1 == b1) && (c == d)) {
        return true;
    }
    else {
        return false;
    }
}

void firstSide(double a, double b, double x0, double y0, Point p1, Point p2) {
    double x1 = p1.x, y1 = p1.y, x2 = p2.x, y2 = p2.y;
    double A = ((x2 - x1) * (x2 - x1)) / (a * a) + ((y2 - y1) * (y2 - y1)) / (b * b);
    double B = 2 * ((x2 - x1) * (x1 - x0) / (a * a) + (y2 - y1) * (y1 - y0) / (b * b));
    double C = ((x1 - x0) * (x1 - x0)) / (a * a) + ((y1 - y0) * (y1 - y0)) / (b * b) - 1;
    double D = B * B - 4 * A * C;
    if (D < 0) {
        std::cout << "Сторона AB параллелограмма и эллипс не пересекаются\n";
    }
    double t1 = (-B + sqrt(D)) / (2 * A);
    double t2 = (-B - sqrt(D)) / (2 * A);
    if ((t1 < 0 || t1>1) && (t2 < 0 || t2>1)) {
        std::cout << "Сторона AB параллелограмма и эллипс не пересекаются\n";
    }
    else if (t1 == t2) {
        Point intersection = { x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1) };
        std::cout << "Точка пересечения стороны AB параллелограмма и эллипса имеет координаты: (" << intersection.x << ", " << intersection.y << ")\n";
    }
    else {
        if (t1 >= 0 && t1 <= 1) {
            Point intersection = { x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1) };
            std::cout << "Точки пересечения стороны AB параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
        if (t2 >= 0 && t2 <= 1) {
            Point intersection = { x1 + t2 * (x2 - x1), y1 + t2 * (y2 - y1) };
            std::cout << "Точки пересечения стороны AB параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
    }
}

void secondSide(double a, double b, double x0, double y0, Point p2, Point p3) {
    double x2 = p2.x, y2 = p2.y, x3 = p3.x, y3 = p3.y;
    double A = ((x3 - x2) * (x3 - x2)) / (a * a) + ((y3 - y2) * (y3 - y2)) / (b * b);
    double B = 2 * ((x3 - x2) * (x2 - x0) / (a * a) + (y3 - y2) * (y2 - y0) / (b * b));
    double C = ((x2 - x0) * (x2 - x0)) / (a * a) + ((y2 - y0) * (y2 - y0)) / (b * b) - 1;
    double D = B * B - 4 * A * C;
    if (D < 0) {
        std::cout << "Сторона BC параллелограмма и эллипс не пересекаются\n";
    }
    double t1 = (-B + sqrt(D)) / (2 * A);
    double t2 = (-B - sqrt(D)) / (2 * A);
    if ((t1 < 0 || t1>1) && (t2 < 0 || t2>1)) {
        std::cout << "Сторона BC параллелограмма и эллипс не пересекаются\n";
    }
    else if (t1 == t2) {
        Point intersection = { x2 + t1 * (x3 - x2), y2 + t1 * (y3 - y2) };
            std::cout << "Точка пересечения стороны BC параллелограмма и эллипса имеет координаты: (" << intersection.x << ", " << intersection.y << ")\n";
    }
    else
    {
        if (t1 >= 0 && t1 <= 1) {
            Point intersection = { x2 + t1 * (x3 - x2), y2 + t1 * (y3 - y2) };
                std::cout << "Точки пересечения стороны BC параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
        if (t2 >= 0 && t2 <= 1) {
            Point intersection = { x2 + t2 * (x3 - x2), y2 + t2 * (y3 - y2) };
            std::cout <<"Точки пересечения стороны BC параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
    }
}

void thirdSide(double a, double b, double x0, double y0, Point p3, Point p4) {
    double x3 = p3.x, y3 = p3.y, x4 = p4.x, y4 = p4.y;
    double A = ((x4 - x3) * (x4 - x3)) / (a * a) + ((y4 - y3) * (y4 - y3)) / (b * b);
    double B = 2 * ((x4 - x3) * (x3 - x0) / (a * a) + (y4 - y3) * (y3 - y0) / (b * b));
    double C = ((x3 - x0) * (x3 - x0)) / (a * a) + ((y3 - y0) * (y3 - y0)) / (b * b) - 1;
    double D = B * B - 4 * A * C;
    if (D < 0) {
        std::cout << "Сторона CD параллелограмма и эллипс не пересекаются\n";
    }
    double t1 = (-B + sqrt(D)) / (2 * A);
    double t2 = (-B - sqrt(D)) / (2 * A);
    if ((t1 < 0 || t1>1) && (t2 < 0 || t2>1)) {
        std::cout << "Сторона CD параллелограмма и эллипс не пересекаются\n";
    }
    else if (t1 == t2) {
        Point intersection = { x3 + t1 * (x4 - x3), y3 + t1 * (y4 - y3) };
        std::cout << "Точка пересечения стороны CD параллелограмма и эллипса имеет координаты: (" << intersection.x << ", " << intersection.y << ")\n";
    }
    else {
        if (t1 >= 0 && t1 <= 1) {
            Point intersection = { x3 + t1 * (x4 - x3), y3 + t1 * (y4 - y3) };
            std::cout << "Точки пересечения стороны CD параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
        if (t2 >= 0 && t2 <= 1) {
            Point intersection = { x3 + t2 * (x4 - x3), y3 + t2 * (y4 - y3) };
            std::cout << "Точки пересечения стороны CD параллелограмма и эллипса имеют координаты : (" << intersection.x << ", " << intersection.y << ")\n";
        }
    }
}

void fourthSide(double a, double b, double x0, double y0, Point p1, Point p4) {
    double x1 = p1.x, y1 = p1.y, x4 = p4.x, y4 = p4.y;
    double A = ((x4 - x1) * (x4 - x1)) / (a * a) + ((y4 - y1) * (y4 - y1)) / (b * b);
    double B = 2 * ((x4 - x1) * (x1 - x0) / (a * a) + (y4 - y1) * (y1 - y0) / (b * b));
    double C = ((x1 - x0) * (x1 - x0)) / (a * a) + ((y1 - y0) * (y1 - y0)) / (b * b) - 1;
    double D = B * B - 4 * A * C;
    if (D < 0) {
        std::cout << "Сторона AD параллелограмма и эллипс не пересекаются\n";
    }
    double t1 = (-B + sqrt(D)) / (2 * A);
    double t2 = (-B - sqrt(D)) / (2 * A);
    if ((t1 < 0 || t1>1) && (t2 < 0 || t2>1)) {
        std::cout << "Сторона AD параллелограмма и эллипс не пересекаются\n";
    }
    else if (t1 == t2) {
        Point intersection = { x1 + t1 * (x4 - x1), y1 + t1 * (y4 - y1) };
        std::cout << "Точка пересечения стороны AD параллелограмма и эллипса имеет координаты: (" << intersection.x << ", " << intersection.y << ")\n";
    }
    else {
        if (t1 >= 0 && t1 <= 1) {
            Point intersection = { x1 + t1 * (x4 - x1), y1 + t1 * (y4 - y1) };
            std::cout << "Точки пересечения стороны AD параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
        if (t2 >= 0 && t2 <= 1) {
            Point intersection = { x1 + t2 * (x4 - x1), y1 + t2 * (y4 - y1) };
            std::cout << "Точки пересечения стороны AD параллелограмма и эллипса имеют координаты: (" << intersection.x << ", " << intersection.y << ")\n";
        }
    }
}
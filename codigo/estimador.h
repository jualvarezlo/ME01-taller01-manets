/*
 * Estimador de posición del collar a partir de lecturas RSSI. Es el mismo que analisis/localizar.py,
 * para que la estimación dentro de la red (cabezas de zona) y la de referencia fuera de línea
 * sean comparables.
 */

#ifndef COLLAR_ESTIMADOR_H
#define COLLAR_ESTIMADOR_H

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <set>
#include <string>
#include <vector>

namespace collar
{

struct Lectura
{
    uint32_t observador;
    double x; // posición GPS reportada
    double y;
    double rssi; // dBm
};

enum class Metodo
{
    CERCANO,      // posición del celular con el RSSI más alto (línea base tipo Find My)
    CENTROIDE,    // centroide ponderado por potencia lineal (mW)
    TRILATERACION // mínimos cuadrados no lineales, pesos 1/d^2, Gauss-Newton desde el centroide
};

struct Resultado
{
    bool valido = false;
    double x = 0;
    double y = 0;
};

inline bool
MetodoDesdeTexto(const std::string& s, Metodo& m)
{
    if (s == "cercano")
    {
        m = Metodo::CERCANO;
    }
    else if (s == "centroide")
    {
        m = Metodo::CENTROIDE;
    }
    else if (s == "trilateracion")
    {
        m = Metodo::TRILATERACION;
    }
    else
    {
        return false;
    }
    return true;
}

inline double
RssiADistancia(double rssi, double p0, double n)
{
    return std::pow(10.0, (p0 - rssi) / (10.0 * n));
}

inline Resultado
Centroide(const std::vector<Lectura>& lecturas)
{
    double sx = 0;
    double sy = 0;
    double sw = 0;
    for (const auto& l : lecturas)
    {
        double w = std::pow(10.0, l.rssi / 10.0);
        sx += w * l.x;
        sy += w * l.y;
        sw += w;
    }
    return {true, sx / sw, sy / sw};
}

inline Resultado
Trilaterar(const std::vector<Lectura>& lecturas, double p0, double n, Resultado inicio)
{
    double x = inicio.x;
    double y = inicio.y;
    for (int it = 0; it < 50; ++it)
    {
        // Ecuaciones normales J^T W J paso = -J^T W r, con J de 2 columnas.
        double a11 = 0;
        double a12 = 0;
        double a22 = 0;
        double b1 = 0;
        double b2 = 0;
        for (const auto& l : lecturas)
        {
            double d = RssiADistancia(l.rssi, p0, n);
            double w = 1.0 / std::pow(std::max(d, 1.0), 2);
            double dx = x - l.x;
            double dy = y - l.y;
            double r = std::max(std::hypot(dx, dy), 1e-6);
            double jx = dx / r;
            double jy = dy / r;
            double res = r - d;
            a11 += w * jx * jx;
            a12 += w * jx * jy;
            a22 += w * jy * jy;
            b1 -= w * jx * res;
            b2 -= w * jy * res;
        }
        // Número de condición de la matriz simétrica 2x2: geometría degenerada => sin estimación.
        double tr = a11 + a22;
        double disc = std::sqrt(std::max(0.0, (a11 - a22) * (a11 - a22) / 4 + a12 * a12));
        double lmax = tr / 2 + disc;
        double lmin = tr / 2 - disc;
        if (lmin <= 0 || lmax / lmin > 1e8)
        {
            return {};
        }
        double det = a11 * a22 - a12 * a12;
        double px = (a22 * b1 - a12 * b2) / det;
        double py = (a11 * b2 - a12 * b1) / det;
        x += px;
        y += py;
        if (std::hypot(px, py) < 1e-3)
        {
            break;
        }
    }
    return {true, x, y};
}

inline Resultado
Estimar(const std::vector<Lectura>& lecturas, Metodo metodo, double p0, double n)
{
    if (lecturas.empty())
    {
        return {};
    }
    switch (metodo)
    {
    case Metodo::CERCANO: {
        auto mejor = std::max_element(lecturas.begin(),
                                      lecturas.end(),
                                      [](const Lectura& a, const Lectura& b) { return a.rssi < b.rssi; });
        return {true, mejor->x, mejor->y};
    }
    case Metodo::CENTROIDE:
        return Centroide(lecturas);
    case Metodo::TRILATERACION: {
        std::set<uint32_t> distintos;
        for (const auto& l : lecturas)
        {
            distintos.insert(l.observador);
        }
        if (distintos.size() < 3)
        {
            return {};
        }
        return Trilaterar(lecturas, p0, n, Centroide(lecturas));
    }
    }
    return {};
}

} // namespace collar

#endif // COLLAR_ESTIMADOR_H

/*
 * Mensajes ns3-ai entre la simulación (C++) y el estimador en Python.
 * Los usan collar-sim.cc y el binding collar_py.cc; el layout debe ser el mismo en los dos lados.
 *
 * Cada vez que una cabeza de zona estima (--estimator=python), C++ escribe una Peticion en memoria
 * compartida, la simulación se detiene, Python calcula y devuelve una Respuesta.
 */

#ifndef COLLAR_MSG_H
#define COLLAR_MSG_H

#include <cstdint>

namespace collar
{

constexpr uint32_t kMaxLecturas = 512; // lecturas por ventana; si hay más, van las más recientes

struct Peticion
{
    uint32_t metodo; // 0 cercano, 1 centroide, 2 trilateracion (mismo orden que collar::Metodo)
    uint32_t zona;
    uint32_t cabezaZona; // id de nodo
    double t;            // instante de la estimación (s)
    double p0;           // RSSI a 1 m (dBm)
    double n;            // exponente de pérdida
    uint32_t num;        // lecturas válidas en los arreglos
    uint32_t observador[kMaxLecturas];
    double tLectura[kMaxLecturas];
    double x[kMaxLecturas]; // posición GPS reportada
    double y[kMaxLecturas];
    double rssi[kMaxLecturas];
};

struct Respuesta
{
    uint32_t valida;
    double x;
    double y;
};

} // namespace collar

#endif // COLLAR_MSG_H

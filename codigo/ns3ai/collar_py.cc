/*
 * Binding pybind11 de los mensajes ns3-ai del collar (módulo de Python collar_ns3ai_py).
 * Lo compila codigo/CMakeLists.txt y queda en codigo/ns3ai/collar_ns3ai_py.cpython-*.so.
 */

#include "collar-msg.h"

#include "ns3/ns3-ai-msg-interface.h"

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

using Interfaz = ns3::Ns3AiMsgInterfaceImpl<collar::Peticion, collar::Respuesta>;

namespace
{

// Copia los primeros p.num elementos de un arreglo de la petición a un arreglo de numpy.
template <typename T>
py::array_t<T>
Copiar(const collar::Peticion& p, const T* datos)
{
    return py::array_t<T>(p.num, datos);
}

} // namespace

PYBIND11_MODULE(collar_ns3ai_py, m)
{
    m.attr("MAX_LECTURAS") = collar::kMaxLecturas;

    py::class_<collar::Peticion>(m, "Peticion")
        .def_readonly("metodo", &collar::Peticion::metodo)
        .def_readonly("zona", &collar::Peticion::zona)
        .def_readonly("cabeza_zona", &collar::Peticion::cabezaZona)
        .def_readonly("t", &collar::Peticion::t)
        .def_readonly("p0", &collar::Peticion::p0)
        .def_readonly("n", &collar::Peticion::n)
        .def_readonly("num", &collar::Peticion::num)
        .def("observador", [](const collar::Peticion& p) { return Copiar(p, p.observador); })
        .def("t_lectura", [](const collar::Peticion& p) { return Copiar(p, p.tLectura); })
        .def("x", [](const collar::Peticion& p) { return Copiar(p, p.x); })
        .def("y", [](const collar::Peticion& p) { return Copiar(p, p.y); })
        .def("rssi", [](const collar::Peticion& p) { return Copiar(p, p.rssi); });

    py::class_<collar::Respuesta>(m, "Respuesta")
        .def_readwrite("valida", &collar::Respuesta::valida)
        .def_readwrite("x", &collar::Respuesta::x)
        .def_readwrite("y", &collar::Respuesta::y);

    // Las esperas sueltan el GIL: así un hilo vigilante puede detectar que la simulación murió.
    py::class_<Interfaz>(m, "Ns3AiMsgInterfaceImpl")
        .def(py::init<bool, bool, bool, uint32_t, const char*, const char*, const char*, const char*>())
        .def("PyRecvBegin", &Interfaz::PyRecvBegin, py::call_guard<py::gil_scoped_release>())
        .def("PyRecvEnd", &Interfaz::PyRecvEnd)
        .def("PySendBegin", &Interfaz::PySendBegin, py::call_guard<py::gil_scoped_release>())
        .def("PySendEnd", &Interfaz::PySendEnd)
        .def("PyGetFinished", &Interfaz::PyGetFinished)
        .def("GetCpp2PyStruct", &Interfaz::GetCpp2PyStruct, py::return_value_policy::reference)
        .def("GetPy2CppStruct", &Interfaz::GetPy2CppStruct, py::return_value_policy::reference);
}

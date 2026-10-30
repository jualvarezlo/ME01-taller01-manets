# scratch/manets (symlink a codigo/). Con este archivo ns-3 no arma el programa solo: lo hacemos aquí
# para poder compilar también el binding de Python de ns3-ai.

build_exec(
  EXECNAME collar-sim
  EXECNAME_PREFIX scratch_manets_
  SOURCE_FILES collar-sim.cc
  HEADER_FILES estimador.h ns3ai/collar-msg.h
  LIBRARIES_TO_LINK "${ns3-libs}" "${ns3-contrib-libs}"
  EXECUTABLE_DIRECTORY_PATH ${CMAKE_OUTPUT_DIRECTORY}/scratch/manets/
)

# Binding para el estimador en Python (--estimator=python). Necesita pybind11 (lo trae contrib/ai).
# Como en contrib/ai: FindPython primero, si no pybind11_add_module no encuentra Python_add_library.
find_package(Python COMPONENTS Interpreter Development QUIET)
find_package(pybind11 CONFIG QUIET)
if(Python_FOUND AND pybind11_FOUND)
  pybind11_add_module(collar_ns3ai_py ns3ai/collar_py.cc)
  # macOS: sin enlazar core, el import falla con «symbol not found … ns3::Time::StaticInit»
  target_link_libraries(collar_ns3ai_py PRIVATE ${libcore})
  set_target_properties(
    collar_ns3ai_py PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/ns3ai
  )
  add_dependencies(scratch_manets_collar-sim collar_ns3ai_py)
else()
  message(STATUS "scratch/manets: sin pybind11, no se compila el binding de ns3-ai")
endif()

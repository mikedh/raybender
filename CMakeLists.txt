cmake_minimum_required(VERSION 3.6)
project(raybender)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

find_package(embree 4.0 REQUIRED)

add_subdirectory(pybind11)

pybind11_add_module(_raybender lib/main.cc)
target_link_libraries(_raybender PUBLIC embree)

cmake_minimum_required(VERSION 4.0)
project(graph)

set(CMAKE_CXX_STANDARD 23)

add_executable(graph
        src/main.cpp
        src/graph.cpp
        src/graph.h)

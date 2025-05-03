cmake_minimum_required(VERSION 3.5)
project(lab2 CXX)

# Set C++ standard / version
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(lab2 "main.cpp" "sequence.txt")

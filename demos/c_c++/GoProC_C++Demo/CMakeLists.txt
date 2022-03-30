project(open_gopro_demo)
cmake_minimum_required(VERSION 3.1)

add_definitions(-D_CRT_SECURE_NO_WARNINGS)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(stream src/stream.cpp)
target_link_libraries(stream CONAN_PKG::libcurl)

add_executable(media src/media.cpp)
target_link_libraries(media CONAN_PKG::libcurl)
target_link_libraries(media CONAN_PKG::cjson)
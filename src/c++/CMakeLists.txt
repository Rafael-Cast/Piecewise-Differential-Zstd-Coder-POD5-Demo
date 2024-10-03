cmake_minimum_required(VERSION 3.16.0)

project(PGNano)

include(${PROJECT_SOURCE_DIR}/../../CMakeMacros.txt)
set_pgnano_compile_options()

find_package(Boost REQUIRED COMPONENTS filesystem)
include_directories(${Boost_INCLUDE_DIRS})

include_directories(src/c++/lib-682-nanopore-compression/c++/src/definitions)

add_subdirectory(lib-682-nanopore-compression)
add_subdirectory(tests)
add_subdirectory(commonLib)
add_subdirectory(third_party)

add_executable(copy copy.cpp)
target_compile_options(copy PRIVATE -Werror -Wall -Wno-comment -Wextra)

# Add pod5_format library
target_link_libraries(copy PUBLIC pgnanoCommonLib)
target_link_libraries(copy PUBLIC pod5_format_fork)
target_link_libraries(copy PUBLIC Boost::filesystem)

find_package(GSL REQUIRED)

include(Findzstd.cmake)
find_package(zstd REQUIRED)
install(
    FILES ${zstd_LIBS_RELEASE}>
    TYPE LIB
    COMPONENT third_party
)
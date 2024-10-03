cmake_minimum_required(VERSION 3.16.0)

project(fork)

set(CMAKE_CXX_STANDARD 20)

set(CXX_SOURCES_ROOT ${CMAKE_SOURCE_DIR}/src/c++)
set(THIRD_PARTY_ROOT ${CXX_SOURCES_ROOT}/third_party)

set(FQZCOMP_SOURCE_DIR ${THIRD_PARTY_ROOT}/fqzcomp)
set(FQZCOMP_INCLUDE_DIR ${FQZCOMP_SOURCE_DIR})

set(PGNANOCOMMON_INCLUDE_DIR ${CXX_SOURCES_ROOT}/commonLib)
set(PGNANOCOMPRESSION_INCLUDE_DIR ${CXX_SOURCES_ROOT}/compressionLib)

include_directories(${PGNANOCOMMON_INCLUDE_DIR})
include_directories(${FQZCOMP_INCLUDE_DIR})
include_directories(${PGNANOCOMPRESSION_INCLUDE_DIR})

add_subdirectory(src/c++)
#add_subdirectory(pod5)

SET(BUILD_TYPE "BUILD_TYPE" CACHE STRING "NULL")
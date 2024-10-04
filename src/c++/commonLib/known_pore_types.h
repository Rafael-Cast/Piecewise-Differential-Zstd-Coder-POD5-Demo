#pragma once

#include <cstdint>

namespace pdz
{

enum PDZ_PORE_TYPE : uint_fast8_t
{
    R10_4_1 = 0,
    R10_3 = 1,
    R9_4_1 = 2,
    UNKNOWN = 3
};

constexpr uint_fast8_t mask = !(0x3);
constexpr uint_fast8_t types_of_pore = 3;

inline PDZ_PORE_TYPE to_pore_type(uint_fast8_t x) { return (x & mask) ? UNKNOWN : static_cast<PDZ_PORE_TYPE>(x) ; }

inline uint_fast8_t from_pore_type(PDZ_PORE_TYPE x) { return (x & mask) ? UNKNOWN : x ; }

};
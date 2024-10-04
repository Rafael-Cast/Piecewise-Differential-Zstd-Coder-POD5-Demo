#pragma once

#include <stdint.h>

namespace pdz
{

uint16_t signed_encode(int16_t x);
int16_t signed_decode(uint16_t x);

}

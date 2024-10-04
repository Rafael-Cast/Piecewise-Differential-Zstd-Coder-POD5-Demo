#pragma once

#include "pod5_format/read_table_utils.h"
#include "known_pore_types.h"

namespace pdz
{

struct Metadata
{
public:
    pod5::ReadData m_read_data;
    size_t samples;
    pdz::PDZ_PORE_TYPE pore_type = pdz::PDZ_PORE_TYPE::UNKNOWN;
};

}
#pragma once

#include <regex>

#include "known_pore_types.h"

namespace pdz
{

class PoreTypeParser
{
public:
    PoreTypeParser();

    PDZ_PORE_TYPE parse_pore_type(const std::string & pore_description);
private:
    std::array<PDZ_PORE_TYPE, types_of_pore + 1> m_match_map;
    std::array<std::regex, types_of_pore> m_regex;
};

};
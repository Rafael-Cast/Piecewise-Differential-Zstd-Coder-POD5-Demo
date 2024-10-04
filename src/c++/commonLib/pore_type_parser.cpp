#include "pore_type_parser.h"

pdz::PoreTypeParser::PoreTypeParser()
{
    m_regex[0] = std::regex(".*R?10(\\.|_|-)4((\\.|_|-)1)?.*");
    m_regex[1] = std::regex(".*R?10((\\.|_|-)3)?.*");
    m_regex[2] = std::regex(".*R?9(((\\.|_|-)4)((\\.|_|-)1)?)?");
    m_match_map[0] = PDZ_PORE_TYPE::R10_4_1;
    m_match_map[1] = PDZ_PORE_TYPE::R10_3;
    m_match_map[2] = PDZ_PORE_TYPE::R9_4_1;
    m_match_map[3] = PDZ_PORE_TYPE::UNKNOWN;
}

pdz::PDZ_PORE_TYPE pdz::PoreTypeParser::parse_pore_type(const std::string & pore_description)
{
    uint_fast8_t i = 0;
    for (; i < types_of_pore; i++)
    {
        if (std::regex_match(pore_description,m_regex[i]))
            break;
    }
    return m_match_map[i];
}
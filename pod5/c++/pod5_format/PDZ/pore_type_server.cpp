#include "pore_type_server.h"

namespace pdz
{

void pdz::PoreTypeServer::put_pore_type(pod5::PoreDictionaryIndex idx, const std::string & pore_description) 
{
    PDZ_PORE_TYPE pore_type = m_parser.parse_pore_type(pore_description);
    std::lock_guard<std::mutex> lk(m_idx_map_mtx);
    m_idx_map.insert({idx,pore_type});
}

pdz::PDZ_PORE_TYPE pdz::PoreTypeServer::get_pore_type(pod5::PoreDictionaryIndex idx) 
{
    // FIXME: Program will terminate if the user did not add the pore type first.
    std::lock_guard<std::mutex> lk(m_idx_map_mtx);
    return m_idx_map.at(idx);
}

};
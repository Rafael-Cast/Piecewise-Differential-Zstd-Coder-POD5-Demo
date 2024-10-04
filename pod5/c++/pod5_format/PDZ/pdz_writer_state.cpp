#include "pdz_writer_state.h"

pgnano::PDZWriterState::PDZWriterState()
{
    m_pore_type_server = std::make_unique<pgnano::PoreTypeServer>();
}
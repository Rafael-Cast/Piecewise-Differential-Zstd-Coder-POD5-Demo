#include "pdz_writer_state.h"

pdz::PDZWriterState::PDZWriterState()
{
    m_pore_type_server = std::make_unique<pdz::PoreTypeServer>();
}
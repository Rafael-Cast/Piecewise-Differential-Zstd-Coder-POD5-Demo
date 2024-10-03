#include "pgnano_writer_state.h"

pgnano::PGNanoWriterState::PGNanoWriterState()
{
    m_pore_type_server = std::make_unique<pgnano::PoreTypeServer>();
}
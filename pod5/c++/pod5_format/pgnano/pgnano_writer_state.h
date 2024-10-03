#pragma once

#include <memory>
#include "pore_type_server.h"

namespace pgnano
{

class PGNanoWriterState
{
public:
    PGNanoWriterState();
    //PGNanoWriterState(const PGNanoWriterState &) = delete;
    //PGNanoWriterState& operator= (const PGNanoWriterState &) = delete;
    //PGNanoWriterState& operator= (PGNanoWriterState &&) = default;

    // FIXME: DON'T MAKE THESE MEMBERS PUBLIC
    std::unique_ptr<PoreTypeServer> m_pore_type_server;
private:
};

};
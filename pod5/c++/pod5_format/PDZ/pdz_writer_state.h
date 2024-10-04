#pragma once

#include <memory>
#include "pore_type_server.h"

namespace pdz
{

class PDZWriterState
{
public:
    PDZWriterState();
    //PDZWriterState(const PDZWriterState &) = delete;
    //PDZWriterState& operator= (const PDZWriterState &) = delete;
    //PDZWriterState& operator= (PDZWriterState &&) = default;

    // FIXME: DON'T MAKE THESE MEMBERS PUBLIC
    std::unique_ptr<PoreTypeServer> m_pore_type_server;
private:
};

};
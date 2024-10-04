#pragma once

#include <stdint.h>

#include "pod5_format/types.h"
#include "pod5_format/read_table_utils.h"

#include "model.h"
#include "metadata.h"
#include "header.h"
#include "default_histogram.h"
#include "pdz_reader_state.h"

namespace pdz 
{

class Decompressor
{
public:
    //Decompressor() : m_high_byte_ctx_class(high_byte_histogram), m_low_byte_ctx_class(low_byte_histogram) {};
    void reset();
    void decompress(uint8_t const * const & in, int16_t * const & dest, size_t const & bytes, PDZReaderState & state);
private:
    void decompress_metadata(uint8_t const * const & in, pdz::Metadata & metadata);
    void decompress_header(uint8_t const * const & in, pdz::Header & header);
    void decompress_signal(uint8_t const * const & in, pdz::Header const & header, int16_t * const & dest, size_t const & bytes);
    RangeCoder m_range_coder;
    Model m_high_byte_ctx_class;
    Model m_low_byte_ctx_class_zero, m_low_byte_ctx_class_non_zero;
};

}
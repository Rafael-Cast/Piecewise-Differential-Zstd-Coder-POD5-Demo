#pragma once

#include "pod5_format/types.h"
#include "pod5_format/read_table_utils.h"
#include "compressor.h"
#include "pdz_reader_state.h"
#include "pdz_writer_state.h"

// TODO: Use SampleType instead of int16_t
namespace pdz {

pod5::Status decompress_signal(
    gsl::span<std::uint8_t const> const & compressed_bytes,
    arrow::MemoryPool * pool,
    gsl::span<std::int16_t> const & destination,
    pdz::PDZReaderState & state);

arrow::Result<std::shared_ptr<arrow::Buffer>> compress_signal(
    gsl::span<std::int16_t const> const & samples,
    arrow::MemoryPool * pool,
    pod5::ReadData const & read_data,
    bool is_last_batch,
    pdz::PDZWriterState & state);

static inline CompressionStats get_compression_stats() { return Compressor::get_compression_stats(); }
};
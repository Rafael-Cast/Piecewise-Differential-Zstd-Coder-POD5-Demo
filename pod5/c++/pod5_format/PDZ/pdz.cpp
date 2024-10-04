#include <arrow/buffer.h>

#include "compressor.h"
#include "decompressor.h"
#include "macros.h"
#include "header.h"

#include "pod5_format/types.h"
#include "pod5_format/read_table_utils.h"
#include "pdz_writer_state.h"
#include "../../../../src/c++/lib-682-nanopore-compression/c++/src/definitions/unconditional286/unconditional286_api.hpp"

// TODO: Use SampleType instead of int16_t
namespace pgnano {

// TODO: FIXME: do not create a compressor every time, use a singleton and create it on library initialization

pod5::Status decompress_signal(
    gsl::span<std::uint8_t const> const & compressed_bytes,
    arrow::MemoryPool * pool,
    gsl::span<std::int16_t> const & destination,
    pgnano::PDZReaderState & state)
{
    Unconditional286CompressorSSE::decode(compressed_bytes.data(), destination.data());
    return pod5::Status::OK();
}

arrow::Result<std::size_t> compress_signal(
    gsl::span<std::int16_t const> const & samples,
    arrow::MemoryPool * pool,
    gsl::span<std::uint8_t> const & destination,
    pod5::ReadData const & read_data,
    bool is_last_batch,
    pgnano::PDZWriterState & state)
{
    const auto final_size = Unconditional286CompressorSSE::encode(samples.data(), samples.size(), destination.data());
    return arrow::Result<std::size_t>(final_size);
}

arrow::Result<std::shared_ptr<arrow::Buffer>> compress_signal(
    gsl::span<std::int16_t const> const & samples,
    arrow::MemoryPool * pool,
    pod5::ReadData const & read_data,
    bool is_last_batch,
    pgnano::PDZWriterState & state)
{
    //Unconditional286VbSerial
    const auto compression_bound = Unconditional286CompressorSSE::encode_bound(samples.size());
    ARROW_ASSIGN_OR_RAISE(
        std::shared_ptr<arrow::ResizableBuffer> out,
        arrow::AllocateResizableBuffer(compression_bound, pool));

    ARROW_ASSIGN_OR_RAISE(
        auto final_size,
        pgnano::compress_signal(samples, pool, gsl::make_span(out->mutable_data(), out->size()), read_data, is_last_batch, state));

    ARROW_RETURN_NOT_OK(out->Resize(final_size));
    return out;
}
};

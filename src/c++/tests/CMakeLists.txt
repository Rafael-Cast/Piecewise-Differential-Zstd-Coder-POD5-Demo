add_executable(compression_decompression_test compression_decompression.cpp)

target_compile_options(compression_decompression_test PRIVATE -pg -g)
target_compile_options(compression_decompression_test PRIVATE -Werror -Wall -Wno-comment)
target_link_options(compression_decompression_test PRIVATE -pg -g)

# Add pod5_format library
target_link_libraries(compression_decompression_test PUBLIC pod5_format_fork)
include_directories("../../../pod5/third_party/include")

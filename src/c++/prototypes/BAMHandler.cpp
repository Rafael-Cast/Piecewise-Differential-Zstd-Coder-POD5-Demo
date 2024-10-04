#include "pod5_format/PDZ/BAM_handler.h"

int main()
{

    pdz::BAMHandler h;
    h.open_BAM_file("","");
    h.build_query_index();
    return 0;
}
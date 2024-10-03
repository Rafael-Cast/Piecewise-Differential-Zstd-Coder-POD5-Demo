include(${PROJECT_SOURCE_DIR}/../../CMakeMacros.txt)
set_pgnano_compile_options()

add_library(
            pgnanoCommonLib 
            codecs.h
            codecs.cpp
            default_histogram.h
            known_pore_types.h
            concepts.h
            default_histogram.h
            known_pore_types.h
            macros.h
            model.h
            model.cpp
            pore_type_parser.h
            pore_type_parser.cpp
           )

get_target_property(COMPILE_OPTIONS pgnanoCommonLib COMPILE_OPTIONS)
message("Compile options for target commonLib: ${COMPILE_OPTIONS}")
get_directory_property(COMPILE_OPTIONS DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} COMPILE_OPTIONS)
message("Global compile options: ${COMPILE_OPTIONS}")
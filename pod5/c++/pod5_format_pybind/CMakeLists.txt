
pybind11_add_module(pod5_format_pybind_fork
    api.h
    bindings.cpp
    repacker.h
    utils.h
)

target_link_libraries(pod5_format_pybind_fork
    PRIVATE
        pod5_format
)


set_target_properties(pod5_format_pybind_fork
    PROPERTIES
        POSITION_INDEPENDENT_CODE 1
        CXX_STANDARD 14
)

set(python_project_root "${CMAKE_SOURCE_DIR}/python/lib_pod5/")

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/_version.py.in
    ${python_project_root}/src/lib_pod5/_version.py
)

set(wheel_output_stub "${CMAKE_CURRENT_BINARY_DIR}/wheel.touch")

set(wheel_output_dir "${CMAKE_CURRENT_BINARY_DIR}/wheel_${POD5_FULL_VERSION}")
file(MAKE_DIRECTORY ${wheel_output_dir})

add_custom_command(
    OUTPUT "${wheel_output_stub}"
    COMMAND ${CMAKE_COMMAND}
    ARGS
        -D "PYTHON_EXECUTABLE=${Python_EXECUTABLE}"
        -D "PYTHON_PROJECT_DIR=${python_project_root}"
        -D "PYBIND_INPUT_LIB=$<TARGET_FILE:pod5_format_pybind_fork>"
        -D "WHEEL_OUTPUT_DIR=${wheel_output_dir}"
        -P "${CMAKE_CURRENT_SOURCE_DIR}/build_wheel.cmake"
    DEPENDS
        pod5_format_pybind_fork
    VERBATIM
)

add_custom_target(lib_pod5_python_wheel_fork ALL
    SOURCES
        build_wheel.cmake
    DEPENDS
        "${wheel_output_stub}"
)

install(
    DIRECTORY "${wheel_output_dir}/"
    DESTINATION "."
    COMPONENT wheel
    FILES_MATCHING PATTERN "lib_pod5*.whl"
)

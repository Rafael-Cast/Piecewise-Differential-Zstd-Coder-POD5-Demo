#/bin/bash

submodules () {
    git submodule update --init --recursive;
}

compile_python_venv () {
    cd pod5;
    ln -s ../.git .git;
    python -m setuptools_scm;
    python -m pod5_make_version;
    cd python/pod5;
    make install;
    cd ../..
    rm .git;
    cd ..;
}

build_original_pod5_version () {
    cd src/c++/third_party/pod5
    python -m setuptools_scm
    python -m pod5_make_version
    cd ../../../../
}

refresh_python_vevn () {
    cd pod5/python/pod5;
    make update;
    cd ../../../;
}

cmake_configure () {
    local build_option=$1
    res=1
    cd build 
    cmake .. ${build_option}
    res=$?
    cd ..
    return $res
}

compile_copy () {
    local local_exit_code=0
    cd build/src/c++
    make -j
    local_exit_code=$?
    cd ../../..
    return $local_exit_code
}

activate_conda () {
    eval "$(conda shell.bash hook)"
    conda activate PDZ
    
}

activate_env () {
    source ./pod5/python/pod5/venv/bin/activate
}

initial_setup () {
    submodules
    compile_python_venv
    pre-commit uninstall
    mkdir build
    cmake_configure
    compile_copy
    activate_env
}

compile_py () {
    compile_python_venv
}

refresh_py() {
    refresh_python_vevn
}

compile_c () {
    local_exit_code=0
    compile_copy
    local_exit_code=$?
    return $local_exit_code
}

compile () {
    compile_py
    compile_c
    activate_env
}

clean_c () {
    rm -rf build
    mkdir build
}

our_exit_code=0
cmake_exit_code=0
compilation_exit_code=0
activate_conda
if [ $# -eq 0 ]; then
    clean_c
    cmake_configure
    compile_c;
    activate_env
elif [ $1 = "c" ]; then
    build_option=""
    if [ $# -ge 3 ]; then
        if [ $3 = "release" ]; then
            build_option="-DBUILD_TYPE:STRING=Release"
        elif [ $3 = "profile" ]; then
            build_option="-DBUILD_TYPE:STRING=Profile"
        elif [ $3 = "debug" ]; then
            build_option="-DBUILD_TYPE:STRING=Debug"
        fi
    fi
    if [ $# -ge 2 ] && [ $2 = "clean" ]; then
        if [ $# -lt 4 ] || [ $4 != "cmklog" ]; then
            clean_c &> /dev/null
            cmake_configure $build_option &> /dev/null
            cmake_exit_code=$?
        else 
            clean_c
            cmake_configure $build_option
            cmake_exit_code=$?
        fi
    fi && compile_c; compilation_exit_code=$?
    activate_env
    if [ $# -ge 2 ] && [ $2 = "clean" ] && [ $cmake_exit_code -ne 0 ]; then
        echo "---------------------------------------------------------------------"
        echo "| FAILED CMAKE CONFIG                                               |"
        echo "---------------------------------------------------------------------"
    fi
elif [ $1 = "py" ]; then
    if [ $# -ge 2 ] && [ $2 = clean ]; then
        compile_py;
        activate_env
    else
        refresh_py
    fi
elif [ $1 = "init" ]; then
    initial_setup
fi
pre-commit uninstall
if [ $compilation_exit_code -eq 0 ] && [ $cmake_exit_code -eq 0 ]; then
    our_exit_code=0
else
    our_exit_code=-1
fi
exit $our_exit_code
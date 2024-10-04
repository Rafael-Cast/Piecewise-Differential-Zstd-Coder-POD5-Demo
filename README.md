# Nanopore Compression Integrated Demo

This project serves as a demo integrated into pod5 of our compression algorithm (PDZ, Piecewise Differential Zstd Coder).

In here, you'll find a modified pod5 version, which adds a new compression method for the signal table which uses our compression algorithm, as well as a CLI utility program that uses standard pod5 C api methods to copy a source pod5 file into another pod5 file with the desired compression algorithm (Vbz, 286BitDistributionZstd, uncompressed) applied to the signal table.

You can either build the binary on your local environment or use our provided Dockerfile to build a Docker image for the demo.

## Local build

The code was only tested in a Linux environment, no other OSes are tested.
The most complex part of building this project are satisfying it's dependencies. We used a strategy combining system libraries plus a conda environment, but feel free to use any other strategy to install required packages and libraries. We continue with a list of notable dependencies which you'll need to install (note that for most you'll need both the library and the development package):

### Required dependencies

- Arrow version 8 (we used 8.0.1)
- Flatbuffers 2.0.0
- Boost 1.73.0
- cmake 3.26.4
- zstd  1.5.5 (1.5.6 should also work fine)
- g++ 8.5.0 (We didn't test other compilers; newer versions should also work)
- gcc 8.5.0 (Same comments as with g++)

Additionally, you might need to install GLS (Guidelines Support Library)

You also need to install the following Python packages (we used Python 3.11):

- setuptools 68.0.0
- setuptools_scm 7.1.0

### Building the project

To build the project you can simply use the provided build.sh script. Note that in order to use this script you **MUST** either provide a conda environment called PDZ, even if it's "empty" or comment out the `activate_conda` line in the script.
For your first installation, you should run:

`bash build.sh init`

Then, for either the first or any other build, you should run:

`bash build.sh c clean release`

The executable will be in: `build/src/c++/copy`

## Docker build

TODO: WIP

## Running the demo

In order to run the demo, you'll need any pod5 file. To download a sample pod5 file refer to [Getting a sample pod5 file].
The program will take as an input a pod5 file with any of the supported compression algorithms: Vbz, the presented compression algorithm or no compression at all. You'll also specify an output path and an output file compression algorithm. Then, the program will copy the input pod5 file into an equivalent output pod5 file whose signal table is now compressed with the specified compression algorithm.
Note that we compile a modified pod5 library version which implements the full C api for our signal compression method. This mean you can write any arbitrary C / C++ programs that manipulates pod5 files that you could write with the original C++ pod5 library  while using our novel compression algorithm.

To run the arguments pass the arguments as follows:

`./copy <input_pod5_file> <output_path> --<compression_algorithm>`

Where `<compression_algorithm>` is one of:
- `uncompressed` for no compression at all
- `VBZ` for standard Vbz compression
- `PDZ` for our novel compression algorithm

## Getting a sample pod5 file

TODO: WIP
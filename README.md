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

We also provide a Dockerfile to build or program inside a container engine. To build our binary with Docker, just run: `docker build -t pdz:latest .`.

Although we only tried Docker, other Docker-compatible container engines might work.

## Running the demo

In order to run the demo, you'll need any pod5 file. To download a sample pod5 file refer to [Getting a sample pod5 file].
The program will take as an input a pod5 file with any of the supported compression algorithms: Vbz, the presented compression algorithm or no compression at all. You'll also specify an output path and an output file compression algorithm. Then, the program will copy the input pod5 file into an equivalent output pod5 file whose signal table is now compressed with the specified compression algorithm.
Note that we compile a modified pod5 library version which implements the full C api for our signal compression method. This mean you can write any arbitrary C / C++ programs that manipulates pod5 files that you could write with the original C++ pod5 library  while using our novel compression algorithm.

To run the program pass the arguments as follows:

`copy <input_pod5_file> <output_path> --<compression_algorithm>`

Where `<compression_algorithm>` is one of:
- `uncompressed` for no compression at all
- `VBZ` for standard Vbz compression
- `PDZ` for our novel compression algorithm

### Docker executor

While you can certainly run a native build, unless you are doing performance benchmarks we strongly recommend running our code inside a Docker container. Just doing `docker run pdz` (assuming you named the image you built pdz), will execute the binary and you can pass arguments simply by doing `docker run pdz <arg1> <arg2> <arg3>`.

Remember that the files you'll find in your Docker container are not the same as in your host machine, so you need to mount volumes in order to actually run the program. Don't worry files won't actually be copied (at least on a Linux based system). For instance, suppose that we want to compress a pod5 file (`PAU59949_pass_ed4a9f02_3084670d_232.pod5`) from the `samples` folder into the same folder, using PDZ and naming the result as `out.pod5` we can run:

`docker run -v $(pwd)/samples:/data/in -v $(pwd)/samples:/data/out pdz /data/in/PAU59949_pass_ed4a9f02_3084670d_232.pod5 /data/out/out.pod5 --PDZ`

Note the `$(pwd)` command before the routes. Docker requires some mount paths to be absolute.

The output file will be in `samples/out.pod5`.

#### On container performance

While running on containers is certainly convenient, it involves some overhead which might insert noise into performance benchmark measurements. Therefore, we don't really recommend running performance benchmarks for pdz in a container, **specially if the host OS is not Linux** (as extra virtualization will happen). All our reported benchmarks are done on native builds, with specific benchmark programs in order to achieve more accurate results. 

Containers are not a problem if you simply want either a (very) rough time estimate or just want to measure compression ratios.

### Using our launcher

//TODO:?

### Native build

To run from a binary compiled in your host machine (ie: no docker), just execute the program `copy` with the aforementioned parameters.

## Getting a sample pod5 file

TODO: WIP
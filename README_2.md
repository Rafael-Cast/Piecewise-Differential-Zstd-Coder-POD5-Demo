# Nanopore Compression Integrated Demo

This repository demonstrates the Piecewise Differential Zstd Coder (PDZ) algorithm integrated into the POD5 library, enhancing the compression of the signal table within POD5 files. A Command Line Interface (CLI) utility is provided to copy a source POD5 file into a new POD5 file with the chosen compression method (VBZ, PDZ, or uncompressed).

## Quickstart

To quickly run the demo, use the `launcher.py` script. Ensure you have Python 3, Docker, and the following Python packages:

```sh
pip install docker boto3
```

Ensure Docker is running before executing the launcher.

Run the full sample quickstart:

```sh
python launcher.py quickstart
```

Or run individual steps for more control:

1. Build the project:

```sh
python launcher.py build
```

2. Download a sample POD5 file:

```sh
python launcher.py download_sample
```

3. Compress the sample file using PDZ:

```sh
python launcher.py run sample.pod5 compressed.pod5 PDZ
```

4. Retrieve the original POD5 file:

```sh
python launcher.py run compressed.pod5 restored.pod5 VBZ
```

## Build Options

### Docker Build (Recommended)

To build the project in an isolated environment, ensuring consistency:

```sh
docker build -t pdz:latest .
```

### Local Build

To build the project on a local Linux environment, install the following dependencies:

- Arrow 8.0.1
- Flatbuffers 2.0.0
- Boost 1.73.0
- CMake 3.26.4
- zstd 1.5.5 (1.5.6 also supported)
- g++ 8.5.0
- gcc 8.5.0
- GLS (Guidelines Support Library)

Python packages (Python 3.11):

- setuptools 68.0.0
- setuptools_scm 7.1.0

Refer to `env.yaml` for a conda environment dump.

To build the project, use the `build.sh` script. Ensure a conda environment named PDZ is active or comment out the `activate_conda` line in the script.

First-time installation:

```sh
bash build.sh init
```

Subsequent builds:

```sh
bash build.sh c clean release
```

The executable will be located at `build/src/c++/copy`.

## Running the Demo

### Using Docker

Run the compression inside a Docker container:

```sh
docker run pdz <arg1> <arg2> <arg3>
```

Mount volumes to access files from the host machine:

```sh
docker run -v $(pwd)/samples:/data/in -v $(pwd)/samples:/data/out pdz /data/in/PAU59949_pass_ed4a9f02_3084670d_232.pod5 /data/out/out.pod5 --PDZ
```

### Using the Launcher

Build and run the project using the launcher script:

```sh
python launcher.py build
python launcher.py run <in_pod5> <out_pod5> <algorithm_without_--_prefix>
```

### Native Execution

Run the compression using the locally built executable:

```sh
./copy <input_pod5_file> <output_pod5_file> --<compression_algorithm>
```

## Compression Algorithms Available

- `uncompressed` for no compression
- `VBZ` for standard VBZ compression
- `PDZ` for custom PDZ compression

## Getting a Sample POD5 File

### Download via Script

To download a sample POD5 file:

```sh
python launcher.py download_sample
```

### Convert FAST5 Files

- Use ONT's [pod5 package](https://pypi.org/project/pod5/) for batch tests.
- Use ONT's [online converter](https://pod5.nanoporetech.com/) for smaller tests.

### Access Additional Datasets

Visit ONT's [official website](https://labs.epi2me.io/category/data-releases/) for more datasets.

## License

- Sample data is licensed under Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) from ONT's public dataset repository.
- The POD5 library is licensed under Mozilla Public License, v. 2.0. A copy of the license is available in `pod5-License.md`.

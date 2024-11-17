# Nanopore Compression Integrated Demo

This repository demonstrates the Piecewise Differential Zstd Coder ([PDZ](https://github.com/Rafael-Cast/Piecewise-Differential-Zstd-Coder)) algorithm integrated into the [POD5 library](https://github.com/nanoporetech/pod5-file-format), enhancing the compression of the signal table within POD5 files. A Command Line Interface (CLI) utility is provided to copy a source POD5 file into a new POD5 file with the chosen compression method (VBZ, PDZ, or uncompressed).

This CLI utility uses a modified version of the POD5 library, which should be viable to use in a wide array of C programs that use the POD5 format.

## Quickstart (Docker)

To quickly run the demo, use the `launcher.py` script. Ensure you have Python 3, Docker, and the following Python packages:

```sh
pip install docker boto3
```

Ensure Docker is running before executing the launcher.

Run the full sample quickstart:

```sh
python launcher.py quickstart

```

If you have a sample POD5 file:

```sh
python launcher.py quickstart --file=<path>
```

If you have already built our docker image:

```sh
python launcher.py quickstart --no_build
```

You can also run individual steps for more control:

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

The list of supported compression algorithms is:

- `uncompressed` for no compression at all
- `VBZ` for standard Vbz compression
- `PDZ` for our novel compression algorithm

The following sections will explain different build alternatives and data retrieval methods if you want to keep on experimenting.

## Additional build options

### Local build

The code was only tested in a Linux environment.
The most complex part of building this project are satisfying it's dependencies. We used a strategy combining **system libraries** plus a **conda environment**, but feel free to use any other strategy. We continue with a list of notable dependencies which you'll need to install (note that for most you'll need both the **library** and the **development** package):

#### Required dependencies

- Arrow version 8 (we used 8.0.1)
- Flatbuffers 2.0.0
- Boost 1.73.0
- cmake 3.26.4
- zstd  1.5.5 (1.5.6 also supported)
- g++ 8.5.0 (or newer)
- gcc 8.5.0 (or newer)
- GSL (Guidelines Support Library)

You also need to install the following Python packages (we used Python 3.11):

- setuptools 68.0.0
- setuptools_scm 7.1.0

In `env.yaml` you can find a dump of one of the conda environments we used when developing the application. Note that we also relied on system-wide libraries, so you might need to install additional packages.

To build the project, use the `build.sh` script. Ensure a conda environment named PDZ is active or comment out the `activate_conda` line in the script.

First-time installation:

```sh
bash build.sh init
```

Subsequent builds:

```sh
bash build.sh c clean release
```

The executable will be located at: `build/src/c++/copy`.

Run the compression using the locally built executable:

```sh
./copy <input_pod5_file> <output_pod5_file> --<compression_algorithm>
```

Local builds are the only one we'd expect reasonably precise computational efficiency results, so if you are interested in evaluating this aspect, please do a local build. All our reported benchmarks are done on native builds, with specific benchmark programs in order to achieve more accurate results. 
This method also has the advantage of building a modified version of the POD5 library which you can use to link to a wide range of C / C++ programs that depend on POD5, while retaining the ability to use our novel compression algorithms.
If you are only interested in compression results, we recommend either using our launcher or performing a Docker build if you want a finer-grained control.

### Docker build

We also provide a Dockerfile to build or program inside a container engine. To build our binary with Docker, just run: `docker build -t pdz:latest .`.

Although we only tried Docker, other Docker-compatible container engines might work.

Then, you can run our demo using:

```sh
docker run pdz <arg1> <arg2> <arg3>
```

Remember to mount volumes to access files from the host machine as in this example:

```sh
docker run -v $(pwd)/samples:/data/in -v $(pwd)/samples:/data/out pdz /data/in/PAU59949_pass_ed4a9f02_3084670d_232.pod5 /data/out/out.pod5 --PDZ
```

Alternatively you can use our simple "launcher" (review our quickstart section for dependencies).

### Launcher build

Build and run the project using the launcher script:

```sh
python launcher.py build # Only need to do this once!
python launcher.py run <in_pod5> <out_pod5> <algorithm_without_--_prefix>
```

## Getting a sample pod5 file

We provide a script to download a sample pod5 file which can be run by doing: 

```sh
python launcher.py download_sample
```

ONT also provides an excellent data repository [here](https://labs.epi2me.io/category/data-releases/) ([landing page](https://labs.epi2me.io/dataindex/), [tutorial](https://labs.epi2me.io/tutorials/)).

If you have fast5 files in which you want to compare our algorithm, you can convert arbitrary fast5 files using either ONT's [pod5 package](https://pypi.org/project/pod5/) (recommended for batch tests) or [ONT's online pod5 converter](https://pod5.nanoporetech.com/) (recommended for small or interactive tests).

## License

The sample data we used in our quickstart is licensed under Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)[https://creativecommons.org/licenses/by-nc/4.0/] and retrieved from ONT's public dataset repository.

The original POD5 library is licensed under Mozilla Public License, v. 2.0. As requested, a copy of such a license can be found in the file `pod5-License.md`.
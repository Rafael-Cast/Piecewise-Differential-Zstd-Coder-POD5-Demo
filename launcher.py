import shutil
import docker
import argparse
import os
import time
import boto3
from botocore import UNSIGNED
from botocore.config import Config

client = docker.from_env()

def to_abs(s):
    if os.path.isabs(s):
        return s
    else:
        return os.path.abspath(s)

def folder_or_self(s):
    if os.path.isdir(s):
        return s
    else:
        return os.path.dirname(s)

def parse_path_for_docker_run(s):
    return folder_or_self(to_abs(s))


def build_docker_image():
    if os.path.isdir("build"):
        shutil.rmtree("build")
    client = docker.APIClient(base_url="unix://var/run/docker.sock")

    response = client.build(
        path=".", dockerfile="Dockerfile", tag="pdz:latest", rm=True, decode=True
    )

    for chunk in response:
        if "stream" in chunk:
            print(chunk["stream"].strip())


def run_on_container(in_file, out_file, alg):
    host_in_file = parse_path_for_docker_run(in_file)
    host_out_file = parse_path_for_docker_run(out_file)

    container_in_file = f"/data/in/{os.path.basename(in_file)}"
    container_out_file = f"/data/out/{os.path.basename(out_file)}"

    try:
        container = client.containers.run(
            image="pdz:latest",
            command=[container_in_file, container_out_file, f"--{alg}"],
            volumes=[
                f"{host_in_file}:{os.path.dirname(container_in_file)}",
                f"{host_out_file}:{os.path.dirname(container_out_file)}"
            ],
            detach=False,  # Run container in attached mode
            stdout=True,
            stderr=True,
            auto_remove=True,  # Automatically remove the container after it exits
        )
    except docker.errors.ContainerError as e:
        # print(f"Container error: {e.stderr.decode('utf-8')}")
        raise e
    except docker.errors.ImageNotFound as e:
        print(f"Image not found: {e}")
        raise e
    except docker.errors.APIError as e:
        print(f"API error: {e}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e

def get_first_pod5_file(bucket, prefix, s3):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" not in response:
        raise Exception("No files found in the specified bucket and prefix.")

    for obj in response["Contents"]:
        if obj["Key"].endswith(".pod5"):
            return obj["Key"]

    raise Exception("No .pod5 file found")


def download_sample_file():
    bucket = "ont-open-data"
    prefix = "colo829_2024.03/flowcells/colo829/"
    dest_path = "sample.pod5"

    # Initialize a session using Amazon S3
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    try:
        # Get the first .pod5 file
        file_key = get_first_pod5_file(bucket, prefix, s3)
        print(f"Found file: {file_key}")
        s3.download_file(bucket, file_key, dest_path)
        print("Download successful")

    except Exception as e:
        print(str(e))

def run_parser_body_from_args(args):
    run_parser_body(args.in_path, args.out_path, args.alg)


def run_parser_body(in_path, out_path, alg):
    t1 = time.time()
    run_on_container(in_path, out_path, alg)
    t2 = time.time()

    input_size = os.stat(in_path).st_size
    output_size = os.stat(out_path).st_size
    elapsed_seconds = t2 - t1

    if output_size < input_size:
        print(f"Output file is smaller than input!")
    else:
        print(f"Output file is bigger than input...")

    size_ratio = output_size / input_size
    percentual_relative_difference = 100 * (output_size - input_size) / input_size
    print(f'Percentual relative difference is {percentual_relative_difference:.3f}')
    print(f"Size ratio is {size_ratio:.3f}")

    print(f"Processed {(input_size / elapsed_seconds) / (2 ** 20):.3f} MB/s")

def main():
    parser = argparse.ArgumentParser(description="PDZ launcher.")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for the 'build' command
    build_parser = subparsers.add_parser('build', help='Build PDZ\'s demo docker image')

    # Subparser for the 'run' command
    run_parser = subparsers.add_parser('run', help='Run the demo')
    run_parser.add_argument('in_path', type=str, help='Input file path')
    run_parser.add_argument('out_path', type=str, help='Output file path')
    run_parser.add_argument('alg', type=str, help='Algorithm to use')

    download_sample_parser = subparsers.add_parser('download_sample', help='Downloads a sample pod5 file')
    quickstart_parser = subparsers.add_parser('quickstart', help='Runs a quickstart')
    quickstart_parser.add_argument(
        '--file',
        type=str,
        help='A POD5 file to use as base for our quickstart demo. If not provided, we will download a sample pod5 file',
        default=None,
        nargs='?',
    )
    quickstart_parser.add_argument(
        "--no_build",
        action="store_true",
        help="Skip docker build",
        default=False
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == 'build':
        build_docker_image()
    elif args.command == 'run':
        run_parser_body_from_args(args)
    elif args.command == 'download_sample':
        download_sample_file()
    elif args.command == 'quickstart':
        if not args.no_build:
            print('Building docker image...')
            build_docker_image()
        else:
            print('Skipping docker build...')
            print('Ensure that you ran `python launcher.py build`')
        sample_file_path = args.file
        if sample_file_path is None:
            print('Downloading sample pod5 file...')
            download_sample_file()
            sample_file_path = 'sample.pod5'
        else:
            print(f'Using provided {sample_file_path} as base input file!')

        print('We will run a compression test first')

        print('\tCompressing the sample file with PDZ...')
        run_on_container(sample_file_path, 'compressed.pod5', 'PDZ')
        print('\tRecovering original file using VBZ...')
        run_on_container('compressed.pod5', 'recovered.pod5', 'VBZ')

        vbz_compressed_size = os.stat('recovered.pod5').st_size
        pdz_compressed_size = os.stat('compressed.pod5').st_size
        if vbz_compressed_size > pdz_compressed_size:
            print('\tThe file compressed with PDZ is SMALLER than with VBZ!')
        else:
            print('\tThe file compressed with PDZ is BIGGER than with VBZ...')

        percentual_diff = 100 * (pdz_compressed_size - vbz_compressed_size) / pdz_compressed_size
        size_ratio = pdz_compressed_size / vbz_compressed_size

        print(f'\tTheir size ratio (PDZ / VBZ) is: {size_ratio:.3f}')
        print(f'\tThe percentual relative difference is: {percentual_diff:.3f}%')

        print(f'\tYou can review the compressed and recovered files at compressed.pod5 and recovered.pod5 respectively')

        print('Now, we will run a simple runtime test')
        print('Please note that:')
        print('\t- This is run on only a single sample file and')
        print('\t- we are running with virtualization (Docker)')
        print('The times reported are really for demonstration purposes only and gaining a rough overview; no real measurements can be extracted from this experiment')

        print('\tDecompressing sample file to ensure consistency...')
        run_on_container(sample_file_path, 'input_time_test.pod5', 'uncompressed')

        print('\tCompressing with PDZ...')
        t1_pdz_compression = time.time()
        run_on_container('input_time_test.pod5', 'pdz_compressed.pod5', 'PDZ')
        t2_pdz_compression = time.time()

        print('\tDecompressing with PDZ...')
        t1_pdz_decompression = time.time()
        run_on_container('pdz_compressed.pod5', 'pdz_decompressed.pod5', 'uncompressed')
        t2_pdz_decompression = time.time()

        print('\tCompressing with VBZ...')
        t1_vbz_compression = time.time()
        run_on_container('input_time_test.pod5', 'vbz_compressed.pod5', 'VBZ')
        t2_vbz_compression = time.time()

        print('\tDecompressing with VBZ...')
        t1_vbz_decompression = time.time()
        run_on_container('vbz_compressed.pod5', 'vbz_decompressed.pod5', 'uncompressed')
        t2_vbz_decompression = time.time()

        def compression_formatted_report(filename, t2, t1, algorithm):
            mb = os.stat(filename).st_size >> 20
            print(f'\t{algorithm} compressed a {mb:.3f} MB file in {(t2 - t1):.3f} seconds')

        compression_formatted_report(
            'input_time_test.pod5',
            t2_pdz_compression,
            t1_pdz_compression,
            'PDZ',
        )
        compression_formatted_report(
            "input_time_test.pod5",
            t2_vbz_compression,
            t1_vbz_compression,
            "VBZ",
        )

        def decompression_formatted_report(filename, t2, t1, algorithm):
            mb = os.stat(filename).st_size >> 20
            print(f'\t{algorithm} decompressed {mb:.3f} MB in {(t2 - t1):.3f} seconds')

        decompression_formatted_report(
            "pdz_decompressed.pod5",
            t2_pdz_decompression,
            t1_pdz_decompression,
            'PDZ'
        )
        decompression_formatted_report(
            "vbz_decompressed.pod5",
            t2_vbz_decompression,
            t1_vbz_decompression,
            "VBZ"
        )

        print('Cleaning up...')
        os.remove('vbz_decompressed.pod5')
        os.remove("pdz_decompressed.pod5")
        os.remove('vbz_compressed.pod5')
        os.remove("pdz_compressed.pod5")
        os.remove('input_time_test.pod5')

if __name__ == "__main__":
    main()

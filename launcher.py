import shutil
import docker
import argparse
import os
import time

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

import boto3
from botocore import UNSIGNED
from botocore.config import Config


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
        print(f"Compressed file is smaller!")
    else:
        print(f"Compressed file is bigger...")

    size_ratio = output_size / input_size
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
        print('Building docker image...')
        build_docker_image()
        print('Downloading sample pod5 file...')
        download_sample_file()
        print('Compressing with PDZ...')
        run_parser_body('sample.pod5', 'compressed.pod5', 'PDZ')
        print('Recovering original file...')
        run_parser_body('compressed.pod5', 'recovered.pod5', 'VBZ')

if __name__ == "__main__":
    main()

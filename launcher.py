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
        print(f"Container error: {e.stderr.decode('utf-8')}")
    except docker.errors.ImageNotFound as e:
        print(f"Image not found: {e}")
    except docker.errors.APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Launcher for foo and bar functions.")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for the 'build' command
    build_parser = subparsers.add_parser('build', help='Call the foo function')

    # Subparser for the 'run' command
    run_parser = subparsers.add_parser('run', help='Call the bar function')
    run_parser.add_argument('in_path', type=str, help='Input file path')
    run_parser.add_argument('out_path', type=str, help='Output file path')
    run_parser.add_argument('alg', type=str, help='Algorithm to use')

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == 'build':
        build_docker_image()
    elif args.command == 'run':
        t1 = time.time()
        run_on_container(args.in_path, args.out_path, args.alg)
        t2 = time.time()

        input_size = os.stat(args.in_path).st_size
        output_size = os.stat(args.out_path).st_size
        elapsed_seconds = t2 - t1

        if output_size < input_size:
            print(f"Compressed file is smaller!")
        else:
            print(f"Compressed file is bigger...")

        size_ratio = output_size / input_size
        print(f"Size ratio is {size_ratio:.3f}")

        print(f"Processed {(input_size / elapsed_seconds) / (2 ** 20):.3f} MB/s")

if __name__ == "__main__":
    main()

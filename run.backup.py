from enum import Enum
import os
import multiprocessing as mp
import pandas as pd
from tqdm import tqdm
import time
import subprocess

executable_path = '/data/pgnanoraw/nanopore-compression-integrated-demo/build/src/c++/copy'

def run_bin(in_path, out_path, alg):
    t1=time.time()
    
    p = subprocess.run([executable_path, in_path, out_path, f"--{alg_to_string(alg)}"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    t2=time.time()

    return t2 - t1

def run_bin_from_test(test, alg):
    return run_bin(test.input_path, test.output_path, alg)

def as_list_of_chunks(xs, chunk_length=20):
    i = 0
    idx = 0
    res = [[]]
    for x in xs:
        res[idx].append(x)
        i += 1
        if i == chunk_length:
            i = 0 
            idx += 1
            res.append([])
    return res

class RunPaths:
    def __init__(self, input_path, output_path, original_path) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.original_path = original_path
    
    def __repr__(self) -> str:
        return f"<in: {self.input_path}; out: {self.output_path}; original: {self.original_path}>"

class CompressionAlgorithm(Enum):
    Uncompressed = 'uncompressed'
    Vbz = 'VBZ'
    Ours = 'pgnano'

def alg_to_string(x):
    match x:
        case CompressionAlgorithm.Uncompressed:
            return 'uncompressed'
        case CompressionAlgorithm.Vbz:
            return 'VBZ'
        case CompressionAlgorithm.Ours:
            return 'pgnano'

def scan_dir(dir):
    return [
        f"{dir}/{x}"
        for x
        in os.listdir(dir)
        if os.path.splitext(x)[-1] == '.pod5'
    ]

if __name__ == "__main__":
    input_paths = []
    
    print("Scanning input paths")
    for folder in os.listdir('/data/pgnanoraw/data_demo/DATABASE_POD5'):
        input_paths.extend(scan_dir(f'/data/pgnanoraw/data_demo/DATABASE_POD5/{folder}'))

    start_paths = input_paths.copy()
    vbz_decompressed_paths = []
    ours_compressed_paths = []
    ours_decompressed_paths = []
    vbz_compressed_paths = []

    print("Building test cases' paths")
    for x in start_paths:
        base_name = os.path.basename(x)
        dir_name = os.path.dirname(x)
        ext = os.path.splitext(base_name)[-1]

        vbz_decompressed_path = f"{dir_name}/{base_name}_vbz_decompressed{ext}"
        ours_compressed_path = f"{dir_name}/{base_name}_ours_compressed{ext}"
        ours_decompressed_path = f"{dir_name}/{base_name}_ours_compressed{ext}"
        vbz_compressed_path = f"{dir_name}/{base_name}_vbz_compressed{ext}"

        vbz_decompressed_paths.append(vbz_decompressed_path)
        ours_compressed_paths.append(ours_compressed_path)
        ours_decompressed_paths.append(ours_decompressed_path)
        vbz_compressed_paths.append(vbz_compressed_path)

    print("Building test cases")
    # 1
    vbz_decompression_speed_tests = [ 
        RunPaths(
            input_path=input_path,
            output_path=output_path,
            original_path=original_path
        )
        for (input_path, output_path, original_path)
        in zip(start_paths, vbz_decompressed_paths, start_paths)
    ]

    # 2,1 (order is irrelevant)
    vbz_compression_speed_tests = [ 
        RunPaths(
            input_path=input_path,
            output_path=output_path,
            original_path=original_path
        )
        for (input_path, output_path, original_path)
        in zip(vbz_decompressed_paths, vbz_compressed_paths, start_paths)
    ]

    # 2,2 (order is irrelevant)
    ours_compression_speed_tests = [
        RunPaths(
            input_path=input_path,
            output_path=output_path,
            original_path=original_path
        )
        for (input_path, output_path, original_path)
        in zip(vbz_decompressed_paths, ours_compressed_paths, start_paths)
    ]

    # 3
    ours_decompression_speed_tests = [
        RunPaths(
            input_path=input_path,
            output_path=output_path,
            original_path=original_path
        )
        for (input_path, output_path, original_path)
        in zip(ours_compressed_paths, ours_decompressed_paths, start_paths)
    ]

    print("Chunking cases")
    chunked_vbz_decompression_speed_tests = as_list_of_chunks(vbz_decompression_speed_tests)
    chunked_vbz_compression_speed_tests = as_list_of_chunks(vbz_compression_speed_tests)
    chunked_ours_decompression_speed_tests = as_list_of_chunks(ours_decompression_speed_tests)
    chunked_ours_compression_speed_tests = as_list_of_chunks(ours_compression_speed_tests)

    njobs = int(mp.cpu_count() / 3) # Avoid hyperthreading and some
    chunks = list(
        zip(
            chunked_vbz_decompression_speed_tests,
            chunked_vbz_compression_speed_tests,
            chunked_ours_decompression_speed_tests,
            chunked_ours_compression_speed_tests
        )
    )

    test_out_path="."
    chunk_number = 0
    total_number_of_chunks = len(chunks)

    def run_vbz_decompression_test(x):
        return run_bin_from_test(x, CompressionAlgorithm.Uncompressed)

    def run_vbz_compression_test(x):
        return run_bin_from_test(x, CompressionAlgorithm.Vbz)

    def run_our_compression_test(x):
        return run_bin_from_test(x, CompressionAlgorithm.Ours)
    
    def run_our_decompression_test(x):
        return run_bin_from_test(x, CompressionAlgorithm.Uncompressed)

    for chunk in tqdm(chunks, total=total_number_of_chunks, leave=True, desc='overall'):
        chunk_size = len(chunk[0])

        vbz_decompression_results = []  
        for x in tqdm(chunk[0], total=chunk_size, desc='VBZ_DESC', leave=False):
            vbz_decompression_results.append(run_vbz_decompression_test(x))

        vbz_compression_results = []
        for x in tqdm(chunk[1], total=chunk_size, desc='VBZ_COMP', leave=False):
            vbz_compression_results.append(run_vbz_compression_test(x))

        our_compression_results = []
        for x in tqdm(chunk[3], total=chunk_size, desc='OUR_COMP', leave=False):
            our_compression_results.append(run_our_compression_test(x))

        our_decompression_results = []
        for x in tqdm(chunk[2], total=chunk_size, desc='OUR_DESC', leave=False):
            our_decompression_results.append(run_our_decompression_test(x))
    
        paths_to_delete = (
            [y[0].output_path for y in chunk] +
            [y[1].output_path for y in chunk] +
            [y[2].output_path for y in chunk] +
            [y[3].output_path for y in chunk]
        )

        for x in paths_to_delete:
            try:
                pass #os.remove(x)
            except:
                pass

        csv_dump_path = f"{test_out_path}/{chunk_number}.csv"
        pd.DataFrame(
            {
                'path': list(map(lambda x: x[0].original_path, chunk)),
                'vbz_decompression_results': vbz_decompression_results,
                'vbz_compression_results': vbz_compression_results,
                'our_compression_results': our_compression_results,
                'our_decompression_results': our_decompression_results
            }
        ).to_csv(csv_dump_path)
        chunk_number += 1
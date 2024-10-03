from enum import Enum
import os
import multiprocessing as mp
import pandas as pd
from tqdm import tqdm
import time
import subprocess
import random

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
    N = 30
    for i in tqdm(range(N), total=N, desc=f"Repeating experiments {N} times"):
        for dataset in tqdm(os.listdir('/data/pgnanoraw/data_demo/DATABASE_POD5'), desc="Processing full datasets"):
            input_paths = scan_dir(f'/data/pgnanoraw/data_demo/DATABASE_POD5/{dataset}')

            start_paths = input_paths.copy()
            vbz_decompressed_paths = []
            ours_compressed_paths = []
            ours_decompressed_paths = []
            vbz_compressed_paths = []

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

            test_out_path="."

            def run_vbz_decompression_test(x):
                return run_bin_from_test(x, CompressionAlgorithm.Uncompressed)

            def run_vbz_compression_test(x):
                return run_bin_from_test(x, CompressionAlgorithm.Vbz)

            def run_our_compression_test(x):
                return run_bin_from_test(x, CompressionAlgorithm.Ours)
            
            def run_our_decompression_test(x):
                return run_bin_from_test(x, CompressionAlgorithm.Uncompressed)

            rnd = random.Random(i)
            for xs in [vbz_decompression_speed_tests, vbz_compression_speed_tests, ours_decompression_speed_tests, ours_compression_speed_tests]:
                rnd.shuffle(xs)

            dataset_size = len(vbz_decompression_speed_tests) #TODO: assert that the datasets are really vbz compressed

            vbz_decompression_results = []
            for x in tqdm(vbz_decompression_speed_tests, total=dataset_size, desc='VBZ_DESC', leave=False):
                vbz_decompression_results.append(run_vbz_decompression_test(x))

            vbz_compression_results = []
            for x in tqdm(vbz_compression_speed_tests, total=dataset_size, desc='VBZ_COMP', leave=False):
                vbz_compression_results.append(run_vbz_compression_test(x))

            our_compression_results = []
            for x in tqdm(ours_compression_speed_tests, total=dataset_size, desc='OUR_COMP', leave=False):
                our_compression_results.append(run_our_compression_test(x))

            our_decompression_results = []
            for x in tqdm(ours_decompression_speed_tests, total=dataset_size, desc='OUR_DESC', leave=False):
                our_decompression_results.append(run_our_decompression_test(x))
            
            paths_to_delete = (
                [x.output_path for x in vbz_decompression_speed_tests] +
                [x.output_path for x in vbz_compression_speed_tests] +
                [x.output_path for x in ours_decompression_speed_tests] +
                [x.output_path for x in ours_compression_speed_tests]
            )

            for x in paths_to_delete:
                try:
                    os.remove(x)
                except:
                    pass

            csv_dump_path = f"{test_out_path}/{dataset}_{i}.csv"
            pd.DataFrame(
                {
                    'path': [x.original_path for x in vbz_decompression_speed_tests],
                    'vbz_decompression_results': vbz_decompression_results,
                    'vbz_compression_results': vbz_compression_results,
                    'our_compression_results': our_compression_results,
                    'our_decompression_results': our_decompression_results
                }
            ).to_csv(csv_dump_path)

from itertools import product
import os
import pandas as pd

dump_folder = 'first_full_run_csvs'

csv_paths = [
    f"{dump_folder}/{x}"
    for x
    in os.listdir(dump_folder)
    if os.path.splitext(x)[-1] == '.csv'
]

partial_dfs = [
    pd.read_csv(x)
    for x
    in csv_paths
]

df = pd.concat(partial_dfs)

partial_dfs = []


df['dataset'] = df['path'].apply(lambda x: os.path.basename(os.path.dirname(x)))
df['original_file_size'] = df['path'].apply(os.path.getsize) #TODO: we should actually use the uncompressed file size...

experiment_variants = list(product(['our', 'vbz'], ['compression', 'decompression']))

for (alg, type) in experiment_variants:
    df[f'normalized_{alg}_{type}_results'] =  df['original_file_size'] / (df[f'{alg}_{type}_results'] * (2 ** 20))

datasets = df['dataset'].unique()

print('Full stats:')
print('\tNormalized speeds:')
for (alg, type) in experiment_variants:
    experiment_series = df[f'normalized_{alg}_{type}_results']
    print(f'\t\t{type} ({alg}):: (mean: {experiment_series.mean():.3f} MB/s; stddev: {experiment_series.std():.3f} MB/s)')
print('\tRaw speeds:')
for (alg, type) in experiment_variants:
    experiment_series = df[f'{alg}_{type}_results']
    print(f'\t\t{type} ({alg}):: (mean: {experiment_series.mean():.3f} s; stddev: {experiment_series.std():.3f} s)')

print('+++++++++++++++++++')

print('Per dataset stats:')
for dataset in datasets:
    print(f'\tDataset: {dataset}')
    print(f'\t\tNormalized speeds:')
    for (alg, type) in experiment_variants:
        experiment_series = df[df['dataset'] == dataset][f'normalized_{alg}_{type}_results']
        print(f'\t\t\t{type} ({alg}):: (mean: {experiment_series.mean():.3f} MB/s; stddev: {experiment_series.std():.3f} MB/s)')
    print(f'\t\tRaw speeds:')
    for (alg, type) in experiment_variants:
        experiment_series = df[df['dataset'] == dataset][f'{alg}_{type}_results']
        print(f'\t\t\t{type} ({alg}):: (mean: {experiment_series.mean():.3f} s; stddev: {experiment_series.std():.3f} s)')
    print('---------------------')
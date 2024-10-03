import pod5
import os

def scan_dir(dir):
    return [
        f"{dir}/{x}"
        for x
        in os.listdir(dir)
        if os.path.splitext(x)[-1] == '.pod5'
    ]

input_paths = []

print("Scanning input paths")
for folder in os.listdir('/data/pgnanoraw/data_demo/DATABASE_POD5'):
    input_paths.extend(scan_dir(f'/data/pgnanoraw/data_demo/DATABASE_POD5/{folder}'))

outs = []

for input_file_path in input_paths:
    with pod5.Reader(input_file_path) as reader:
        outs.append((input_file_path, reader.is_vbz_compressed))

any_failed = any(map(lambda x: not x[1], outs))
if any_failed:
    print("Failed paths:")
    print(list(map(lambda x: x[0], filter(lambda x: not x[1], outs))))
else:
    print("All files are Vbz compressed")
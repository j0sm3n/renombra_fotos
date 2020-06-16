import subprocess

info_dict = {}
exif_tool_path = 'exiftool'
image_path = './images/2020-05-19__145947.JPG'

process = subprocess.Popen(
        [exif_tool_path, image_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)

for tag in process.stdout:
    line = tag.strip().split(':', 1)
    if line[0].strip() == 'Camera Model Name':
        print('\n' + 30 * '-')
        print(f'{line[0].strip()} -> {line[-1].strip()}')
    if line[0].strip() == r'Date/Time Original':
        print(f'{line[0].strip()} -> {line[-1].strip()}')
        print(30 * '-', '\n')
    info_dict[line[0].strip()] = line[-1].strip()

for k, v in info_dict.items():
    print(k, ':', v)
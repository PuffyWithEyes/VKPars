import os


all_root = os.getcwd()
all_root = list(all_root.split('\\')[:-2])
zero_string = ''
for root in all_root:
    zero_string += root + '\\'
try:
    os.mkdir(f"{zero_string}\\data (VKPars)")
    zero_string += 'data (VKPars)' + '\\'
    paths = [f"{zero_string}gallery", f"{zero_string}voices", f"{zero_string}other"]
except:
    paths = [f"{zero_string}gallery", f"{zero_string}voices", f"{zero_string}other"]

try:
    for path in paths:
        os.mkdir(path)
except OSError:
    for path in paths:
        print("Создать директорию не удалось", path)

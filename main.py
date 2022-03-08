import glob
import os
import sys
import numpy as np

from pathlib import Path
from PIL import Image

import image_operations


def clean_output():
    if not os.path.isdir('output'):
        os.makedirs('output')
    else:
        for file in glob.glob(os.path.join('output', '*')):
            try:
                os.remove(file)
            except OSError as e:
                print("Error - ", file, ":", e)


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        filepath = f.readline().strip()
        functions = [line.strip().split() for line in f.readlines()]

    clean_output()

    img_count = 0
    for file in glob.glob(os.path.join(filepath, '*.BMP')):
        try:
            filename = Path(file).stem
            print(filename)

            with Image.open(file) as ori_img:
                ori_img.show()
                copy_img = np.array(ori_img)
        except IOError as e:
            print("Error - ", filepath, ":", e)
            continue

        for func in functions:
            copy_img = image_operations.execute_function(func, copy_img, filename)

        mod_img = Image.fromarray(copy_img)
        mod_img.save(os.path.join('output', filename + '_mod.BMP'))
        mod_img.show()

        img_count += 1
        if img_count > 0:
            break

    # print(img_count)

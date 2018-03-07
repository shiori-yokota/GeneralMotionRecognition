import glob
import re
import sys
import os

# ..\\*.txt
for path in glob.glob('..\\*.txt'):
    filename = path[3:]
    temp = '..\\temp_'+filename
    print(filename)
    try:
        input = open(path, 'r')

        output = open(temp, 'w')

        for line in input:
            if line.find('CookingShopsticks') != -1:
                line = re.sub('CookingShopsticks', 'CookingChopsticks', line)
            elif line.find('WoodenSptula') != -1:
                line = re.sub('WoodenSptula', 'WoodenSpatula', line)
            output.write(line)
    finally:
        input.close()
        output.close()

    if os.path.isfile(path) and os.path.isfile(temp):
        os.remove(path)
        os.rename(temp, path)
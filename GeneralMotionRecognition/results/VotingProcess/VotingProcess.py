import glob
import numpy as np
from xlwt import Workbook

wb = Workbook()
ws = wb.add_sheet("Confusion Matrix")
rowNum = 0

n = 18
list = [[0 for col in range(n)] for row in range(n)]

for path in glob.glob('..\\..\\train\\*'):
    recipe = path[-1]
    for folder in glob.glob(path+'\\*'):
        tool = folder[len(path)+1:]
        for bvh in glob.glob(folder+'\\*.bvh'):
            textName = bvh[len(folder)+1:]
            # print(textName)

            for fileName in glob.glob('..\\*.txt'):
                if textName[:-4] == fileName[3:-4]:
                    # print(fileName[3:])
                    # print('Result')
                    Line = open(fileName, 'r')
                    Str = Line.readlines()[20]
                    Line.close
                    # print(Str)

                    words = Str.split(' ')
                    recipeNum = words[1]
                    toolNum = words[2]
                    print(recipeNum[1:-2]+toolNum[1:-3])

                    if recipeNum[1:-2]+toolNum[1:-3] == "1CookingChopsticks":
                        list[rowNum][0] += 1
                        print('list['+str(rowNum)+'][0] = '+str(list[rowNum][0]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "1Whisk-L":
                        list[rowNum][1] += 1
                        print('list['+str(rowNum)+'][1] = '+str(list[rowNum][1]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "1WoodenSpatula":
                        list[rowNum][2] += 1
                        print('list['+str(rowNum)+'][2] = '+str(list[rowNum][2]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "2CookingChopsticks":
                        list[rowNum][3] += 1
                        print('list['+str(rowNum)+'][3] = '+str(list[rowNum][3]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "2Spoon-L":
                        list[rowNum][4] += 1
                        print('list['+str(rowNum)+'][4] = '+str(list[rowNum][4]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "2Whisk-L":
                        list[rowNum][5] += 1
                        print('list['+str(rowNum)+'][5] = '+str(list[rowNum][5]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "2Whisk-S":
                        list[rowNum][6] += 1
                        print('list['+str(rowNum)+'][6] = '+str(list[rowNum][6]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "3Spoon-S":
                        list[rowNum][7] += 1
                        print('list['+str(rowNum)+'][7] = '+str(list[rowNum][7]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "3Whisk-L":
                        list[rowNum][8] += 1
                        print('list['+str(rowNum)+'][8] = '+str(list[rowNum][8]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "3Whisk-S":
                        list[rowNum][9] += 1
                        print('list['+str(rowNum)+'][9] = '+str(list[rowNum][9]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "4Rice-Spoon":
                        list[rowNum][10] += 1
                        print('list['+str(rowNum)+'][10] = '+str(list[rowNum][10]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "4WoodenSpatula":
                        list[rowNum][11] += 1
                        print('list['+str(rowNum)+'][11] = '+str(list[rowNum][11]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "5CookingChopsticks":
                        list[rowNum][12] += 1
                        print('list['+str(rowNum)+'][12] = '+str(list[rowNum][12]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "5Whisk-L":
                        list[rowNum][13] += 1
                        print('list['+str(rowNum)+'][13] = '+str(list[rowNum][13]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "5Whisk-S":
                        list[rowNum][14] += 1
                        print('list['+str(rowNum)+'][14] = '+str(list[rowNum][14]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "5WoodenSpatula":
                        list[rowNum][15] += 1
                        print('list['+str(rowNum)+'][15] = '+str(list[rowNum][15]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "6Hand":
                        list[rowNum][16] += 1
                        print('list['+str(rowNum)+'][16] = '+str(list[rowNum][16]))
                    elif recipeNum[1:-2]+toolNum[1:-3] == "6WoodenSpatula":
                        list[rowNum][17] += 1
                        print('list['+str(rowNum)+'][17] = '+str(list[rowNum][17]))

                else:
                    continue

        rowNum += 1

for i in range(n):
    for j in range(n):
        # print('list['+str(i)+']['+str(j)+'] = '+str(list[i][j]))
        ws.write(i, j, list[i][j])

wb.save("Results.xls")

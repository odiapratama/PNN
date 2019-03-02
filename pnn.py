import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import xlwt
import time


"""======== Nama    : Odia Pratama ========"""
"""======== Kelas   : IF 39-13     ========"""
"""======== NIM     : 1301154405   ========"""

dataTrain = list()
dataTest = list()
dataDoang = list()
dataGauss1 = list()
dataGauss2 = list()
dataGauss3 = list()
data1 = list()
data2 = list()
data3 = list()
cx = list()
cy = list()
cz = list()

start_time = time.time()

workbook = xlrd.open_workbook("dataset.xlsx")

worksheet1 = workbook.sheet_by_name("data_train_PNN")
worksheet2 = workbook.sheet_by_name("data_test_PNN")
worksheet3 = workbook.sheet_by_name("test_doang")

wb=xlwt.Workbook()
ws=wb.add_sheet("Hasil")

smoothing =  0.1

def gaussian(x1, x2, x3, xt1, xt2, xt3, smoothing):
    hasil = (math.exp(-(((x1-xt1)**2)+((x2-xt2)**2)+((x3-xt3)**2))/(2*((smoothing)**2))))
    return hasil

def gaussianT1(x1, x2, xt1, xt2, smoothing):
    hasil = (math.exp(-(((x1-xt1)**2)+((x2-xt2)**2))/(2*((smoothing)**2))))
    return hasil

def akurasi(dataTrain,worksheet2):
    sum =0
    total = 0
    for i in range(1, 151):
        #print((dataTrain[i][4]), (float(worksheet1.cell(i+1, 5).value)))
        if ((dataTrain[i+1][3])==(float(worksheet2.cell(i+1, 3).value))):
            sum += 1
        total += 1
    return ("Total Benar = ",sum,"Dari total data = ",total,"Akurasi = ",(sum/total)*100,"Percent")

for b in range (1,31):
    for a in range (0,4):
        data1.append((worksheet2.cell(b, a).value))
    dataTest.append(data1)
    data1 = []

for d in range (1,151):
    for c in range (0,4):
        data2.append((worksheet1.cell(d, c).value))
        if (c==0):
            cx.append(worksheet1.cell(d, c).value)
        elif (c==1):
            cy.append(worksheet1.cell(d, c).value)
        elif (c==2):
            cz.append(worksheet1.cell(d, c).value)
    dataTrain.append(data2)
    data2 = []

ws.write(0, 0, "x1")
ws.write(0, 1, "x2")
ws.write(0, 2, "x3")
ws.write(0, 3, "kelas")
for k in range(len(dataTest)):
    totalGaus0 = 0
    totalGaus1 = 0
    totalGaus2 = 0
    for l in range(len(dataTrain)):
        hasilGaussian = gaussian(dataTest[k][0], dataTest[k][1], dataTest[k][2], dataTrain[l][0], dataTrain[l][1], dataTrain[l][2], smoothing)
        if (dataTrain[l][3]== 0):
            totalGaus0 += hasilGaussian
        elif (dataTrain[l][3]== 1):
            totalGaus1 += hasilGaussian
        elif (dataTrain[l][3] == 2):
            totalGaus2 += hasilGaussian
    # print(k+1, dataTest[k][0], dataTest[k][1], dataTest[k][2], dataTrain[l][0], dataTrain[l][1], dataTrain[l][2], totalGaus0)
    # print(k+1, dataTest[k][0], dataTest[k][1], dataTest[k][2], dataTrain[l][0], dataTrain[l][1], dataTrain[l][2], totalGaus1)
    # print(k+1, dataTest[k][0], dataTest[k][1], dataTest[k][2], dataTrain[l][0], dataTrain[l][1], dataTrain[l][2], totalGaus2)

    if ((totalGaus0 >= totalGaus1) and (totalGaus0 >= totalGaus2)):
        dataTest[k][3] = 0
    elif ((totalGaus1 >= totalGaus0) and (totalGaus1 >= totalGaus2)):
        dataTest[k][3] = 1
    elif ((totalGaus2 >= totalGaus0) and (totalGaus2 >= totalGaus1)):
        dataTest[k][3] = 2

    ws.write(k+1, 0, dataTest[k][0])
    ws.write(k+1, 1, dataTest[k][1])
    ws.write(k+1, 2, dataTest[k][2])
    ws.write(k+1, 3, dataTest[k][3])

wb.save("Result.xls")

workbook2 = xlrd.open_workbook("Result.xls")
worksheet4 = workbook2.sheet_by_name("Hasil")

for i in range(len(dataTest)):
    print("Data Test",i+1,dataTest[i])

handle = open("prediksi.txt", "w")
x = ("No.", "           x1      ", "            x2          ","         x3      ","         Label       ","\n")
handle.writelines(x)

for i in range(len(dataTest)):
    x = (str(i+1),"     |       ", str(dataTest[i][0]), "    |   ", str(dataTest[i][1]),"   |   ", str(dataTest[i][2]), "  |   ", str(dataTest[i][3]),"\n")
    handle.writelines(x)
handle.close()

"""=====================================TEST DATA===================================="""
for e in range (1,8):
    for f in range (0,3):
        data3.append(float(worksheet3.cell(e, f).value))
    dataDoang.append(data3)
    data3 = []

for m in range(len(dataDoang)):
    totalGausDoang1 = 0
    totalGausDoang2 = 0
    totalGausDoang3 = 0

    hasilGaussian = gaussianT1(0.2, 0.6, dataDoang[m][0], dataDoang[m][1], smoothing)
    # print(hasilGaussian)
    if (dataDoang[m][2] == 1):
        totalGausDoang1 += hasilGaussian
    elif (dataDoang[m][2] == 2):
        totalGausDoang2 += hasilGaussian
    elif (dataTrain[m][2] == 3):
        totalGausDoang3 += hasilGaussian

if ((totalGausDoang1 >= totalGausDoang2) and (totalGausDoang1 >= totalGausDoang3)):
    hasil = 1
elif ((totalGausDoang2 >= totalGausDoang1) and (totalGausDoang2 >= totalGausDoang3)):
    hasil = 2
elif ((totalGausDoang3 >= totalGausDoang1) and (totalGausDoang3 >= totalGausDoang2)):
    hasil = 3

# print(hasil)

"""==================================================================================="""

# print(akurasi(dataTrain,worksheet4))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(cx, cy, cz, c= cx, marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
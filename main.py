# Project: Recursive depth first search using Heap's algo
# Class: AI
# Author: Tamas Gyenis - LXWFGC
# Date: 2019.10.22.
# ---------------------------------------------------------------------------------------------------------------------

class Mat:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.M = [[0 for x in range(self.m)] for y in range(self.n)]
        self.shape = [self.n, self.m]

    def print(self):
        for i in range(self.n):
            print(self.M[i])

    def printForTest(self):
        for i in range(self.n):
            x = "\t".join(map(str, self.M[i]))
            print(x)

    def sum(self):
        sum = 0
        for i in range(self.n):
            for j in range(self.m):
                sum = sum + self.M[i][j]
        return sum

    def submat(self, fn, tn, fm, tm):
        submat = Mat(tn - fn, tm - fm)
        for i in range(0, tn - fn):
            for j in range(0, tm - fm):
                submat.M[i][j] = self.M[i + fn][j + fm]
        return submat

    def place(self, fn, tn, fm, tm, matrix):
        for i in range(0, tn - fn):
            for j in range(0, tm - fm):
                self.M[i + fn][j + fm] = matrix[i][j]

    def place(self, fn, tn, fm, tm, lst):
        for i in range(0, tn - fn):
            for j in range(0, tm - fm):
                self.M[i + fn][j + fm] = lst[i][j]


class Vehicle:
    def __init__(self, index, h, w):
        self.index = index
        self.h = h
        self.w = w
        self.a = self.h * self.w
        self.M = [[index for x in range(self.w)] for y in range(self.h)]
        self.T = [[index for x in range(self.h)] for y in range(self.w)]

    def print(self):
        print(self.M)


class Search:
    def __init__(self, map, vehicleList):
        self.runCnt = 0
        self.map = map
        self.vehicleList = vehicleList
        self.vehiclesBig = []
        self.vehiclesSmall = []
        self.isSeparated = False

        self.n = len(self.vehicleList)
        self.c = self.n * [0]
        self.i = 0

    def median(self, lst):
        n = len(lst)
        s = sorted(lst)
        return (sum(s[n // 2 - 1:n // 2 + 1]) / 2.0, s[n // 2])[n % 2] if n else None

    def separate(self):
        areaList = []
        for i in range(len(self.vehicleList)):
            self.vehicleList.sort(key=lambda x: x.a, reverse=True)
        for i in range(len(self.vehicleList)):
            areaList.append(self.vehicleList[i].a)
        med = self.median(areaList)
        med = int(med)
        for i in range(len(self.vehicleList)):
            if self.vehicleList[i].a <= med:
                self.vehiclesSmall.append(self.vehicleList[i])
            else:
                self.vehiclesBig.append(self.vehicleList[i])
        self.vehicleList = self.vehiclesBig + self.vehiclesSmall
        self.isSeparated = True

    def permuteSmall(self):
        while self.i < self.n:
            if self.c[self.i] < self.i:
                if self.i % 2 == 0:
                    tmp = self.vehiclesSmall[0]
                    self.vehiclesSmall[0] = self.vehiclesSmall[self.i]
                    self.vehiclesSmall[self.i] = tmp
                else:
                    tmp = self.vehiclesSmall[self.c[self.i]]
                    self.vehiclesSmall[self.c[self.i]] = self.vehiclesSmall[self.i]
                    self.vehiclesSmall[self.i] = tmp
                self.c[self.i] += 1
                self.i = 0
                self.vehicleList = self.vehiclesBig + self.vehiclesSmall
                return
            else:
                self.c[self.i] = 0
                self.i += 1


    def permuteBig(self):
        while self.i < self.n:
            if self.c[self.i] < self.i:
                if self.i % 2 == 0:
                    tmp = self.vehiclesBig[0]
                    self.vehiclesBig[0] = self.vehiclesBig[self.i]
                    self.vehiclesBig[self.i] = tmp
                else:
                    tmp = self.vehiclesBig[self.c[self.i]]
                    self.vehiclesBig[self.c[self.i]] = self.vehiclesBig[self.i]
                    self.vehiclesBig[self.i] = tmp
                self.c[self.i] += 1
                self.i = 0
                self.vehicleList = self.vehiclesBig + self.vehiclesSmall
                return
            else:
                self.c[self.i] = 0
                self.i += 1

    def checkMap(self):
        isFull = True
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map.M[i][j] == 0:
                    isFull = False
                    return isFull
                    break
        return isFull

    def run(self, lst):
        if not self.isSeparated:
            self.separate()
        if self.checkMap():
            return self.map
        else:
            for k in range(len(lst)):
                vehicle = lst[k]
                for i in range(self.map.shape[0]):
                    for j in range(self.map.shape[1]):
                        if i + vehicle.h <= self.map.shape[0] and j + vehicle.w <= self.map.shape[1]:
                            subm = self.map.submat(i, i + vehicle.h, j, j + vehicle.w)
                            # print("sub=")
                            # subm.print()
                            if subm.sum() == 0:
                                self.map.place(i, i + vehicle.h, j, j + vehicle.w, vehicle.M)
                                # print("map=")
                                # self.map.print()
                                lstc = lst.copy()
                                lstc.remove(lstc[k])
                                if self.checkMap():
                                    return self.map
                                else:
                                    self.run(lstc)
                            if self.checkMap():
                                return self.map
                        elif i + vehicle.w <= self.map.shape[0] and j + vehicle.h <= self.map.shape[1]:
                            subrot = self.map.submat(i, i + vehicle.w, j, j + vehicle.h)
                            # print("subrot=")
                            # subrot.print()
                            if subrot.sum() == 0:
                                self.map.place(i, i + vehicle.w, j, j + vehicle.h, vehicle.T)
                                # print("map=")
                                # self.map.print()
                                lstc = lst.copy()
                                lstc.remove(lstc[k])
                                if self.checkMap():
                                    return self.map
                                else:
                                    self.run(lstc)
                            if self.checkMap():
                                return self.map
                        if self.checkMap():
                            return self.map
                    if self.checkMap():
                        return self.map
                if self.checkMap():
                    return self.map
            if self.checkMap():
                return self.map
        if self.checkMap():
            return self.map
        else:
            self.runCnt = self.runCnt+1
            # print(self.runCnt)
            self.map = Mat(self.map.shape[0], self.map.shape[1])
            self.permuteSmall()
            self.permuteBig()
            self.run(self.vehicleList)


# v1 = Vehicle(1, 4, 2)
# v2 = Vehicle(2, 3, 2)
# v3 = Vehicle(3, 1, 2)
# v4 = Vehicle(4, 2, 5)
# v5 = Vehicle(5, 2, 2)
# v6 = Vehicle(6, 2, 1)
# v7 = Vehicle(7, 3, 1)
# v8 = Vehicle(8, 1, 1)
# v9 = Vehicle(9, 1, 1)
# v10 = Vehicle(10, 1, 2)
# v11 = Vehicle(11, 1, 3)
# v12 = Vehicle(12, 1, 1)
# v13 = Vehicle(13, 1, 1)
# v14 = Vehicle(14, 1, 4)
# v15 = Vehicle(15, 1, 1)
# v16 = Vehicle(16, 8, 1)
# vehicleList = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16]
# mapp = Mat(8, 7)

# s = Search(mapp, vehicleList)
# s.separate()
# s.permute()
# s.permute()

vehicleList = []

mapSizeIn = input()
mapSizeN = int(mapSizeIn.split('\t')[0])
mapSizeM = int(mapSizeIn.split('\t')[1])
mapp = Mat(mapSizeN, mapSizeM)

vehNum = input()
vehNum = int(vehNum)

for i in range(vehNum):
    vehIndex = i+1
    vehSizeIn = input()
    vehSizeN = int(vehSizeIn.split('\t')[0])
    vehSizeM = int(vehSizeIn.split('\t')[1])
    v = Vehicle(vehIndex, vehSizeN, vehSizeM)
    vehicleList.append(v)
#
s = Search(mapp, vehicleList)
finalMap = s.run(vehicleList)
finalMap.printForTest()

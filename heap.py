class Heap:
    def __init__(self, lst):
        self.lst = lst
        self.n = len(self.lst)
        self.l = self.lst
        self.c = self.n * [0]
        self.i = 0;

    def permute(self):
        while self.i < self.n:
            if self.c[self.i] < self.i:
                if self.i % 2 == 0:
                    tmp = self.l[0]
                    self.l[0] = self.l[self.i]
                    self.l[self.i] = tmp
                else:
                    tmp = self.l[self.c[self.i]]
                    self.l[self.c[self.i]] = self.l[self.i]
                    self.l[self.i] = tmp
                vehOrder = self.l;
                self.c[self.i] += 1
                self.i = 0
                return vehOrder
            else:
                self.c[self.i] = 0
                self.i += 1


l = [1, 2, 3, 4]

h = Heap(l)
for i in range(20):
    print(h.permute())

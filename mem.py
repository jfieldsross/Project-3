from helpers import SetUp
import cache

class MEM:

    def __init__(self, R, postMemBuff, preMemBuff, opcodeStr, arg1, arg2, arg3, dataval, address, numInstructions):
        self.R = R
        self.postMemBuff = postMemBuff
        self.preMemBuff = preMemBuff
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstructions

    def run(self):

        if self.preMemBuff[0] != -1:
            i = self.preMemBuff[0]
            if self.opcodeStr[i] == "LDUR":
                addrOffest = self.R[self.arg2[i]] + (self.arg1[i] * 4)
                found = False
                dataIn = -1
                addrIn = 0
                if addrOffest <= self.address[len(self.address) - 1]:
                    found = True
                if not found:
                    lastAddr = self.address[len(self.address) - 1] + 4
                    while lastAddr != addrOffest + 4:
                        self.address.append(lastAddr)
                        lastAddr += 4
                    while len(self.address) - self.numInstructions > len(self.dataval):
                        self.dataval.append(0)
                    self.R[self.arg3[i]] = 0
                    dataIn = len(self.dataval) - 1

                if found:
                    for j in range(len(self.address)):
                        if self.address[j] == addrOffest:
                            addrIn = j

                    dataIn = addrIn - self.numInstructions

                    if dataIn < 0:
                        dataIn = -1
                        self.R[self.arg3[i]] = self.R[self.arg3[addrIn]]
                    else:
                        self.R[self.arg3[i]] = self.dataval[dataIn]

                hit = cache.Cache.checkCache(dataIn, i, 0, 0)

                if hit:
                    self.postMemBuff = [self.R[self.arg3[i]], i]
                    if self.preMemBuff[1] != -1:
                        self.preMemBuff[0] = self.preMemBuff[1]
                        self.preMemBuff[1] = -1
                    else:
                        self.preMemBuff = [-1, -1]

            if self.opcodeStr[i] == "STUR":
                addrOffest = self.R[self.arg2[i]] + (self.arg1[i] * 4)
                found = False
                addrIn = 0
                dataIn = -1
                if addrOffest <= self.address[len(self.address) - 1]:
                    found = True
                if not found:
                    lastAddr = self.address[len(self.address) - 1] + 4
                    while lastAddr != addrOffest + 4:
                        self.address.append(lastAddr)
                        lastAddr += 4
                    while len(self.address) - self.numInstructions - 1 > len(self.dataval):
                        self.dataval.append(0)
                    self.dataval.append(self.R[self.arg3[i]])
                    dataIn = len(self.dataval) - 1
                    hit = cache.Cache.checkCache(dataIn, i, 1, self.R[self.arg3[i]])
                if found:
                    addrIn = 0
                    for j in range(len(self.address)):
                        if self.address[j] == addrOffest:
                            addrIn = j

                    dataIn = addrIn - self.numInstructions

                    if dataIn < 0:
                        dataIn = -1
                        self.R[self.arg3[addrIn]] = self.R[self.arg3[i]]
                        hit = cache.Cache.checkCache(dataIn, i, 1, self.R[self.arg3[addrIn]])
                    else:
                        self.dataval[dataIn] = self.R[self.arg3[i]]
                        hit = cache.Cache.checkCache(dataIn, i, 1, self.dataval[dataIn])

                if hit:
                    if self.preMemBuff[1] != -1:
                        self.preMemBuff[0] = self.preMemBuff[1]
                    else:
                        self.preMemBuff = [-1, -1]
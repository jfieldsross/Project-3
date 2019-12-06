from helpers import SetUp

class ALU:

    def __init__(self, R, postALUBuff, preALUBuff, opcodeStr, arg1, arg2, arg3):
        self.R = R
        self.postALUBuff = postALUBuff
        self.preALUBuff = preALUBuff
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def run(self):

        if self.preALUBuff[0] != -1:
            i = self.preALUBuff[0]
            if self.opcodeStr[i] == "ADD": #ADD
                self.postALUBuff = [self.R[self.arg1[i]] + self.R[self.arg2[i]], i]
            elif self.opcodeStr[i] == "SUB": #SUB
                self.postALUBuff = [self.R[self.arg1[i]] - self.R[self.arg2[i]], i]
            elif self.opcodeStr[i] == "AND":
                self.postALUBuff = [self.R[self.arg1[i]] & self.R[self.arg2[i]], i]
            elif self.opcodeStr[i] == "ORR":
                self.postALUBuff = [self.R[self.arg1[i]] | self.R[self.arg2[i]], i]
            elif self.opcodeStr[i] == "ADDI":
                self.postALUBuff = [self.R[self.arg1[i]] + self.arg2[i], i]
            elif self.opcodeStr[i] == "SUBI":
                self.postALUBuff = [self.R[self.arg1[i]] - self.arg2[i], i]
            elif self.opcodeStr[i] == "MOVZ":
                self.postALUBuff = [self.arg2[i] * self.arg1[i], i]
            elif self.opcodeStr[i] == "MOVK":
                if self.arg1[i] == 0:
                    self.R[self.arg3[i]] = self.R[self.arg3[i]] & 0xFFFFFFFFFFFF0000
                elif self.arg1[i] == 16:
                    self.R[self.arg3[i]] = self.R[self.arg3[i]] & 0xFFFFFFFF0000FFFF
                elif self.arg1[i] == 32:
                    self.R[self.arg3[i]] = self.R[self.arg3[i]] & 0xFFFF0000FFFFFFFF
                else:
                    self.R[self.arg3[i]] = self.R[self.arg3[i]] & 0x0000FFFFFFFFFFFF
                self.R[self.arg3[i]] = self.arg2[i] + (self.R[self.arg3[i]] * self.arg1[i])
                self.postALUBuff = [self.R[self.arg3[i]], i]
            elif self.opcodeStr[i] == "ASR":
                self.postALUBuff = [self.R[self.arg1[i]] >> self.arg2[i], i]
            elif self.opcodeStr[i] == "LSL":
                self.postALUBuff = [(self.R[self.arg1[i]] % (1 << 32)) << (self.arg2[i]), i]
            elif self.opcodeStr[i] == "LSR":
                self.postALUBuff = [(self.R[self.arg1[i]] % (1 << 32)) >> (self.arg2[i]), i]
            elif self.opcodeStr[i] == "EOR":
                self.postALUBuff = [self.R[self.arg1[i]] ^ self.R[self.arg2[i]]]
            else:
                print("ERROR!!! INSPECT IMMEDIATELY")
                exit()

            if self.preALUBuff[1] != -1:
                self.preALUBuff[0] = self.preALUBuff[1]
                self.preALUBuff[1] = -1

            else:
                self.preALUBuff = [-1, -1]

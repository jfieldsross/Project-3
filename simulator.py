import sys

import cache
import fetch
import writeBack
import alu
import mem
import issue
from helpers import SetUp
import masking_constants as MASKs

class simClass:

    def __init__(self, instruction, opcodes, opcodeStr, dataval, address, arg1, arg2, arg3, arg1Str,
                 arg2Str, arg3Str, numInstrs, destReg, src1Reg,
                 src2Reg):
        self.instruction = instruction
        self.opcode = opcodes
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.opcodeStr = opcodeStr
        self.PC = 96
        self.cycle = 1
        self.R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.postMemBuff = [-1, -1] # first number is value, second is instr index
        self.postALUBuff = [-1, -1] # first number is value, second is instr index
        self.preMemBuff = [-1, -1]
        self.preALUBuff = [-1, -1]
        self.preIssueBuff = [-1, -1, -1, -1]

        #uncomment these lines as the classes are developed :)

        self.WB = writeBack.WriteBack(self.R, self.postMemBuff, self.postALUBuff, destReg)
        self.ALU = alu.ALU(self.R, self.postALUBuff, self.preALUBuff, opcodeStr, arg1, arg2, arg3)
        self.MEM = mem.MEM(self.R, self.postMemBuff, self.preMemBuff, opcodeStr, arg1, arg2, arg3, dataval, address,
                           self.numInstructions)
        self.cache = cache.Cache(numInstrs, instruction, dataval, address)
        self.issue = issue.Issue(instruction, opcodes, opcodeStr, dataval, address, arg1, arg2, arg3, numInstrs,
                                 destReg, src1Reg, src2Reg)
        self.fetch = fetch.Fetch(instruction, opcodeStr, dataval, address, arg1, arg2, arg3, self.numInstructions,
                                 destReg, src1Reg, src2Reg, self.preALUBuff, self.postALUBuff, self.PC, cache,
                                 self.preIssueBuff)

        self.outputFileName = SetUp.get_output_filename()

    def printState(self):
        outputFileName = SetUp.get_output_filename()

        with open(outputFileName + "_pipeline.txt", 'a') as outFile:
            outFile.write("--------------------\n")
            outFile.write("Cycle " + str(self.cycle) + ":\n\n")
    
            outFile.write("Pre-Issue Buffer:\n")
            if self.preIssueBuff[0] != -1:
                outFile.write("\tEntry 0:\t" + str(self.opcodeStr[self.preIssueBuff[0]]) + str(self.arg1Str[self.preIssueBuff[0]])
                      + str(self.arg2Str[self.preIssueBuff[0]]) + str(self.arg3Str[self.preIssueBuff[0]]) + '\n')
            else:
                outFile.write("\tEntry 0:\t\n")
    
            if self.preIssueBuff[1] != -1:
                outFile.write("\tEntry 1:\t" + str(self.opcodeStr[self.preIssueBuff[1]]) +
                              str(self.arg1Str[self.preIssueBuff[1]]) + str(self.arg2Str[self.preIssueBuff[1]]) +
                              str(self.arg3Str[self.preIssueBuff[1]]) + '\n')
            else:
                outFile.write("\tEntry 1:\t\n")
    
            if self.preIssueBuff[2] != -1:
                outFile.write("\tEntry 2:\t" + str(self.opcodeStr[self.preIssueBuff[2]]) +
                              str(self.arg1Str[self.preIssueBuff[2]]) + str(self.arg2Str[self.preIssueBuff[2]]) +
                              str(self.arg3Str[self.preIssueBuff[2]]) + '\n')
            else:
                outFile.write("\tEntry 2:\t\n")
    
            if self.preIssueBuff[3] != -1:
                outFile.write("\tEntry 3:\t" + str(self.opcodeStr[self.preIssueBuff[3]]) +
                              str(self.arg1Str[self.preIssueBuff[3]]) + str(self.arg2Str[self.preIssueBuff[3]]) +
                              str(self.arg3Str[self.preIssueBuff[3]]) + '\n')
            else:
                outFile.write("\tEntry 3:\t\n")
    
            outFile.write("Pre_ALU Queue:\n")
            if self.preALUBuff[0] != -1:
                outFile.write("\tEntry 0:\t" + str(self.opcodeStr[self.preALUBuff[0]]) +
                              str(self.arg1Str[self.preALUBuff[0]]) + str(self.arg2Str[self.preALUBuff[0]]) +
                              str(self.arg3Str[self.preALUBuff[0]]) + '\n')
            else:
                outFile.write("\tEntry 0:\t\n")
                
            if self.preALUBuff[1] != -1:
                outFile.write("\tEntry 1:\t" + str(self.opcodeStr[self.preALUBuff[1]]) +
                              str(self.arg1Str[self.preALUBuff[1]])  + str(self.arg2Str[self.preALUBuff[1]]) +
                              str(self.arg3Str[self.preALUBuff[1]]) + '\n')
            else:
                outFile.write("\tEntry 1:\t\n")
    
            outFile.write("Post_ALU Queue:\n")
            if self.postALUBuff[0] != -1:
                outFile.write("\tEntry 0:\t" + str(self.opcodeStr[self.postALUBuff[0]]) +
                              str(self.arg1Str[self.postALUBuff[0]]) +
                              str(self.arg2Str[self.postALUBuff[0]]) + str(self.arg3Str[self.postALUBuff[0]]) + '\n')
            else:
                outFile.write("\tEntry 0:\t\n")
    
            outFile.write("Pre_MEM Queue:\n")
            if self.preMEMBuff[0] != -1:
                outFile.write("\tEntry 0:\t" + str(self.opcodeStr[self.preMEMBuff[0]]) +
                              str(self.arg1Str[self.preMEMBuff[0]]) + str(self.arg2Str[self.preMEMBuff[0]]) +
                              str(self.arg3Str[self.preMEMBuff[0]]) + '\n')
            else:
                outFile.write("\tEntry 0:\t\n")
    
            if self.preMEMBuff[1] != -1:
                outFile.write("\tEntry 1:\t" + str(self.opcodeStr[self.preMEMBuff[1]]) +
                              str(self.arg1Str[self.preMEMBuff[1]]) + str(self.arg2Str[self.preMEMBuff[1]]) +
                              str(self.arg3Str[self.preMEMBuff[1]]) + '\n')
            else:
                outFile.write("\tEntry 1:\t\n")
    
            outFile.write("Post_MEM Queue:\n")
            if self.postMEMBuff[0] != -1:
                outFile.write("\tEntry 0:\t" + str(self.opcodeStr[self.postMEMBuff[0]]) +
                              str(self.arg1Str[self.postMEMBuff[0]]) + str(self.arg2Str[self.postMEMBuff[0]]) +
                              str(self.arg3Str[self.postMEMBuff[0]]) + '\n')
            else:
                outFile.write("\tEntry 0:\t\n")
    
            outFile.write("\nRegisters\n")
            outStr = "R00:"
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "R08:"
            for i in range(8, 16):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "R16:"
            for i in range(16, 24):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "R24:"
            for i in range(24, 32):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n\n")
            outFile.write("Cache\n")

            outFile.write("Set 0: LRU=" + str(self.cache.lruBit[0]) + "\n")
            outFile.write("\tEntry 0: [(" + str(self.cache.cacheSets[0][0][0]) + ", " +
                          str(self.cache.cacheSets[0][0][1]) + ", " + str(self.cache.cacheSets[0][0][2]) + ")<" +
                          str(self.cache.cacheSets[0][0][3]) + ", " + str(self.cache.cacheSets[0][0][4]) + ">]\n")
            outFile.write("\tEntry 1: [(" + str(self.cache.cacheSets[0][1][0]) + ", " +
                          str(self.cache.cacheSets[0][1][1]) + ", " + str(self.cache.cacheSets[0][1][2]) + ")<" +
                          str(self.cache.cacheSets[0][1][3]) + ", " + str(self.cache.cacheSets[0][1][4]) + ">]\n")

            outFile.write("Set 1: LRU=" + str(self.cache.lruBit[1]) + "\n")
            outFile.write("\tEntry 0: [(" + str(self.cache.cacheSets[0][0][0]) + ", " +
                          str(self.cache.cacheSets[1][0][1]) + ", " + str(self.cache.cacheSets[1][0][2]) + ")<" +
                          str(self.cache.cacheSets[1][0][3]) + ", " + str(self.cache.cacheSets[1][0][4]) + ">]\n")
            outFile.write("\tEntry 1: [(" + str(self.cache.cacheSets[0][1][0]) + ", " +
                          str(self.cache.cacheSets[1][1][1]) + ", " + str(self.cache.cacheSets[1][1][2]) + ")<" +
                          str(self.cache.cacheSets[1][1][3]) + ", " + str(self.cache.cacheSets[1][1][4]) + ">]\n")

            outFile.write("Set 2: LRU=" + str(self.cache.lruBit[2]) + "\n")
            outFile.write("\tEntry 0: [(" + str(self.cache.cacheSets[2][0][0]) + ", " +
                          str(self.cache.cacheSets[2][0][1]) + ", " + str(self.cache.cacheSets[2][0][2]) + ")<" +
                          str(self.cache.cacheSets[2][0][3]) + ", " + str(self.cache.cacheSets[2][0][4]) + ">]\n")
            outFile.write("\tEntry 1: [(" + str(self.cache.cacheSets[2][1][0]) + ", " +
                          str(self.cache.cacheSets[2][1][1]) + ", " + str(self.cache.cacheSets[2][1][2]) + ")<" +
                          str(self.cache.cacheSets[2][1][3]) + ", " + str(self.cache.cacheSets[2][1][4]) + ">]\n")

            outFile.write("Set 3: LRU=" + str(self.cache.lruBit[3]) + "\n")
            outFile.write("\tEntry 0: [(" + str(self.cache.cacheSets[3][0][0]) + ", " +
                          str(self.cache.cacheSets[3][0][1]) + ", " + str(self.cache.cacheSets[3][0][2]) + ")<" +
                          str(self.cache.cacheSets[3][0][3]) + ", " + str(self.cache.cacheSets[3][0][4]) + ">]\n")
            outFile.write("\tEntry 1: [(" + str(self.cache.cacheSets[3][1][0]) + ", " +
                          str(self.cache.cacheSets[3][1][1]) + ", " + str(self.cache.cacheSets[3][1][2]) + ")<" +
                          str(self.cache.cacheSets[3][1][3]) + ", " + str(self.cache.cacheSets[3][1][4]) + ">]\n")

            outFile.write("\nData\n")
            outStr = "\n"
            for i in range(len(self.dataval)):

                if i % 8 == 0 and i != 0 or i == len(self.dataval):
                    outFile.write(outStr + "\n")

                if i % 8 == 0:
                    outStr = str(self.address[i + self.numInstructions]) + ":" + str(self.dataval[i])

                if (i % 8 != 0):
                    outStr = outStr + "\t" + str(self.dataval[i])

            outFile.write(outStr + "\n")
            outFile.close()


    def run(self):
        go = True

        while go:
            self.WB.run()
            self.ALU.run()
            self.MEM.run()
            self.issue.run()
            go = self.fetch.run()
            self.printState()
            self.cycle += 1

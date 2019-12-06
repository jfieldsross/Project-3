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
        self.preIssueBuff = [-1, -1]

        #uncomment these lines as the classes are developed :)

        self.WB = writeBack.WriteBack(self.R, self.postMemBuff, self.postALUBuff, destReg)
        self.ALU = alu.ALU(self.R, self.postALUBuff, self.preALUBuff, opcodeStr, arg1, arg2, arg3)
        self.MEM = mem.MEM(self.R, self.postMemBuff, self.preMemBuff, opcodeStr, arg1, arg2, arg3, dataval, address, self.numInstructions)
        self.cache = cache.Cache(numInstrs, instruction, dataval, address)
        self.issue = issue.Issue(instruction, opcodes, opcodeStr, dataval, address, arg1, arg2,
                                 arg3, numInstrs, destReg, src1Reg, src2Reg, self.preIssueBuff,
                                 self.preALUBuff, self.preMemBuff, self.postALUBuff, self.postMemBuff)
        #self.fetch = fetch.Fetch(instruction, opcodes, opcodeStr, dataval, address, arg1, arg2,
        #                        arg3, numInstrs, destReg, src1Reg, src2Reg)

        self.outputFileName = SetUp.get_output_filename()


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

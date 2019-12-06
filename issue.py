class issue:

    def __init__(self, instruction, opcodes, opcodeStr, dataval, address, arg1, arg2,
                                 arg3, numInstrs, destReg, src1Reg, src2Reg):

        self.instruction = instruction
        self.opcodes = opcodes
        self.opcodeStr = opcodeStr
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstrs = numInstrs
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg


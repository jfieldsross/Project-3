
class Fetch:

    def __init__(self, instruction, opcodeStr, dataval, address, arg1, arg2,
                                 arg3, numInstructions, destReg, src1Reg, src2Reg,
                                 preALUBuff, postALUBuff, PC, cache, preIssueBuff):

        self.instruction = instruction
        self.opcodeStr = opcodeStr
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstrs = numInstructions
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.preALUBuff = preALUBuff
        self.postALUBuff = postALUBuff
        self.PC = PC
        self.cache = cache
        self.preIssueBuff = preIssueBuff

    def run(self):

        # if the second element in the buffer is -1, there is empty space
        # if there is no empty space, the fetch unit stalls
        emptyRoomInPreIssueBuffer = self.preIssueBuff[3] == -1

        # check to see if cache contains next instruction
        # instructionIndex = the index of the next instruction to be fetched
        instructionIndex = (self.PC - 96) / 4
        # cacheHit = boolean that equals true if there is a cache hit

        numIssued = 0
        cacheHit = self.cache.checkCache(-1, instructionIndex, -1, -1)
        notBranch = True

        while numIssued < 2 and emptyRoomInPreIssueBuffer and instructionIndex < self.numInstrs and cacheHit \
                and notBranch:

            notBranch = False
            notBreak = True
            hazard = False
            # before fetching following conditions must be true
            #notStalled = notBranch and cacheHit and emptyRoomInPreIssueBuffer

            if cacheHit:
                #TODO decode the instruction

                if self.opcodeStr[instructionIndex] == "B": #Branch w/o checks
                    self.PC = self.PC + ((4 * self.arg1[instructionIndex]) - 4)

                elif self.opcodeStr[instructionIndex] == "CBZ": #Conditional Branch if Zero and checks for hazard
                    if self.R[self.arg2[instructionIndex]] == 0:
                        for i in range(len(self.preIssueBuff)):
                            if self.preIssueBuff[i] != -1:
                                if self.src1Reg[instructionIndex] == self.destReg[self.preIssueBuff[i]] or self.src2Reg[instructionIndex] == self.destReg[self.preIssueBuff[i]]:
                                    hazard = True
                        if not hazard: #if there's no hazards jump PC
                            self.PC = self.PC + ((4 * self.arg1[instructionIndex]) - 4)

                elif self.opcodeStr[instructionIndex] == "CBNZ": #Conditional Branch if not zero and checks for hazard if hazard clear hazard
                    if self.R[self.arg2[instructionIndex]] != 0:
                        for i in range(len(self.preIssueBuff)):
                            if self.preIssueBuff[i] != -1:
                                if self.src1Reg[instructionIndex] == self.destReg[self.preIssueBuff[i]] or self.src2Reg[instructionIndex] == self.destReg[self.preIssueBuff[i]]:
                                    hazard = True
                        if not hazard:
                            self.PC = self.PC + ((4 * self.arg1[instructionIndex]) - 4)

                elif self.opcodeStr[instructionIndex] == "NOP":
                    self.PC += 4
                    notBranch = True

                elif self.opcodeStr[instructionIndex] == "BREAK":
                    notBreak = False
                    notBranch = True

                else: # Let's Fetch!
                    notBranch = True
                    i = 0
                    while self.preIssueBuff[i] != -1:
                        i += 1
                    self.preIssueBuff[i] = instructionIndex
                    self.PC += 4
                    instructionIndex = (self.PC - 96) / 4
                    numIssued += 1

            cacheHit = self.cache.checkCache(-1, instructionIndex, -1, -1)


        #before fetching following conditions must be true
        #notStalled = notBranch and cacheHit and emptyRoomInPreIssueBuffer

        return notBreak

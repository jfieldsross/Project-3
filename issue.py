class Issue:

    def __init__(self, instruction, opcodes, opcodeStr, dataval, address, arg1, arg2,
                                arg3, numInstrs, destReg, src1Reg, src2Reg, preIssueBuff,
                                preALUBuff, preMemBuff):

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
        self.preIssueBuff = preIssueBuff
        self.preALUBuff = preALUBuff
        self.preMemBuff = preMemBuff

    # this method issues the given instruction to the preMemBuff
    # warning: do not call this method until all necessary conditions have been met!
    @classmethod
    def issueMemInstruction(self, instructionIndex):
        if self.preMemBuff[0] == -1:
            self.preMemBuff[0] = instructionIndex
        elif self.preMemBuff[1] == -1:
            self.preMemBuff[1] = instructionIndex
        else:
            print("ERROR!!! trying to issue an instruction into preMemBuff while there is no room")

    # this method issues the given instruction to the preALUBuff
    # warning: do not call this method until all necessary conditions have been met!
    @classmethod
    def issueALUInstruction(self, instructionIndex):
        if self.preALUBuff[0] == -1:
            self.preALUBuff[0] = instructionIndex
        elif self.preALUBuff[1] == -1:
            self.preALUBuff[1] = instructionIndex
        else:
            print("ERROR!!! trying to issue an instruction into preALUBuff while there is no room")

    def run(self):

        # if there is no room in the preALUBuff or preMemBuff then instructions
        # of that type can't be issued this cycle to avoid a structural hazard
        thereIsRoomInPreALUBuff = self.preALUBuff[1] == -1
        thereIsRoomInPreMemBuff = self.preMemBuff[1] == -1

        # if the instruction is load or store, it can't be issued until all prior stores
        # instructions are issued.
        # this variable will be set to True if there is a store instruction in the pre issue
        # buffer that can't be issued for any reason.
        storeInstructionSkippedThisCycle = False

        # for each instruction in the preIssueBuff, check to see if it can be issued.
        # if all conditions are met, issue the instruction via the issueMemInstruction()
        # or issueALUInstruction() methods
        for i in range(len(self.preIssueBuff)):

            # if the instruction is using the preMemBuff
            if self.opcodeStr[i] == "LDUR" or self.opcodeStr[i] == "STUR":

                # if there is an empty spot in the preMemBuff AND no skip instructions
                # have been skipped this cycle
                if thereIsRoomInPreMemBuff and not storeInstructionSkippedThisCycle:
                    # this method issues the instruction to the preMemBuff
                    self.issueMemInstruction(i)

                    # check to see if the buffer is full after issuing a new instruction to it
                    thereIsRoomInPreMemBuff = self.preMemBuff[1] == -1

                # if the mem instruction doesn't get issued, AND is a store instruction,
                # then storeInstructionSkippedThisCycle must be set to True
                elif self.opcodeStr[i] == "STUR":
                    storeInstructionSkippedThisCycle = True

            # TODO: Add non-mem instructions

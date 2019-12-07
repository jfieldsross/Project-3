from helpers import SetUp
import simulator


class Issue:

    def __init__(self, instruction, opcodes, opcodeStr, dataval, address, arg1, arg2,
                                arg3, numInstrs, destReg, src1Reg, src2Reg, preIssueBuff,
                                preALUBuff, preMemBuff, postALUBuff, postMemBuff):

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
        self.postALUBuff = postALUBuff
        self.postMemBuff = postMemBuff

    # this method checks for Read After Write hazards between the current
    # instruction and the other instructions in the buffers
    # returns False if there is a hazard, True otherwise
    def RAWCheck(self, curr):

        index = self.preIssueBuff[curr]

        if curr > 0:
            for i in range(0, curr):
                if self.src1Reg[index] == self.destReg[self.preIssueBuff[i]] or self.src2Reg[index] == self.destReg[self.preIssueBuff[i]]:
                    # found RAW in preIssueBuff
                    return False

        # see if there is a RAW in the preMemBuff
        for i in range(0, len(self.preMemBuff)):
            if self.preMemBuff[i] != -1:
                if self.src1Reg[index] == self.destReg[self.preMemBuff[i]] or self.src2Reg[index] == self.destReg[self.preMemBuff[i]]:
                    # found RAW in preMemBuff
                    return False

        # see if there is a RAW in the preALUBuff
        for i in range(0, len(self.preALUBuff)):
            if self.preALUBuff[i] != -1:
                if self.src1Reg[index] == self.destReg[self.preALUBuff[i]] or self.src2Reg[index] == self.destReg[self.preALUBuff[i]]:
                    # found RAW in preALUBuff
                    return False

        # see if there is a RAW in the post buffs too
        if self.postALUBuff[1] != -1:
            if self.src1Reg[index] == self.destReg[self.postALUBuff[1]] or self.src2Reg[index] == self.destReg[self.postALUBuff[1]]:
                # found RAW in postALUBuff
                return False

        # if there are no RAW hazards, return True
        return True

    def run(self):

        numInPreIssueBuffer = 0
        numIssued = 0
        curr = self.preIssueBuff[0]

        # if the instruction is load or store, it can't be issued until all prior stores
        # instructions are issued.
        # this variable will be set to True if there is a store instruction in the pre issue
        # buffer that can't be issued for any reason.
        storeInstructionSkippedThisCycle = False

        # count how many entries in the preIssueBuff have instructions in them
        for i in range(len(self.preIssueBuff)):
            if i != -1:
                numInPreIssueBuffer += 1

        while (numIssued < 2 and numInPreIssueBuffer > 0 and curr < 4):
            # if there is no room in the preALUBuff or preMemBuff then instructions
            # of that type can't be issued this cycle to avoid a structural hazard
            thereIsRoomInPreALUBuff = self.preALUBuff[1] == -1
            thereIsRoomInPreMemBuff = self.preMemBuff[1] == -1

            index = self.preIssueBuff[curr]
            issueMe = False

            if index != -1:
                # if the instruction is a mem instruction and there is room in the pre mem buffer
                if SetUp.isMemOp(self.opcodeStr[index]) and thereIsRoomInPreMemBuff:
                    # RAWCheck method will check if there are any RAW hazards with the current instruction
                    # issueMe will equal True if there are no RAW hazards, false if there are
                    issueMe = self.RAWCheck(curr)

                # if the instruction is an ALU instruction and there is room in the pre ALU buffer
                if (not SetUp.isMemOp(self.opcodeStr[index])) and thereIsRoomInPreALUBuff:
                    # RAWCheck method will check if there are any RAW hazards with the current instruction
                    # issueMe will equal True if there are no RAW hazards, false if there are
                    issueMe = self.RAWCheck(curr)

                # if the instruction is a store instruction, and it isn't being issued,
                # then no subsequent mem instructions may be issued for the rest of the cycle
                if self.opcodeStr[index] == "STUR" and not issueMe:
                    storeInstructionSkippedThisCycle = True

                # if the instruction is a mem instruction, check to see that all previous store
                # instructions have been issued. If not, the instruction may not be issued this cycle
                if SetUp.isMemOp(self.opcodeStr[index]) and storeInstructionSkippedThisCycle:
                    issueMe = False


                # if issueMe = True at this point, it has passed all of the tests and met all
                # of the necessary criteria to be issued!
                if issueMe:
                    numIssued += 1
                    # copy the instruction to the appropriate buffer
                    if SetUp.isMemOp(self.opcodeStr[index]):
                        self.preMemBuff[self.preMemBuff.index(-1)] = index
                    else:
                        self.preALUBuff[self.preALUBuff.index(-1)] = index

                    # move the instrs in the preIssueBuff down one level
                    self.preIssueBuff[0:curr] = self.preIssueBuff[0:curr]
                    self.preIssueBuff[curr:3] = self.preIssueBuff[curr + 1:]  # dropped 4, think will go to end always
                    self.preIssueBuff[3] = -1
                    numInPreIssueBuffer -= 1
                else:
                    # move on to the next instruction in preIssueBuff
                    curr += 1
            else:
                # move on to the next instruction in preIssueBuff
                curr += 1
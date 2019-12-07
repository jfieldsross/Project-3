from helpers import SetUp
import os
import masking_constants as MASKs
import sys


class dissasembler:
    opcodeStr = []
    instrSpaced = []
    arg1 = []
    arg2 = []
    arg3 = []
    arg1Str = []
    arg2Str = []
    arg3Str = []
    dataval = []
    rawdata = []
    address = []
    numInstructs = 0
    destReg = []
    src1Reg = []
    src2Reg = []
    instructions = []

    def run(self):

        self.instructions = SetUp.import_data_file()
        for i in self.instructions:
            print(i)

        outputFilename = SetUp.get_output_filename()

        print("raw output filename is ", outputFilename)

        print(hex(MASKs.bMask))
        print(bin(MASKs.bMask))
        print(f'{MASKs.bMask:032b}')

        for i in range(len(self.instructions)):
            self.address.append(96 + (i*4))

        opcode = []

        for z in self.instructions:
            opcode.append(int(z, base=2) >> 21)

        for i in range(len(opcode)):
            self.numInstructs = self.numInstructs + 1
            if opcode[i] == 1112:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("ADD")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append((self.arg2[i]))
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
            elif opcode[i] == 1624:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("SUB")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append((self.arg2[i]))
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
            elif opcode[i] == 1104:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("AND")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append((self.arg2[i]))
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
            elif opcode[i] == 1360:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("ORR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append((self.arg2[i]))
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
            elif opcode[i] >= 160 and opcode[i] <= 191:
                self.instrSpaced.append(SetUp.bin2StringSpacedB(self.instructions[i]))
                self.opcodeStr.append("B")
                bImm = int(self.instructions[i], base=2) & MASKs.bMask
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter(bImm, 26))
                self.arg2.append(0)
                self.arg3.append(0)
                self.destReg.append(-1)
                self.src1Reg.append(-2)
                self.src2Reg.append(-3)
                self.arg1Str.append("\t#" + str(self.arg1[i]))
                self.arg2Str.append("")
                self.arg3Str.append("")
            elif opcode[i] >= 1160 and opcode[i] <= 1161:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(self.instructions[i]))
                self.opcodeStr.append("ADDI")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.imMask) >> 10)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append(-4)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
            elif opcode[i] >= 1672 and opcode[i] <= 1673:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(self.instructions[i]))
                self.opcodeStr.append("SUBI")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.imMask) >> 10)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append(-5)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
            elif opcode[i] == 1986:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(self.instructions[i]))
                self.opcodeStr.append("LDUR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.addrMask) >> 12)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg2[i]))
                self.src2Reg.append(-6)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg1[i]) + "]")
            elif opcode[i] == 1984:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(self.instructions[i]))
                self.opcodeStr.append("STUR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.addrMask) >> 12)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg2[i])
                self.src1Reg.append((self.arg3[i]))
                self.src2Reg.append(-7)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg1[i]) + "]")
            elif opcode[i] >= 1440 and opcode[i] <= 1447:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(self.instructions[i]))
                self.opcodeStr.append("CBZ")
                cbAddr = (int(self.instructions[i], base=2) & MASKs.addr2Mask) >> 5
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter(cbAddr, 19))
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.arg3.append(0)
                self.destReg.append(-8)
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(-9)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")
            elif opcode[i] >= 1448 and opcode[i] <= 1455:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(self.instructions[i]))
                self.opcodeStr.append("CBNZ")
                cbnzAddr = (int(self.instructions[i], base=2) & MASKs.addr2Mask) >> 5
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter(cbnzAddr, 19))
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.arg3.append(0)
                self.destReg.append(-10)
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(-11)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")
            elif opcode[i] >= 1684 and opcode[i] <= 1687:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(self.instructions[i]))
                self.opcodeStr.append("MOVZ")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.imsftMask) >> 21)
                self.arg1[i] = self.arg1[i] * 16
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.imdataMask) >> 5)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(-12)
                self.src2Reg.append(-13)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(" ," + str(self.arg2[i]) + ", LSL")
                self.arg3Str.append(" " + str(self.arg1[i]))
            elif opcode[i] >= 1940 and opcode[i] <= 1943:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(self.instructions[i]))
                self.opcodeStr.append("MOVK")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.imsftMask) >> 21)
                self.arg1[i] = self.arg1[i] * 16
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.imdataMask) >> 5)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(-14)
                self.src2Reg.append(-15)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(" ," + str(self.arg2[i]) + ", LSL")
                self.arg3Str.append(" " + str(self.arg1[i]))
            elif opcode[i] == 1690:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("LSR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.shmtMask) >> 10)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1)
                self.src2Reg.append(-16)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
            elif opcode[i] == 1691:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("LSL")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.shmtMask) >> 10)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-17)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
            elif opcode[i] == 1692:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("ASR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.shmtMask) >> 10)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-18)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
            elif opcode[i] == 1872:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("EOR")
                self.arg1.append((int(self.instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(self.instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(self.instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.destReg.append(self.arg3[i])
                self.src1Reg.append((self.arg1[i]))
                self.src2Reg.append((self.arg2[i]))
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
            elif opcode[i] == 0:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(self.instructions[i]))
                self.opcodeStr.append("NOP")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.destReg.append(-19)
                self.src1Reg.append(-20)
                self.src2Reg.append(-21)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
            elif opcode[i] == 2038 and (int(self.instructions[i], base=2) & MASKs.specialMask) == 2031591:
                self.instrSpaced.append(SetUp.bin2StringSpaced(self.instructions[i]))
                self.opcodeStr.append("BREAK")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.destReg.append(-22)
                self.src1Reg.append(-23)
                self.src2Reg.append(-24)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print("breaking")
                break
            else:
                self.opcodeStr.append("unknown")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.destReg.append(-25)
                self.src1Reg.append(-26)
                self.src2Reg.append(-27)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print("i =: " + str(i))
                print("opcode =: " + str(opcode[i]))
                sys.exit("You have found an unknown instruction, investigate NOW")

        #Reading Raw Data
        k = self.numInstructs

        while k < len(opcode):
            self.rawdata.append(self.instructions[k])
            k = k + 1

        for i in range(len(self.rawdata)):
            self.dataval.append(SetUp.immSignedToTwosConverter(int(self.rawdata[i], base=2)))

        return {
            "opcodes":opcode,
            "opcodeStr":self.opcodeStr,
            "arg1":self.arg1,
            "arg1Str":self.arg1Str,
            "arg2":self.arg2,
            "arg2Str":self.arg2Str,
            "arg3":self.arg3,
            "arg3Str":self.arg3Str,
            "dataval":self.dataval,
            "address":self.address,
            "numInstructions":self.numInstructs,
            "destReg":self.destReg,
            "src1Reg":self.src1Reg,
            "src2Reg":self.src2Reg,
            "instruction":self.instructions}

    def print(self):
        outFile = open(SetUp.get_output_filename() + "_dis.txt", 'w')

        for i in range(self.numInstructs):
            outFile.write(str(self.instrSpaced[i]) + '\t' + str(self.address[i]) + '\t' + str(self.opcodeStr[i]) + str(self.arg1Str[i]) + str(self.arg2Str[i]) + str(self.arg3Str[i]) + '\n')

        for i in range(len(self.dataval)):
            outFile.write(self.rawdata[i] + '\t' + str(self.address[self.numInstructs + i]) + '\t' + str(self.dataval[i]) + '\n')

        outFile.close()
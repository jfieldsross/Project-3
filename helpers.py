import sys

class SetUp:

    def __init__(self):
        pass

    @classmethod
    def get_input_filename(cls):
        for i in range(len(sys.argv)):
            if(sys.argv[i] == '-i' and i < (len(sys.argv) -1)):
                inputFileName = sys.argv[i + 1]

        return inputFileName

    @classmethod
    def get_output_filename(cls):

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-o' and i < (len(sys.argv) -1)):
                outputFileName = sys.argv[i + 1]

        return outputFileName


    @classmethod
    def import_data_file(cls):

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]

        try:
            instructions = [line.rstrip() for line in open(inputFileName, 'r')]
        except IOError:
            print("Could not open input file, is path correct?")

        return instructions

    @classmethod
    def imm_bit_to_32_bit_converter(cls, num, bitsize):
        negBitMask = 2**(bitsize - 1)  # bit mask to determine if the first digit is a 1 or 0
        extendMask = 0

        i = 31
        while (i >= bitsize):
            extendMask += 2**i
            i -= 1

        if (negBitMask & num) > 0:
            num = num | extendMask  # extend to 32 bits
            num = num ^ 0xFFFFFFFF  # toggle bits
            num = num + 1  # add 1
            num = num * -1  # make negative
        return num

    @classmethod
    def immSignedToTwosConverter(cls, num): #num is assumed to be 32 bits
        negBitMask = 0x80000000
        bitFlipMask = 0xFFFFFFFF  # num xor bitFlipMask toggles all bits except for the first one
        #Changed bitFlipMask to mirror method above. prior gave incorrect response. --JFR
        if (num & negBitMask) > 0:  #if number is negative
            # convert to twos complement by flipping bits and adding 1
            num = num ^ bitFlipMask
            num += 1
            num = num * -1
        # if num is positive, it is already in twos complement :)

        return num

    @classmethod
    def bin2StringSpaced(cls, s):
        spacedStr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedD(cls, s):
        spacedStr = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedIM(cls, s):
        spacedStr = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedCB(cls, s):
        spacedStr = s[0:8] + " " + s[8:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedI(cls, s):
        spacedStr = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr;

    @classmethod
    def bin2StringSpacedR(cls, s):
        spacedStr = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedB(cls, s):
        spacedStr = s[0:6] + " " + s[6:32]
        return spacedStr

    @classmethod
    def imm_32_bit_unsigned_to_32_bit_signed_converter(cls, num):
        firstBitOneMask = 0X80000000 #or
        firstBitZeroMask = 0X7FFFFFFF #and
        if (num < 0):
            num = num | firstBitOneMask
        else:
            num = num & firstBitZeroMask
        return num

    @classmethod
    def decimalToBinary(cls, num):
        if num > 1:
            cls.decimalToBinary(num // 2)
        print(num % 2, end='')

    @classmethod
    def binaryToDecimal(cls, binary):
        print("\n")
        print(int(binary, 2))
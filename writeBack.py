from helpers import SetUp

class WriteBack:

    def __init__(self, R, postMemBuff, postALUBuff, destReg):
        self.R = R
        self.postMemBuff = postMemBuff
        self.postALUBuff = postALUBuff
        self.destReg = destReg

    def run(self):

        # if there is a valid instruction index in the postMemBuff
        if self.postMemBuff[1] != -1:
            # write the value to the corresponding register
            self.R[self.destReg[self.postMemBuff[1]]] = self.postMemBuff[0]
            self.postMemBuff = [-1, -1]

        # same as above, but for the postALUBuff instead of postMemBuff
        if self.postALUBuff[1] != -1:
            self.R[self.destReg[self.postALUBuff[1]]] = self.postALUBuff[0]
            self.postALUBuff = [-1, -1]


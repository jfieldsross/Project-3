import writeBack

#This file is used to test the WriteBack class

R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

postMemBuff = [2, 2]
postALUBuff = [4, 1]
destReg = [0, 17, 3]

WB = writeBack.WriteBack(R, postMemBuff, postALUBuff, destReg)
WB.run()

print(R)
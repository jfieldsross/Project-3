import sys


class masking_constants:
    global bMask
    bMask = 0x3FFFFFF
    global jAddrMask
    jAddrMask = 0xFC000000
    global specialMask
    specialMask = 0x1FFFFF
    global rnMask
    rnMask = 0x3E0
    global rmMask
    rmMask = 0x1F0000
    global rdMask
    rdMask = 0x1F
    global imMask
    imMask = 0x3FFc00
    global shmtMask
    shmtMask = 0xFC00
    global addrMask
    addrMask = 0x1FF000
    global addr2Mask
    addr2Mask = 0xFFFFE0
    global imsftMask
    imsftMask = 0x600000
    global imdataMask
    imdataMask = 0x1FFFE0
# alu_tests.asm
#
# Expected output: 
# 4
# 6
# 0
# 255
# 16320
# 255
# 3

# Test
LDI R0, 20
LDI R1, 6
AND R0, R1
PRN R0
OR R0, R1
PRN R0
XOR R0, R1
PRN R0
NOT R0
PRN  R0
SHL R0, R1
PRN R0
SHR R0, R1
PRN R0
MOD R0, R1
PRN R0
HLT

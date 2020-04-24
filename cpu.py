"""CPU functionality."""

import sys

CALL = 0b01010000
HLT = 0b00000001
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110
LDI = 0b10000010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
ST = 0b10000100
# ALU ops
ADD = 0b10100000
AND = 0b10101000
CMP = 0b10100111
DIV = 0b10100011
MOD = 0b10100100
MUL = 0b10100010
NOT = 0b01101001
OR = 0b10101010
SHL = 0b10101100
SHR = 0b10101101
SUB = 0b10100001
XOR = 0b10101011
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.fl = 0b00000000
        self.register[SP] = 0xF4
        self.branchtable = {
            CALL: self.call,
            HLT : self.hlt,
            JEQ : self.jeq,
            JMP : self.jmp,
            JNE : self.jne,
            LDI : self.ldi,
            POP : self.pop,
            PRA : self.pra,
            PRN : self.prn,
            PUSH : self.push,
            RET : self.ret,
            ST : self.st,
            ADD : self.alu,
            AND : self.alu,
            CMP : self.alu,
            DIV : self.alu,
            MOD : self.alu,
            MUL : self.alu,
            NOT : self.alu,
            OR : self.alu,
            SHL : self.alu,
            SHR : self.alu,
            SUB : self.alu,
            XOR : self.alu
        }
    
    def call(self, op_a, op_b=None):
        '''
        Calls a subroutine(function) at address stored in register[op_a]
        '''
        # Decriment SP
        self.register[SP] -= 1
        # Write return point
        self.ram_write(self.register[SP], self.pc + 2)
        # Set pc to subroutine at register[op_a]
        self.pc = self.register[op_a]
    
    # No operands but cleaner to pass as unused paramters here
    def hlt(self, op_a=None, op_b=None):
        '''
        Halt cpu and exit emulator
        '''
        sys.exit()
    
    def jeq(self, op_a, op_b=None):
        '''
        Check 'Equal' flag. If true, jump to register[op_a]
        '''
        if self.fl & 0b1 == 1:
            self.pc = self.register[op_a]
        else:
            self.pc += 2

    def jmp(self, op_a, op_b=None):
        '''
        Jump to the address stored in register[op_a]
        '''
        self.pc = self.register[op_a]
    
    def jne(self, op_a, op_b=None):
        '''
        Check 'Equal' flag. If clear, jump to register[op_a]
        '''
        if self.fl & 0b1 == 0:
            self.pc = self.register[op_a]
        else:
            self.pc += 2
    
    def ldi(self, op_a, op_b):
        '''
        Set the value of register[op_a] to op_b
        '''
        self.register[op_a] = op_b 
    
    def pop(self, op_a, op_b=None):
        '''
        Pop the value at the top of the stack into register[op_a]
        '''
        # Get value from ram at SP in register
        value = self.ram_read(self.register[SP])
        # Set register at address given to value
        self.register[op_a] = value
        # Increment SP
        self.register[SP] += 1
        return value
      
    def pra(self, op_a, op_b=None):
        '''
        Print alpha character value stored in the given register
        '''
        print(chr(self.register[op_a]))
        
    # Only one operand but was cleaner to just pass them as unused parameters here
    def prn(self, op_a, op_b=None):
        '''
        Print numeric value stored in register[op_a]
        '''
        print(self.register[op_a])

    def push(self, op_a, op_b=None):
        '''
        Push the value in the register[op_a] onto the stack
        '''
        # Decriment SP
        self.register[SP] -= 1
        # Write value given to ram at SP address
        self.ram_write(self.register[SP], self.register[op_a])
    
    def ret(self, op_a=None, op_b=None):
        '''
        Return from subroutine
        '''
        self.pc = self.ram_read(self.register[SP])
        self.register[SP] += 1

    def st(self, op_a, op_b):
        '''
        Store value in register[op_b] in the address stored in register[op_a]
        '''
        self.ram_write(self.register[op_a], self.register[op_b])


    def load(self, filename):
        """Load a program into memory."""

        # Counter
        address = 0

        # Open ls8 file
        with open(filename) as f:
            # Read each line
            for line in f:
                # Split on # to remove comments
                line = line.split('#')
                # Remove empty spaces
                line = line[0].strip()
                if line == '':
                    continue
                # Convert to int (base 2 binary) and save to ram at address
                self.ram[address] = int(line, 2)
                # Incriment address counter
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.register[reg_a] += self.register[reg_b]

        elif op == AND:
            self.register[reg_a] &= self.register[reg_b]

        elif op == CMP:
            op_a = self.register[reg_a]
            op_b = self.register[reg_b]
            if op_a == op_b:
                self.fl = 0b00000001
            elif op_a < op_b:
                self.fl = 0b00000100
            elif op_a > op_b:
                self.fl = 0b00000010

        elif op == DIV:
            if self.register[reg_b] != 0:
                self.register[reg_a] /= self.register[reg_b]
            else:
                raise Exception("Cannot divide by 0")
        
        elif op == MOD:
            if self.register[reg_b] != 0:
                self.register[reg_a] %= self.register[reg_b]
            else:
                raise Exception('Cannot divide by 0')

        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        
        elif op == NOT:
            self.register[reg_a] ^= 0b11111111
        
        elif op == OR:
            self.register[reg_a] |= self.register[reg_b]

        elif op == SHL:
            self.register[reg_a] <<= self.register[reg_b]

        elif op == SHR:
            self.register[reg_a] >>= self.register[reg_b]

        elif op == SUB:
            self.register[reg_a] -= self.register[reg_b]

        elif op == XOR:
            self.register[reg_a] ^= self.register[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, mar):
        '''
        Takes address (mar) in ram and returns the value (mdr) stored there
        '''
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mar, mdr):
        '''
        Stores 'value' (MDR) at given 'address' (MAR) in ram
        '''
        self.ram[mar] = mdr

    def run(self):
        '''
        Run the CPU
        '''

        # TODO: Include interupt handler
        
        while True:
            # Get opcodes and operands
            ir = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            # To update self.pc counter
            run_counter = (ir >> 6) + 1
            # To handle alu operations
            # NOTE: Less code but adds another if statement, may be quicker to implement
                  # individual helper functions that call ALU with specified operations
            alu_op = ((ir >> 5) & 0b1)
            # To handle ops that set pc
            set_pc = ((ir >> 4) & 0b1)
    
            if ir in self.branchtable:
                if alu_op:
                    self.branchtable[ir](ir, op_a, op_b)
                else:
                    self.branchtable[ir](op_a, op_b)
            else:
                print('Unsupported operation')
            if not set_pc:
                self.pc += run_counter
    

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

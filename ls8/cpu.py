"""CPU functionality."""

import sys
LDI = 0b10000010  # LDI R0,8
PRN = 0b01000111  # PRN R0
HLT = 0b00000001  # HLT
MUL = 0b10100010  # MUL R0,R1
ADD = 0b10100000  # ADD R0, R1
PUSH = 0b01000101  # PUSH R0
POP = 0b01000110  # POP R0
CALL = 0b01010000  # CALL R1
RET = 0b00010001  # RET
# Initialize and set default for our StackPointer
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # this is our memory
        self.pc = 0  # the Program Counter ~~> aka indexof the current instruction
        self.running = True  # a variable used to run our RUN repl
        # this is our registry as we do not want to write everythin to our RAM. Just what we are using
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.branch_table = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.mul,
            ADD: self.add,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret
        }

    def mul(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def add(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def hlt(self):
        # print('self.running before tiggle', self.running)
        self.pc += 1
        self.running = False
        # print('self.running after tiggle', self.running)

    def prn(self):
        # save our MAR to a variable using ram_read()
        reg_num = self.ram_read(self.pc + 1)
        # print out our variable above in order to PRN properly
        # TODO read from register NOT ram
        print("PRN:", self.reg_read(reg_num))
        # increment to the next command in the stack past our MAR & MDR
        self.pc += 2

    def ldi(self):
        # get the LDI's MAR, which we designed to be the very next index of LDI
        reg_num = self.ram_read(self.pc + 1)
        # get the LDI's MDR which we designed to be 2 away from our LDI index
        reg_val = self.ram_read(self.pc + 2)
        # we then need to run our write function in order to access the MAR + MDR

        self.reg_write(reg_num, reg_val)
        # we know that an LDI has an MAR & MDR to follow so we need to skip those two indecies in order to move through the stack cleanly
        self.pc += 3

    def push(self):
        self.reg[SP] -= 1
        # Get the value we want to store from the register
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]  # <-- this is the value that we want to push
        # Figure out where to store it
        top_of_stack_addr = self.reg[SP]
        # Store it
        self.ram[top_of_stack_addr] = value
        self.pc += 2

    def pop(self):
        top_stack_val = self.reg[SP]
        # lets get the register address
        reg_addr = self.ram[self.pc + 1]
        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[reg_addr] = self.ram[self.reg[SP]]

        self.reg[SP] += 1
        self.pc += 2

        """
        OVERVIEW
        - take the value out of ram and copy that to the register
        - then increment the stack pointer
        PLAN:
        - find the stack pointer in memory and extract its value
        - we then copy that SP memory value to the register at the position provided with the POP function
        - incrment the stack pointer
        """

    def call(self):
        return_addr = self.pc + 2  # Where we're going to RET to
        # Push on the stack
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = return_addr
        # Get the address to call
        reg_num = self.ram[self.pc + 1]
        subroutine_addr = self.reg[reg_num]

        # Call it
        self.pc = subroutine_addr

    def ret(self):
        """ Return from subroutine.
            Pop the value from the top of the stack and store it in the `PC`.
        """
        top_stack_val = self.reg[SP]
        # lets get the register address
        reg_addr = self.ram[self.pc + 1]
        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[reg_addr] = self.ram[self.reg[SP]]
        # print('asdfasdfsdaf', self.ram[self.reg[SP]])
        self.reg[SP] += 1
        self.pc = self.reg[reg_addr]

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as f:
            for line in f:
                # split our enumerated list at any hashmark which indicates a comment
                line = line.split('#')
                # print("\/\/ line[0]", line[0])

                try:
                    # we access line[0] bc this is the 0th index in our enumerated list and we do not want any thing past it.
                    v = int(line[0], 2)  # working at a base 2 level
                    # print("    hello v ", v)
                except ValueError:
                    continue

                self.ram[address] = v

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        """ Memory Address Register: holds our address in memory which we read or write to """
        mar_reg = self.ram[mar]  # this varible holds the current index of our Memory Address Register
        return mar_reg

    def ram_write(self, mar, mdr):
        """ Memory Data Register: assigns data to a piece of memory at a specific address """
        self.ram[mar] = mdr  # this simply gives us our value at the MAR given

    def reg_read(self, mar):
        """ Memory Address Register: holds our address in memory which we read or write to """
        mar_reg = self.reg[mar]  # this varible holds the current index of our Memory Address Register
        return mar_reg

    def reg_write(self, mar, mdr):
        """ Memory Data Register: assigns data to a piece of memory at a specific address """
        self.reg[mar] = mdr  # this simply gives us our value at the MAR given

    def run(self):
        """Run the CPU."""
        # while the CPU is running do some cool stuff
        while self.running:
            # store our Instruction Register at the place in memory at the index of our current PC
            # ir = self.ram[self.pc]
            ir = self.ram[self.pc]
            # print("IR", ir)

            # branch_table = {
            #     LDI: self.ldi,
            #     PRN: self.prn,
            #     HLT: self.hlt,
            #     MUL: self.mul,
            #     PUSH: self.push,
            #     POP: self.pop
            # }

            if ir in self.branch_table:
                self.branch_table[ir]()

            # otherwise we want to tell our user what the issue is with the cpu run method
            else:
                print(f"Unknown expression {ir} at address {self.pc}")
                sys.exit(1)

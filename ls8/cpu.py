"""CPU functionality."""

import sys
LDI = 0b10000010  # LDI R0,8
PRN = 0b01000111  # PRN R0
HLT = 0b00000001  # HLT
MUL = 0b10100010  # MUL R0,R1


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # this is our memory
        self.pc = 0  # the Program Counter ~~> aka indexof the current instruction
        self.running = True  # a variable used to run our RUN repl
        self.reg = [0] * 8

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

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

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
            ir = self.ram[self.pc]
            # print("IR", ir)

            # if our pc is on a LoaD Imediatley index then we need to...
            if ir == LDI:
                # get the LDI's MAR, which we designed to be the very next index of LDI
                reg_num = self.ram_read(self.pc + 1)
                # get the LDI's MDR which we designed to be 2 away from our LDI index
                reg_val = self.ram_read(self.pc + 2)
                # we then need to run our write function in order to access the MAR + MDR

                # TODO
                self.reg_write(reg_num, reg_val)
                # we know that an LDI has an MAR & MDR to follow so we need to skip those two indecies in order to move through the stack cleanly
                self.pc += 3

            # if our current index register finds a PRN statement we need to ...
            elif ir == PRN:
                # sasve our MAR to a variable
                reg_num = self.ram_read(self.pc + 1)
                # print out our variable above in order to PRN properly
                # TODO read from register NOT ram
                print("PRN:", self.reg_read(reg_num))
                # increment to the next command in the stack past our MAR & MDR
                self.pc += 2

            elif ir == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3

            # if we find a HLT command...
            elif ir == HLT:
                # stop the CPU from running...
                self.running = False
                # and move on in the stack.
                self.pc += 1

            # otherwise we want to tell our user what the issue is with the cpu run method
            else:
                print(f"Unknown expression {ir} at address {self.pc}")
                sys.exit(1)

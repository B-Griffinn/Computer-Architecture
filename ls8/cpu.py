"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 pieces of memory
        self.pc = 0  # index of current instruction - POINTER to an address in memory
        self.running = True  # running flag if necessary

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8 == 130
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mem_address_reg=None, mem_data_reg=None):
        """ accept the address to read and return the value stored there. """

        # loop thru ram in order to access MAR
        for i in range(0, len(self.ram)):
            # print(self.ram[i])
            if self.ram[i] == 130:  # that is the code for LDI R0,8
                # print(self.ram[i])
                # save our Memory Registration Address in a variable
                mem_address_reg = self.ram[i + 1]
                print('mem_address_reg', mem_address_reg)
                # print('mem_address_reg', mem_address_reg)
                # we know our Memory Data Register is right after our MAR
                mem_data_reg = self.ram[i + 2]
                print('mem_data_reg', mem_data_reg)
                # move the pointer up 3 posiitons so we do not count the MAR or MDR
                self.pc += 3
            elif self.ram[i] == 71:
                print("ELIF", mem_data_reg)
            elif self.ram[i] == 0:
                continue
            elif self.ram[i] == 1:
                break
        return mem_data_reg

    def ram_write(self, value=None, mem_address_reg=None):
        """ should accept a value to write, and the address to write it to. """
        # similar to ram_read() we need to loop through our ram and find the first
        for i in range(0, len(self.ram)):
            if self.ram[i] == 0 and self.ram[i + 1] == 0 and self.ram[i + 2] == 0:
                mem_address_reg = self.ram[i]
                self.ram[i + 1] = value
                print('MEM ADDRESS', mem_address_reg)
                print('VAL', self.ram[i + 1])
                break

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        pass


# TESTS
cpu_new = CPU()
cpu_new.load()
# print(cpu_new.ram_read())
print(cpu_new.ram_write("hello", 1))
# print(cpu_new.ram)

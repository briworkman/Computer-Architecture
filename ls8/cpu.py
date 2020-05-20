"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # * Program Counter
        self.pc = 0
        # * Memory storage for ram
        self.ram = [0] * 256
        # * 8 new registers
        self.reg = [0] * 8

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     LDI,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     PRN,  # PRN R0
        #     0b00000000,
        #     HLT,  # HLT
        # ]

        try:
            address = 0
            # open the file
            with open(sys.argv[1]) as f:
                # read every line
                for line in f:
                    # parse out comments
                    comment_split = line.strip().split("#")
                    # Cast number string to int
                    value = comment_split[0].strip()
                    # ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # populate memory array
                    self.ram[address] = instruction
                    address += 1

        except:
            print("cant find file")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
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

    # * mar = memory address register
    # * mdr = memory data register

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        halt = False

        while not halt:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction == MUL:
                self.alu(instruction, operand_a, operand_b)
                self.pc += 3
            elif instruction == HLT:
                sys.exit(0)
            elif instruction == PUSH:
                value = self.reg[operand_a]
                self.reg[7] -= 1
                self.ram_write(value, self.reg[7])
                self.pc += 2
            elif instruction == POP:
                self.reg[operand_a] = self.ram_read(self.reg[7])
                value = self.reg[operand_a]
                self.reg[7] += 1
                self.pc += 2
            else:
                print("Unknown instruction")
                sys.exit(1)

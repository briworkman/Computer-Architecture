import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.SP = 7
        self.fl = 5
        self.l = 0
        self.g = 0
        self.e = 0
        self.reg[self.SP] = 0xF4
        self.instruction = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b10100000: self.add,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE
        }

    def HLT(self, op1, op2):
        return (0, False)

    def LDI(self, op1, op2):
        self.reg[op1] = op2
        return (3, True)

    def PRN(self, op1, op2):
        print(self.reg[op1])
        return (2, True)

    def MUL(self, op1, op2):
        self.alu("MUL", op1, op2)
        return (3, True)

    def add(self, op1, op2):
        self.alu('ADD', op1, op2)
        return (3, True)

    def call(self, op1, op2):
        self.SP -= 1
        self.ram[self.SP] = self.pc + 2
        self.pc = self.reg[op1]
        return (0, True)

    def ret(self, op1, op2):
        self.pc = self.ram[self.SP]
        return (0, True)

    def CMP(self, op1, op2):
        self.alu("CMP", op1, op2)
        return (3, True)

    def JMP(self, op1, op2):
        # * Jump to the address stored in the given register
        # * Set the `PC` to the address stored in the given register.
        self.pc = self.reg[op1]
        return (0, True)

    def JEQ(self, op1, op2):
        # * If `equal` flag is set(true), jump to the address stored in the given register.
        if self.e == 1:
            self.pc = self.reg[op1]
            return (0, True)
        else:
            return (2, True)

    def JNE(self, op1, op2):
        # * If `E` flag is clear (false, 0), jump to the address stored in the given register.
        if self.e == 0:
            self.pc = self.reg[op1]
            return (0, True)
        else:
            return(2, True)

    def load(self, program):
        """Load a program into memory."""

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
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        elif op == "CMP":  # * compare two numbers in the register
            if self.reg[reg_a] == self.reg[reg_b]:
                # * if the numbers are equal , e(equal) = 1 for true, l(less than) = 0 for false, and g(greater than) = 0 for false
                self.e = 1
                self.l = 0
                self.g = 0
            elif self.reg[reg_a] <= self.reg[reg_b]:
                # * if the first number is less than the second number, e = 0, l = 1, g = 0
                self.e = 0
                self.l = 1
                self.g = 0
            else:
                # * if the first number is greater than the second number, e = 0, l = 0, g = 1
                self.e = 0
                self.l = 0
                self.g = 1
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
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def push(self, op1, op2):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[op1]
        return (2, True)

    def pop(self, op1, op2):
        self.reg[op1] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        return (2, True)

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram[self.pc]

            op1 = self.ram_read(self.pc + 1)
            op2 = self.ram_read(self.pc + 2)

            try:
                opo = self.instruction[instruction](op1, op2)
                running = opo[1]
                self.pc += opo[0]

            except:
                print("Unknown instruction")
                sys.exit(1)

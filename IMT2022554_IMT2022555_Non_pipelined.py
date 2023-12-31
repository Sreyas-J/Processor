import os

pc=0
clock=0
mem=[]
file_path = "Sorting.txt" 
dataMem=[]
regMem = []

with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

mem=file_contents.split('\n')

def decimal_to_binary(number, num_bits):
    if number >= 0:
        # For non-negative numbers, convert to binary as usual
        binary_representation = bin(number)[2:]
    else:
        # For negative numbers, convert to binary using two's complement
        binary_representation = bin(2**num_bits + number)[2:]

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding


def binary_to_decimal(number_str):
    if len(number_str) > 0 and number_str[0] == '1':
        # If the most significant bit is 1, indicating a negative number
        num_bits = len(number_str)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in number_str[1:])
        decimal_value = -int(inverted_bits, 2) - 1
    else:
        # If the most significant bit is 0, indicating a non-negative number
        decimal_value = int(number_str, 2)

    return decimal_value

instructions={
    "li":"li",
    "move":"move",
    "subi":"subi",
    "bgt":"bgt",
    "addiu":decimal_to_binary(9,6),
    "addu":decimal_to_binary(0,6),
    "add":decimal_to_binary(0,6),
    "beq":decimal_to_binary(4,6),
    "mul":decimal_to_binary(28,6),
    "lw":decimal_to_binary(35,6),
    "sw":decimal_to_binary(43,6),
    "addi":decimal_to_binary(8,6),
    "j":decimal_to_binary(2,6),
    "sub":decimal_to_binary(0,6),
    "slt":decimal_to_binary(0,6),

    "bne":decimal_to_binary(5,6)
} 

for i in range(32):
    regMem.append(0)

# regMem[0] = 0
regMem[9] = 4
regMem[10] = 0
regMem[11] = 24

# regMem[10] = 0
# regMem[11] = 8
for i in range(200):
    dataMem.append("0"*8)

# a=decimal_to_binary(5,32)
# dataMem[0] = a[0:8]
# dataMem[1] = a[8:16]
# dataMem[2] = a[16:24]
# dataMem[3] = a[24:32]

a = decimal_to_binary(2, 32)
b = decimal_to_binary(-3, 32)
c = decimal_to_binary(100, 32)
d = decimal_to_binary(10, 32)

dataMem[0] = a[0:8]
dataMem[1] = a[8:16]
dataMem[2] = a[16:24]
dataMem[3] = a[24:32]

dataMem[4] = b[0:8]
dataMem[5] = b[8:16]
dataMem[6] = b[16:24]
dataMem[7] = b[24:32]

dataMem[8] = c[0:8]
dataMem[9] = c[8:16]
dataMem[10] = c[16:24]
dataMem[11] = c[24:32]

dataMem[12] = d[0:8]
dataMem[13] = d[8:16]
dataMem[14] = d[16:24]
dataMem[15] = d[24:32]

class control_unit:

    def __init__(self,instruction):
        self.instruction = instruction
        self.op = instruction[0:6]
        self.control_signals = {
        "MemtoReg":0,# 1 => ALu res to register,0=> dataMem to reg /
        "MemWrite":0,#1=> writes into the data memory /
        "Branch":0,#1=>branch / 
        "AluControl":0,#000 AND, 001 OR, 010 add, 011 sub, 100 less than, 101 is mul /
        "AluSrc":0,#0=> from register 1=>imm /
        "RegDest":0,#0=>I format, 1=>R form /
        "RegWrite":0,#1=>Write back to register /
        "jump":0#1 is jump
        }

    def control_unit_assign(self,MemtoReg,MemWrite,Branch,AluCont,AluSrc,Regdst,regWr,jmp):
        self.control_signals["MemtoReg"] = MemtoReg
        self.control_signals["MemWrite"] = MemWrite
        self.control_signals["Branch"] = Branch
        self.control_signals["AluControl"] = AluCont
        self.control_signals["AluSrc"] = AluSrc
        self.control_signals["RegDest"] = Regdst
        self.control_signals["RegWrite"] = regWr
        self.control_signals["jump"] = jmp
    
    def alu_control(self):#return string
        if(self.op=="000000"):
            funct = self.instruction[26:32]
            if(funct=="100000"):  
                return "010"
            elif(funct=="100010"):
                return "011"
            elif(funct=="100100"):
                return "000"
            elif(funct=="100101"):
                return "001"
            elif(funct == "101010"):
                return "100"
            elif(funct == "100001"):
                return "010"
            elif(funct == "000010"):
                return "101"

def IF(instruction):
    global clock
    clock+=1
    return instruction[0:6]

def ID(opcode,control):
    global clock
    clock+=1

    if(opcode == "000000"):
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        rd=binary_to_decimal(mem[pc][16:21])

        funct = control.alu_control()

        control.control_unit_assign(1,0,0,funct,0,1,1,0)

        return [rs,rt,rd]
    
    elif(opcode=="000010"):

        control.control_unit_assign(1,0,0,"0",0,0,0,1)

        return [mem[pc][6:32]]
    
    elif(opcode == instructions["mul"]):
            rs=binary_to_decimal(mem[pc][6:11])
            rt=binary_to_decimal(mem[pc][11:16])
            rd=binary_to_decimal(mem[pc][16:21])

            mtr = 1
            memw = 0
            brnch = 0
            alucont = "101"
            alusrc = 0
            regdst = 1
            regwr = 1
            control.control_unit_assign(1,0,0,"101",0,1,1,0)
            return[rs,rt,rd]
    
    else:
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        imm=binary_to_decimal(mem[pc][16:32])

        mtr = 0
        memw = 0
        brnch = 0
        alucont = "010"
        alusrc = 1
        regdst = 1
        regwr = 1

        if(opcode == instructions["lw"]):
            mtr = 0
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 0
            regwr = 1
        elif(opcode == instructions["sw"]):
            mtr = 0
            memw = 1
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 0
            regwr = 0

        elif(opcode == instructions["addi"]):
            mtr = 1
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 0
            regwr = 1
        
        elif(opcode == instructions["addiu"]):
            mtr = 1
            memw =0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 0
            regwr = 1
        
        elif(opcode == instructions["beq"]):
            mtr = 0
            memw = 0
            brnch = 1
            alucont = "011"
            alusrc = 0
            regdst = 1
            regwr = 0

        elif(opcode == instructions["bne"]):
            mtr = 0
            memw = 0
            brnch = 1
            alucont = "011"
            alusrc = 0
            regdst = 1
            regwr = 0
        
        control.control_unit_assign(mtr,memw,brnch,alucont,alusrc,regdst,regwr,0)
        return [rs,rt,imm]
    
def EX(srcA,srcB,controller,imm = 0):
    global clock
    clock+=1

    alu_control = controller.control_signals["AluControl"]
    branch = controller.control_signals["Branch"]
    src = controller.control_signals["AluSrc"]
    
    if(branch):
        if(alu_control == "111"):
            if(srcA>srcB):
                return imm+1
            else: return 1

    if(not src):
        if(alu_control == "010"):
            return srcA + srcB
        elif(alu_control == "011"):
            if(controller.op == instructions["bne"]):
                if(srcA - srcB==0):
                    return 1
                else: return 0
            return srcA - srcB
        elif(alu_control == "001"):
            return srcA | srcB
        elif(alu_control == "111"):
            return srcA > srcB
        elif(alu_control == "101"):
            return srcA * srcB
        elif(alu_control == "100"):
            if(srcA < srcB):
                return 1
            else: return 0
    elif(src):
        if(alu_control == "010"):
            return srcA + imm
        elif(alu_control == "011"):
            return srcA - imm
        elif(alu_control == "001"):
            return srcA | imm
        elif(alu_control == "111"):
            return srcA > imm
        elif(alu_control == "101"):
            return srcA * srcB

def memory(controller,AluRes,reg1):
    global clock
    clock+=1
    memw = controller.control_signals["MemWrite"]
    if(controller.op == instructions["lw"] or controller.op == instructions["sw"]):
        if(memw):
            x = decimal_to_binary(regMem[reg1],32)
            dataMem[AluRes] = x[0:8]
            dataMem[AluRes+1] = x[8:16]
            dataMem[AluRes+2] = x[16:24]
            dataMem[AluRes+3] = x[24:32]

            return 0
        else:
            return binary_to_decimal(dataMem[AluRes] + dataMem[AluRes+1] + dataMem[AluRes+2] + dataMem[AluRes+3])
    else: return 0
    
def writeBack(controller,dataAlures,memdata,reg1,reg2):
    global clock
    clock+=1

    regw = controller.control_signals["RegWrite"]

    if(not regw):
        return
    mtr = controller.control_signals["MemtoReg"]
    regdst = controller.control_signals["RegDest"]
    if(mtr and regdst):
        regMem[reg1] = dataAlures
    if(not mtr and regdst):
        regMem[reg1] = memdata
    if(mtr and not regdst):
        regMem[reg2] = dataAlures
    if(not mtr and not regdst):
        regMem[reg2] = memdata

while(pc<len(mem)):
    instruction = mem[pc]
    
    opcode = IF(mem[pc])

    control = control_unit(instruction)
    l = ID(opcode,control)
    if(len(l)==1):
        pc = binary_to_decimal(l[0])
        continue
    alures = EX(regMem[l[0]],regMem[l[1]],control,l[2])

    if(control.control_signals["Branch"] and alures == 0):
        pc = pc + 1 + l[2]
        continue

    w = memory(control,alures,l[1])
    print("rmem",regMem)
    print(pc)
    print()
    writeBack(control,alures,w,l[2],l[1])
    pc = pc + 1

print("-------------------------------------------------------------------------------------------------------------------------")
print("clock cycles: ",clock)
print("Regmem",regMem)
print()
print("DataMem",dataMem)
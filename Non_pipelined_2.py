import os

# instr_begg = 2**20
pc=0
mem=[]
file_path = "Fake_Output.txt" 
dataMem=[]
regMem = []

with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

mem=file_contents.split('\n')

def decimal_to_binary(number, num_bits):
    # Convert the decimal number to binary
    binary_representation = bin(number)[2:]  # Remove '0b' prefix

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

def binary_to_decimal(number_str):
    if(len(number_str)>30 and number_str[30:32]=="b1"):
        number_str =number_str[0:29]+ "01"
    # print(number_str)
    number = int(number_str,2)
    # print(number)
    return number

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
regMem[9] = 3
regMem[10] = 0
regMem[11] = 20

for i in range(200):
    dataMem.append("0"*8)

dataMem[0] = decimal_to_binary(13,32)[0:8]
dataMem[1] = decimal_to_binary(13,32)[8:16]
dataMem[2] = decimal_to_binary(13,32)[16:24]
dataMem[3] = decimal_to_binary(13,32)[24:32]

dataMem[4] = decimal_to_binary(7,32)[0:8]
dataMem[5] = decimal_to_binary(7,32)[8:16]
dataMem[6] = decimal_to_binary(7,32)[16:24]
dataMem[7] = decimal_to_binary(7,32)[24:32]

dataMem[8] = decimal_to_binary(10,32)[0:8]
dataMem[9] = decimal_to_binary(10,32)[8:16]
dataMem[10] = decimal_to_binary(10,32)[16:24]
dataMem[11] = decimal_to_binary(10,32)[24:32]

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
            # print("HI")
            funct = self.instruction[26:32]
            if(funct=="100000"):  #100001
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



def IF(instruction):
    return instruction[0:6]

def ID(opcode,control):

    # funct = control.alu_control()
    # print("j")
    if(opcode == "000000"):
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        rd=binary_to_decimal(mem[pc][16:21])

        funct = control.alu_control()
        # print(funct)
        # print(funct)

        control.control_unit_assign(1,0,0,funct,0,0,1,0)

        return [rs,rt,rd]
    
    elif(opcode=="000010"):

        control.control_unit_assign(1,0,0,"0",0,0,0,1)

        return [0,0,mem[pc][6:32]]
    
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
            regdst = 1
            regwr = 1
        elif(opcode == instructions["sw"]):
            mtr = 0
            memw = 1
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 1
            regwr = 0

        elif(opcode == instructions["addi"]):
            mtr = 1
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 1
            regwr = 1
        
        elif(opcode == instructions["bgt"]):
            mtr = 1
            memw = 0
            brnch = 1
            alucont = "111"# new alu_control signal for bgt
            alusrc = 0
            regdst = 1
            regwr = 0
        
        elif(opcode == instructions["beq"]):
            mtr = 0
            memw = 0
            brnch = 1
            alucont = "011"
            alusrc = 0
            regdst = 1
            regwr = 0
        
        elif(opcode == instructions["mul"]):
            # 1,0,0,funct,0,0,1,0
            mtr = 1
            memw = 0
            brnch = 0
            alucont = "101"
            alusrc = 0
            regdst = 0
            regwr = 1
        elif(opcode == instructions["addu"]):
            mtr = 1
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 0
            regdst = 0
            regwr = 1
        # elif(opcode == instructions["lui"]):
        #     pass

        # elif(opcode == instructions["ori"]):
        #     pass
        
        control.control_unit_assign(mtr,memw,brnch,alucont,alusrc,regdst,regwr,0)
        return [rs,rt,imm]
    
def EX(srcA,srcB,controller,imm = 0):

    alu_control = controller.control_signals["AluControl"]
    branch = controller.control_signals["Branch"]
    src = controller.control_signals["AluSrc"]

    if(not branch and not src):
        if(alu_control == "010"):
            return srcA + srcB
        elif(alu_control == "011"):
            return srcA - srcB
        elif(alu_control == "001"):
            return srcA | srcB
        elif(alu_control == "111"):
            return srcA > srcB
        elif(alu_control == "101"):
            return srcA * srcB
    elif(not branch and src):
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
    else:
        if(alu_control=="011"):
            if(srcA == srcB):
                return imm + 1
            else: return 1
        elif(alu_control == "111"):
            if(srcA>srcB):
                return imm+1
            else: return 1

def memory(controller,AluRes,reg1):
    memw = controller.control_signals["MemWrite"]
    # print(memw)
    if(controller.op == instructions["lw"] or controller.op == instructions["sw"]):
        if(memw):
            # dataMem[AluRes] = regMem[reg1]
            # print(regMem[reg1])
            x = decimal_to_binary(regMem[reg1],32)
            # print("Fuck")
            # print(controller.op)
            dataMem[AluRes] = x[0:8]
            dataMem[AluRes+1] = x[8:16]
            dataMem[AluRes+2] = x[16:24]
            dataMem[AluRes+3] = x[24:32]

            print()
            return 0
        else:
            return binary_to_decimal(dataMem[AluRes] + dataMem[AluRes+1] + dataMem[AluRes+2] + dataMem[AluRes+3])
    else: return 0
    
def writeBack(controller,dataAlures,memdata,reg1,reg2):

    # if(controller.control_signals["RegDest"]):
    #     reg = reg2
    # else:
    #     reg = reg1

    # regWr = controller.control_signals["RegWrite"]
    # memtr = controller.control_signals["MemtoReg"]
    # if(regWr and not memtr):
    #     regMem[reg] = dataMem
    #     return 
    # elif(regWr and memtr):
    #     regMem[reg] = dataAlures
    #     return

    regw = controller.control_signals["RegWrite"]
    # print(controller.instruction)
    # print(regw)
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

    print(pc)
    
    print("mem",dataMem)

    instruction = mem[pc]
    
    opcode = IF(mem[pc])

    control = control_unit(instruction)
    print(control.op)
    l = ID(opcode,control)
    # print(control.control_signals["MemWrite"])

    alures = EX(l[0],l[1],control,l[2])  #000000 00000010010110100000100001

    w = memory(control,alures,l[1])

    pc = pc + 1

    # writeBack(control,alures,w,)
    writeBack(control,alures,w,l[2],l[1])


print("Regmem",regMem)
print()
print()
print("DataMem",dataMem)
# controller = control_unit("0000")
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


for i in range(32):
    regMem.append("0"*32)

regMem[0] = decimal_to_binary(0,32)
regMem[9] = decimal_to_binary(3,32)
regMem[10] = decimal_to_binary(0,32)
regMem[11] = decimal_to_binary(5,32)

for i in range(50):
    dataMem.append("0"*32)

dataMem[0] = decimal_to_binary(13,32)
dataMem[1] = decimal_to_binary(7,32)
dataMem[2] = decimal_to_binary(10,32)

control_signals = {
    "MemtoReg":0,# 1 => ALu res to register,0=> dataMem to reg
    "MemWrite":0,#1=> writes into the data memory
    "Branch":0,#1=>branch
    "AluControl":0,#000 AND, 001 OR, 010 add, 011 sub, 100 less than
    "AluSrc":0,#0=> from register 1=>imm
    "RegDest":0,#0=>I format, 1=>R form
    "RegWrite":0,#1=>Write back to register
    "jump":0#1 is jump
}

def control_unit_assign(MemtoReg,MemWrite,Branch,AluCont,AluSrc,Regdst,regWr,jmp):
    control_signals["MemtoReg"] = MemtoReg
    control_signals["MemWrite"] = MemWrite
    control_signals["Branch"] = Branch
    control_signals["AluControl"] = AluCont
    control_signals["AluSrc"] = AluSrc
    control_signals["RegDest"] = Regdst
    control_signals["RegWrite"] = regWr
    control_signals["jump"] = jmp

class control_unit:

    def __init__(self,instruction):
        self.instruction = instruction
        self.op = instruction[0:6]
        control_signals = {
        "MemtoReg":0,# 1 => ALu res to register,0=> dataMem to reg
        "MemWrite":0,#1=> writes into the data memory
        "Branch":0,#1=>branch
        "AluControl":0,#000 AND, 001 OR, 010 add, 011 sub, 100 less than
        "AluSrc":0,#0=> from register 1=>imm
        "RegDest":0,#0=>I format, 1=>R form
        "RegWrite":0,#1=>Write back to register
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



def IF(instruction):
    return instruction[0:6]

def ID(opcode,control):

    if(opcode == "000000"):
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        rd=binary_to_decimal(mem[pc][16:21])

        funct = control.alu_control()

        control.control_unit_assign(1,0,0,funct,0,0,1)

        return [rs,rt,rd]
    
    elif(opcode=="000010"):

        control.control_unit_assign(1,0,0,"0",0,0,1)

        return mem[pc][6:32]
    
    else:
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        imm=mem[pc][16:32]

        mtr = 0
        memw = 0
        brnch = 0
        alucont = "010"
        alusrc = 1
        regdst = 1
        regwr = 1

        if(opcode == "lw"):
            mtr = 0
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 1
            regwr = 1
        elif(opcode == "sw"):
            mtr = 0
            memw = 1
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 1
            regwr = 0

        elif(opcode == "addi"):
            mtr = 1
            memw = 0
            brnch = 0
            alucont = "010"
            alusrc = 1
            regdst = 1
            regwr = 1
        
        elif(opcode == "bgt"):
            mtr = 1
            memw = 0
            brnch = 1
            alucont = "111"# new alu_control signal for bgt
            alusrc = 0
            regdst = 1
            regwr = 0
        
        elif(opcode == "beq"):
            mtr = 0
            memw = 0
            brnch = 1
            alucont = "011"
            alusrc = 0
            regdst = 1
            regwr = 0
        
        elif(opcode == "lui"):
            pass

        elif(opcode == "ori"):
            pass
        
        control_unit_assign(mtr,memw,brnch,alucont,alusrc,regdst,regwr,0)
        return [rs,rt,imm]
    
def EX(srcA,srcB,controller,imm = 0):

    alu_control = controller.control_signals["AluControl"]
    branch = controller.control_signals["Branch"]

    if(not branch):
        if(alu_control == "010"):
            return srcA + srcB
        elif(alu_control == "011"):
            return srcA - srcB
        elif(alu_control == "001"):
            return srcA | srcB
        elif(alu_control == "111"):
            return srcA > srcB
    else:
        if(alu_control=="011"):
            if(srcA == srcB):
                return imm + 4
            else: return 4
        elif(alu_control == "111"):
            if(srcA>srcB):
                return imm+4
            else: return 4

def memory(controller,AluRes,writeData):
    memw = controller.control_signals["MemWrite"]
    if(memw):
        dataMem[AluRes] = writeData
        return
    else:
        return dataMem[AluRes]
    
def writeBack(controller,data,reg):
    regWr = controller.control_signals["MemWrite"]
    if(regWr):
        regMem[reg] = data
        return



controller = control_unit("0000")
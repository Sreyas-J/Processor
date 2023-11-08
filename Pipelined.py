import os
from collections import deque

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
# regMem[9] = 4
# regMem[10] = 0
# regMem[11] = 24

regMem[10] = 0
regMem[11] = 8
for i in range(200):
    dataMem.append("0"*8)

a=decimal_to_binary(5,32)
dataMem[0] = a[0:8]
dataMem[1] = a[8:16]
dataMem[2] = a[16:24]
dataMem[3] = a[24:32]

# a = decimal_to_binary(10,32)
# b= decimal_to_binary(6,32)
# c = decimal_to_binary(8,32)
# d=decimal_to_binary(100,32)

# dataMem[0] = a[0:8]
# dataMem[1] = a[8:16]
# dataMem[2] = a[16:24]
# dataMem[3] = a[24:32]

# dataMem[4] = b[0:8]
# dataMem[5] = b[8:16]
# dataMem[6] = b[16:24]
# dataMem[7] = b[24:32]

# dataMem[8] = c[0:8]
# dataMem[9] = c[8:16]
# dataMem[10] = c[16:24]
# dataMem[11] = c[24:32]

# dataMem[12] = d[0:8]
# dataMem[13] = d[8:16]
# dataMem[14] = d[16:24]
# dataMem[15] = d[24:32]

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
            elif(funct == "000010"):
                return "101"

IF_ID={}
ID_Ex={}
Ex_Mem={}
Mem_WB={}

class INSTRUCTION:
    def __init__(self,instruction):
        self.instruction=instruction
        # self.control

    def updateInstr(self,instr):
        self.instruction = instr

    def updateStage(self,stage):
        self.stage=stage

    def assignControlSignals(self,signals):
        self.control_signals=signals


    def IF(self):
        IF_ID["opcode"] = self.instruction[0:6]
        IF_ID["instruction"] = self.instruction
        # print(IF_ID["instruction"],"if_instruction")
        return

    def ID(self):
        self.control = control_unit(self.instruction)
        control = self.control
        opcode = IF_ID["opcode"]
        if(opcode == "000000"):
            rs=binary_to_decimal(mem[pc][6:11])
            rt=binary_to_decimal(mem[pc][11:16])
            rd=binary_to_decimal(mem[pc][16:21])

            funct = control.alu_control()

            control.control_unit_assign(1,0,0,funct,0,1,1,0)

            ID_Ex["list"] = [rs,rt,rd]
        
        elif(opcode=="000010"):

            control.control_unit_assign(1,0,0,"0",0,0,0,1)

            ID_Ex["list"] = [mem[pc][6:32],-1,-1]
        
        elif(opcode == instructions["mul"]):
                rs=binary_to_decimal(mem[pc][6:11])
                rt=binary_to_decimal(mem[pc][11:16])
                rd=binary_to_decimal(mem[pc][16:21])
                # 1,0,0,funct,0,0,1,0
                mtr = 1
                memw = 0
                brnch = 0
                alucont = "101"
                alusrc = 0
                regdst = 1
                regwr = 1
                control.control_unit_assign(1,0,0,"101",0,1,1,0)
                ID_Ex["list"] = [rs,rt,rd]
        
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
            
            # elif(opcode == instructions["addu"]):
            #     mtr = 1
            #     memw = 0
            #     brnch = 0
            #     alucont = "010"
            #     alusrc = 0
            #     regdst = 0
            #     regwr = 1
            elif(opcode == instructions["bne"]):
                mtr = 0
                memw = 0
                brnch = 1
                alucont = "011"
                alusrc = 0
                regdst = 1
                regwr = 0
            # elif(opcode == instructions["lui"]):
            #     pass

            # elif(opcode == instructions["ori"]):
            #     pass
            
            control.control_unit_assign(mtr,memw,brnch,alucont,alusrc,regdst,regwr,0)
            # print(rs,rt,imm,"ID")
            print(mem[pc],"ID")
            ID_Ex["list"]  = [rs,rt,imm]
        ID_Ex["instruction"] = IF_ID['instruction']
        ID_Ex["opcode"] = IF_ID['opcode']
        # print(ID_Ex["instruction"],"id_ex_instruction")
    def EX(self):
        if(ID_Ex["list"][2]==-1):
            return
        # print(pc,"pc")
        # print("op",ID_Ex["opcode"])
        # print(ID_Ex["list"])
        srcA = regMem[ID_Ex["list"][0]]
        srcB = regMem[ID_Ex["list"][1]]
        imm = ID_Ex["list"][2]
        controller = self.control

        alu_control = controller.control_signals["AluControl"]
        branch = controller.control_signals["Branch"]
        src = controller.control_signals["AluSrc"]
        
        if(branch):
            if(alu_control == "111"):
                if(srcA>srcB):
                    Ex_Mem["alures"] =  imm+1
                    Ex_Mem["opcode"] = ID_Ex["opcode"]
                    Ex_Mem["instruction"] = ID_Ex["instruction"]
                    Ex_Mem["list"] = ID_Ex["list"]
                    return
                else: 
                    Ex_Mem["alures"] =  1
                    Ex_Mem["opcode"] = ID_Ex["opcode"]
                    Ex_Mem["instruction"] = ID_Ex["instruction"]
                    Ex_Mem["list"] = ID_Ex["list"]
                    return

        if(not src):
            if(alu_control == "010"):
                Ex_Mem["alures"] =  srcA + srcB
            elif(alu_control == "011"):
                if(controller.op == instructions["bne"]):
                    if(srcA - srcB==0):
                        Ex_Mem["alures"] =  1
                    else: Ex_Mem["alures"] =  0
                # if(pc==16):
                Ex_Mem["alures"] =  srcA - srcB
            elif(alu_control == "001"):
                Ex_Mem["alures"] =  srcA | srcB
            elif(alu_control == "111"):
                Ex_Mem["alures"] =  srcA > srcB
            elif(alu_control == "101"):
                Ex_Mem["alures"] =  srcA * srcB
            elif(alu_control == "100"):
                print("slt")
                if(srcA < srcB):
                    Ex_Mem["alures"] =  1
                else: Ex_Mem["alures"] =  0
        elif(src):
            if(alu_control == "010"):
                Ex_Mem["alures"] =  srcA + imm
            elif(alu_control == "011"):
                Ex_Mem["alures"] =  srcA - imm
            elif(alu_control == "001"):
                Ex_Mem["alures"] =  srcA | imm
            elif(alu_control == "111"):
                Ex_Mem["alures"] =  srcA > imm
            elif(alu_control == "101"):
                Ex_Mem["alures"] =  srcA * srcB
        
        Ex_Mem["opcode"] = ID_Ex["opcode"]
        Ex_Mem["instruction"] = ID_Ex["instruction"]
        Ex_Mem["list"] = ID_Ex["list"]
        # else:
        #     if(alu_control=="011"):
        #         if(srcA - srcB == 0):
        #             return imm + 1
        #         else: return 1
        #     if(alu_control == "111"):
        #         if(srcA>srcB):
        #             return imm+1
        #         else: return 1
        
    def memory(self):

        if(ID_Ex["list"][2]==-1):
            return

        controller = self.control
        AluRes = Ex_Mem["alures"]
        reg1 = Ex_Mem["list"][1]
        

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

                # print()
                Mem_WB["memdata"] =  0
            else:
                # print(AluRes)
                Mem_WB["memdata"] = binary_to_decimal(dataMem[AluRes] + dataMem[AluRes+1] + dataMem[AluRes+2] + dataMem[AluRes+3])
        else: Mem_WB["memdata"] = 0

        Mem_WB["instruction"] = Ex_Mem["instruction"]
        Mem_WB["opcode"] = Ex_Mem["opcode"]
        Mem_WB["list"] = Ex_Mem["list"]
        Mem_WB["alures"] = Ex_Mem["alures"]
        
    def writeBack(self):
        if(ID_Ex["list"][2]==-1):
            return

        controller = self.control
        dataAlures = Mem_WB["alures"]
        memdata = Mem_WB["memdata"]
        reg1 = Mem_WB["list"][2]
        reg2 = Mem_WB["list"][1]
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

curr_instructions=deque() #0=>IF,4=>WB
while(pc<len(mem)):
    if(len(curr_instructions)<5):
    
        obj = INSTRUCTION(mem[pc])
        curr_instructions.append(obj)

        # for i in range(len(curr_instructions)):
        #     print(curr_instructions[i].instruction)

    n=len(curr_instructions)

    if(pc<len(mem)-4):

        # curr_instructions[n-1].IF()
        # # print(curr_instructions[n-1].instruction)

        # if(n-2>=0):
        #     curr_instructions[n-2].ID()
        #     # print(curr_instructions[n-2].instruction)
        # if(n-3>=0):
        #     curr_instructions[n-3].EX()
        #     # print(curr_instructions[n-3].instruction)
        # if(n-4>=0):
        #     curr_instructions[n-4].memory()
        #     # print(curr_instructions[n-4].instruction)
        # if(n-5>=0):
        #     curr_instructions[n-5].writeBack()
        #     # print(curr_instructions[n-5].instruction)
        # if(n==5 and pc+1<len(mem)):
        #     item = curr_instructions.popleft()
        #     item.updateInstr(mem[pc+1])
        #     curr_instructions.append(item)


        if(n-5>=0):
            curr_instructions[n-5].writeBack()
            # print(curr_instructions[n-5].instruction)

        if(n-4>=0):
            curr_instructions[n-4].memory()
            # print(curr_instructions[n-4].instruction)
        
        if(n-3>=0):
            curr_instructions[n-3].EX()
            # print(curr_instructions[n-3].instruction)
        
        if(n-2>=0):
            curr_instructions[n-2].ID()
        #     # print(curr_instructions[n-2].instruction)

        curr_instructions[n-1].IF()
        # print(curr_instructions[n-1].instruction)

        if(n==5 and pc+1<len(mem)):
            item = curr_instructions.popleft()
            item.updateInstr(mem[pc+1])
            curr_instructions.append(item)

        

    else:
        if(len(mem)-pc==4):
            curr_instructions[n-2].ID()
            curr_instructions[n-3].EX()
            curr_instructions[n-4].memory()
            curr_instructions[n-5].writeBack()
        elif(len(mem)-pc==3):
            curr_instructions[n-3].EX()
            curr_instructions[n-4].memory()
            curr_instructions[n-5].writeBack()
        elif(len(mem)-pc==2):
            curr_instructions[n-4].memory()
            curr_instructions[n-5].writeBack()
        elif(len(mem)==1):
            curr_instructions[n-5].writeBack()
    print(IF_ID,"if_id")
    print(ID_Ex,"ID_Ex")
    print(Ex_Mem,"Ex_Mem")
    print(Mem_WB,"Mem_WB")
    print(pc,"pc")
    print('\n\n')
    pc = pc + 1
    

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

while(pc<len(mem)):
    print()
    op=mem[pc][0:6]
    # print(regMem[23])

    if(op=="000000"):
        
        # print(mem[pc][16:21])
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        rd=binary_to_decimal(mem[pc][16:21])
        # print("HI")
        # print(regMem[rd])
        # print(rd)

        HI=""
        LO=""

        funct = mem[pc][26:32]

        if(funct == "010000"):
            regMem[rd] = decimal_to_binary(binary_to_decimal(regMem[rs]) + binary_to_decimal(regMem[rt]),32)

        elif(funct == "100010"):
            regMem[rd] = decimal_to_binary(binary_to_decimal(regMem[rs]) - binary_to_decimal(regMem[rt]),32)

        elif(funct=="011000"):
            x=decimal_to_binary(binary_to_decimal(regMem[rs])*binary_to_decimal(regMem[rt]),64)
            HI=x[0:32]
            LO=x[32:64]
        elif(funct=="010010"):
            regMem = LO

    elif(op=="000010" or op=="000011"):
        j=mem[pc][6:32] + "00"
        pc = binary_to_decimal(j)

    else:
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        imm=mem[pc][16:32]

        if(op==decimal_to_binary(35,6)):
            regMem[rt] = dataMem[binary_to_decimal(regMem[rs])+binary_to_decimal(imm)]
        elif(op==decimal_to_binary(43,6)):
            dataMem[binary_to_decimal(regMem[rs])+binary_to_decimal(imm)] = regMem[rt]
        elif(op==decimal_to_binary(8,6)):
            regMem[rt] = decimal_to_binary(binary_to_decimal(regMem[rs])+binary_to_decimal(imm),32)
        elif(op==decimal_to_binary(15,6)):
            regMem[rt][0:16] = imm
        elif(op==decimal_to_binary(13,6)):
            regMem[rs] = decimal_to_binary(binary_to_decimal(regMem[rt]) | binary_to_decimal(imm),32)
        elif(op==decimal_to_binary(4,6)):
            # print(rt)
            if(binary_to_decimal(regMem[rs])==binary_to_decimal(regMem[rt])):
                pc = pc + 1 + binary_to_decimal(imm)
        elif(op==decimal_to_binary(7,6)):
            if(binary_to_decimal(regMem[rs])>binary_to_decimal(regMem[rt])):
                pc = pc + 1 + binary_to_decimal(imm)

    pc+=1

# output = [dataMem[5],dataMem[6],dataMem[7]]
print("RegMem")
print(regMem)
print()
print()
print("DataMem")
print(dataMem)
import os

pc=0
mem=[]
file_path = "RealOutput.asm" 
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
    number = int(number_str,2)
    return number



for i in range(32):
    regMem.append(0)
# regMem[9] =
# regMem[10] = 
# regMem[11] = 

for i in range(mem.len()):
    op=mem[pc][0:6]

    if(op=="000000"):
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        rd=binary_to_decimal(mem[pc][16:21])

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
        j=mem[pc][6:32]
        

    else:
        rs=binary_to_decimal(mem[pc][6:11])
        rt=binary_to_decimal(mem[pc][11:16])
        imm=binary_to_decimal(mem[pc][16:32])

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
        


    if(op=="001001"):
        pass

    pc+=1

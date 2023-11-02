import os

pc=0
mem=[]
file_path = "RealOutput.asm" 

with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

mem=file_contents.split('\n')

dataMem=[]

for i in range(mem.len()):
    op=mem[pc][0:5]

    if(op=="000000"):
        rs=mem[pc][6:10]
        rt=mem[pc][11:15]
        rd=mem[pc][16:20]

    elif(op=="000010" or op=="000011"):
        j=mem[pc][6:31]

    else:
        rs=mem[pc][6:10]
        rt=mem[pc][11:15]
        imm=mem[pc][16:31]

    if(op=="001001"):
        pass

    pc+=1

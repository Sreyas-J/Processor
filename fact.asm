lw $t4,0($t2)
addi $t5,$0,1
move $t6,$t4
factorial_loop:
beq $t5,$t4,factorial_done
mul $t6,$t5,$t6
addi $t5,$t5,1
j factorial_loop
factorial_done:
sw $t6,0($t3)
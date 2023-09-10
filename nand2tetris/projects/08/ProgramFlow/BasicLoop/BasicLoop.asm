
//push constant 0
@0
D = A
@SP
A=M
M=D
@SP
M=M+1

//pop local 0
@0
D=A
@LCL
D=M+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D

//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//label LOOP_START
($LOOP_START)

//push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
AM=M-1
D=M
A=A-1
M=M+D

//pop local 0
@0
D=A
@LCL
D=M+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D

//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 1
@1
D = A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

//pop argument 0
@0
D=A
@ARG
D=M+D
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D

//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

//if-goto LOOP_START
@SP
A = M - 1
D=M
@$LOOP_START
D;JNE

//push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
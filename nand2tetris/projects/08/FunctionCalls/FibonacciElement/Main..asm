
//function Main.fibonacci 0
(Main.fibonacci)

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

//push constant 2
@2
D = A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=0
@lt_0
D;JGE
@SP
A=M-1
M=-1
(lt_0)

//if-goto IF_TRUE
@SP
A = M - 1
D=M
@Main.fibonacci$IF_TRUE
D;JNE

//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP

//label IF_TRUE
(Main.fibonacci$IF_TRUE)

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

//return
@LCL
D=M
@R15
M=D
@5
D=A
@R15
A=M-D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R15
A=M-1
D=M
@THAT
M=D
@2
D=A
@R15
A=M-D
D=M
@THIS
M=D
@3
D=A
@R15
A=M-D
D=M
@ARG
M=D
@4
D=A
@R15
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP

//label IF_FALSE
(Main.fibonacci$IF_FALSE)

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

//push constant 2
@2
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

//call Main.fibonacci 1
@End$Main.fibonacci$0
D=A
@SP
A=M
M=D
SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(End$Main.fibonacci$0)

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

//call Main.fibonacci 1
@End$Main.fibonacci$1
D=A
@SP
A=M
M=D
SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(End$Main.fibonacci$1)

//add
@SP
AM=M-1
D=M
A=A-1
M=M+D

//return
@LCL
D=M
@R15
M=D
@5
D=A
@R15
A=M-D
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R15
A=M-1
D=M
@THAT
M=D
@2
D=A
@R15
A=M-D
D=M
@THIS
M=D
@3
D=A
@R15
A=M-D
D=M
@ARG
M=D
@4
D=A
@R15
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP

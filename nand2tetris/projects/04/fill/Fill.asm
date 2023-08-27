@SCREEN
D = A
@cur
M = D  //初始化光标的位置

//判断是否存在输入，无输入跳转到loop2,清0，有输入跳转到loop1,置1
(loop)
@KBD
D = M
@loop2
D;JEQ   

//先判断光标是否还有空余，有空余填充1
@cur
D = M
@KBD
D = D - A
@end
D;JEQ
@cur
A = M
M = 1
@cur
M = M + 1
@loop
0;JMP

//先判断光标是否到屏幕的起点，没有到填充0
(loop2)
@cur
D = M
@SCREEN
D = D - A
@end
D;JEQ
@cur
M = M - 1
A = M
M = 0
@loop
0;JMP

//回到开始继续判断是否键盘有输入
(end)
@loop
0;JMP

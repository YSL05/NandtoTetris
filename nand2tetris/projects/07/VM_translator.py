import sys
import os

class VMTranslator:
    """
    translate the vm code into the hack assemble code 
    """
    def __init__(self, file_path):
        """
        open the file & filter the blanks and comments
        @attr self.vm_filename (str): input file
        @attr self.asm_filename (str): out file
        @attr self.rela_path (str): relative path for the output_file
        @attr self.asm_codes (list of str): a list contains assembly codes genersted from self.code
        """
        super().__init__()
        #获取文件的路径和名称
        self.vm_filename = os.path.basename(file_path)
        self.rela_path = file_path[:-len(self.vm_filename)]
        #判断输入文件的类型是否是.vm，如果不是输出警告信息，停止运行
        suffix = self.vm_filename[self.vm_filename.find(".") + 1:]
        assert suffix == "vm","please choose an input file named xxx.vm"
        #设置输出文件的名字
        self.asm_filename = self.vm_filename[:-3] + '.asm'
        self.codes = []
        self.asm_codes = []
        self.arith_dict = {
            "not":"!","neg":"-","add":"+","sub":"-","and":"&","or":"|",
		"eq":"JNE","lt":"JGE","gt":"JLE",
        }
        self.mapping = {
            "local":"LCL","argument":"ARG","this":"THIS","that":"THAT",
		"temp":"5","pointer":"3",
        }
        self.symbol_index = 0
        #打开文件进行处理，去除空格及相关注释
        with open(file_path,'r') as file:
            for line in file:
                _line = line.strip()
                if len(_line) == 0 or _line[0] == '/':
                    continue
                if _line.find('/') != -1:
                    _line = _line[:_line.find('/')]
                self.codes.append(_line.strip())
        
    def parse(self):
        """
        for each line in self.codes, generate its corresponding assembly codes
        """
        for code in self.codes:
            part = code.split()
            if len(part) == 1: #arithmetic commend
                self.asm_codes += self.asm_arith(part[0])
            elif part[0] == "push": #push command
                self.asm_codes += self.asm_push(part[1:])
            elif part[0] == "pop":
                self.asm_codes += self.asm_pop(part[1:])

    def asm_arith(self, command):
        """
        generate assembly code for arithmetic commands
        @para command(str): the arithmetic command to be translate
        """
        if command in ["not","neg"]:
            spec = "M=" + self.arith_dict[command] + "M"
            asm_code = ["@SP",'A=M-1',spec]
        if command in ["add","sub","and","or"]:
            spec = "M=M" + self.arith_dict[command] + "D"
            asm_code = ["@SP","AM=M-1","D=M","A=A-1",spec]
        #使用跳转符号实现算术比较
        if command in ["eq","lt","gt"]:
            symbol=command+"_"+str(self.symbol_index)
            symbol1="@"+symbol
            symbol2="("+symbol+")"
            spec="D;"+self.arith_dict[command]
            asm_code=["@SP","AM=M-1","D=M","A=A-1","D=M-D","M=0",symbol1,spec,"@SP","A=M-1","M=-1",symbol2]
            self.symbol_index+=1
        return asm_code
    
    def asm_push(self, command):
        """
        generate assembly codes for push command
        @param command(list of str): the push command to be translate
        """
        asm_code = []
        if command[0] == "constant":
            asm_code = ["@" + command[1], "D = A"]
        if command[0] in ["local","argument","this","that"]:
            asm_code=["@"+command[1],"D=A","@"+self.mapping[command[0]],"A=M+D","D=M"]
        if command[0] in ["temp","pointer"]:
            asm_code=["@"+command[1],"D=A","@"+self.mapping[command[0]],"A=A+D","D=M"]
        if command[0] == "static":
            symbol = "@" + self.vm_filename[:-3] + "." + command[1]
            asm_code = [symbol,"D=M"]
        
        return asm_code + ["@SP","A=M","M=D","@SP","M=M+1"]
    
    def asm_pop(self, command):
        """
        generate assembly codes for pop command
        @param command(list of str): command to be translate
        """
        asm_code = []
        if command[0] in ["local","argument","this","that"]:
            asm_code = ["@"+command[1],"D=A","@"+self.mapping[command[0]],"D=M+D","@R15","M=D"]
        if command[0] in ["temp","pointer"]:
            asm_code = ["@"+command[1],"D=A","@"+self.mapping[command[0]],"D=A+D","@R15","M=D"]
        elif command[0] == "static":
            symbol="@"+self.vm_filename[:-3]+"."+command[1]
            asm_code=[symbol,"D=M","@R15","M=D"]
        
        return asm_code + ["@SP","AM=M-1","D=M","@R15","A=M","M=D"]
    
    def save_file(self):
        """
        save self.asm_codes into xxx.asm
        """
        output_path = os.path.join(self.rela_path, self.asm_filename)
        with open(output_path,'w') as file:
            for line in self.asm_codes:
                file.write(line + '\n')
    
    def main():
        
        file_path = sys.argv[1]
        vmtranslator = VMTranslator(file_path)
        vmtranslator.parse()
        vmtranslator.save_file()
        for line in vmtranslator.asm_codes:
            print(line)
    
    if __name__ == '__main__':
        main()
    






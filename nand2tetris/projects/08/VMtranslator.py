import os
import sys

class VMTranslator:
    """
    docstring for VMTranslator
    """
    def __init__(self, file_path):
        """
        @attr self.vm_files (list of str): the xxx.vm needed to be translated
        @attr self.asm_filename(str): output filename
        @attr self.output_path(str): path for output filename
        @attr self.symbol_index(int): use it to make sure that each symbol is unique
        @attr self.ret_index(int): use it to make sure that each ret label is unique
        """
        self.vm_files = []
        self.asm_codes = []
        self.symbol_index = 0
        self.ret_index = 0
        if os.path.isdir(file_path):
            for file in os.listdir(file_path):
                if file[-2:] == "vm":
                    self.vm_files.append(os.path.join(file_path, file))
            assert len(self.vm_files) > 0,"please choose a dir with xxx.vm files in it"
            self.asm_filename = "A.asm"
            self.output_path = file_path
            self.multi = True
        else:
            self.vm_filename = os.path.basename(file_path)
            suffix = self.vm_filename[self.vm_filename.find(".") + 1:]
            assert suffix == "vm","please choose a vm file like xxx.vm"
            self.vm_files=[file_path]
            self.asm_filename = os.path.basename(file_path)[:-2] + "asm"
            if file_path.find("/") == -1:
                self.output_path = os.getcwd()
            else:
                self.output_path = file_path[:file_path.rfind('/')]
            self.multi = False
    
    def parse(self):
        """
        translate the vm files in self.vm_files into assembly codes, store them into self.asm_codes
        """
        if self.multi:
            self.asm_codes+=["@256","D=A","@SP","M=D"] # set SP=256
            self.asm_codes+=["@1","D=A","@LCL","M=D"]
            self.asm_codes+=["@2","D=A","@ARG","M=D"]
            self.asm_codes+=["@3","D=A","@THIS","M=D"]
            self.asm_codes+=["@4","D=A","@THAT","M=D"]
            push_D=["@SP","A=M","M=D","@SP","M=M+1"]
            self.asm_codes+=(["@bootstrap","D=A"]+push_D) # push retAddr
            for x in ["LCL","ARG","THIS","THAT"]: # push LCL,ARG,THIS,THAT
                self.asm_codes+=(["@"+x,"D=M"]+push_D)
            self.asm_codes+=["@5","D=A","@SP","D=M-D","@ARG","M=D"]# ARG=SP-n-5
            self.asm_codes+=["@SP","D=M","@LCL","M=D"] # LCL=SP
            self.asm_codes+=["@Sys.init","0;JMP","(bootstrap)"]
        for file in self.vm_files:
            single_parse = SingleVMTranslator(file, self.symbol_index, self.ret_index)
            single_parse.parse()
            self.asm_codes += single_parse.asm_codes
            self.symbol_index = single_parse.symbol_index
            self.ret_index = single_parse.ret_index
    
    def save_file(self):
        """
        save self.asm_codes into xxx.asm file
        """
        output = os.path.join(self.output_path, self.asm_filename)
        with open (output,'w') as file:
            for line in self.asm_codes:
                file.write(line + '\n')
        
class SingleVMTranslator:
    """
    translator a .vm into assembly codes for hack machine
    """

    def __init__(self, file_path, symbol_index, ret_index):
        """
        open the file and ignore blanks and comments
        @attr self.vm_filename(str): input file
        @attr self.codes(list of str): a list contains clean vm code with no blank or comment
        @attr self.asm_codes(list of str): a list contains assembly codes generated from self.codes
        @attr self.symbol_index(int): use it to make sure that each symbol is unique
        @attr self.ret_idx(int): use it to make sure that each ret label is unique
        """

        #获取VM文件的名字
        self.vm_filename = os.path.basename(file_path)
        suffix = self.vm_filename[self.vm_filename.find(".") + 1:]
        assert suffix == "vm","please choose an input file named xxx.vm"
        #定义保存vm code和 asm code的列表
        self.codes = []
        self.asm_codes = []

        #处理文件，清除空格及注释，从文件中转换为字符串列表
        with open (file_path,'r') as file:
            for line in file:
                _line = line.strip()
                if len(_line) == 0 or _line[0] == '/':
                    continue
                if _line.find('/') != -1:
                    _line = _line[:_line.find('/')]
                self.codes.append(_line.strip())
        
        #vm code与asm code的映射对照表
        self.arith_dict = {
            "not":"!","neg":"-","add":"+","sub":"-","and":"&","or":"|",
		"eq":"JNE","lt":"JGE","gt":"JLE",
        }
        self.mapping = {
            "local":"LCL","argument":"ARG","this":"THIS","that":"THAT",
		"temp":"5","pointer":"3",
        }

        self.symbol_index = symbol_index
        self.ret_index = ret_index
        self.cur_funcname = ""
    
    def parse(self):
        """
        for each code in self.codes generate its corresponding assmembly codes
        """
        #遍历翻译每一行vm code
        for code in self.codes:
            part = code.split()
            if len(part) == 1:
                if part[0] == "return":
                    #翻译return vm code
                    self.asm_codes += ["\n//" + code]
                    self.asm_codes += self.ret_asm()
                else:
                    #翻译 逻辑算法指令 vm code
                    self.asm_codes += ["\n//" + code]
                    self.asm_codes += self.arith_asm(part[0])
            elif part[0] == "push":
                self.asm_codes += ["\n//" + code]
                self.asm_codes += self.push_asm(part[1:])
            elif part[0] == "pop":
                self.asm_codes += ["\n//" + code]
                self.asm_codes += self.pop_asm(part[1:])
            elif part[0] == "label":
                self.asm_codes += ["\n//" + code]
                label_ = self.cur_funcname + "$" + part[1]
                self.asm_codes += ["(" + label_ + ")"]
            elif part[0] == "goto":
                self.asm_codes += ["\n//" + code]
                label_ = self.cur_funcname + "$" + part[1]
                self.asm_codes += ["@" + label_, "0;JMP"]
            elif part[0] == "if-goto":
                self.asm_codes += ["\n//" + code]
                label_ = self.cur_funcname + "$" + part[1]
                self.asm_codes += ["@SP","A = M - 1","D=M","@" + label_, "D;JNE"]
            elif part[0] == "function":
                self.asm_codes += ["\n//" + code]
                self.asm_codes += self.function_asm(part[1:])
            elif part[0] == "call":
                self.asm_codes += ["\n//" + code]
                self.asm_codes += self.call_asm(part[1:])
            else:
                raise ValueError("illegal vm codes found")
    def call_asm(self, command):
        """
        generate assembly code for call commands
        @param command(list of str): call command like [func_name,argument_num]
        @attr: the call code can div into serises of commands:
                push retaddress
                push LCL
                push ARG
                push THIS
                push THAT
                ARG = SP - n - 5
                LCL = SP
                goto func_name
                (retaddress)
        """
        label = "End$" + command[0] + "$" + str(self.ret_index)
        self.ret_index += 1
        push_label = ["@SP","A=M","M=D","@SP","M=M+1"]
        asm_code = (["@"+ label, "D=A"] + push_label)
        for x in ["LCL","ARG","THIS","THAT"]:
            asm_code += (["@"+ x, "D=M"] + push_label)
        asm_code += ["@" + str(int(command[1]) + 5), "D=A", "@SP", "D=M-D", "@ARG", "M=D"]
        asm_code += ["@SP","D=M","@LCL","M=D"]
        asm_code += ["@" + command[0], "0;JMP"]
        asm_code += ["(" + label + ")"]

        return asm_code
    
    def ret_asm(self):
        """
        generate assembly codes for return commands
        """
        asm_code  = ["@LCL","D=M","@R15","M=D"] # put LCL into R15
        asm_code += ["@5","D=A","@R15","A=M-D","D=M","@R14","M=D"] # put retAddr into R14
        asm_code += ["@SP","AM=M-1","D=M","@ARG","A=M","M=D"] # *ARG=pop()
        asm_code += ["@ARG","D=M+1","@SP","M=D"] # SP=ARG+1
        asm_code += ["@R15","A=M-1","D=M","@THAT","M=D"] # THAT=*(FRAME-1)
        asm_code += ["@2","D=A","@R15","A=M-D","D=M","@THIS","M=D"] #THIS=*(FRAME-2)
        asm_code += ["@3","D=A","@R15","A=M-D","D=M","@ARG","M=D"] # ARG=*(FRAME-3)
        asm_code += ["@4","D=A","@R15","A=M-D","D=M","@LCL","M=D"] # LCL=*(FRAME-4)
        asm_code += ["@R14","A=M","0;JMP"] # goto retAddr
        
        return asm_code
    
    def function_asm(self, command):
        """
        generate assembly codes for function code
        @param command(str of list): [function_name, local var num] 
        """
        self.cur_funcname = command[0]
        asm_code = ["(" + command[0] + ")"]
        for i in range(int(command[1])):
            asm_code += ["@SP", "A=M","M=0","@SP","M = M+1"]
        return asm_code
    def arith_asm(self, command):
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
    def push_asm(self, command):
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
    
    def pop_asm(self, command):
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
            asm_code=[symbol,"D=A","@R15","M=D"]
        
        return asm_code + ["@SP","AM=M-1","D=M","@R15","A=M","M=D"]
def main():
    assert len(sys.argv)>=2,"please enter a filename or dir"
    file_path = sys.argv[1]
    vmtranslator = VMTranslator(file_path)
    vmtranslator.parse()
    vmtranslator.save_file()

if __name__ == '__main__':
    main()
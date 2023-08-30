/*
功能：解析文本文件的字符串转化为域和字段
*/
#include "data_type.h"

int Paser(const char *file_name, struct asm_field cmd[])
{
    char *line[100];
    char *cmd_str[100];
    int line_size = 0;
    int i = 0;
    while(i < 30)
    {
        line[i] = (char *)malloc(100);
        i++;
    }
    Init(file_name, line, &line_size);
    for (i = 0; i <= line_size; i++)
    {
        delete_space(line[i], cmd_str[i]);
    }
}
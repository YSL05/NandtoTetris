/*
功能：定义语法解析使用的数据类型
*/
#ifndef DATATYPE_H
#define DATATYPE_H
struct asm_field
{
    char cmd_type;
    unsigned short a_cmd_addr;
    char dest;
    char comp[3];
    char jmp[3];
};
#endif
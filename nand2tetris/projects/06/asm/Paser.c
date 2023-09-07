/*
功能：解析文本文件的字符串转化为域和字段
*/
#include <stdio.h>
#include <stdlib.h>
//#include "data_type.h"

int paser_analysis(const char *file_name, struct asm_field *cmd)
{
    char line[100][100] = {0};
    FILE *file = fopen(file_name, "rt");
    int i = 0;
    int j = 0;
    int k = 0;
    char temp_line;
    while(!feof(file))
    {
        temp_line = fgetc(file);
        if(temp_line == '\n')
        {
            while (!feof(file))
            {
                temp_line = fgetc(file);
                if(temp_line != '\n')
                {
                    *(line[i] + j) = '\0';
                    i++;
                    j = 0;
                    break;
                }
            }
        }
        if (feof(file))
        {
            break;
        }
        *(line[i] + j) = temp_line;
        j++;
    }
    j = 0;
    while (j <= i)
    {
        printf("%s\n", line[j]);
        j++;
    }
}
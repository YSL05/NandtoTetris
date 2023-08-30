/*
功能：读取文本文件的内容，并转为字符串
*/

#include<stdio.h>
#include<stdlib.h>

int Init(const char *file_name, char *line[], int *line_size)
{
    int j = 0;
    FILE *file = fopen(file_name, "rt");
    if(!file){
        return -1;
    }
    while (!feof(file)){
        fgets(line[j], 99, file);
        j++;
    }
    *line_size = j;
    fclose(file);
    return 0;
}
#include <stdio.h>
#include <stdlib.h>

#include "Init.c"
//#include "Code.c"
#include "Paser.c"
#include "data_type.h"

int main()
{
    struct asm_field cmd_line[100] = {0};
    paser_analysis("./Add.asm", cmd_line);
}

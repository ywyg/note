#include "apue.h"
#include <fcntl.h>

#define BUFFSIZE    4096

int 
main(void)
{
    int n;
    char buf[BUFFSIZE];

    int fd_in = open("./file.txt",0);
    int fd_out = open("./copy_file.txt",2);

    while((n = read(fd_in, buf, BUFFSIZE)) > 0)
        if(write(fd_out, buf, n) != n)
            err_sys("write error");

    if(n < 0)
        err_sys("read error");

    exit(0);
}
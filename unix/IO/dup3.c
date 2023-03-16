#include <apue.h>
#include <fcntl.h>


int dup3(int fd,int expectfd)
{
    int readfd = dup(fd);
    while(expectfd < readfd)
    {
        close(expectfd);
        readfd = dup(fd);
    }
    int need_close_fd[1000];
    int index = 0,i = 0;
    while(expectfd != readfd){
        need_close_fd[index++] = readfd;
        readfd = dup(fd);
    }
    for(i = 0;i<index;i++){
        close(need_close_fd[i]);
    }
    return readfd;
}

int main(void)
{
    int fd,fd2;
    if((fd= open("./file.txt",O_RDWR)) < 0)
        err_sys("open error");
    printf("fd is %d ",fd);
    
    fd2 = dup3(fd,20);
    printf("fd2 is %d ",fd2);

    if(write(fd2,"1234",10) < 0)
        err_sys("write error");
    
    close(fd);
    close(fd2);

}

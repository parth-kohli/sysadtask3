#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
void win() {
    system("cat flag.txt");
}
void vuln() {
    char name[100];
    char buffer[64];
    printf("Hello. What's up?\n");
    fgets(name, sizeof(name), stdin);
    printf(name); 
    printf("\nWhat good?\n");
    fflush(stdout);
    fgets(buffer, sizeof(buffer) + 16, stdin);
    printf("Aight\n");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    vuln();
    return 0;
}


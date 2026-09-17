#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]){
    //Pre: El mensaje está en castellano, escrito sin tildes
    if(argc != 2){
        perror("uso...");
        exit(0);
    }

    char *mensajeCifrado = argv[1];

    for(int i = 0; i < 26; i++){
        for(int j = 0; j < strlen(mensajeCifrado); j++){
            //Si el caracter no está en el abecedario latino, se salta
            if((mensajeCifrado[j] > 64 && mensajeCifrado[j] < 91) || (mensajeCifrado[j] > 96 && mensajeCifrado[j] < 123)){
                if(mensajeCifrado[j] == 90) mensajeCifrado[j] = 64;
                else if(mensajeCifrado[j] == 122) mensajeCifrado[j] = 96;
                mensajeCifrado[j]++; 
            }
        }
        printf("Key: %d %s\n", i + 1, mensajeCifrado);
    }
    exit(1);

}
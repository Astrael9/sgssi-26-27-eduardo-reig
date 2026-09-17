#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]){
    //Pre: El mensaje está en castellano, escrito sin tildes
    if(argc != 2){
        perror("uso...");
        exit(1);
    }

    char *mensajeCifrado = argv[1];
    float frecs[27]; 
    for(int i = 0; i < 27; i++) frecs[i] = 0;
    int cont = 0;

    for(int j = 0; j < strlen(mensajeCifrado); j++){
        //Si el caracter no está en el abecedario latino, se salta
        if((mensajeCifrado[j] >= 'a' && mensajeCifrado[j] <= 'z')){
            frecs[mensajeCifrado[j]-97]++;
        } 
        else if(mensajeCifrado[j] >= 'A' && mensajeCifrado[j] <= 'Z'){
            frecs[mensajeCifrado[j]-65]++;
        }
        else if(mensajeCifrado[j] == 'ñ'|| mensajeCifrado[j] == 'Ñ'){
            frecs[14]++;
            printf("hay ñ");
        }
        else {
            cont++;
            printf("%d\n",strlen(mensajeCifrado));
        }
    }

    printf("Letra        |  Frecuencia \n");
    for(int i = 0; i < 27; i++){
        frecs[i] /= strlen(mensajeCifrado) - cont;
        if(i == 15) printf("-> Ñ : %.2f  ",frecs[i]);
        else printf("-> %c : %.2f  ",i + 65,frecs[i]);
        if(i % 2 == 1) printf("\n");
    }
    exit(0);

}
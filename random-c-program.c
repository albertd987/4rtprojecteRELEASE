#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Inicializar la semilla para generar números aleatorios
    srand(time(NULL));
    
    // Generar un número aleatorio entre 0 y 100
    int random_number = rand() % 101;
    
    // Imprimir el número aleatorio
    printf("Número aleatorio generado: %d\n", random_number);
    
    return 0;
}
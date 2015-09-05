#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *fp;
	fp = fopen("trasposta.txt", "r");

	char ch;
	char tmp[8];
	int tmpIndex, rowIndex, colIndex, j,i;

	tmpIndex = 0;
	rowIndex = 0;
	colIndex = 0;

	double f[450][800];

	while (EOF != (ch = fgetc(fp))) {
		switch(ch) {
			case ',':
				// Andiamo a destra, alla prossima colonna
				f[rowIndex][colIndex] = atof(tmp);
				colIndex++;
				tmpIndex = 0;
				break;

			case ';':
				// Andiamo giu e a sinistra
				f[rowIndex][colIndex] = atof(tmp);
				colIndex = 0;
				rowIndex++;
				tmpIndex = 0;
				break;

			default:
				if (ch != '\n') {
					// Aggiungiamo numero a tmp
					tmp[tmpIndex] = ch;
					tmpIndex++;
				}	
				break;			
		}

	}

	double f100[800], f200[800];
	double x;

	for (j=0; j < 800; j++) {
		f100[j] = f[100][j];
		f200[j] = f[200][j];

		x = (double) (j+1) / 100;
		printf("%f\t%f\n",x,f100[j]);
	}

	fclose(fp);
	return 0;
}
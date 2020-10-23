#include <stdio.h> 
#include <time.h> 
#include <rpc/rpc.h> 

#include "load.h" 
#define RMACHINE "sprc2.dfilip.xyz"

int main(int argc, char *argv[]){

	/* variabila clientului */
	CLIENT *handle;

	char **res;
	
	handle=clnt_create(
		RMACHINE,		/* numele masinii unde se afla server-ul */
		CHECKPROG,		/* numele programului disponibil pe server */
		CHECKVERS,		/* versiunea programului */
		"tcp");			/* tipul conexiunii client-server */
	
	if(handle == NULL) {
		perror("");
		return -1;
	}

	struct student student;
	student.nume = "Alexandra Minea";
	student.grupa = "342C3";
	res = grade_1(&student, handle); 
	printf("%s", *res);
	
	return 0;
}

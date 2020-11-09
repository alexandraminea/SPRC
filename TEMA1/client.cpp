#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <rpc/rpc.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include "rpcdb.h"
#define RMACHINE "localhost"

using namespace std;

string getNthWord(std::string s, size_t n)
{
    std::istringstream iss (s);
    while(n-- > 0 && (iss >> s));
    return s;
}

int main(int argc, char *argv[]){

	/* variabila clientului */
	CLIENT *handle;
    
    string filename = "";
    string commands_file = "commands.txt";
    ifstream fcom(commands_file);
	
    char **res;
	
	handle=clnt_create(
		RMACHINE,		/* numele masinii unde se afla server-ul */
		RPCDB_PROG,		/* numele programului disponibil pe server */
		RPCDB_VERS,		/* versiunea programului */
		"tcp");			/* tipul conexiunii client-server */
	
	if(handle == NULL) {
		perror("");
		return -1;
	}

    bool load = false;

    string line;
    getline(fcom, line);

    if(line.compare(0, 5, "login") != 0)
        cout << "You must login first: login <username>" << endl;
    else {
        string name = getNthWord(line, 3);
        cout<<name<<endl;
        
        username *user = (username *) malloc(sizeof(username));
        response *resp = (response *) malloc (sizeof(response));        
        user->name = strdup(name.c_str());

        // login
        resp = login_1(user, handle);
        cout << resp->resp << endl;

    }
    getline(fcom, line);
    if(line.compare(0, 4, "load") == 0)
        load = true;
	while(getline(fcom, line)) {
        //cout << line << endl;
    }


	
	return 0;
}
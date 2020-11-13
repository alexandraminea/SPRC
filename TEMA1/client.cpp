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

    username *user = (username *) malloc(sizeof(username));
    response *resp = (response *) malloc (sizeof(response)); 

    bool load_data = false;
    unsigned long *key;
    string line;
    getline(fcom, line);

    if(line.compare(0, 5, "login") != 0)
    {
        cout << "You must login first: login <username>" << endl;
        exit(1);
    }

    // username
    string name = getNthWord(line, 3);
    user->name = strdup(name.c_str());

    // login
    key = login_1(user, handle);
    cout << "Received key from server: " << *key << endl;

    getline(fcom, line);
    if(line.compare(0, 4, "load") == 0)
        load_data = true;

    // load
    if(load_data) {

        resp = load_1(key, handle);
        cout << resp->resp << endl;
    } else {
        // no load
    }

	while(getline(fcom, line)) {

        // store
        if (!line.compare("store")) {
            resp = store_1(key, handle);
            cout << resp->resp << endl;
        }
        else if (!line.compare(0, 3, "add")) {
            istringstream iss(line);
            int id, n;
            struct sensor_data val;
            struct user_data data;
            
            // build struct sensor_data
            string word;
            iss >> word >> id >> n;
            // cout << n << endl;
            val.values.values_val = (float *) malloc (n * sizeof (float));
            for (int i = 0 ; i < n ; i++)
                iss >> val.values.values_val[i];
            val.data_id = id;
            val.values.values_len = n;
            
            //build struct user data
            data.key = *key;
            data.data = val;

            resp = add_1(&data, handle);
            cout << resp->resp << endl;
        }
        else if (!line.compare(0, 3, "del")) {
            istringstream iss(line);
            int id;
            struct del_data data;
            
            // build struct sensor_data
            string word;
            iss >> word >> id;
            
            //build struct user data
            data.key = *key;
            data.data_id = id;

            resp = del_1(&data, handle);
            cout << resp->resp << endl;
        } else if (!line.compare(0, 6, "update")) {
            istringstream iss(line);
            int id, n;
            struct sensor_data val;
            struct user_data data;
            
            // build struct sensor_data
            string word;
            iss >> word >> id >> n;
            // cout << n << endl;
            val.values.values_val = (float *) malloc (n * sizeof (float));
            for (int i = 0 ; i < n ; i++)
                iss >> val.values.values_val[i];
            val.data_id = id;
            val.values.values_len = n;
            
            //build struct user data
            data.key = *key;
            data.data = val;

            resp = update_1(&data, handle);
            cout << resp->resp << endl;
        } else if (!line.compare(0, 4, "read")) {
            istringstream iss(line);
            int id;
            struct read_data data;
            
            // build struct sensor_data
            string word;
            iss >> word >> id;
            
            //build struct user data
            data.key = *key;
            data.data_id = id;

            resp = read_1(&data, handle);
            cout << resp->resp << endl;
        } else if (!line.compare(0, 8, "get_stat") && line[8] != '_') {
            istringstream iss(line);
            int id;
            struct read_data data;
            
            // build struct sensor_data
            string word;
            iss >> word >> id;
            
            //build struct user data
            data.key = *key;
            data.data_id = id;

            resp = get_stat_1(&data, handle);
            cout << resp->resp << endl;
        }
    }
	
	return 0;
}
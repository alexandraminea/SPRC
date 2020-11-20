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

CLIENT *handle;
string filename = "";
char **res;
unsigned long *key;
static username *user;

void parse_line(string line) {
        response *resp;
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

            free(val.values.values_val);
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

            free(val.values.values_val);

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

        } else if (!line.compare(0, 9, "get_stat_")) {
            resp = get_stat_all_1(key, handle);
            cout << resp->resp << endl;
        } else if (!line.compare(0, 6, "logout")) {
            resp = logout_1(key, handle);
            cout << resp->resp << endl;
            clnt_destroy(handle);
            exit(0);
        } else if(line.compare(0, 4, "load") == 0) {
            cout << "LOAD HAS NO EFFECT\n";
        } else {
            cout << "USUPPORTED COMAND" << endl;
            cout << "USAGE: store/add/del/read/get_stat/get_stat_all" << endl;
        }
}

string getNthWord(std::string s, size_t n)
{
    std::istringstream iss (s);
    while(n-- > 0 && (iss >> s));
    return s;
}

int main(int argc, char *argv[]){

	/* variabila clientului */
    
    string filename = "";
		
	handle=clnt_create(
		RMACHINE,
		RPCDB_PROG,
		RPCDB_VERS,
		"tcp");
	
	if(handle == NULL) {
		perror("");
		return -1;
	}

    response *resp;
    user = (username *) malloc(sizeof(username)); 

    bool load_data = false;
    string line;
    getline(cin, line);

    if(line.compare(0, 5, "login") != 0)
    {
        cout << "YOU MUST LOGIN FIRST: login <USERNAME>" << endl;
        exit(1);
    }

    // username
    string name = getNthWord(line, 3);
    user->name = strdup(name.c_str());

    // login
    key = login_1(user, handle);
    free(user->name);
    free(user);
    cout << "RECEIVED KEY: " << *key << endl;
    if(*key == 0) {
        cout << "USER " << user->name << " ALREADY LOGGED IN" << endl;
        exit(1);
    }

    getline(cin, line);
    if(line.compare(0, 4, "load") == 0)
        load_data = true;

    // load
    if(load_data) {
        resp = load_1(key, handle);
        cout << resp->resp << endl;
    } else {
        parse_line(line);
    }

	while(getline(cin, line)) {
        parse_line(line);
    }

	return 0;
}
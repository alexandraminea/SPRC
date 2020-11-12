#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <rpc/rpc.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <string>
#include <vector>
#include <dirent.h>
#include <unordered_set>


#include "rpcdb.h"

using namespace std;

const char *ACK = "OK";
const char *NACK = "CONNECTION DENIED";
unsigned long count = 1;

map<string, unsigned long> users;
map<string, vector<struct sensor_data>> database;

unordered_set<string> filenames;

bool search_user(string name) {
    map<string , unsigned long>::iterator it;
    it = users.find(name);
    return it != users.end();
}

bool search_db_for_user(string name) {
    map<string , vector<struct sensor_data>>::iterator it;
    it = database.find(name);
    return it != database.end();
}

bool search_filename(string name) {
    return filenames.find(name) != filenames.end();
}

void add_file(string filename) {
    // create file
    string path = "./database/" + filename;
    ofstream f(path.c_str());
    f << "";
    f.close();

    // add entry in memory
    vector<struct sensor_data> v;
    database[filename] = v;
}

void load_file(string filename) {
    string path = "./database/" + filename;
    ifstream f(path.c_str());
    int id, n;
    string line;
    while(getline(f, line)) {

        istringstream iss(line);
        //cout << line << endl;
        // create entry in db
        struct sensor_data val;
        iss >> id >> n;
        val.values.values_val = (float *) malloc (n * sizeof (float));
        for (int i = 0 ; i < n ; i++)
        {
            iss >> val.values.values_val[i];
        }
        val.data_id = id;
        val.values.values_len = n;

        //add entry to temporary db
        database[filename].push_back(val);
    }
    f.close();
}

string get_user(unsigned long *key) {
    string name;
    for (auto &i : users) {
        if (i.second == *key) {
            name = i.first;
            break;
        }
    }
    return name;
}

void store_file(string filename) {
    string path = "./database/" + filename;
    ofstream f(path.c_str());
    vector<struct sensor_data> v = database[filename];
    for(int i = 0; i < v.size(); i++)
    {   
        f << v[i].data_id << " " << v[i].values.values_len << " "; 
        for(int j = 0; j < v[i].values.values_len; j++)
            f << v[i].values.values_val[j] << " ";
        f << endl;
    }

    f.close();
}

void add_data(string filename, struct sensor_data data) {
    
    database[filename].push_back(data);        
}

unsigned long* login_1_svc(username* user, struct svc_req *cl) {
    static unsigned long res = 0;
    if(search_user(string(user->name)))
        cout << "USER " << user->name << " ALREADY LOGGED IN" << endl;
    else {
        // add user in map
        users[user->name] = count;
        res = count;
        count++;
    }
    return &res;
}

response* load_1_svc(unsigned long *key, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));

    string name = get_user(key);
    DIR *dir; struct dirent *diread;
    string file = name + ".dbms";

    if ((dir = opendir("./database")) != nullptr) {
        while ((diread = readdir(dir)) != nullptr
                && (string(diread->d_name)).compare(".") != 0
                && (string(diread->d_name)).compare("..")) {
            filenames.insert(string(diread->d_name));
        }
        closedir (dir);
    } else {
        perror ("opendir");
        exit(10);
    }

    // user file doesn't exist on disk yet
    if(!search_filename(file)) {
        add_file(file);
    } else
        load_file(file);
    resp->resp = strdup("LOAD DONE");
    return resp;
}

response* add_1_svc(struct user_data *data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    string name = get_user(&key);

    // copy the sensor data into a db entry
    struct sensor_data entry = data->data;

    // deep copy of float*
    entry.values.values_val = (float *)malloc(entry.values.values_len *sizeof(float));
    memcpy(entry.values.values_val, data->data.values.values_val, entry.values.values_len *sizeof(float));


    string file = name + ".dbms";

    // add entry in local db (in memory)
    add_data(file, entry);
    resp->resp = strdup("DATA ADDED");
    return resp;
}

response* store_1_svc(unsigned long *key, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    string name = get_user(key);
    string file = name + ".dbms";
    store_file(file);
    resp->resp = strdup("DB STORED");
    return resp;
}

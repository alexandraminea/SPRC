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
#include <algorithm>


#include "rpcdb.h"


using namespace std;

const char *ACK = "OK";
const char *NACK = "CONNECTION DENIED";
unsigned long contor = 1;
unsigned long err = 0;

map<string, unsigned long> users;
map<string, vector<struct sensor_data>> database;

vector<string> filenames;

bool user_exists(string name) {
    map<string , unsigned long>::iterator it;
    it = users.find(name);
    return it != users.end();
}

bool filename_exists(string name) {
    return find(filenames.begin(), filenames.end(), name) != filenames.end();
}

bool data_id_exists(int data_id, string filename) {
    return find_if (database[filename].begin(), 
                    database[filename].end(), 
                    [&](const struct sensor_data &f) 
                    { return f.data_id == data_id; }) != database[filename].end();
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

        //add entry to temporary if it doesn't exist
        if(!data_id_exists(id, filename))
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
    ofstream f(path.c_str(), ofstream::trunc);
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

void del_entry(int data_id, string filename) {
    
    int i = 0;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            free(data.values.values_val);
            database[filename].erase(database[filename].begin() + i);
            return;
        }
        i++;
    }
}

void update_entry(struct sensor_data data_updated, string filename) {
    
    int i = 0;
    for(auto data : database[filename]) {
        if(data.data_id == data_updated.data_id) {
            int len = data_updated.values.values_len;
            memcpy(data.values.values_val, data_updated.values.values_val, len * sizeof(float));
            return;
        }
        i++;
    }
}

string read_entry(int data_id, string filename) {
    
    int i = 0;
    string s;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            ostringstream os;
            int len = data.values.values_len;
            for (int i = 0 ; i < len; i++) {
                os << data.values.values_val[i] << " " ;
            }
            string str(os.str());
            s = str;
            return s;
        }
        i++;
    }
    return s;
}

float mean(float a[], int n)
{
    float sum = 0.0f;
    for (int i = 0; i < n; i++)
        sum += a[i];

    return sum / n;
}

float median(float a[], int n)
{
    sort(a, a + n);
    if (n % 2 != 0)
        return (double)a[n / 2];

    return (double)(a[(n-1)/2] + a[n/2]) / 2;
}

string get_min(int data_id, string filename) {
    int i = 0;
    string s;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            int len = data.values.values_len;
            float* m = min_element(data.values.values_val, data.values.values_val + len);
            ostringstream os;
            os << *m;
            string str(os.str());
            return str;
        }
        i++;
    }
    return s;
}

string get_max(int data_id, string filename) {
    int i = 0;
    string s;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            int len = data.values.values_len;
            float* m = max_element(data.values.values_val, data.values.values_val + len);
            ostringstream os;
            os << *m;
            string str(os.str());
            return str;
        }
        i++;
    }
    return s;
}

string get_mean(int data_id, string filename) {
    int i = 0;
    string s;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            int len = data.values.values_len;
            float m = mean(data.values.values_val, len);
            ostringstream os;
            os << m;
            string str(os.str());
            return str;
        }
        i++;
    }
    return s;
}

string get_median(int data_id, string filename) {
    int i = 0;
    string s;
    for(auto data : database[filename]) {
        if(data.data_id == data_id) {
            int len = data.values.values_len;
            float m = median(data.values.values_val, len);
            ostringstream os;
            os << m;
            string str(os.str());
            return str;
        }
        i++;
    }
    return s;
}

string get_one_stat(int data_id, string file) {
    return "STATS FOR ID: " + to_string(data_id)
        + "\n"
        + "MIN: " + get_min(data_id, file)
        + "\nMAX: " + get_max(data_id, file)
        + "\nMEAN: " + get_mean(data_id, file)
        + "\nMEDIAN: " + get_median(data_id, file)
        + "\n";
}

string get_all_stats(string filename) {
    string res;
    for(auto data : database[filename]) {
        string s = get_one_stat(data.data_id, filename);
        res += s;
    }

    return res;
}

void end_session(string name, string filename) {
    map<string, vector<struct sensor_data>>::iterator it;
    it = database.find(filename);
    database.erase (it, database.end());

    map<string , unsigned long>::iterator it2;
    it2 = users.find(name);
    users.erase (it2, users.end());
}

unsigned long* login_1_svc(username* user, struct svc_req *cl) {
    static unsigned long res = 0;
    if(user_exists(string(user->name)))
    {
        return &err;
    }
    // add user in map
    users[user->name] = contor;
    res = contor;
    contor++;

    return &res;
}

response* load_1_svc(unsigned long *key, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));

    string name = get_user(key);
    DIR *dir; struct dirent *diread;
    string file = name + ".dbms";

    if ((dir = opendir("./database/")) != NULL) {
        while ((diread = readdir(dir)) != NULL)
        {
            filenames.push_back(string(diread->d_name));
        }
        closedir (dir);
    } else {
        perror ("opendir");
        exit(10);
    }

    // user file doesn't exist on disk yet
    if(!filename_exists(file)) {
        add_file(file);
    } else {
        load_file(file);
    }
    resp->resp = strdup("LOAD DONE");
    return resp;
}

response* add_1_svc(struct user_data *data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    string name = get_user(&key);
    string file = name + ".dbms";

    // check if data is already added
    if(!data_id_exists(data->data.data_id, file)) {

        // copy the sensor data into a db entry
        struct sensor_data entry = data->data;
        int len = entry.values.values_len;

        // deep copy of float*
        entry.values.values_val = (float *)malloc(len *sizeof(float));
        memcpy(entry.values.values_val, data->data.values.values_val, len *sizeof(float));

        // add entry in local db (in memory)
        add_data(file, entry);
        resp->resp = strdup("DATA ADDED");
        return resp;
    }
    resp->resp = strdup("DATA ALREADY ADDED");
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

response* del_1_svc(struct del_data* data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    int data_id = data->data_id;
    string name = get_user(&key);
    string file = name + ".dbms";

    if(data_id_exists(data_id, file)) {
        del_entry(data_id, file);
        resp->resp = strdup("DATA DELETED");
        return resp;
    }
    resp->resp = strdup("NO SUCH DATA");
    return resp;
}

response* update_1_svc(struct user_data* data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    struct sensor_data entry = data->data;
    string name = get_user(&key);
    string file = name + ".dbms";
    
    if(data_id_exists(data->data.data_id, file)) {
        update_entry(entry, file);
        resp->resp = strdup("DATA UPDATED");
        return resp;
    }
    resp->resp = strdup("NO SUCH DATA");
    return resp;
}

response* read_1_svc(struct read_data* data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    int data_id = data->data_id;
    string name = get_user(&key);
    string file = name + ".dbms";
    
    if(data_id_exists(data_id, file)) {
        string s = "VALUES: " + read_entry(data_id, file);
        resp->resp = strdup(s.c_str());
        return resp;
    }
    resp->resp = strdup("NO SUCH DATA");
    return resp;
}

response* get_stat_1_svc(struct read_data* data, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    unsigned long key = data->key;
    int data_id = data->data_id;
    string name = get_user(&key);
    string file = name + ".dbms";
    
    if(data_id_exists(data_id, file)) {
        string s = get_one_stat(data_id, file);
        resp->resp = strdup(s.c_str());
        return resp;
    }
    resp->resp = strdup("NO SUCH DATA");
    return resp;
}

response* get_stat_all_1_svc(unsigned long *key, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    string name = get_user(key);
    string file = name + ".dbms";
    
    string res = get_all_stats(file);
    resp->resp = strdup(res.c_str());
    return resp;
}

response* logout_1_svc(unsigned long *key, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    string name = get_user(key);
    string file = name + ".dbms";
    
    end_session(name, file);
    resp->resp = strdup("BYE");
    return resp;
}

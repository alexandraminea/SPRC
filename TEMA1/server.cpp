#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <rpc/rpc.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <string>

#include "rpcdb.h"

using namespace std;

const char *ACK = "OK";
const char *NACK = "CONNECTION DENIED";
unsigned long count = 0;

map<string, unsigned long> users;

bool search_user(string name) {
    map<string , unsigned long>::iterator it;
    it = users.find(name);
    return it != users.end();
}


response* login_1_svc(username* user, struct svc_req *cl) {
	response *resp = (response *) malloc (sizeof(response));
    if(search_user(string(user->name)))
        resp->resp = strdup("USER ALREADY LOGGED IN");
    else {
        // add user in map
        users[user->name] = count;
        count++;
        resp->resp = strdup("ADDED");
    }
    return resp;
}
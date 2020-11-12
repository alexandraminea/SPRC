struct sensor_data{
    int data_id;
    float values<>;
};

struct user_data {
    struct sensor_data data;
    unsigned long key;
};

struct response {
    string resp<>;
};

struct username {
    string name<>;
};

program RPCDB_PROG {
	version RPCDB_VERS {
		unsigned long login(username) = 1;
        response load(unsigned long) = 2;
        response store(unsigned long) = 3;
        response add(user_data) = 4;
	} = 1;
} = 1;
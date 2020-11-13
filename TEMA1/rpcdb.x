struct sensor_data{
    int data_id;
    float values<>;
};

struct user_data {
    struct sensor_data data;
    unsigned long key;
};

struct del_data {
    int data_id;
    unsigned long key;
};

struct read_data {
    int data_id;
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
        response del(del_data) = 5;
        response update(user_data) = 6;
        response read(read_data) = 7;
        response get_stat(read_data) = 8;
        response get_stat_all(unsigned long) = 9;
	} = 1;
} = 1;
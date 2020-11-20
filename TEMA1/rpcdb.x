/* sensor data */
struct sensor_data{
    int data_id;
    float values<>;
};

/* parameter for add and update functions */
struct user_data {
    struct sensor_data data;
    unsigned long key;
};

/* parameter for delete function */
struct del_data {
    int data_id;
    unsigned long key;
};

/* parameter type for read and get_stat functions */
struct read_data {
    int data_id;
    unsigned long key;
};

/* response from the server */
struct response {
    string resp<>;
};

/* username */
struct username {
    string name<>;
};

program RPCDB_PROG {
	version RPCDB_VERS {
        /* login function */
		unsigned long login(username) = 1;

        /* load function */
        response load(unsigned long) = 2;

        /* store function */
        response store(unsigned long) = 3;

        /* add function */
        response add(user_data) = 4;

        /* delete funciton */
        response del(del_data) = 5;

        /* update function */
        response update(user_data) = 6;

        /* read function */
        response read(read_data) = 7;

        /* get stats function */
        response get_stat(read_data) = 8;

        /* get stats of all entries in database */
        response get_stat_all(unsigned long) = 9;

        /* logout function */
        response logout(unsigned long) = 10;
	} = 1;
} = 1;
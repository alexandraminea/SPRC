struct sum_data {
	int x;
	int y;
};

struct response {
    string resp<>;
};

struct username {
    string name<>;
};

program RPCDB_PROG {
	version RPCDB_VERS {
		response login(username) = 1;
	} = 1;
} = 1;
build:
	rpcgen -C rpcdb.x
	g++ -o server -g server.cpp rpcdb_svc.c rpcdb_xdr.c -lnsl
	g++ -o client -g client.cpp rpcdb_clnt.c rpcdb_xdr.c -lnsl

clean:
	rm -f server client rpcdb_* rpcdb.h
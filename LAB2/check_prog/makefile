build:
	rpcgen -C load.x
	#gcc -o server rpc_server.c load_svc.c -lnsl -Wall
	gcc -o client rpc_client.c load_clnt.c load_xdr.c -lnsl -Wall

clean:
	rm -f client server load.h load_svc.c load_clnt.c

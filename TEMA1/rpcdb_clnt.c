/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#include <memory.h> /* for memset */
#include "rpcdb.h"

/* Default timeout can be changed using clnt_control() */
static struct timeval TIMEOUT = { 25, 0 };

u_long *
login_1(username *argp, CLIENT *clnt)
{
	static u_long clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, login,
		(xdrproc_t) xdr_username, (caddr_t) argp,
		(xdrproc_t) xdr_u_long, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
load_1(u_long *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, load,
		(xdrproc_t) xdr_u_long, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
store_1(u_long *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, store,
		(xdrproc_t) xdr_u_long, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
add_1(user_data *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, add,
		(xdrproc_t) xdr_user_data, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
del_1(del_data *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, del,
		(xdrproc_t) xdr_del_data, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
update_1(user_data *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, update,
		(xdrproc_t) xdr_user_data, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
read_1(read_data *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, read,
		(xdrproc_t) xdr_read_data, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

response *
get_stat_1(read_data *argp, CLIENT *clnt)
{
	static response clnt_res;

	memset((char *)&clnt_res, 0, sizeof(clnt_res));
	if (clnt_call (clnt, get_stat,
		(xdrproc_t) xdr_read_data, (caddr_t) argp,
		(xdrproc_t) xdr_response, (caddr_t) &clnt_res,
		TIMEOUT) != RPC_SUCCESS) {
		return (NULL);
	}
	return (&clnt_res);
}

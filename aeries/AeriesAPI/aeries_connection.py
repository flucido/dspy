import pymssql

SERVER = "sql1.millercreeksd.aeries.net"
DATABASE = "DST23000MillerCreekSD"
USER = "MCSD.ROSQL"
PASSWORD = "BHnPV5nuf2Mv"


def aeries_connection():
	conn = pymssql.connect(SERVER, USER, PASSWORD, DATABASE)
	return conn

import urequests as requests

LOCAL_HOST = 'http://127.0.0.1'


def buildQuery(dicted: dict):
	query = ""
	for key in list(dicted.keys()):
		query += f"{key}={dicted[key]}&"
	print(f"Query from buildQuery: {query}")
	return query


def Query(hostIP=LOCAL_HOST, query='', path=''):
	r = requests.get(f'{hostIP}{path}?{query}')
	return r.status_code

import sys
from elasticsearch import Elasticsearch
es = Elasticsearch()

query = "virginia"
if len(sys.argv) == 2:
    query = sys.argv[1]

body = {
	"query": {
		"match": {
			"message": query
		}
	}
}
res = es.search(index="tweets", body=body)
print("Got %d hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(date)s %(author)s: %(message)s" % hit["_source"])
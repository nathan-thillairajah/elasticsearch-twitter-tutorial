from elasticsearch import Elasticsearch
es = Elasticsearch()

body = {
	"query": {
		"match": {
			"message": "virginia"
		}
	}
}
res = es.search(index="tweets", body=body)
print("Got %d hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(date)s %(author)s: %(message)s" % hit["_source"])
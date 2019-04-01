from elasticsearch import Elasticsearch
es = Elasticsearch()

res = es.search(index="tweets", body={"query": {"match": {"message": "virginia"}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(date)s %(author)s: %(message)s" % hit["_source"])
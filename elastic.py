from urllib.request import urlopen
import urllib.parse
import simplejson
import json

def search(query):

    tuples = [('q',query)]

    solr_url = "http://localhost:9200/cv/_search?"
    # enocde for URL format
    encoded_solr_tuples = urllib.parse.urlencode(tuples)
    complete_url = solr_url + encoded_solr_tuples
    print(complete_url)
    connection = urlopen(complete_url)
    raw_response = simplejson.load(connection)

    return raw_response


if __name__ == "__main__":

    search_res = search('data scientist')

    results = search_res['hits']['hits']
    
    with open('hits.json','w') as f:
        json.dump(results,f)
    print(search_res)
from urllib.request import urlopen
import urllib.parse
import simplejson
import json
from nltk.util import ngrams
from collections import Counter

def search(query):

    tuples = [('q',query)]

    solr_url = "http://localhost:9200/cv/_search?"
    # enocde for URL format
    encoded_solr_tuples = urllib.parse.urlencode(tuples)
    complete_url = solr_url + encoded_solr_tuples
    connection = urlopen(complete_url)
    raw_response = simplejson.load(connection)

    return raw_response


def ngram_gen(input, gram=2):

    tokens = [token for token in input.split(" ") if token!=""]
    counts = Counter(list(ngrams(tokens, gram)))
    return list(map(lambda x:(x[0], x[1]), counts.items()))

if __name__ == "__main__":

    queries = ['Big Data Engineer']
    search_res = search("or".join(queries))

    results = search_res['hits']['hits']
    
    with open('hits.json','w') as f:
        json.dump(results,f)

    queries_gram = {}
    for i,query in enumerate(queries):
        queries_gram[i] = ngram_gen(query)

    profiles = []
    for result in results:
        profile = {}
        profile["_id"] = result["_id"]
        profile["_index"] = result["_index"]
        profile["_score"] = result["_score"]
        experiences = result["_source"]["experience"]
        for experience in experiences:
            experience["title"] = ngram_gen(experience["title"],2)
            experience["description"] = ngram_gen(experience["description"])

        profile["_source"] = {
            "title" : ngram_gen(result["_source"]["title"]),
            "experience" : experiences
        }
        profile["skills"] = result["_source"]["skills"]

        profiles.append(profile)

    with open('profiles.json','w') as f:
        json.dump(profiles,f)



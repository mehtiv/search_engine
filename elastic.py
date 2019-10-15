from urllib.request import urlopen
import urllib.parse
import simplejson
import json
from nltk.util import ngrams
from collections import Counter
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import re
import string
from functools import reduce


stop_words = set(stopwords.words('english'))

def clean_string(text):

    text = text.lower().strip()
    spec_chars =  "([" + string.punctuation + "\° ].*?)"
    #spec_chars = 
    text = re.sub(spec_chars, ' ', text)
    
    word_tokens = word_tokenize(text) 
    
    return " ".join([w for w in word_tokens if not w in stop_words])


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

    # return list(map(lambda x:(x[0], x[1]), counts.items()))
    return counts


def cross_ngrams(query, text):

    query_gram = ngram_gen(query)
    text_gram  = ngram_gen(text)
    intersect = query_gram & text_gram
    for element in intersect:
        intersect[element] = text_gram[element]
    return intersect


def score_ngram(ngrams, type_text, coef = 0):

    if type_text == "title":
        return ngrams
    else:
        for gram in ngrams:
            ngrams[gram] = coef * ngrams[gram]
        return ngrams


if __name__ == "__main__":

    queries = ['developer java', 'developer c#', 'web developer']
    search_res = search("OR".join(queries))

    results = search_res['hits']['hits']
    
    with open('hits.json','w') as f:
        json.dump(results,f)


    profiles = []
    experienc_score = [1, 0.5, 0.25]

    for result in results:
        profile = {}
        profile["_id"] = result["_id"]
        profile["_index"] = result["_index"]
        profile["_score"] = result["_score"]
        experiences = result["_source"]["experience"]
        print("")
        for experience in experiences:
            n_grams = [score_ngram(cross_ngrams(clean_string(query), clean_string(experience['title'])), 'title') for query in queries]
            n_grams_experience = [score_ngram(cross_ngrams(clean_string(query), clean_string(experience['description'])),'experience', 
            coef=experience['duration']) for query in queries]
            
            title_score = reduce(lambda a,b:a+b, n_grams)
            experience_score = reduce(lambda a,b: a+b, n_grams_experience)

            experience["score"] = 0.5*sum(title_score.values()) + sum(experience_score.values())
            
        n_grams_title = [score_ngram(cross_ngrams(clean_string(query), clean_string(result["_source"]["title"])), 'title') for query in queries]
        print(n_grams_title)
        title_score = reduce(lambda a,b:a+b, n_grams_title)
        print(title_score)
        title_score = 0.8*sum(title_score.values())
        profile["_source"] = {
            "title" : result["_source"]["title"],
            "title_score" : title_score,
            "experience" : experiences
        }
        profile["skills"] = result["_source"]["skills"]

        profiles.append(profile)
    #print(profiles)
    with open('profiles.json','w') as f:
        json.dump(profiles,f)

    



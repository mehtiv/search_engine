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

stop_words = set(stopwords.words('french'))

import operator

def clean_string(text : str) -> str:
    """[summary]
        Clean a string removing stop word and special caracters
    Arguments:
        text {str} -- string to clean

    Returns:
        str -- cleaned string
    """
    
    text = text.lower().strip()
    spec_chars =  "([" + string.punctuation + "\° ].*?)"
    text = re.sub(spec_chars, ' ', text)
    
    word_tokens = word_tokenize(text) 
    
    return " ".join([w for w in word_tokens if not w in stop_words])


def search(query : str ) -> dict:
    """[summary]
        get result of a query from elasticsearch
    Arguments:
        query {str} -- [description]
    
    Returns:
        dict -- [description]
    """

    tuples = [('q',query)]

    solr_url = "http://localhost:9200/cv/_search?"
    # enocde for URL format
    encoded_solr_tuples = urllib.parse.urlencode(tuples)
    complete_url = solr_url + encoded_solr_tuples
    connection = urlopen(complete_url)
    raw_response = simplejson.load(connection)

    return raw_response


def ngram_gen(input : str, gram:int =2) -> Counter:
    """[summary]
        calculate N_gram 
    Arguments:
        input {str} -- [description]
    
    Keyword Arguments:
        gram {int} -- [description] (default: {2})
    
    Returns:
        Counter -- [description]
    """
    tokens = [token for token in input.split(" ") if token!=""]
    counts = Counter(list(ngrams(tokens, gram)))

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


def sort_candidate(json_file):
    

    return sorted(json_file.items(), key=operator.itemgetter(1))


if __name__ == "__main__":

    queries = ['data scientist', 'machine learning', 'deep learning']
    search_res = search("OR".join(queries))

    results = search_res['hits']['hits']
    
    with open('hits.json','w') as f:
        json.dump(results,f)


    profiles = []
    experienc_score = [1, 0.5, 0.25]
    
    # calculate new score for each candidate from the results of elastic search
    for result in results:

        profile = {}
        profile["_id"] = result["_id"]
        profile["_index"] = result["_index"]
        profile["_score"] = result["_score"]
        experiences = result["_source"]["experience"]

        
        experience_total_score = 0
        for experience in experiences:
            n_grams = [score_ngram(cross_ngrams(clean_string(query), clean_string(experience['title'])), 'title') for query in queries]
            n_grams_experience = [score_ngram(cross_ngrams(clean_string(query), clean_string(experience['description'])),'experience', coef=experience['duration']) for query in queries]
            
            title_score = reduce(lambda a,b:a+b, n_grams)
            experience_score = reduce(lambda a,b: a+b, n_grams_experience)

            experience["score"] = (0.5*sum(title_score.values()) + sum(experience_score.values()))*experience['duration']
            
            experience_total_score += experience['score']

        
        n_grams_title = [score_ngram(cross_ngrams(clean_string(query), clean_string(result["_source"]["title"])), 'title') for query in queries]
        
        title_score = reduce(lambda a,b:a+b, n_grams_title)
        
        title_score = 0.8*sum(title_score.values())
        
        profile["_source"] = {
            "title" : result["_source"]["title"],
            "title_score" : title_score,
            "experience" : experiences
        }
        
        #profile["skills"] = result["_source"]["skills"]
        profile["total_score"] = experience_total_score + title_score + np.log(profile["_score"])
        profiles.append(profile)
    
    
    tuples = [(x['_id'], x['total_score'], x) for x in profiles]

    profiles = sorted(tuples, key = lambda tup:tup[1], reverse=True)

    with open('profiles.json','w') as f:
        json.dump(profiles,f)
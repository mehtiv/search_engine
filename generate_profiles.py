import json
import random
from elasticsearch import Elasticsearch
import codecs
import string
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import math
import numpy as np

MEAN_EXPE = 18
SD_EXPE   = math.sqrt(12)

list_exp = np.random.normal(MEAN_EXPE, math.sqrt(SD_EXPE), 1000)
stop_words = set(stopwords.words('french'))

porter = PorterStemmer()

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
    
    return " ".join([porter.stem(w) for w in word_tokens if not w in stop_words])


PATH = './Data/cv'



es = Elasticsearch(
    ['localhost'],
    port=9200

)


with codecs.open(PATH+'/resumes.json', encoding='utf-8') as resumes:
    data = json.load(resumes)['data']

resumes.close()
i = 0
for profile in data:
    i +=1
    file_profil = {}
    experiences = []
    file_profil['id'] = i
    file_profil['title'] = clean_string(profile['title'])
    for experience in profile['experiences']:
        experience_content = {}

        experience_content['title'] = clean_string(experience['title'])
        experience_content['description'] = clean_string(experience['description'])
        experience_content['duration'] = int(random.choice(list_exp))

        experiences.append(experience_content)

    file_profil['experience'] = experiences
    

    with open(PATH+'/profile_'+str(i)+'.json', 'w', encoding='utf8') as file:
        json.dump(file_profil, file, ensure_ascii=False)

    file.close()

    es.index(index='cv', doc_type='Blog', id=i, body=file_profil)

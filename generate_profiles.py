import json
import random
from elasticsearch import Elasticsearch
import codecs

PATH = './Data/cv'



es = Elasticsearch(
    ['localhost'],
    port=9200

)


with codecs.open(PATH+'/resumes.json', encoding='latin1') as resumes:
    data = json.load(resumes)['data']

resumes.close()
i = 0
for profile in data:
    i +=1
    file_profil = {}
    experiences = []
    file_profil['id'] = i
    file_profil['title'] = profile['title']
    for experience in profile['experiences']:
        experience_content = {}

        experience_content['title'] = experience['title']
        experience_content['description'] = experience['description']
        experience_content['duration'] = random.randint(3,120)

        experiences.append(experience_content)

    file_profil['experience'] = experiences
    

    with open(PATH+'/profile_'+str(i)+'.json', 'w') as file:
        json.dump(file_profil, file)

    file.close()

    #es.index(index='cv', doc_type='Blog', id=i, body=file_profil)

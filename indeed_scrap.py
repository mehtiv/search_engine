from selenium import webdriver
from time import sleep
from parsel import Selector
import json
from time import sleep

nb_page = 20

driver = webdriver.Chrome("/home/mehdi/Documents/chromedriver")
request = "data scientist"

job_links_list = []
for i in range(nb_page):
    sleep(4)
    url = 'https://www.indeed.com/jobs?q='+"+".join(request.split(" "))+'&l=New+York%2C+NY&start='+str(i*10)
    driver.get(url)

    job_container = driver.find_element_by_id('resultsCol')

    job_list = driver.find_elements_by_xpath("//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")


    for job in job_list:
        job_links_list.append(job.find_element_by_tag_name('a').get_attribute("href"))

elements = {
    request : job_links_list
}

for i,offre in enumerate(elements[request]):
    sleep(2)
    driver.get(offre)
    
    offre_title = driver.find_element_by_tag_name('h3').text
    job_company = driver.find_element_by_xpath("//div[@class='icl-u-lg-mr--sm icl-u-xs-mr--xs']").text
    job_description = driver.find_element_by_xpath("//div[@class='jobsearch-JobComponent-description  icl-u-xs-mt--md  ']").text
    
    json_content = {
        "title" : offre_title,
        "company" : job_company,
        "description" : job_description
    }

    with open("Data/Jobs/"+request+"_"+str(i+1)+".json", "w", encoding='utf8') as file:
        json.dump(json_content, file, ensure_ascii=False)

    file.close()
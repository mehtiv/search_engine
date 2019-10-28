from selenium import webdriver
from time import sleep
from parsel import Selector
import json
from time import sleep

nb_page = 2

driver = webdriver.Chrome("/home/mehdi/Documents/chromedriver")
request = "data scientist"
states = ["New+York%2C+NY", "Atlanta%2C+GA", "Chicago%2C+IL", "Houston%2C+TX", "Orlando%2C+FL", "Las+Vegas%2C+NV", "New+Jersey", "Los+Angeles%2C+CA"]
job_links_list = []

with open("job_title_by_categories.json") as f:
    job_categories = json.load(f)

for job_category in job_categories:
    list_offers = []
    for job_title in job_categories[job_category]:
        for state in states:
            for i in range(nb_page):
                sleep(4)
                url = 'https://www.indeed.com/jobs?q='+"+".join(job_title.split(" "))+'&l='+state+'&start='+str(i*10)
                driver.get(url)
                try:
                    job_container = driver.find_element_by_id('resultsCol')

                    job_list = driver.find_elements_by_xpath("//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")


                    for job in job_list:
                        job_links_list.append(job.find_element_by_tag_name('a').get_attribute("href"))
                except:
                    pass

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
                    "job_category":job_category,
                    "job_title_category":job_title,
                    "title" : offre_title,
                    "company" : job_company,
                    "state":state,
                    "city":state,
                    "description" : job_description
                }
                list_offers.append(json_content)

    with open("Data/Jobs/"+job_category+".json", "w", encoding='utf8') as file:
        json.dump(list_offers, file, ensure_ascii=False)

    file.close()
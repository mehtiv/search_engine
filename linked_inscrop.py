from selenium import webdriver
from time import sleep
from parsel import Selector



driver = webdriver.Chrome("/home/mehdi/Documents/chromedriver")

driver.get('https://www.linkedin.com')
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
sleep(0.5)

username = driver.find_element_by_id('username')
username.send_keys('mehdi.studies@gmail.com')
sleep(0.3)

password = driver.find_element_by_id('password')
password.send_keys('mehdi1993A')
sleep(0.3)

log_in_btn = driver.find_element_by_class_name('login__form_action_container ')
log_in_btn.click()
sleep(0.5)

driver.get("https://www.linkedin.com/in/mehdizarria/")
sleep(0.5)

sel = Selector(text=driver.page_source)

name = driver.find_element_by_xpath("//ul[@class='pv-top-card-v3--list inline-flex align-items-center']")
name = name.find_element_by_xpath("//li[@class='inline t-24 t-black t-normal break-words']")
name = name.text

page = []
#experiences = driver.find_element_by_xpath("//ul[@class='pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more']")
#experiences = driver.find_elements_by_class_name("pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more")
#print(experiences)
experiencess = [experience for experience in driver.find_elements_by_xpath("//section[@id='experience-section']/ul") ]
experiences = experiencess[0].find_elements_by_tag_name("li")
#print(experiences)

#for experience in experiences:
    #print(experience.text)
    # experience = experience.find_element_by_xpath("//div[@class='display-flex justify-space-between full-width']")
experience = experiences[0]
print (type(experience))

profile = {}

name_experience = experience.find_element_by_xpath("//h3[@class='t-16 t-black t-bold']").text
company_name = experience.find_element_by_xpath("//p[@class='pv-entity__secondary-title t-14 t-black t-normal']").text
duration = experience.find_element_by_xpath("//span[@class='pv-entity__bullet-item-v2']").text
location = experience.find_element_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']").text
try:
    description = experience.find_element_by_xpath("//p[@class='pv-entity__description t-14 t-black t-normal mb4 ember-view']").text

except:
    description = ""


profile["name_experience"] = name_experience
profile["company_name"] = company_name
profile["duration"] = duration
profile["location"] = location
profile["description"] = description
print(profile)
page.append(profile)
del profile

print("\n \n")

candidate = {"name":name,
"experiences" : page}
print(page)

driver.quit()
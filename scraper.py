from bs4 import BeautifulSoup
from shutil import copyfile
import requests
import configparser
from urllib.parse import urlparse

url = "https://wrblogs.samnabi.com/"

#Get the URL
#Parse the URL using BS4
#Extract the list of URLs
page = requests.get(url)

if page.status_code != 200:
	print("Status code returned is", page.status_code)
	print("Could not fetch page!")
else:

	soup = BeautifulSoup(page.text,"html.parser")

	#print(soup.prettify())

	links = soup.find_all('a')

	filtered_links = []

	for i in links:
		if i.parent.name == 'li':
			#print(i["href"])
			filtered_links.append(i["href"])

	#print(filtered_links)

	
#Backup the config file to preserve its structure
copyfile("data_articles.ini","data_articles.ini.bak")

#Preprocessing - drop headers that will cause the parser to fail
str = "title = "
with open("data_articles.ini", "r") as f:
    lines = f.readlines()
with open("data_articles.ini", "w") as f:
    for line in lines:
        if str not in line.strip("\n"):
            f.write(line)

#Parse the preprocessed existing articles.ini
article_config = configparser.ConfigParser()
article_config.read('data_articles.ini')

#Compare Sam's links to the existing ini. For any links not found, set up for writeback
for i in filtered_links:
	if i not in article_config:# This definitely isn't accurate since it seems searching is done on config sections only
		o = urlparse(i)
		sectionname = o.hostname.replace(".com", "") #what if it's not .com...probably better to use a regex for this
		sectionscheme = o.scheme
		sectionfqdn = o.netloc
		shortlink = sectionscheme + "://" + sectionfqdn
		article_config[sectionname] = {'link': shortlink, 'feed': i }

#Open the ini file and write the results
with open('new_articles.ini', 'w+') as f:
	article_config.write(f)

#Verify that what we expect is happening...
new_articles = configparser.ConfigParser()
new_articles.read('new_articles.ini')
print(new_articles.sections())




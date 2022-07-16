import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import math



def url_extract():
    url = "https://tr.indeed.com/jobs?q=developer&l=istanbul&start=10&vjk=f92002aecd1889e5"

    url = url.split('start=')[0]
    goto_url = url + 'start='
    domain = url.split('/jobs?')[0]

    return goto_url,domain


def page_count_total():
    goto_url,domain = url_extract()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = goto_url
    r = requests.get(url, headers)

    soup = BeautifulSoup(r.content,'html.parser')

    count = soup.find_all('div',class_='searchCountContainer')
    for i in count:
        count_ = i.find('div',id='searchCountPages').text
        page_total_count = count_.split("(")[1]

    return page_total_count


def page_count_extract():
    count_text = page_count_total()
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    if re.search(p, count_text) is not None:
        for catch in re.finditer(p, count_text):
            count = catch[0]

    page_count = math.ceil(int(count) / int(10))
    return page_count


def extract(page):
    goto_url,domain = url_extract()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url =  goto_url+f"{page}"
    r = requests.get(url, headers)

    soup = BeautifulSoup(r.content,'html.parser')
    return soup


def transform(soup):
    goto_url,domain = url_extract()
    divs = soup.find_all('div',class_='job_seen_beacon')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span',class_='companyName').text.strip()
        try:
            salary = item.find('div',class_='salaryOnly').text.strip()
        except:
            salary = 'Not Found'

        try:
            company_link = item.find('a',class_='turnstileLink companyOverviewLink')['href']
            company_link = domain + company_link
        except:
            company_link = 'Not Found'

        summary = item.find('div',class_='job-snippet').text.strip()
        location = item.find('div',class_='companyLocation').text.strip()
        link = item.find('a',class_='jcs-JobTitle')['href']
        link = domain + link
        job = {
            'link':link,
            'title':title,
            'company':company,
            'company_link':company_link,
            'salary':salary,
            'summary':summary,
            'location':location
        }
        
        joblist.append(job)

    return     

joblist = []

count_page=page_count_extract()

for i in range(0,(count_page*10),10):
    print(f'Getin Page,{i}')

    c = extract(i)
    transform(c)

    #print(joblist)

print(len(joblist))


df = pd.DataFrame(joblist)
print(df.head())
df.to_excel('jobs.xlsx')
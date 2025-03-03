from bs4 import BeautifulSoup
import requests
import time

print("Put any skills that you are not familiar with")
unfamiliar_skill = input('>').split()
print(f"Filtering out {','.join(unfamiliar_skill)}")

def find_jobs():
    html_text = requests.get('https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_ = 'srp-listing clearfix')

    for index, job in enumerate(jobs):
        date = job.find('h4').find('span', class_ = "posting-time").text
        

        #date filter:
        parts = date.split()
        days = int(parts[0])


        if days < 9:
            skills = job.find('div', class_ = "srp-keyskills").text.split()
            for uskill in unfamiliar_skill:
                if uskill not in skills:
                    
                    company_name = job.find('h4').find('span', class_ = "srp-comp-name").text.replace(' ','')
                    more_info = job.div.a['href']   
            
                    with open(f'posts/{index}.txt', 'w') as f:
                        f.write(f"Company Name: {company_name} \n")
                        f.write(f"Required Skills: {skills} \n")
                        f.write(f"More info: {more_info} \n")
                    print(f"File {index} saved")
                 



if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} seconds...')
        time.sleep(time_wait)
from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
   base_url = "https://weworkremotely.com/remote-jobs/search?term="

   response = get (f"{base_url}{keyword}")

   if response.status_code != 200:
      raise Exception("Failed to load page")
   else:
      results = []
      soup = BeautifulSoup(response.text, "html.parser") 
      jobs = soup.find_all('section', class_="jobs")  # section with class jobs
      
      for job_section in jobs:
         jobs_posts = job_section.find_all('li') # 섹션 안에있는 모든 li를 찾기
         jobs_posts.pop(-1)
         for post in jobs_posts:
               anchors = post.find_all('a')
               anchor = anchors[1]
               link = anchor['href']
               company, kind, region = anchor.find_all('span', class_="company")
               title = anchor.find('span', class_='title')
               job_data = {
                  '링크' : f"https://weworkremotely.com{link}",
                  '회사이름': company.string.replace(",", " " ), #html 코드 없이 글자만 받아옴
                  '근무지': region.string.replace(",", " " ),
                  '직책': title.string.replace(",", " " ),
               }
               results.append(job_data)
      return results
      
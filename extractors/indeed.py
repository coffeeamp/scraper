# https://weworkremotely.com/ 웹 스크래핑
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path= ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)



def get_page_count(keyword): # 페이지 수 가져오기
   base_url = "https://kr.indeed.com/jobs?q="
   response = driver.get(f"{base_url}{keyword}")

   soup = BeautifulSoup(driver.page_source, "html.parser")
   pagination = soup.find("nav", class_="css-jbuxu0 ecydgvn0") # ecydgvn0 라는 클래스의 nav를 찾음
   if pagination == None:
      return 1
      
   pages = pagination.find_all("div", recursive=False) # pagination의 모든 div를 찾고, recursive = False : 자식만 찾음 깊게 안가고 바로 밑의 것만
   count = len(pages)
   if count >= 5:
      return 5
   else:
      return count

def extract_indeed_jobs(keyword): # indeed.com 웹 스크래핑 키워드 받아서 스크래핑
   pages = get_page_count(keyword)
   print("Found", pages, "pages")
   results = []
   
   for page in range(pages):
      base_url = "https://kr.indeed.com/jobs"
      final_url = f"{base_url}?q={keyword}&start={page*10}"
      print("Requesting: ", final_url)
      response = driver.get(f"{base_url}?q={keyword}&start={page*10}")

      soup = BeautifulSoup(driver.page_source, "html.parser")
      job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
      jobs = job_list.find_all('li', recursive=False) # recursive = False : 자식만 찾음 깊게 안가고 바로 밑의 것만

      for job in jobs:
         zone = job.find("div", class_="mosaic-zone")
         if zone == None: # job.find로 찾은 내용이 없을 경우
            anchor = job.select_one("h2 a") # h2태그의 하나의 anchor를 찾음
            title = anchor['aria-label']
            link = anchor['href']
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            job_data = {
               '링크': f" https://kr.indeed.com{link}",
               '회사이름': company.string.replace("," ," " ),
               '근무지': location.string.replace(",", " " ),
               '직책': title.replace(",", " " )
            }
            results.append(job_data)
      # for result in results:
      #    print(result, "\n/////////\n")

   return results

   while(True):
      pass





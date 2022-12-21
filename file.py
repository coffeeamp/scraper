def save_to_file(file_name, jobs):
      file = open(f"{file_name}.csv", "w", encoding="utf-8")

      file.write("URL,회사,지역,직책\n")

      for job in jobs: # jobs list의 job을 하나씩 가져와 입력
         file.write(f"{job['직책']},{job['회사이름']},{job['근무지']},{job['링크']}\n") # \n 필수
         
         
      file.close()
from flask import Flask, render_template, request
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

app = Flask("JobScrapper")

@app.route("/") # start page
def home():
    return render_template("home.html", name="suhyun") # home.html을 렌더링하고, name이라는 변수에 suhyun를 넣어줌

@app.route("/search") # 검색창
def search():
    keyword = request.args.get("keyword") # request.args.get("keyword")를 통해 검색창에 입력한 keyword를 가져옴
    indeed = extract_indeed_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = indeed + wwr # 두개의 리스트를 합침
    return render_template("search.html", keyword = keyword, jobs = jobs) # search.html을 렌더링하고, keyword와 jobs를 넣어줌



app.run("127.0.0.1") # 서버를 실행시
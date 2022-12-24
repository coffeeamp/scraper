from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {} # cache

@app.route("/") # start page
def home():
    return render_template("home.html", name="suhyun") # home.html을 렌더링하고, name이라는 변수에 suhyun를 넣어줌

@app.route("/search") # 검색창
def search():
    keyword = request.args.get("keyword") # request.args.get("keyword")를 통해 검색창에 입력한 keyword를 가져옴
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr # 두개의 리스트를 합침
        db[keyword] = jobs
    return render_template("search.html", keyword = keyword, jobs = jobs) # search.html을 렌더링하고, keyword와 jobs를 넣어줌

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword]) # save_to_file을 통해 파일을 저장
    return send_file(f"{keyword}.csv", as_attachment=True) # send_file을 통해 파일을 다운로드
 
app.run("127.0.0.1") 
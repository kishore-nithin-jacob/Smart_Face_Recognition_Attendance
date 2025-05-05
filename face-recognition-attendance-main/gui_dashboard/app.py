from flask import Flask, render_template, request
from pymongo import MongoClient
from collections import defaultdict

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/") # Your mongodb connection string here
db = client["attendance"]
papers_col = db["papers"]
periods_col = db["periods"]
semester_col = db["semester"]
students_col = db["students"]

@app.route("/")
def index():
    students = students_col.distinct("student_id")
    return render_template("index.html", students=students)

@app.route("/student/<int:student_id>")
def student_detail(student_id):
    # Fetch attendance records for this student
    records = list(students_col.find({"student_id": student_id}))
    papers = {p["subjectcode"]: p for p in papers_col.find()}
    periods = list(periods_col.find())
    semester = semester_col.find_one()

    # Compute percentage per course
    attendance = defaultdict(lambda: {"present": 0, "total": 0})
    for rec in records:
        key = rec["course_id"]
        attendance[key]["total"] += 1
        if rec["status"] == "Present":
            attendance[key]["present"] += 1

    percentages = {
        course_id: round((v["present"] / v["total"]) * 100, 2) if v["total"] else 0
        for course_id, v in attendance.items()
    }

    return render_template("student_detail.html",
                           student_id=student_id,
                           records=records,
                           percentages=percentages,
                           semester=semester,
                           periods=periods,
                           papers=papers)

if __name__ == "__main__":
    app.run(debug=True)

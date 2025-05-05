from flask import Flask, render_template, request
from new_sty import new_stu
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form.get('name')
        rollno = request.form.get('rollno')
        
        try:
            rollno = int(rollno)    
            result = f"Name: {name}, Roll No: {rollno}"
        except ValueError:
            result = "Roll No must be an integer."
        finally:
            new_stu(rollno,name)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

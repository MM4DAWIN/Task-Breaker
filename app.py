from flask import Flask
import google.generativeai as palm 
import cgi 
from flask import render_template
from flask import request 
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/submitted', methods=['POST'])
def submitted():
    task = request.form.get('task')
    time = request.form.get('time')
    key = "AIzaSyAnF2Z_rCk2WxtUhkEOhKsi0XFAtBcanuk"
    palm.configure(api_key=key)
    model_id = 'models/text-bison-001'
    prompt = "I need to do " + task + " in " + time + ". Please break this down and give me a numbered list of smaller tasks to accomplish (with line breaks) and with consideration to the timeline I specified. Also put an extra newline between each main task on the list and don't put bullet points in your response. Give it to me in the format Task: Time:. Include the subtasks in this list and include the time in the task title. Also format the tasks as the following: ## Task 1: Research the [task] (1 day)" 
    completion = palm.generate_text(
        model = model_id,
        prompt = prompt,
        temperature = 0
    )
    if len(completion.candidates) == 0:
        print("API Error")
        return render_template('submitted.html', output = "No response generated :(")
    else:
        output = completion.candidates[0]["output"].replace("\n", "<br>") 
        output = output.replace("*", "<li>")
        output = output.replace(".", "</li>")
        output = output.replace("##", "<br><input type=\"checkbox\"><strong><span id=\"check\">")
        output = output.replace(":", ":</span>")
        output = output.replace(")", ")</strong>")
        return render_template('submitted.html', output = output)
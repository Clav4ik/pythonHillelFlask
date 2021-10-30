
from flask import Flask, g, redirect, url_for, render_template, request, flash
import datetime
import uuid


import time
app = Flask(__name__)

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route("/")
def hello_world():
    return f"<p>Hello, World!</p>"

@app.route("/<int:num_question>")
def answer(num_question):

    answer = []
    print("hello")


    for i in range(1, num_question+1):
        answer.append(
            {
                "UUID":uuid.uuid4(),
                "request_time":g.request_time(),
                "date_now":datetime.datetime.now()
            }
        )
    return render_template('answer.html', answer=answer)


if __name__== "__main__":
    app.run(debug=True)
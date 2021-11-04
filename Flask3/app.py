
from flask import Flask, g, redirect, url_for, render_template, request, flash, session, make_response
import datetime
import uuid


import time
app = Flask(__name__)

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


# @app.route("/<int:num_question>")
# def answer(num_question):
#
#     answer = []
#
#     for i in range(1, num_question+1):
#         answer.append(
#             {
#                 "UUID":uuid.uuid4(),
#                 "request_time":g.request_time(),
#                 "date_now":datetime.datetime.now()
#             }
#         )
#     return render_template('answer.html', answer=answer)
@app.route("/")
def get_count_of_user_visits_by_cookie():

    visited = 0

    if request.cookies.get('visited'):

        try:
            visited = int(request.cookies['visited'])
        except ValueError:
            return make_response(render_template('index.html', visited='Incorrect'))

    # Далее просто передадим этот счетчик в темлейт чтобы распечатать его
    response = make_response(render_template('index.html', visited=visited))

    # Но и в конце инкрементим счетчик на один
    response.set_cookie('visited', str(visited + 1))
    return response
@app.route("/login", methods=['GET', 'POST'])
def login_in_session():
    if request.method == 'POST':
        username = request.form['username']
        response = make_response(render_template('login.html', username=username))
        response.set_cookie('username', username)
        return response


    username = request.cookies.get('username')

    if username:
        #check so that it is impossible to get back to the form with the help of back
        return render_template('login.html', username=username)
    return render_template('login.html')





@app.route("/logout")
def logout_in_session():
    user = request.cookies.get('username')
    if user:
        resp = make_response(redirect(url_for("get_count_of_user_visits_by_cookie")))
        resp.set_cookie('visited', '', expires=0)
        resp.set_cookie('username', '', expires=0)
        return resp
    return f"Для обновления нужно ввести юзернайм<br><a href ='/'> переход на главную </a><br><a href ='/login'> переход на логин </a>"

if __name__== "__main__":
    app.run(debug=True)
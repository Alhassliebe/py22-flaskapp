from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    user_name = db.Column('user_name', db.Text)
    user_age = db.Column('user_age', db.Integer)
    user_sex = db.Column('user_sex', db.Integer)
    user_region = db.Column('user_region', db.Text)


class Questions(db.Model):
    __tablename__ = "questions"

    question_id = db.Column('question_id', db.Integer, primary_key=True)
    question_text = db.Column('question_text', db.Text, unique=True)


class Answers(db.Model):
    __tablename__ = "answers"

    answer_id = db.Column('answer_id', db.Integer, primary_key=True)
    q1 = db.Column('anwer_1', db.Integer)
    q2 = db.Column('anwer_2', db.Integer)
    q3 = db.Column('anwer_3', db.Integer)
    q4 = db.Column('anwer_4', db.Integer)
    q5 = db.Column('anwer_5', db.Integer)
    q6 = db.Column('anwer_6', db.Integer)
    q7 = db.Column('anwer_7', db.Integer)
    q8 = db.Column('anwer_8', db.Integer)
    q9 = db.Column('anwer_9', db.Integer)
    q10 = db.Column('anwer_10', db.Integer)
    q11 = db.Column('anwer_11', db.Integer)
    q12 = db.Column('anwer_12', db.Integer)
    q13 = db.Column('anwer_13', db.Integer)
    q14 = db.Column('anwer_14', db.Integer)


db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        with open('Questions.txt', 'r', encoding='utf-8') as questions_file:
            for line in questions_file:
                line = line[:-1]
                question = Questions(question_text=line)
                db.session.add(question)
                db.session.commit()
    except:
        pass


@app.route('/')
def index():
    return render_template('main_page.html')


#верхнее меню
@app.route('/main_page')
def index_after_change():
    return render_template('main_page.html')


@app.route('/opros')
def question_page():
    questions = Questions.query.all()

    return render_template(
        'opros.html',
        questions=questions
    )


@app.route('/process', methods=['get'])
def answer_anketa():
    if not request.args:
        return redirect(url_for('question_page'))

    user_name = request.args.get('Name')
    user_age = request.args.get('Age')
    user_sex = request.args.get('Sex')
    user_region = request.args.get('Region')

    # создаем профиль пользователя
    user = User(
        user_name=user_name,
        user_age=user_age,
        user_sex=user_sex,
        user_region=user_region
    )
    # добавляем в базу и сохраняем
    db.session.add(user)
    db.session.commit()
    # получаем юзера с айди
    db.session.refresh(user)

    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')
    q9 = request.args.get('q9')
    q10 = request.args.get('q10')
    q11 = request.args.get('q11')
    q12 = request.args.get('q12')
    q13 = request.args.get('q13')
    q14 = request.args.get('q14')

    # привязываем ответы к пользователю
    answer = Answers(answer_id=user.user_id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10,
                     q11=q11, q12=q12, q13=q13, q14=q14)
    # добавляем в базу и сохраняем
    db.session.add(answer)
    db.session.commit()

    return render_template('smth.html')


@app.route('/statistics')
def statistics():
    all_stat = {}
    age_stats = db.session.query(
        func.avg(User.user_age),
        func.min(User.user_age),
        func.max(User.user_age)
    ).one()
    all_stat['age_mean'] = age_stats[0]
    all_stat['age_min'] = age_stats[1]
    all_stat['age_max'] = age_stats[2]
    all_stat['total_count'] = User.query.count()

    men = db.session.query(User).filter(User.user_sex == 1)
    count_men = 0
    for m in men:
        count_men += 1
    all_stat['men'] = count_men

    women = db.session.query(User).filter(User.user_sex == 2)
    count_women = 0
    for w in women:
        count_women += 1
    all_stat['women'] = count_women


    questions = Questions.query.all()

    whole_ans = []
    whole_ans.append('')

    options = {
        1: 'Нет',
        2: 'Да'
    }

    ans_q = {}
    ans = db.session.query(Answers.q2).group_by(Answers.q2).all()
    counter = db.session.query(db.func.count(Answers.q2)).group_by(Answers.q2).all()
    n = 0
    for i in ans:
        i = int(str(i)[1])
        option_select = options[i]
        stat = str(counter[n]).replace(',)', '')
        stat = stat.replace('(', '')
        ans_q[option_select] = stat
        n += 1
    whole_ans.append(ans_q)


    return render_template('statistics.html', all_stat=all_stat, whole_ans=whole_ans, questions=questions)


if __name__ == '__main__':
    app.run()
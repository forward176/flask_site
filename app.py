import DB
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json


COUNT_GAME_LVLS = 20
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'login' in session:
        return redirect(url_for('levels'), 301)  
    context = {}
    context['output'] = ''
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password') 
        context['login'] = login
        context['password'] = password
        if not DB.is_user_exist(login):
            context['output'] = 'Такого пользователся не существует!'
        elif not DB.check_password(login, password):
            context['output'] = 'Неверный пароль!'
        else: 
            # context['output'] = 'Успешный вход!'
            session['login'] = login
            return redirect(url_for('levels'), 301)  
    return render_template('index.html', context=context)
    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'login' in session:
        return redirect(url_for('levels'), 301)  
    context = {}
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password')
        if not login:
            context['output'] = 'Введите логин!'
        elif not password:
            context['output'] = 'Введите Пароль!'
        elif DB.is_user_exist(login):
            context['output'] = 'Такой пользователь уже существует!'
        else:
            DB.create_user(login, password)
            # context['output'] = 'Вы успешно зарегистрированы!'
            session['login'] = login
            return redirect(url_for('levels'), 301)  
    return render_template('registration.html', context=context)


@app.route('/levels', methods=['GET', 'POST'])
def levels():
    if 'login' not in session: 
        return index()  #  TODO СДЕЛАТЬ НОРМАЛЬНЫЙ РЕДИРЕКТ НА ГЛАВНУЮ
    context = {}
    context['count_levels'] = COUNT_GAME_LVLS
    context['passed_levels'] = DB.get_count_level(session['login'])
    return render_template('levels.html', context=context)


@app.route('/level', methods=['GET', 'POST'])
def level():
    if 'login' not in session: 
        return index()  #  TODO СДЕЛАТЬ НОРМАЛЬНЫЙ РЕДИРЕКТ НА ГЛАВНУЮ

    if request.method == 'POST': 
        try:
            data = request.json
            if 'update_count_level' in data:
                DB.update_count_level(session['login'])                            
                return jsonify({'message': 'Success!'}), 200
            else:
                raise KeyError('Value key not found')
        except (KeyError, json.JSONDecodeError) as e:
            return jsonify({'error': 'Invalid data format'}), 400  

    if 'lvl' not in request.args:
        return redirect(url_for('levels'), 301)
    
    context = {}
    requested_lvl = int(request.args.get('lvl'))
    max_available_lvl = DB.get_count_level(session['login']) + 1
    if requested_lvl > max_available_lvl or requested_lvl > COUNT_GAME_LVLS or requested_lvl % 2 == 0:
        return redirect(url_for('levels'), 301)
    context['lvl'] = requested_lvl
    path = f'levels/{(context["lvl"] + 1) // 2}.lvl'
    mat = open(path, encoding="UTF-8").read().split()
    context["mat"] = mat
    context["is_max_available_lvl"] = requested_lvl == max_available_lvl
    return render_template('level.html', context=context)    


@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'login' not in session: 
        return index()  #  TODO СДЕЛАТЬ НОРМАЛЬНЫЙ РЕДИРЕКТ НА ГЛАВНУЮ
    
    if request.method == 'POST':  
        try:
            data = request.json
            if 'update_count_level' in data:
                DB.update_count_level(session['login'])                            
                return jsonify({'message': 'Success!'}), 200
            else:
                raise KeyError('Value key not found')
        except (KeyError, json.JSONDecodeError) as e:
            return jsonify({'error': 'Invalid data format'}), 400  

    if 'lvl' not in request.args:
        return redirect(url_for('levels'), 301)
    
    context = {}
    requested_lvl = int(request.args.get('lvl'))    
    max_available_lvl = DB.get_count_level(session['login']) + 1
    if requested_lvl > max_available_lvl or requested_lvl > COUNT_GAME_LVLS or requested_lvl % 2 == 1:
        print('!!!')
        return redirect(url_for('levels'), 301)   
    question_number = requested_lvl // 2 - 1 
    with open('questions.txt','r',encoding='UTF-8') as file:
        lines = file.readlines()
    context['question'] = lines[question_number * 2].strip()
    context['answer'] = lines[question_number * 2 + 1].strip()
    context['lvl'] = requested_lvl
    context["is_max_available_lvl"] = requested_lvl == max_available_lvl   
    return render_template('question.html', context=context)


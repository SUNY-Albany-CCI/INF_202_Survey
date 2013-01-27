# -*- coding: utf-8 -*-
### required - do no delete

def user():
    return dict(form=auth())

def download():
    return response.download(request,db)

def call():
    return service()
    
### end requires

def index():
    questions = db().select(db.questions.ALL)
    return dict(questions=questions)

def error():
    return dict()
   
def show():
    question = db.questions(request.args(0,cast=int)) or redirect(URL('index'))
    db.answers.question_id.default = question.id
    db.answers.user_id.default = auth.user_id
    form = SQLFORM(db.answers)
    next_question_id = question.id+1
    if form.process().accepted:
        response.flash = 'Your answer has been stored'
        redirect(URL('show',args=next_question_id))
    answer = db(db.answers.question_id==question.id).select()
    answer.user_id = auth.user_id
    answer.answer = answer
    return dict(question=question, answer=answer, form=form)

def managequestions():
    grid = SQLFORM.smartgrid(db.questions, linked_tables=['answers'])
    return dict(grid=grid)

def manage():
    grid = SQLFORM.smartgrid(db.answers, linked_tables=['questions'])
    return dict(grid=grid)

@auth.requires_login()
def clearanswers():
    db(db.answers.id>0).delete()
    return dict()

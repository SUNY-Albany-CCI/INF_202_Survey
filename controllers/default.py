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
    return dict()

@auth.requires_login()
def startsurvey():
    questions = db().select(db.questions.ALL)
    return dict(questions=questions)

def error():
    return dict()
   
@auth.requires_login()   
def show():
    currentuser = db(db.auth_user.id==auth.user_id).select()[0]
    question = db.questions(request.args(0,cast=int)) or redirect(URL('index'))
    db.answers.question_id.default = question.id
    db.answers.user_id.default = auth.user_id
    db.answers.tbl_group_id.default = currentuser.tbl_group_id
    form = SQLFORM(db.answers)
    next_question_id = question.id+1
    if form.process().accepted:
        response.flash = 'Your answer has been stored'
        redirect(URL('show',args=next_question_id))
    answer = db(db.answers.question_id==question.id).select()
    return dict(question=question, answer=answer, form=form)

def correlate2questions():
    form = SQLFORM(db.correlations,fields=['question_id1','question_id2','tbl_group_id'])
    if form.process().accepted:
        redirect(URL('showmutualinformation'))
        response.flash = 'Your correlation has been stored'
    answers1 = db(db.answers.question_id==db.correlations.question_id1).select()
    answers2 = db(db.answers.question_id==db.correlations.question_id2).select()
    return dict(answers1=answers1,answers2=answers2,form=form)

def showmutualinformation():
    form = SQLFORM(db.answers)
    return dict(form=form)

@auth.requires_login()
def managequestions():
    grid = SQLFORM.smartgrid(db.questions, linked_tables=['answers'])
    return dict(grid=grid)

@auth.requires_login()
def manage():
    grid = SQLFORM.smartgrid(db.answers, linked_tables=['questions'])
    return dict(grid=grid)

@auth.requires_login()
def clearanswers():
    db(db.answers.id>0).delete()
    return dict()

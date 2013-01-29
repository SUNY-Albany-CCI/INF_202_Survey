# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

db.define_table('tbl_groups',
    Field('name', unique=True))

auth.settings.extra_fields['auth_user']= [
    Field('tbl_group_id', 'reference tbl_groups', requires = IS_IN_DB(db, db.tbl_groups.id))]

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.localhost:25'
mail.settings.sender = 'luis.ibanez@kitware.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

db.define_table('questions',
    Field('question', unique=True))

db.questions.question.requires = IS_NOT_IN_DB(db, db.questions.question)


db.define_table('answers',
    Field('user_id','reference auth_user'),
    Field('tbl_group_id','reference tbl_groups'),
    Field('question_id','reference questions'),
    Field('answer'))

db.answers.question_id.requires = IS_IN_DB(db, db.questions.id)
db.answers.user_id.requires = IS_IN_DB(db, db.auth_user.id)

db.answers.answer.requires = IS_IN_SET(['Yes', 'No', 'Maybe'])

db.answers.question_id.writable = False
db.answers.question_id.readable = True

db.answers.user_id.writable = False
db.answers.user_id.readable = True

db.answers.tbl_group_id.writable = False
db.answers.tbl_group_id.readable = True


db.define_table('correlations',
    Field('question_id1','reference questions'),
    Field('question_id2','reference questions'),
    Field('tbl_group_id','reference tbl_groups'),
    Field('mutual_information','double'))


db.correlations.question_id1.requires = IS_IN_DB(db, db.questions.question)
db.correlations.question_id2.requires = IS_IN_DB(db, db.questions.question)
db.correlations.tbl_group_id.requires = IS_IN_DB(db, db.tbl_groups.id)


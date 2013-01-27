from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'INF 202 Survey'
settings.subtitle = 'powered by web2py'
settings.author = 'Luis Ibanez'
settings.author_email = 'luis.ibanez@kitware.com'
settings.keywords = ''
settings.description = 'Survey to use in INF 202 class'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '5e2e4513-11c9-44b6-88b2-b2a8a7a87d4d'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = ['jqmobile', 'translate', 'dropdown']

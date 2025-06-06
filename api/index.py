from devadmin.wsgi import application
from vercel_wsgi import handle_request

def handler(event, context):
    return handle_request(application, event, context)

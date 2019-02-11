from flask import Flask, url_for ,render_template
app = Flask(__name__)
#app.debug = True

class PrefixMiddleware(object):
#class for URL sorting 
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        #in this line I'm doing a replace of the word flaskredirect which is my app name in IIS to ensure proper URL redirect
        if environ['PATH_INFO'].lower().replace('/flaskredirect','').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/flaskredirect','')[len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])            
            return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/foo')

@app.route('/bar')
def bar():    
    return "The URL for this page is {}".format(url_for('bar'))

	
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9010)

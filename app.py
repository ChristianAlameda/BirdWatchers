from flask import Flask, render_template, request

class MyFlaskApp:
    def __init__(self):
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        
        #HOMEPAGE
        self.app.add_url_rule('/', 'index', self.index)
        

    def index(self):
        return render_template('homepage.html')


def startFlask(requestQ, dataQ):
    newFlask = MyFlaskApp(requestQ, dataQ)
    newFlask.run()

# Usage
if __name__ == '__main__':
    request_queue = Queue()
    data_queue = Queue()
    my_flask_app = MyFlaskApp(request_queue, data_queue)
    my_flask_app.run()
# The application running file that imports the package "website" and runs it on the local machine/server
from website import create_app
import webbrowser
from threading import Timer

app = create_app()

def open_web_browser():
    '''
    Function to open a webbrowser window object using localhost and Port where the Flask application is running
    '''
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    Timer(1, open_web_browser()).start()
    app.run()


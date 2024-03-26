from flask import Flask


def create_app():
    '''
    The function initiates the flask application server.
    The flask application servers utilizes the .config method to enable 3 critical elements:
    1. The app.secret_key allows encryption of current session data stored in cookies and utilizing session variables to display visualizations
    2. Allow pdf files to be stored within the project directory using app.configy['PDF_FOLDER']
    3. ['TEMPLATE_FOLDER'] allows flask's render_template to identify the html content to display when loading

    Additionally,
    Importing html blueprints from views directory to configure the web page HTTP requests for application to run

    RETURNS
    _________
    The flask application object to run
    '''
    app = Flask(__name__)
    app.secret_key = 'M602_Computer_Programming'
    app.config['TEMPLATE_FOLDER'] = "templates/"

    from .views import carbon_footprint
    app.register_blueprint(carbon_footprint, url_prefix="/")
    
    return app

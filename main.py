# The application running file that imports the package "website" and runs it on the local machine/server
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

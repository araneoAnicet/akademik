from flaskapp import app
from flaskapp.models import db, User, Day, Profilechange

if __name__ == '__main__':
    app.run(debug=True)
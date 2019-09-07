import sys, getopt
from flaskapp import db
from flaskapp.models import (DatabaseManager, User, Day, Profilechange,
    UserRejectedRegistrationError, UserDoesNotExistError)


def main(argv):
    pass

if __name__ == '__main__':
    main(sys.argv[1:])
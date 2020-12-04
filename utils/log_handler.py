import logging

flask_log_handler = logging.FileHandler('flask.log')
flask_log_handler.setLevel('DEBUG')


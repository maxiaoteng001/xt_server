from gevent.pywsgi import WSGIServer
from src import create_app

http_server = WSGIServer(('', 5000), create_app())
http_server.serve_forever()
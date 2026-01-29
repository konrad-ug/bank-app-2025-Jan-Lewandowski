import threading
import time
from wsgiref.simple_server import make_server

from app.api import app, registry


def before_all(context):
    context.server = make_server("127.0.0.1", 5005, app)
    context.thread = threading.Thread(target=context.server.serve_forever, daemon=True)
    context.thread.start()
    time.sleep(0.1)


def after_all(context):
    context.server.shutdown()
    context.thread.join()


def before_scenario(context, scenario):
    registry.accounts.clear()
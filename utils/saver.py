from contextlib import contextmanager
from langgraph.checkpoint.postgres import PostgresSaver
from config import DB_URI

@contextmanager
def get_saver():
    saver_ctx = PostgresSaver.from_conn_string(DB_URI)
    saver = saver_ctx.__enter__()
    try:
        yield saver
    finally:
        saver_ctx.__exit__(None, None, None)

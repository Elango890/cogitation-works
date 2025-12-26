import os
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

Timer(2, open_browser).start()

os.system("python3 manage.py runserver")

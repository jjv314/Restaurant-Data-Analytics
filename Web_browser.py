def load_browser():
    import time
    time.sleep(2)
    url = "http://127.0.0.1:2002"
    import webbrowser
    webbrowser.open(url, new=1)
    print('Now loading the browser')

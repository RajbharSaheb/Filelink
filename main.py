from FileStream.bot import run_bot
from FileStream.webserver.routes import run_webserver
import threading

if __name__ == "__main__":
    threading.Thread(target=run_webserver).start()
    run_bot()

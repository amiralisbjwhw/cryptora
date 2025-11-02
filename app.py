from flask import Flask, request
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    ip = request.remote_addr
    print(f"ورود از آی‌پی: {ip}")
    return "سلام امیر جان! پروژه‌ت روی Cloudflare بالا اومد 🎉"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])

@app.route('/')
def home():
    # چاپ آی‌پی کاربر در ترموکس
    print(f"ورود از آی‌پی: {request.remote_addr}")
    return '''
    <html>
        <head><title>خوش آمدی امیر جان</title></head>
        <body>
            <h1>سلام امیر جان! 🎉</h1>
            <p>پروژه‌ت روی Cloudflare بالا اومد و آی‌پی‌ت ثبت شد.</p>
            <a href="/about">صفحه درباره</a>
        </body>
    </html>
    '''

@app.route('/about')
def about():
    return '''
    <html>
        <head><title>درباره پروژه</title></head>
        <body>
            <h2>این یه صفحه درباره‌ست</h2>
            <p>این پروژه با Flask ساخته شده و از طریق Cloudflared قابل دسترسه.</p>
            <a href="/">برگشت به صفحه اصلی</a>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

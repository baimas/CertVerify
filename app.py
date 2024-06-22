from flask import Flask, render_template
import ssl
import socket
import datetime

app = Flask(__name__)

def get_certificate_info(url):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=url) as conn:
            conn.connect((url, 443))
            cert = conn.getpeercert()
            cn = dict(x[0] for x in cert['subject'])['commonName']
            not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_remaining = (not_after - datetime.datetime.utcnow()).days
            return {'url': url, 'cn': cn, 'validity': not_after, 'days_remaining': days_remaining}
    except Exception as e:
        return {'url': url, 'error': str(e)}

@app.route('/')
def index():
    urls = [
        "www.google.com",
        "www.github.com"
    ]
    results = [get_certificate_info(url) for url in urls]
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

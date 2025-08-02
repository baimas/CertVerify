from flask import Flask, render_template, request, redirect, url_for
import ssl
import socket
import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')


def get_certificate_info(url):
    try:
        context = ssl.create_default_context()

        # Cria um socket e faz o handshake TLS com SNI
        with socket.create_connection((url, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                cert = ssock.getpeercert()

        # Extrai o CN (Common Name)
        subject = dict(x[0] for x in cert['subject'])
        cn = subject.get('commonName')

        # Extrai validade
        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_remaining = (not_after - datetime.datetime.utcnow()).days
        near_expiry = days_remaining < 30

        return {
            'url': url,
            'cn': cn,
            'validity': not_after,
            'days_remaining': days_remaining,
            'near_expiry': near_expiry
        }

    except Exception as e:
        print(f"Erro ao obter certificado para {url}: {e}")
        return {'url': url, 'error': str(e)} 

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Lógica de autenticação
        if username == 'admin' and password == 'password':
            # Autenticação bem-sucedida, redireciona para a página principal (index)
            return redirect(url_for('index'))
        else:
            # Autenticação falhou, redireciona de volta para a página de login
            return render_template('login.html', error="Usuário ou senha inválidos.")
    else:
        # Se o método for GET, apenas renderiza a página de login
        return render_template('login.html')

# Rota para a página principal após o login
@app.route('/index')
def index():
    urls = [
        "www.google.com",
        "www.github.com",
        "www.facebook.com",
        "www.instagram.com",
        # 26 URLs adicionais
        "www.twitter.com", "www.microsoft.com", "www.apple.com", "www.amazon.com", 
        "www.netflix.com", "www.spotify.com", "www.tesla.com", "www.linkedin.com", 
        "www.pinterest.com", "www.wordpress.com", "www.adobe.com", "www.oracle.com", 
        "www.ibm.com", "www.intel.com", "www.uber.com", "www.slack.com",
        "www.zoom.us", "www.paypal.com", "www.dropbox.com", "www.samsung.com", 
        "www.bing.com"
    ]
    results = [get_certificate_info(url) for url in urls]
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)


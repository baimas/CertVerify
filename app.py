from flask import Flask, render_template
import OpenSSL
import socket
import datetime

app = Flask(__name__)

def get_certificate_info(url):
    try:
        # Conectar ao servidor e obter o certificado
        conn = socket.create_connection((url, 443))
        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        sock = OpenSSL.SSL.Connection(context, conn)
        sock.set_connect_state()
        sock.do_handshake()
        cert = sock.get_peer_certificate()
        
        # Extração do CN (Common Name)
        cn = None
        for component in cert.get_subject().get_components():
            if component[0] == b'CN':
                cn = component[1].decode('utf-8')
                break
        
        # Extração da data de validade e cálculo dos dias restantes
        not_after = datetime.datetime.strptime(cert.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        days_remaining = (not_after - datetime.datetime.utcnow()).days

        return {'url': url, 'cn': cn, 'validity': not_after, 'days_remaining': days_remaining}
    except Exception as e:
        # Depuração: Exibir erros
        print(f"Erro ao obter certificado para {url}: {e}")
        return {'url': url, 'error': str(e)}

@app.route('/')
def index():
    urls = [
        "www.google.com",
        "www.github.com",
        "www.facebook.com",
        "www.instagram.com"
    ]
    results = [get_certificate_info(url) for url in urls]
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

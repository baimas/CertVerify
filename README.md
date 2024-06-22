Claro, aqui está um exemplo de `README.md` que inclui todas as informações necessárias para implantar sua aplicação no OpenShift usando um Service Account para autenticação.

```markdown
# CertVerify

CertVerify é uma aplicação Flask que verifica certificados SSL de uma lista de URLs e exibe informações como CN, data de validade e dias restantes para expiração.

## Requisitos

- Python 3.9+
- OpenShift CLI (`oc`)
- Docker
- Kubernetes Python Client (`kubernetes`)

## Instalação

1. Clone o repositório:

```sh
git clone https://github.com/baimas/CertVerify.git
cd CertVerify
```

2. Instale as dependências:

```sh
pip install -r requirements.txt
```

## Configuração do OpenShift

### 1. Criar um Service Account

```sh
oc create serviceaccount certverify-sa
oc policy add-role-to-user view -z certverify-sa
```

### 2. Obter o token do Service Account

```sh
oc sa get-token certverify-sa
```

Anote o token gerado, pois será usado na configuração da aplicação.

### 3. Configurar o Deployment no OpenShift

Crie um arquivo chamado `openshift-deployment.yaml` e adicione o seguinte conteúdo:

```yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: certverify
  labels:
    app: certverify
spec:
  replicas: 1
  selector:
    app: certverify
  template:
    metadata:
      labels:
        app: certverify
    spec:
      serviceAccountName: certverify-sa
      containers:
        - name: certverify
          image: <your-registry>/certverify:latest
          ports:
            - containerPort: 5000
          env:
            - name: FLASK_ENV
              value: "production"
            - name: KUBERNETES_SERVICE_HOST
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: KUBERNETES_SERVICE_PORT
              value: "443"
  strategy:
    type: Rolling

---
apiVersion: v1
kind: Service
metadata:
  name: certverify
  labels:
    app: certverify
spec:
  ports:
    - port: 5000
      targetPort: 5000
  selector:
    app: certverify

---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: certverify
  labels:
    app: certverify
    router-agora: "true"
spec:
  to:
    kind: Service
    name: certverify
  port:
    targetPort: 5000
  tls:
    termination: edge
```

### 4. Implantar a Aplicação no OpenShift

```sh
oc apply -f openshift-deployment.yaml
```

## Código da Aplicação

O código principal da aplicação Flask pode ser encontrado no arquivo `app.py`:

```python
from flask import Flask, render_template
import OpenSSL
import socket
import datetime
from kubernetes import client, config
import os

app = Flask(__name__)

def get_certificate_info(url):
    try:
        conn = socket.create_connection((url, 443))
        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        sock = OpenSSL.SSL.Connection(context, conn)
        sock.set_connect_state()
        sock.do_handshake()
        cert = sock.get_peer_certificate()
        
        cn = None
        for component in cert.get_subject().get_components():
            if component[0] == b'CN':
                cn = component[1].decode('utf-8')
                break
        
        not_after = datetime.datetime.strptime(cert.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        days_remaining = (not_after - datetime.datetime.utcnow()).days

        return {'url': url, 'cn': cn, 'validity': not_after, 'days_remaining': days_remaining}
    except Exception as e:
        print(f"Erro ao obter certificado para {url}: {e}")
        return {'url': url, 'error': str(e)}

def get_routes_with_label(label_selector):
    config.load_incluster_config()  # Isso carrega a configuração a partir do Pod
    v1 = client.CustomObjectsApi()

    routes = v1.list_cluster_custom_object(
        group="route.openshift.io",
        version="v1",
        plural="routes",
        label_selector=label_selector
    )
    
    urls = []
    for route in routes.get('items', []):
        spec = route.get('spec', {})
        host = spec.get('host')
        if host:
            urls.append(host)
    
    return urls

@app.route('/')
def index():
    label_selector = "router-agora=true"
    urls = get_routes_with_label(label_selector)
    results = [get_certificate_info(url) for url in urls]
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
```

## Testando a Aplicação

Depois que a implantação estiver concluída, verifique se a aplicação está acessível e funcionando conforme o esperado.

```sh
flask run
```

Acesse a aplicação no navegador usando a rota configurada no OpenShift.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

```

Salve este conteúdo como `README.md` no repositório do seu projeto. Certifique-se de ajustar quaisquer detalhes específicos, como o nome do registro da imagem do Docker (`<your-registry>/certverify:latest`). 

Se precisar de mais alguma coisa, estou aqui para ajudar!
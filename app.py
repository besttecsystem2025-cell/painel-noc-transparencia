from flask import Flask, jsonify, render_template
import requests
import time

app = Flask(__name__)

links = {
    "Câmara Valparaíso": "https://valparaiso.go.leg.br/",
    "Câmara Cidade Ocidental": "https://cidadeocidental.go.leg.br/",
    "Câmara Luziânia": "https://luziania.go.leg.br/",
    "Câmara São João d'Aliança": "https://saojoaodalianca.go.leg.br/",
    "Câmara Alto Paraíso": "https://altoparaiso.go.leg.br/",
    "Prefeitura Simolândia": "https://simolandia.go.gov.br/",
    "Prefeitura Terezópolis": "https://terezopolis.go.gov.br/",
    "Prefeitura Acreúna": "https://transparencia.acreuna.go.gov.br/"
}

def verificar(url):
    tentativas = 2
    for tentativa in range(tentativas):
        try:
            inicio = time.time()

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            r = requests.get(url, timeout=6, headers=headers)
            tempo = int((time.time() - inicio) * 1000)

            if r.status_code == 200:
                if tempo < 400:
                    return {"status": "DISPONÍVEL", "tempo": tempo}
                else:
                    return {"status": "LENTO", "tempo": tempo}
            else:
                return {"status": "INSTÁVEL", "tempo": tempo}

        except:
            if tentativa == tentativas - 1:
                return {"status": "FORA DO AR", "tempo": 0}


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/dados")
def dados():
    resultado = {}

    for nome, url in links.items():
        resultado[nome] = verificar(url)

    return jsonify(resultado)

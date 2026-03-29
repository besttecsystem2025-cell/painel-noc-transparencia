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
    try:
        inicio = time.time()
        r = requests.get(url, timeout=5)
        tempo = int((time.time() - inicio) * 1000)

        if r.status_code == 200:
            return {"status": "DISPONÍVEL", "tempo": tempo}
        else:
            return {"status": "INSTÁVEL", "tempo": tempo}
    except:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

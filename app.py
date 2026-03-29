from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

links = {
    "Câmara Alto Paraíso": "https://altoparaiso.go.leg.br/",
    "Câmara Cidade Ocidental": "https://cidadeocidental.go.leg.br/",
    "Câmara Luziânia": "https://luziania.go.leg.br/",
    "Câmara São João d'Aliança": "https://saojoaodalianca.go.leg.br/",
    "Câmara Valparaíso": "https://valparaiso.go.leg.br/",
    "Prefeitura Acreúna": "https://transparencia.acreuna.go.gov.br/",
    "Prefeitura Simolândia": "https://simolandia.go.gov.br/",
    "Prefeitura Terezópolis": "https://terezopolis.go.gov.br/"
}

def verificar(url):
    try:
        inicio = time.time()

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html"
        }

        r = requests.get(url, timeout=10, headers=headers, allow_redirects=True)

        tempo = int((time.time() - inicio) * 1000)

        if r.status_code == 200:
            if tempo < 500:
                return {"status": "DISPONÍVEL", "tempo": tempo}
            else:
                return {"status": "LENTO", "tempo": tempo}

        elif r.status_code in [301, 302]:
            return {"status": "REDIRECIONANDO", "tempo": tempo}

        else:
            return {"status": "INSTÁVEL", "tempo": tempo}

    except requests.exceptions.Timeout:
        return {"status": "LENTO", "tempo": 999}

    except:
        return {"status": "INSTÁVEL", "tempo": 0}


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/dados")
def dados():
    resultado = {}
    for nome, url in links.items():
        resultado[nome] = verificar(url)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)

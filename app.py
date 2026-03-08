from flask import Flask, render_template, jsonify
import requests
import time
import os
from datetime import datetime

app = Flask(__name__)

PORTAIS = {
    "Valparaíso": "https://transparencia.camaravalparaiso.go.gov.br/",
    "Cidade Ocidental": "https://transparencia.cidadeocidental.go.leg.br/",
    "Luziânia": "https://transparencia.luziania.go.leg.br/",
    "São João d'Aliança": "https://transparencia.saojoaodalianca.go.leg.br/",
    "Alto Paraíso": "https://transparencia.altoparaisodegoias.go.leg.br/",
    "Simolândia": "https://transparencia.simolandia.go.gov.br/",
    "Terezópolis": "https://transparencia.terezopolis.go.gov.br/"
}

def verificar_portal(nome, url):

    inicio = time.time()

    try:

        resposta = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        tempo = round((time.time() - inicio) * 1000)

        if resposta.status_code == 200:
            status = "DISPONÍVEL"

        elif resposta.status_code >= 500:
            status = "ERRO SERVIDOR"

        elif resposta.status_code >= 400:
            status = "ERRO PÁGINA"

        else:
            status = "INSTÁVEL"

    except requests.exceptions.Timeout:
        status = "TIMEOUT"
        tempo = 0

    except requests.exceptions.ConnectionError:
        status = "INDISPONÍVEL"
        tempo = 0

    except Exception:
        status = "ERRO"
        tempo = 0

    return {
        "nome": nome,
        "status": status,
        "tempo": tempo
    }

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/dados")
def dados():

    resultados = []
    disponiveis = 0

    for nome, url in PORTAIS.items():

        resultado = verificar_portal(nome, url)

        resultados.append(resultado)

        if resultado["status"] == "DISPONÍVEL":
            disponiveis += 1

    total = len(PORTAIS)

    percentual = round((disponiveis / total) * 100)

    return jsonify({
        "portais": resultados,
        "percentual": percentual,
        "total": total,
        "online": disponiveis,
        "offline": total - disponiveis,
        "atualizado": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)

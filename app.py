from flask import Flask, render_template, jsonify
import requests
import time
from datetime import datetime
import os

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
    try:
        inicio = time.time()

        resposta = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        tempo = round((time.time() - inicio) * 1000)
        html = resposta.text.lower()

        if resposta.status_code == 200:
            if "404" in html or "500" in html or "erro" in html:
                status = "INSTÁVEL"
            else:
                status = "DISPONÍVEL"
        else:
            status = "INSTÁVEL"

    except:
        status = "INDISPONÍVEL"
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
  

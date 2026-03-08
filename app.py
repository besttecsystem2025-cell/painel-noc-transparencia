
from flask import Flask, render_template, jsonify
import requests
import time
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
            headers={"User-Agent": "Mozilla/5.0"},
            verify=True
        )

        tempo = round((time.time() - inicio) * 1000)

        html = resposta.text.lower()

        status = "DISPONÍVEL"

        # ERROS HTTP
        if resposta.status_code >= 500:
            status = "ERRO SERVIDOR"

        elif resposta.status_code >= 400:
            status = "ERRO PÁGINA"

        # DETECTAR ERROS NO HTML
        palavras_erro = [
            "erro",
            "error",
            "exception",
            "sql",
            "internal server error",
            "pagina nao encontrada",
            "não encontrado"
        ]

        for palavra in palavras_erro:
            if palavra in html:
                status = "ERRO SISTEMA"
                break

        # PORTAL LENTO
        if tempo > 2000 and status == "DISPONÍVEL":
            status = "LENTO"

    except requests.exceptions.SSLError:
        status = "ERRO SSL"
        tempo = 0

    except requests.exceptions.Timeout:
        status = "TIMEOUT"
        tempo = 0

    except requests.exceptions.ConnectionError:
        status = "FORA DO AR"
        tempo = 0

    except Exception:
        status = "FALHA"
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
    app.run(host="0.0.0.0", port=5000)

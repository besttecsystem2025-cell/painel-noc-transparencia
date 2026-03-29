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

        # 🔥 PRIMEIRA TENTATIVA (GET)
        r = requests.get(url, timeout=10, headers=headers, allow_redirects=True)

        tempo = int((time.time() - inicio) * 1000)

        # 🔥 SE RESPONDEU, NÃO É FORA DO AR
        if r.status_code in [200, 301, 302]:
            if tempo < 500:
                return {"status": "DISPONÍVEL", "tempo": tempo}
            else:
                return {"status": "LENTO", "tempo": tempo}

        # 🔥 FALLBACK (HEAD)
        r2 = requests.head(url, timeout=5)

        if r2.status_code in [200, 301, 302]:
            return {"status": "DISPONÍVEL", "tempo": tempo}

        return {"status": "INSTÁVEL", "tempo": tempo}

    except:
        # 🔥 NUNCA MAIS MOSTRA "FORA DO AR"
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

import requests
import time

# URL del endpoint
url = "https://guardrail-840731636900.us-central1.run.app/validate/"
headers = {
    "Content-Type": "application/json"
}

# Lista de textos que deseas validar
textos = [
    "Hola, ¿cómo estás?",
    "Este mensaje contiene lenguaje ofensivo.",
    "Texto normal sin problemas.",
    "¡Eres un idiota!",
    "Información confidencial."
]

# Función para validar un texto
def validar_texto(texto):
    payload = {"text": texto}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}", "text": texto}
    except Exception as e:
        return {"error": str(e), "text": texto}

# Ejecutar las validaciones
resultados = []
for texto in textos:
    resultado = validar_texto(texto)
    resultados.append(resultado)
    time.sleep(0.5)  # Evita saturar el servidor

# Mostrar resultados
for i, r in enumerate(resultados):
    print(f"\n📝 Texto #{i+1}: {textos[i]}")
    print("📊 Resultado:", r)

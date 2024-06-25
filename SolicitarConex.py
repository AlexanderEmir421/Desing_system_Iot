import requests

# Configura la URL del endpoint del REST API de Kafka Connect
url = "http://192.168.100.5:8083/connectors"

# Carga el contenido del archivo JSON con la configuración del conector MQTT
with open("./tmp/custom/connect-mqtt-source.json", "r") as config_file:
    config_data = config_file.read()

# Define las cabeceras para la solicitud POST
headers = {
    "Content-Type": "application/json"
}

# Realiza la solicitud POST al REST API
try:
    response = requests.post(url, data=config_data, headers=headers)
    response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
    print("Conector creado exitosamente:", response.json())
except requests.exceptions.RequestException as e:
    print("Error al crear el conector:", e)

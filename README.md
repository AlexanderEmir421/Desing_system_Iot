Sistema para tu domotica,uso de Broker con protocolo MQTT para el envio y recepcion de datos para el dispositivo Iot
Sistema de colas como kafka para el encolamiento de topicos ,reduccion de carga y sin fallas de recepcion para posterior procesamiento
Mqtt Connector utilizado ya que Kafka y el Broker en este caso mosquitto no tienen los mismos protocolos de comunicacion a lo que dificulta en la llegada de datos
Apache Spark para el procesamiento en tiempo real por lotes este se encarga de  subcribirse a la cola de kafka e ir filtrando los datos en colados a su respectiva base de datos 
Mysql para el almacenamiento de los datos
Uso de docker para levantar los servicios en un contenedor y poder desplegarlo de una manera mas facil
Este sistema esta en desarrollo ya que no tengo mucho conocimiento en estas areas...

from flask import Flask
from flask_ask import Ask, statement, question
from random import randint
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

clientId = "PythonPublisher"
host = "HOST_IP"
port = 9001
topic = "door1"

generatedPass = None
password = None

@ask.launch
def launch():
    def generate_code():
        global generatedPass
        generatedPass = ''.join(["{}".format(randint(1, 9)) for num in range(0, 6)])
        print(generatedPass)
        return generatedPass
    global password
    password = generate_code()

    #publish.single(topic, payload=password, hostname=host, port=int(port), transport="websockets")
    #A linha acima manda o código para o app de celular, está comentada só para que se possa realizar o teste com esse script e o Alexa Developer COnsole
    #O código da porta é printado no console


    first_contact = 'Bem-vindo à Skill que controla sua porta. Você quer abrir ou fechar a porta?'
    return question(first_contact).reprompt('Você deseja abrir ou fechar a porta?')


@ask.intent('OpenDoorIntent')
def open_door(openOrClose, codeValue):
    print('Entrei')
    print(openOrClose)
    print(codeValue)
    print(password)

    GPIO.setup(18,GPIO.OUT)

    if openOrClose is None and codeValue is None:
        return question('Não entendi, você deseja abrir ou fechar a porta?')

    elif openOrClose == "abrir" or openOrClose == "fechar":

        if openOrClose == "abrir" and codeValue == password:
            GPIO.output(18, GPIO.HIGH)
        elif openOrClose == "fechar" and codeValue == password:
            GPIO.output(18, GPIO.LOW)
        else:
            return question('Código incorreto!')
        
        response_text = f"sua porta está a {openOrClose}"
        return statement(response_text).simple_card('Comando', response_text)


if __name__ == "__main__":
    app.run(debug=True)
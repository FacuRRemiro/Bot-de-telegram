import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# URL para obtener el precio del dólar
url_dolar = "https://dolarhoy.com/cotizaciondolarblue"

# URL de la API de Telegram
url_telegram = 'https://api.telegram.org/bot6392855948:AAFdtszzbDIOjvZPHOx9z2Rb5kz_oxxOomc/sendMessage'  # Reemplaza 'TOKEN' con tu token de Telegram

# Intervalo de tiempo en segundos para actualizar el precio del dólar
intervalo = 1800

class PrecioDolar:
    def __init__(self):
        self.precio_anterior = None

    def obtener_precio(self, url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        precio_padre = soup.find("div", {"class": "tile is-parent is-8"}).contents[1]
        precio_hijo = precio_padre.find("div", {"class": "value"}).contents[0]
        return float(precio_hijo.replace('$','').replace(',',''))


###################################################################################################################
#################################### FUNCIONES TELEGRAM ###########################################################
###################################################################################################################

    def precio_cerrado(self, precio):
        mensaje = f"El precio del dolar cerro el dia en ${precio:1.2f}"
        data = {
            'chat_id': '-1001977544508',  # Reemplaza con tu chat_id
            'text': mensaje
        }
        response = requests.post(url_telegram, data=data)
        if response.status_code == 200:
            print('Mensaje enviado exitosamente.')
        else:
            print('Error al enviar el mensaje a Telegram. Código de estado:', response.status_code)


    def precio_inicial(self, precio):
        mensaje = f"El precio del dolar blue arranca el dia en ${precio:1.2f}"
        data = {
            'chat_id': '-1001977544508',  # Reemplaza con tu chat_id
            'text': mensaje
        }
        response = requests.post(url_telegram, data=data)
        if response.status_code == 200:
            print('Mensaje enviado exitosamente.')
        else:
            print('Error al enviar el mensaje a Telegram. Código de estado:', response.status_code)

    def precio_subida(self, precio):
        mensaje = f"El precio del dólar blue subió a ${precio:1.2f}"
        data = {
            'chat_id': '-1001977544508',  # Reemplaza con tu chat_id
            'text': mensaje
        }
        response = requests.post(url_telegram, data=data)
        if response.status_code == 200:
            print('Mensaje enviado exitosamente.')
        else:
            print('Error al enviar el mensaje a Telegram. Código de estado:', response.status_code)


    def precio_igualado(self, precio):
        mensaje = f"El precio del dólar blue se mantiene en ${precio:1.2f}"
        data = {
            'chat_id': '-1001977544508',  # Reemplaza con tu chat_id
            'text': mensaje
        }
        response = requests.post(url_telegram, data=data)
        if response.status_code == 200:
            print('Mensaje enviado exitosamente.')
        else:
            print('Error al enviar el mensaje a Telegram. Código de estado:', response.status_code)

    def precio_baja(self, precio):
        mensaje = f"El precio del dólar blue bajó a ${precio:1.2f}"
        data = {
            'chat_id': '-1001977544508',  # Reemplaza con tu chat_id
            'text': mensaje
        }
        response = requests.post(url_telegram, data=data)
        if response.status_code == 200:
            print('Mensaje enviado exitosamente.')
        else:
            print('Error al enviar el mensaje a Telegram. Código de estado:', response.status_code)


###################################################################################################################
###################################################################################################################
###################################################################################################################

    def monitorear_precio(self):
        while True:
            precio_actual = self.obtener_precio(url_dolar)
            now = datetime.now()

            if now.hour >= 18 or now.hour < 10:
                self.precio_cerrado(precio_actual)
                print("El precio del dólar blue cerró el día a $", precio_actual)
                break
            elif self.precio_anterior is None:
                self.precio_inicial(precio_actual)
                print(f"Precio inicial del dólar blue ${precio_actual:1.2f}")
            elif precio_actual > self.precio_anterior:
                self.precio_subida(precio_actual)
                print(f"El precio del dólar blue subió a ${precio_actual:1.2f}")
            elif precio_actual == self.precio_anterior:
                self.precio_igualado(precio_actual)
                print(f"El precio del dólar blue se mantiene en ${precio_actual:1.2f}")
            else:
                self.precio_baja(precio_actual)
                print(f"El precio del dólar blue bajó a ${precio_actual:1.2f}")

            self.precio_anterior = precio_actual
            time.sleep(intervalo)

if __name__ == "__main__":
    precio_dolar = PrecioDolar()
    precio_dolar.monitorear_precio()

from machine import Pin
import time
import wpp

wpp.connect_wifi('SEUSSID', 'SUASENHA')

def le_touch():
    print("ESP32 Touch Test")

    # Configura o pino de toque
    touch_pin = Pin(19)
    count = 0
    while True:
        # Lê o valor do pino de toque
        touch_value = touch_pin.value()
        if (touch_value == 1):
            count += 1
        else:
            count = 0
        print(touch_value)  # Imprime o valor lido
        time.sleep_ms(100)  # Espera 1 segundo
        if count >= 10 and count < 30:
            touch_value = touch_pin.value()
            if touch_value == 1:
                continue
            else:
                wpp.send_message('NUMEROWPP', 'APIKEY', 'Mensagem%20Um')
        if count >= 30:
            touch_value = touch_pin.value()
            if touch_value == 1:
                continue
            else:
                wpp.send_message('NUMEROWPP', 'APIKEY', 'Mensagem%20Dois')

le_touch()


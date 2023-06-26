from gpiozero import PWMOutputDevice

class Buzzer:
    def __init__(self, pin):
        self.buzzer = PWMOutputDevice(pin)
        self.buzzer.value = 0  # 초기에 부저를 중지 상태로 설정

    def start(self):
        if self.buzzer.value == 0: # 현재 부저가 울리고 있지 않은 경우에만 부저 울리기
            self.buzzer.value = 0.5  # 부저 울리기 (50% duty cycle)

    def stop(self):
        self.buzzer.value = 0  # 부저 중지


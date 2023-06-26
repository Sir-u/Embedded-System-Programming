from gpiozero import DistanceSensor, PWMOutputDevice
from buzzer import Buzzer
import time

# GPIO 핀 번호 설정
trigger_pin = 23
echo_pin = 24
buzzer_pin = 12

# 초음파 거리 센서 및 부저 객체 생성
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
buzzer = Buzzer(buzzer_pin)

# 거리 측정 및 부저 제어
while True:
    distance = sensor.distance * 100  # 거리 측정 (단위: 센티미터)
    print("Distance:", distance, "cm")
    
    if distance > 20:  # 20cm 이상의 거리일 때
        buzzer.start() 
    else:
        buzzer.stop()  # 부저 멈추기

    time.sleep(0.5)  # 0.5초 대기
  

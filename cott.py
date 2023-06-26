import serial
import RPi.GPIO as GPIO
import time

# UART 설정
port = "/dev/serial0"  # 사용할 시리얼 포트
baudrate = 9600  # 통신 속도
ser = serial.Serial(port, baudrate)

# GPIO 설정
motor_pin = 18  # 모터에 연결된 GPIO 핀 번호
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(motor_pin, GPIO.OUT)

# UART 명령 패킷 생성 함수
def create_uart_command():
    start_byte_1 = 0x42
    start_byte_2 = 0x4D
    command = 0x00
    CO2_high = 0x00
    CO2_low = 0x00
    Cal_A_high = 0x00
    Cal_A_low = 0x2C
    Cal_B_high = 0x41
    Cal_B_low = 0x00

    checksum_high = (start_byte_1 + start_byte_2 + command + CO2_high + CO2_low + Cal_A_high + Cal_A_low + Cal_B_high + Cal_B_low) // 256
    checksum_low = (start_byte_1 + start_byte_2 + command + CO2_high + CO2_low + Cal_A_high + Cal_A_low + Cal_B_high + Cal_B_low) % 256

    uart_command = bytearray([start_byte_1, start_byte_2, command, CO2_high, CO2_low, Cal_A_high, Cal_A_low, Cal_B_high, Cal_B_low, checksum_high, checksum_low])
    return uart_command

# CO2 측정 함수
def measure_co2():
    uart_command = create_uart_command()
    ser.write(uart_command)  # UART 명령 전송

    response = ser.read(9)  # UART 응답 받기
    if len(response) == 9:
        co2_high = response[3]/16
        #print(co2_high)
        co2_low = response[4]/16
        #print(co2_low)
        co2_concentration = co2_high * 25.6 + co2_low
        return co2_concentration
    else:
        return None

# 모터 회전 함수

def rotate_motor():
    pwm = GPIO.PWM(motor_pin, 50)  # 50Hz 주파수로 PWM 생성
    pwm.start(2.5)  # 모터의 초기 위치로 설정 (0도)
    time.sleep(10)  # 0.5초 대기
    pwm.ChangeDutyCycle(7.5)  # 모터를 90도로 회전 (90도)
    time.sleep(1)  # 1초 대기
    pwm.stop()  # PWM 중지



# CO2 측정 및 모터 동작 실행
co2_count = 0  # CO2 농도가 300 이상인 횟수를 세는 변수
while True:
    # co2_value = measure_co2()
    co2_value = 400
    if co2_value is not None:
        # print("CO2 Concentration:", co2_value, "ppm")
        if co2_value > 300:
            co2_count += 1
            if co2_count >= 5:
                rotate_motor()
        else:
            co2_count = 0  # CO2 농도가 300 미만일 때는 카운트 초기화
    else:
        print("CO2 Measurement Failed")

    time.sleep(1)  # 1초 대기

# UART 종료
ser.close()


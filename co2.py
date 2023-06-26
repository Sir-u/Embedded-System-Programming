import serial

# 시리얼 포트 및 설정
port = "/dev/serial0"  # 시리얼 포트 경로 (Raspberry Pi에서 UART 포트)
baudrate = 9600  # 통신 속도 (CO2 센서와 동일한 속도로 설정)

# 시리얼 통신 객체 생성
ser = serial.Serial(port, baudrate)

# CO2 센서에 명령을 전송하는 함수
def send_command(command):
    ser.write(command.encode())

# CO2 농도 읽기 함수
def read_co2_concentration():
    send_command("\xFF\x01\x86\x00\x00\x00\x00\x00\x79")  # CO2 센서에 농도 측정 명령 전송
    response = ser.read(9)  # 응답 수신

    if len(response) >= 4 and response[0] == 0xFF and response[1] == 0x86:
        co2_concentration = (response[2] << 8) | response[3]
        return co2_concentration
    else:
        return None

try:
    while True:
        co2_concentration = read_co2_concentration()
        if co2_concentration is not None:
            print("CO2 농도:", co2_concentration, "ppm")
        else:
            print("응답 오류")

except KeyboardInterrupt:
    ser.close()






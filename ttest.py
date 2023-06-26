import serial

# 시리얼 포트 설정
serial_port = '/dev/serial0'
baud_rate = 9600

try:
    # 시리얼 포트 열기
    ser = serial.Serial(serial_port, baud_rate)
    
    # 시리얼 포트 장치 정보 출력
    print("시리얼 포트 장치 정보:", ser)

    # 시리얼 포트 장치 권한 확인
    print("시리얼 포트 권한:", ser.is_open)

    # 시리얼 포트 장치 읽기 예제
    response = ser.read(9)  # 응답 수신
    print("수신 데이터:", response)

    # 시리얼 포트 장치 쓰기 예제
    ser.write(b'Hello')  # 데이터 전송

    # 시리얼 포트 닫기
    ser.close()

except serial.SerialException as e:
    print("시리얼 포트 예외 발생:", e)

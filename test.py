import smbus
import time

# RT9161 칩셋의 I2C 주소
I2C_ADDRESS = 0x48

# PCF8591T의 ADC 채널 설정
ADC_CHANNEL = 0

# 심박수 측정
def measure_heartbeat():
    bus = smbus.SMBus(1)  # I2C 버스 번호 (라즈베리 파이 모델에 따라 다를 수 있음)

    while True:
        try:
            # ADC 채널 설정 및 데이터 읽기
            bus.write_byte(I2C_ADDRESS, ADC_CHANNEL)
            value = bus.read_byte(I2C_ADDRESS)

            # 심박수 계산
            heartbeat = value   # 측정값을 심박수로 변환

            print("심박수:", heartbeat)

        except IOError:
            print("I/O 에러 발생")

        time.sleep(0.1)

# 메인 함수
if __name__ == '__main__':
    measure_heartbeat()


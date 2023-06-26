import cv2
import dlib
import numpy as np
from imutils import face_utils
from gpiozero import PWMOutputDevice
from buzzer import Buzzer
import time

# 눈 감김 임계값과 경고음 지속 시간 설정
EYE_AR_THRESH = 0.2  # 눈 감김 임계값
ALERT_DURATION = 3 # 경고음 지속 시간 (초)

# GPIO 핀 번호 설정
BUZZER_PIN = 12  # 부저의 GPIO 핀 번호

# 부저 초기화
buzzer = Buzzer(BUZZER_PIN)

# 얼굴 인식을 위한 초기화
detector = dlib.get_frontal_face_detector()   
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 눈 감김 관련 변수 초기화
EYES_CLOSED_TIME = 0

# 비디오 스트림 시작
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 크기 축소
    frame = cv2.resize(frame, (640, 480))

    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = detector(gray, 0)

    for face in faces:
        # 얼굴 랜드마크 검출
        shape = predictor(gray, face)
          
        shape = face_utils.shape_to_np(shape)

        # 눈 좌표 추출
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        # 눈 가로세로 비율 계산
        left_eye_aspect_ratio = (np.linalg.norm(left_eye[1] - left_eye[5]) +
                                 np.linalg.norm(left_eye[2] - left_eye[4])) / (2 * np.linalg.norm(left_eye[0] - left_eye[3]))
        right_eye_aspect_ratio = (np.linalg.norm(right_eye[1] - right_eye[5]) +
                                  np.linalg.norm(right_eye[2] - right_eye[4])) / (2 * np.linalg.norm(right_eye[0] - right_eye[3]))

        # 눈 깜빡임 검사
        eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0
        if eye_aspect_ratio < EYE_AR_THRESH:
            EYES_CLOSED_TIME += 1
            if EYES_CLOSED_TIME >= ALERT_DURATION:
                print("일정 시간 동안 눈을 감았습니다. 경고음이 울립니다.")
                buzzer.start()  # 부저 울리기 (50% duty cycle)
        else:
            EYES_CLOSED_TIME = 0
            buzzer.stop() # 부저 중지

        # 얼굴과 눈 영역 표시
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

    # 화면에 출력
    cv2.imshow("Eye Blink Detection", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 스트림 정리
cap.release()
cv2.destroyAllWindows()


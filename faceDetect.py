import cv2
import dlib
from imutils import face_utils

# 눈깜박임 감지를 위한 상수 값 설정
EAR_THRESHOLD = 0.3  # EAR 임계값
CONSECUTIVE_FRAMES = 3  # 눈 감은 상태를 인식하기 위한 연속 프레임 수

# 얼굴 탐지기 초기화
detector = dlib.get_frontal_face_detector()
# 눈 깜박임 탐지기 초기화
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 눈 깜박임 비율(EAR)을 계산하는 함수
def eye_aspect_ratio(eye):
    # 눈의 수평 좌표 계산
    a = ((eye[1][0] - eye[5][0]) ** 2 + (eye[1][1] - eye[5][1]) ** 2) ** 0.5
    b = ((eye[2][0] - eye[4][0]) ** 2 + (eye[2][1] - eye[4][1]) ** 2) ** 0.5
    # 눈의 수직 좌표 계산
    c = ((eye[0][0] - eye[3][0]) ** 2 + (eye[0][1] - eye[3][1]) ** 2) ** 0.5
    # EAR 계산
    ear = (a + b) / (2.0 * c)
    return ear

# 비디오 스트림 시작
video_capture = cv2.VideoCapture(0)

# 초기화
frame_counter = 0
blink_counter = 0
eyes_closed = False
left_eye = 0
right_eye = 0
ear = 0

while True:
    # 비디오 프레임 읽기
    ret, frame = video_capture.read()
    if not ret:
        break

    # 프레임 크기 조정
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = detector(gray, 0)
    
    # 검출된 얼굴들을 순회하며 눈 깜박임 검출
    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        left_eye = shape[42:48]
        right_eye = shape[36:42]
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # 눈 깜박임을 검출하기 위해 EAR 값을 비교
        if ear < EAR_THRESHOLD:
            frame_counter += 1
            if frame_counter >= CONSECUTIVE_FRAMES:
                eyes_closed = True
                blink_counter += 1
                frame_counter = 0
        else:
            frame_counter = 0
            eyes_closed = False

    # 프레임에 정보 표시
    cv2.putText(frame, "Blinks: {}".format(blink_counter), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if ear is not None:
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if eyes_closed:
        cv2.putText(frame, "Eyes Closed", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 영상 출력
    cv2.imshow("Frame", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 스트림 및 창 종료
video_capture.release()
cv2.destroyAllWindows()

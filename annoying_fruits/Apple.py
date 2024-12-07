import cv2
import dlib
from imutils import face_utils, resize
import numpy as np

# 사과 이미지와 dlib 랜드마크 모델 경로 설정
apple_img_path = 'assets/Apple.jpg'
landmark_model_path = 'shape_predictor_68_face_landmarks.dat'

# 사과 이미지 불러오기 및 크기 조정
apple_img = cv2.imread(apple_img_path)
apple_img = cv2.resize(apple_img, (512, 512))

# dlib 얼굴 감지기와 랜드마크 예측기 로드
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(landmark_model_path)

# 웹캠 연결
cap = cv2.VideoCapture(0)

# 카메라가 열려 있을 때까지 반복
while cap.isOpened():
    ret, img = cap.read()  # 프레임 읽기

    if not ret:
        break  # 읽기 실패 시 종료

    # 얼굴 감지 준비: 이미지를 그레이스케일로 변환
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces = detector(gray_img)

    # 사과 이미지의 복사본 생성
    result = apple_img.copy()

    if len(faces) > 0:  # 얼굴이 감지되었다면,
        face = faces[0]  # 첫 번째 얼굴만 사용

        # 얼굴 랜드마크 감지
        shape = predictor(gray_img, face)
        shape = face_utils.shape_to_np(shape)  # 랜드마크 좌표를 NumPy 배열로 변환

        # 눈과 입의 좌표를 추출하고 각각 사과에 합성
        try:
            # 왼쪽 눈 좌표
            le_x1, le_y1, le_x2, le_y2 = shape[36, 0], shape[37, 1], shape[39, 0], shape[41, 1]
            le_margin = int((le_x2 - le_x1) * 0.18)
            left_eye_img = img[le_y1 - le_margin:le_y2 + le_margin, le_x1 - le_margin:le_x2 + le_margin].copy()
            left_eye_img = resize(left_eye_img, width=100)
            result = cv2.seamlessClone(
                left_eye_img, result, np.full(left_eye_img.shape[:2], 255, left_eye_img.dtype), (100, 200), cv2.MIXED_CLONE
            )

            # 오른쪽 눈 좌표
            re_x1, re_y1, re_x2, re_y2 = shape[42, 0], shape[43, 1], shape[45, 0], shape[47, 1]
            re_margin = int((re_x2 - re_x1) * 0.18)
            right_eye_img = img[re_y1 - re_margin:re_y2 + re_margin, re_x1 - re_margin:re_x2 + re_margin].copy()
            right_eye_img = resize(right_eye_img, width=100)
            result = cv2.seamlessClone(
                right_eye_img, result, np.full(right_eye_img.shape[:2], 255, right_eye_img.dtype), (250, 200), cv2.MIXED_CLONE
            )

            # 입 좌표 추출 및 합성
            mouth_x1, mouth_y1, mouth_x2, mouth_y2 = shape[48, 0], shape[50, 1], shape[54, 0], shape[57, 1]
            mouth_margin = int((mouth_x2 - mouth_x1) * 0.1)
            mouth_img = img[mouth_y1 - mouth_margin:mouth_y2 + mouth_margin, mouth_x1 - mouth_margin:mouth_x2 + mouth_margin].copy()
            mouth_img = resize(mouth_img, width=250)
            result = cv2.seamlessClone(
                mouth_img, result, np.full(mouth_img.shape[:2], 255, mouth_img.dtype), (180, 320), cv2.MIXED_CLONE
            )
        except Exception as e:
            print(f"Error in merging: {e}")

        # 결과 이미지 출력
        cv2.imshow('result', result)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) == ord('q'):
        break

# 카메라 및 모든 창 종료
cap.release()
cv2.destroyAllWindows()
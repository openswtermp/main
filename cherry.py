import cv2
import dlib
import numpy as np
from imutils import face_utils
import os

def process(cherry_img_path='C:/Users/royal/Desktop/cpfl.jpg', 
            landmark_model_path='C:/Users/royal/Desktop/shape_predictor_68_face_landmarks.dat'):
    # 1. 체리 이미지 로드
    if not os.path.exists(cherry_img_path):
        print(f"Error: Cherry image not found at {cherry_img_path}")
        return

    cherry_img = cv2.imread(cherry_img_path)
    if cherry_img is None:
        print("Error: Failed to read the cherry image!")
        return

    cherry_img = cv2.resize(cherry_img, (512, 512))

    # 2. dlib 모델 로드
    if not os.path.exists(landmark_model_path):
        print(f"Error: Landmark model not found at {landmark_model_path}")
        return

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(landmark_model_path)

    # 3. 웹캠 연결
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Webcam not accessible!")
        return

    def extract_and_resize_feature(img, points, size):
        """얼굴의 특정 부위를 추출하고 크기를 조정"""
        mask = np.zeros_like(img)
        points = points.astype(np.int32)
        cv2.fillPoly(mask, [points], (255, 255, 255))
        feature = cv2.bitwise_and(img, mask)
        x, y, w, h = cv2.boundingRect(points)
        extracted = feature[y:y+h, x:x+w]
        resized = cv2.resize(extracted, size)
        return resized

    def overlay_feature(background, feature, center_x, center_y, alpha=0.7):
        """체리 위에 눈이나 입 합성"""
        h, w = feature.shape[:2]
        x1, y1 = max(0, center_x - w // 2), max(0, center_y - h // 2)
        x2, y2 = x1 + w, y1 + h

        # 배경과 겹치는 부분만 합성
        if x2 > background.shape[1] or y2 > background.shape[0]:
            return background  # 범위를 벗어나면 무시
        blend = cv2.addWeighted(background[y1:y2, x1:x2], 1 - alpha, feature, alpha, 0)
        background[y1:y2, x1:x2] = blend
        return background

    # 4. 체리 원형 감지
    gray_cherry = cv2.cvtColor(cherry_img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray_cherry, cv2.HOUGH_GRADIENT, dp=1.5, minDist=50,
        param1=50, param2=30, minRadius=30, maxRadius=60
    )

    if circles is None:
        print("No cherries detected. Please check the image.")
        return

    # 두 알만 선택
    circles = np.round(circles[0, :2]).astype("int")  # 첫 두 알만 선택
    print(f"Detected {len(circles)} cherries.")  # 체리 감지 로그

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # 얼굴 감지 및 랜드마크 추출
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        result = cherry_img.copy()

        if len(faces) > 0:
            face = faces[0]
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            # 눈과 입 영역 추출
            left_eye = extract_and_resize_feature(frame, shape[36:42], (30, 15))
            right_eye = extract_and_resize_feature(frame, shape[42:48], (30, 15))
            mouth = extract_and_resize_feature(frame, shape[48:60], (40, 20))

            for (x, y, r) in circles:
                try:
                    # 체리 중심부에 자연스럽게 배치
                    result = overlay_feature(result, left_eye, x - int(r * 0.4), y - int(r * 0.3))  # 왼쪽 눈
                    result = overlay_feature(result, right_eye, x + int(r * 0.4), y - int(r * 0.3))  # 오른쪽 눈
                    result = overlay_feature(result, mouth, x, y + int(r * 0.1))  # 입
                except Exception as e:
                    print(f"Error blending feature on cherry: {e}")
        else:
            print("No faces detected. Please adjust webcam position.")

        # 결과 출력
        cv2.imshow("Result", result)

        # 종료 조건: 'q' 키를 누르면 종료
        if cv2.waitKey(1) == ord('q'):
            break

    # 자원 정리
    cap.release()
    cv2.destroyAllWindows()


# 실행
process()
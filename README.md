# Annoying Fruits with OpenCV
### GCU OpenSourceSW 2024

사용자의 얼굴을 어노잉 오렌지처럼 과일에 합성해주는 프로그램입니다.

dlib패키지를 통해 사용자의 캠을 통해 유저의 얼굴을 감지하고

dlib.shape_predictor()를 통해 얼굴의 좌표(눈, 코, 입 등 68개의 좌표)를 추출합니다.

## 예시화면

<img src="https://github.com/user-attachments/assets/a1b18d2d-7504-4d05-9741-61ce4b50a27e" alt="Annoying Orange" width="300">

## 사용 패키지 및 모듈
OpenCV - 사용자의 얼굴을 식별하기 위해 openCV와 opencv-contrib-python 패키지를 사용하였습니다.

    pip install opencv-python opencv-python-headless

    pip install opencv-contrib-python

Dilb - 얼굴 검출 및 랜드마크 추출과 같은 머신러닝 기능을 사용하기 위해 Dilb 패키지를 사용하였습니다.

    pip install cmake
    
    pip install dlib

Imutils - 이미지 처리와 관련된 유틸리티 함수들을 사용하기 위해 Imutils모듈을 사용하였습니다.

    pip install imutils

NumPy - 배열과 수학적 계산을 사용하므로 NumPy 라이브러리를 사용하였습니다.

    pip install numpy

tkinter - GUI구현을 위해 tkinter 라이브러리를 사용하였습니다, 별도 설치는 필요하지 않습니다.

Pillow - Image 및 ImageTk를 사용하여 이미지를 로드하고 Tkinter와 호환 가능하도록 변환하기 위해 pillow 라이브러리를 사용하였습니다.

    pip install pillow

## 실행방법

1. **합성할 과일 선택**
   - 유저는 프로그램 실행 후, 합성하고 싶은 과일의 버튼을 클릭합니다.

2. **얼굴 인식 및 합성**
   - 카메라가 실행되며, 첫 번째로 인식된 얼굴이 선택한 과일에 합성됩니다.

3. **저장 기능**
   - `export` 버튼을 눌러 현재 합성된 이미지를 캡처하고 저장할 수 있습니다.

4. **프로그램 종료**
   - 프로그램 실행 중 `q`를 누르면 프로그램을 종료할 수 있습니다.

## 참고문헌
https://www.youtube.com/watch?v=9VYUXchrMcM

## contributers
* 202135587 최재경
* 202434643 윤석원
* 202434863 현태건
* 202434601 김지후
* 202434816 이준서

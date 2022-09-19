## -*- coding: utf-8 -*-  # 한글 주석쓸려면 적기
import cv2
import time
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime 
font = cv2.FONT_ITALIC

def faceDetect():
    global score
    global end_time
    global start_t
    score = 0
    music_on = 0
    start_t = time.time() #시작 시간
    eye_detect = False
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "\\haarcascade_eye.xml")

    try:
        cam = cv2.VideoCapture(0)
    except:
        print("camera loading error")
        return
    max_time_end = start_t + (10)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in eyes:
            cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0),2)
            cv2.putText(frame, "Detected Eyes", (x-5,y-5), font, 0.5, (255,255,0), 2)
            if eye_detect:
                roi_gray = gray[y, x]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0),2)
            else:
                global info
                info = "Eye Detection ON"
                cv2.putText(frame, info, (5,15), font, 0.5, (255,0,255), 1)
        
                if info == "Eye Detection ON":
                    max_time_end = time.time() + (10)
        
        if time.time() > max_time_end:  #눈 감은 시간이 n초 이상일 경우 점수 차감(현재시간 - max_time_end)
            score -= 1
            music_on -= 1
            print(datetime.now().time(), '점수 감소 중')
        
        if music_on == -300:
            os.system('노래.wav')
            music_on = 0

        if time.time() > end_time:
            end = time.time()
            on = end - start_t
            print(on)
            print('끝났습니다')
            print(score/100)
            break

        cv2.imshow('program', frame)
        k = cv2.waitKey(30)

        if k == 27:
            break
    
    cam.release()
    cv2.destroyAllWindows()

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        pal = QPalette()
        pal.setColor(QPalette.Background,QColor('orange'))
        self.setPalette(pal)

    def initUI(self):
        main_layout = QVBoxLayout()
        title = QLabel('공부할 시간을 정해주세요.')
        btn_layout = QHBoxLayout()
        self.one_btn = QPushButton('1시간')
        self.two_btn = QPushButton('2시간')
        self.three_btn = QPushButton('3시간')

        self.one_btn.clicked.connect(self.one_hour)
        self.two_btn.clicked.connect(self.two_hour)
        self.three_btn.clicked.connect(self.three_hour)
        
        btn_layout.addWidget(self.one_btn)
        btn_layout.addWidget(self.two_btn)
        btn_layout.addWidget(self.three_btn)

        main_layout.addWidget(title)
        main_layout.addLayout(btn_layout)

        self.setWindowTitle('졸음 스코어 프로그램')
        self.setLayout(main_layout)
        self.show()
    
    def one_hour(self):
        global score
        global end_time
        end_time = time.time() + (60*60*1)
        faceDetect()
        new_score = score/100
        with open('hour1.txt','a+',encoding='utf8') as file:
            if os.stat("hour1.txt").st_size == 0:
                file.write("1번 진행함.\n")
                file.write(f'점수: {new_score}점')
        with open('hour1.txt','r',encoding='utf8') as file:
            for x,l in enumerate(file):
                if x == 0:
                    new_str0 = str(int(l[:1]) + 1)+l[1:]
                if x == 1:
                    new_str1 = l[:4]+str(float(l[4:-1]) + new_score)+l[-1:]
        with open('hour1.txt', 'w', encoding='utf8') as file:
                file.write(new_str0)
                file.write(new_str1)
    def two_hour(self):
        global score
        global end_time
        end_time = time.time() + (60*60*2)
        faceDetect()
        new_score = score/100
        with open('hour1.txt','a+',encoding='utf8') as file:
            if os.stat("hour1.txt").st_size == 0:
                file.write("1번 진행함.\n")
                file.write(str(new_score))
        with open('hour1.txt','r',encoding='utf8') as file:
            for x,l in enumerate(file):
                if x == 0:
                    new_str0 = str(int(l[:1]) + 1)+l[1:]
                if x == 1:
                    new_str1 = l[:4]+str(float(l[4:-1]) + new_score)+l[-1:]
        with open('hour1.txt', 'w', encoding='utf8') as file:
                file.write(new_str0)
                file.write(new_str1)
    def three_hour(self):
        global score
        global end_time
        end_time = time.time() + (60*60*3)
        faceDetect()
        new_score = score/100
        with open('hour1.txt','a+',encoding='utf8') as file:
            if os.stat("hour1.txt").st_size == 0:
                file.write("1번 진행함.\n")
                file.write(str(new_score))
        with open('hour1.txt','r',encoding='utf8') as file:
            for x,l in enumerate(file):
                if x == 0:
                    new_str0 = str(int(l[:1]) + 1)+l[1:]
                if x == 1:
                    new_str1 = l[:4]+str(float(l[4:-1]) + new_score)+l[-1:]
        with open('hour1.txt', 'w', encoding='utf8') as file:
                file.write(new_str0)
                file.write(new_str1)
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./휴먼편지체.ttf')        #폰트 추가(컴퓨터 내에 있는 폰트만 가능)
    app.setFont(QFont('휴먼편지체'))                     #폰트 적용
    main=Main()
    sys.exit(app.exec_())



        
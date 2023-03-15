from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import cv2
from cvzone.HandTrackingModule import HandDetector

class MainApp(MDApp):

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.capture = cv2.VideoCapture(0)
        #self.capture.set(3, 720)
        #self.capture.set(4, 480)
        self.detector = HandDetector(detectionCon=0.5, maxHands=2)
        Clock.schedule_interval(self.load_video, 1.0/60.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        hands, frame = self.detector.findHands(frame)

        if hands:
            for i, hand in enumerate(hands):
                lmList = hand["lmList"]
                handType = hand["type"]
                fingers = self.detector.fingersUp(hand)
                height1, _, _ = self.detector.findDistance(lmList[5][0:2], lmList[6][0:2], frame)
                height2, _, _ = self.detector.findDistance(lmList[6][0:2], lmList[7][0:2], frame)
                height3, _, _ = self.detector.findDistance(lmList[7][0:2], lmList[8][0:2], frame)
                height = height1 + height2 + height3
                width, _, _ = self.detector.findDistance(lmList[7][0:2], lmList[8][0:2], frame)
                dist = tuple(round(num, 3) for num in (height, width))
                color = (0, 0, 0) if i == 0 else (0, 0, 0)
                cv2.putText(frame, f'Index Finger{i+1}: {handType} - {dist} - {fingers}', (10, 30+i*30), cv2.FONT_HERSHEY_PLAIN, 1.12, color, 2)

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    MainApp().run()

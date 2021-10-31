from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from random import randint
import cv2.cv2 as cv2


class WindowMenu(Screen):
	img_inp = ObjectProperty(None)
	img_exp = ObjectProperty(None)
	nr_zdj_text = ObjectProperty(None)
	tryb_text = ObjectProperty(None)
	mode = 'default'
	nr = 1

	def random_img(self):
		new_nr = randint(1, 16)
		while new_nr == self.nr:
			new_nr = randint(1, 16)
		self.load_img(new_nr)

	def load_img(self, nr):
		self.nr = nr
		self.nr_zdj_text.text = f'Aktualne zdjęcie: {nr}'
		self.img_inp.source = f'./Image_Input/{nr}.jpg'
		self.img_inp.reload()

	def change_mode(self, tryb):
		self.tryb_text.text = f'Tryb: {tryb.upper()}'
		self.mode = tryb

	def detect_faces(self):
		img = cv2.imread(self.img_inp.source)
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_cascade = cv2.CascadeClassifier(f'cascades/data/haarcascade_frontalface_{self.mode}.xml')
		color = (0, 255, 0)
		face_rects = face_cascade.detectMultiScale(
			gray_img, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
		if len(face_rects):
			for faceRect in face_rects:
				x, y, w, h = faceRect
				cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)

		cv2.imshow('image', img)


class WindowManager(ScreenManager):
	pass


kv = Builder.load_file('ui.kv')


class FaceRecApp(App):
	def build(self):
		return kv


if __name__ == "__main__":
	FaceRecApp().run()

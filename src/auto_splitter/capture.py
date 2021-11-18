
import pytesseract
import cv2
import numpy as np
from PIL import Image

class Capture():
    def __init__(self, cam_number, width, height):
        self.cap = cv2.VideoCapture(cam_number)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        return self.cap.read()

    def get_text_from_frame(self, frame, coord, thresh):
        crop   = cv2.cvtColor(frame[coord.y:coord.y+coord.h, coord.x:coord.x+coord.w], cv2.COLOR_BGR2GRAY)
        image  = Image.fromarray(crop).point(lambda p: p > thresh and 255)
        try: 
            txt = pytesseract.image_to_string(image)
            return txt
        except: 
            print('Trying default Tesseract install directory...')
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            txt = pytesseract.image_to_string(image)
            return txt

    def save_frame(name):
        ret, frame = self.cap.read()
        if ret: 
            image_orig = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image_gray = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            image_orig.save("%s/%s_orig.png" % (debug_path, name), "PNG")
            image_gray.save("%s/%s_gray.png" % (debug_path, name), "PNG")

    def draw_capture_zones(self, *args):
            ret, frame = self.cap.read()
            if ret: 
                for i in args:
                    cv2.rectangle(frame, (i.x, i.y),(i.x2, i.y2),(0,255,0))

            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def get_average_color(self, zone):
        ret, frame = self.cap.read()
        if ret: 
            img = cv2.cvtColor(frame[zone.y:zone.y+zone.h, zone.x:zone.x+zone.w], cv2.COLOR_BGR2RGB)
            average = img.mean(axis=0).mean(axis=0)
            return average
    
    def get_average_color_from_frame(self, frame, zone):
        img = cv2.cvtColor(frame[zone.y:zone.y+zone.h, zone.x:zone.x+zone.w], cv2.COLOR_BGR2RGB)
        average = img.mean(axis=0).mean(axis=0)
        return [round(average[0]), round(average[1]), round(average[2])]

    def close(self):
        print('releasing...')
        self.cap.release()

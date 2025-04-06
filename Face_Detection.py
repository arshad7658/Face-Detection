##authored by Shaik Arshad

import face_alignment
import cv2
import torch
import os
import numpy as np

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

class FaceDetection:
    def __init__(self, image):
        self.fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D,
                                     flip_input = False, device= device)
        self.raw_image = cv2.imread(image)
        self.FIGSIZE = 5
    def _get_landmarks(self):
        landmarks = self.fa.get_landmarks(self.raw_image)
        return landmarks
    def _draw_landmarks(self, landmarks):
        for landmark in landmarks:
            x_coords = landmark[:,0]
            y_coords = landmark[:,1]

            x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
            y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))
            cv2.rectangle(self.raw_image, (x_min, y_min), (x_max, y_max), (255,0, 0), 2)
            # for x, y in landmark:
            #     # cv2.circle(self.raw_image, (int(x), int(y)),
            #     #            5, (255, 0, 0), -1)
            #     print(f'x:{x}, y:{y}')
            # print('Next Face')

    def show(self):
        ld = self._get_landmarks()
        self._draw_landmarks(ld)
        return self.raw_image[:,:,::-1]
        # cv2.imshow("Detectted Faces", self.raw_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


# image_path= os.path.abspath('173.jpg')
# fa = FaceDetection(image_path)
# image = fa.show()


from tkinter import *
import tkinter
from PIL import Image, ImageTk
from tkinter import filedialog
root = Tk()
root.title('Face Detection(WIP)')

root.geometry('1280x720')
root.config(background='#000000')

def file_browser():
    filepath = filedialog.askopenfilename(filetypes=
                                          [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    fa = FaceDetection(filepath)
    processed_image = fa.show()
    pil_image = Image.fromarray(processed_image)
    max_size = (800, 800)
    pil_image.thumbnail(max_size)
    photo = ImageTk.PhotoImage(image=pil_image)
    label = tkinter.Label(root, image=photo)
    label.image = photo
    label.pack()
    # photo = ImageTk.PhotoImage(image)


    # if hasattr(file_browser, "image_label"):
    #     file_browser.image_label.config(image=photo)
    #     file_browser.image_label.image = photo
    # else:
    #     file_browser.image_label = tkinter.Label(root, image=photo)
    #     file_browser.image_label.image = photo
    #     file_browser.image_label.pack()

button = Button(root, text='Select Image', command=file_browser)
button.pack(padx=20, pady=20)

root.mainloop()
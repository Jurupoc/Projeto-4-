import tkinter as tk
import constant
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from controler import Controller


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.controller_instance = Controller()
        self.current_image_path = ''
        self.choose = 0

        # FRAMES

        self.frame_image = tk.Frame(width=constant.frame_image_width, height=constant.screen_height,
                                    background=constant.color_red, borderwidth=2, relief="groove")
        self.frame_option = tk.Frame(width=constant.frame_option_width, height=constant.screen_height,
                                     background=constant.color_blue, borderwidth=2, relief="groove")

        # LABELS

        self.img_label = tk.Label(self.frame_image)
        self.information_label = tk.Label(self.frame_image)

        # BUTTONS

        self.bt_add_image_width = 240
        self.bt_add_image_height = 35
        self.bt_add_image = tk.Button(self.frame_option, text='Select Image', borderwidth=2, relief="groove",
                                      font=('Courier New', 14,))

        self.bt_face_recognizer_width = 230
        self.bt_face_recognizer_height = 70
        self.bt_face_recognizer = tk.Button(self.frame_option, text='Face Recognizer', font=('Courier New', 13,))

        self.bt_celebrity_recognizer_width = 300
        self.bt_celebrity_recognizer_height = 70
        self.bt_celebrity_recognizer = tk.Button(self.frame_option, text='Celebrity Recognizer',
                                                 font=('Courier New', 13))

        self.bt_text_recognizer_width = 230
        self.bt_text_recognizer_height = 70
        self.bt_text_recognizer = tk.Button(self.frame_option, text='Text Recognizer', font=('Courier New', 13,))

        # BUTTONS ACTION

        self.bt_add_image['command'] = lambda: self.render_image()
        self.bt_face_recognizer['command'] = lambda: self.face_recognizer()
        self.bt_celebrity_recognizer['command'] = lambda: self.celeb_recognizer()
        self.bt_text_recognizer['command'] = lambda: self.text_recognizer()

        # RENDER

        self.frame_option.pack(side='right')
        self.frame_image.pack(side='left')

        self.bt_add_image.place(width=self.bt_add_image_width, height=self.bt_add_image_height,
                                x=(constant.frame_option_width / 2 - (self.bt_add_image_width / 2)),
                                y=constant.screen_height / 6)

        self.bt_celebrity_recognizer.place(width=self.bt_face_recognizer_width,
                                           height=self.bt_celebrity_recognizer_height,
                                           x=(constant.frame_option_width / 2 - (self.bt_face_recognizer_width / 2)),
                                           y=constant.screen_height / 3)

        self.bt_face_recognizer.place(width=self.bt_face_recognizer_width, height=self.bt_face_recognizer_height,
                                      x=(constant.frame_option_width / 2 - (self.bt_face_recognizer_width / 2)),
                                      y=constant.screen_height / 2)
        self.bt_text_recognizer.place(width=self.bt_text_recognizer_width, height=self.bt_text_recognizer_height,
                                      x=(constant.frame_option_width / 2 - (self.bt_face_recognizer_width / 2)),
                                      y=constant.screen_height * 2 / 3)

    def select_file(self):
        file = askopenfilename()
        self.current_image_path = file
        return file

    def render_label(self, text=''):
        self.information_label['text'] = text
        self.information_label['bg'] = constant.color_red
        self.information_label['font'] = ('Courier New', 20,)
        self.information_label.place(y=constant.screen_height - 50, x=constant.frame_image_width/2 - 160 if len(text) == 19 else constant.frame_image_width/2 - 190)

    def render_image(self, file_path=None):
        file = self.select_file() if file_path is None else file_path
        if file:
            load = Image.open(file)

            new_size = (700, 500) if load.size[0] > load.size[1] else (400, 600)
            render = ImageTk.PhotoImage(load.resize(new_size, Image.ANTIALIAS))

            self.render_label()
            self.img_label['image'] = render
            self.img_label.image = render
            if load.size[0] > load.size[1]:
                self.img_label.place(x=(constant.frame_image_width / 2 - (new_size[0] / 2)),
                                     y=constant.screen_height / 8)
            else:
                self.img_label.place(x=(constant.frame_image_width / 2 - (new_size[0] / 2)),
                                     y=constant.screen_height / 20)

    def face_recognizer(self):
        if self.current_image_path:
            faces = self.controller_instance.recognize_face(self.current_image_path)
            if faces != 0:
                self.render_image(file_path=f'final_image/{self.current_image_path.split("/")[-1]}')
                self.render_label(f'{faces} rosto(s) encontrado(s)')
            else:
                self.render_label('0 rostos encontrados')
        else:
            self.render_label('Selecione um imagem')

    def celeb_recognizer(self):
        if self.current_image_path:
            celebs = self.controller_instance.recognize_celebrity(self.current_image_path)
            if celebs != 0:
                self.render_image(file_path=f'final_image/{self.current_image_path.split("/")[-1]}')
                self.render_label(f'{celebs} celebridade(s) encontrada(s)')
            else:
                self.render_image(self.current_image_path)
                self.render_label('0 celebridades encontradas')
        else:
            self.render_label('Selecione um imagem')

    def text_recognizer(self):
        if self.current_image_path:
            texts = self.controller_instance.text_recognizer(self.current_image_path)
            if texts != 0:
                self.render_image(file_path=f'final_image/{self.current_image_path.split("/")[-1]}')
                self.render_label(f'{texts} texto(s) encontrado(s)')
            else:
                self.render_image(self.current_image_path)
                self.render_label('0 textos encontrados')
        else:
            self.render_label('Selecione um imagem')


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Recognizer')
    root.geometry(f"{constant.screen_width}x{constant.screen_height}+10+20")
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

import tkinter
import tkinter.ttk
import tkinter.font
from tkinter import filedialog
import webbrowser
from Information import open_pages
import os
import tkinter.messagebox
import threading
from textsts import info
from exceptions import EX


class Application(tkinter.ttk.Frame):
    def __init__(self, master=None):
        """ Создаём окно и задаём ему параметры """
        super().__init__(master)
        self.pack()
        s = tkinter.ttk.Style()
        s.theme_use('alt')
        s.configure('BtnStyle.TButton', background='gray17', foreground='white')
        s.map('BtnStyle.TButton', background=[('active', 'gray14')], foreground=[('active', 'white smoke')])

        s.configure('StandartLabel.TLabel', anchor='center', justify=tkinter.CENTER, padding=tkinter.SUNKEN,
                    borderwidth=2, foreground='white', background='gray32')

        self._create_widgets()
        self.master.iconbitmap('images\\icon.ico')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.master.title('VKPars v0.1 BETA')
        self.master.resizable(False, False)
        self.files_dict = []

    def _create_widgets(self):
        """ Создаём стартовое окно """
        self._forget_widgets()
        self.font = tkinter.font.Font(self, family='Times New Roman', size=14)

        self.mainLbl = tkinter.ttk.Label(self, text='Выберите папку,\n где находятся все сообщения.',
                                         style='StandartLabel.TLabel', font=self.font)
        self.mainLbl.grid(row=0, column=0, sticky='n')

        self.rootBtn = tkinter.ttk.Button(self, text='Выбрать путь', style='BtnStyle.TButton', command=self._callback)
        self.rootBtn.grid(row=1, column=0, sticky='ws')

        self.infoBtn = tkinter.ttk.Button(self, text='Информация', style='BtnStyle.TButton', command=self._print_info)
        self.infoBtn.grid(row=1, column=0, sticky='es')

    def _print_info(self):
        """ Функция информации """
        self._forget_widgets()
        self.infoLbl = tkinter.ttk.Label(self, text=info, style='StandartLabel.TLabel', font=self.font, cursor='hand2')
        self.infoLbl.bind('<Button-1>', lambda e: self._open_url('https://vk.com/data_protection?section=rules&scroll'
                                                                 '_to_archive=1'))
        self.infoLbl.grid(row=0, column=0, sticky='n')

        self.backBtn = tkinter.ttk.Button(self, text='Назад', style='BtnStyle.TButton', command=self._create_widgets)
        self.backBtn.grid(row=1, column=0, sticky='ws')

        self.extBtn = tkinter.ttk.Button(self, text='Выход', style='BtnStyle.TButton', command=root.destroy)
        self.extBtn.grid(row=1, column=0, sticky='es')

    def _forget_widgets(self):
        """ Убираем все файлы с приложения """
        try:
            self.mainLbl.grid_forget()
            self.rootBtn.grid_forget()
            self.infoBtn.grid_forget()
        except EX as ex:
            print(ex)

        try:
            self.infoLbl.grid_forget()
            self.backBtn.grid_forget()
            self.extBtn.grid_forget()
        except EX as ex:
            print(ex)

        try:
            self.chsLbl.grid_forget()
            self.backBtn.grid_forget()
            self.extBtn.grid_forget()
            self.agnBtn.grid_forget()
        except EX as ex:
            print(ex)

    def _callback(self):
        """ Функция для выбора директории """
        self._forget_widgets()
        self.chsLbl = tkinter.ttk.Label(self, text='Выберете папку с html файлами переписки.\n Если хотите вернуться '
                                                   'назад, используйте кнопки.', style='StandartLabel.TLabel',
                                        font=self.font)
        self.chsLbl.grid(row=0, column=0, sticky='n')

        self.backBtn.grid(row=1, column=0, sticky='ws')

        self.extBtn.grid(row=1, column=0, sticky='es')

        self.agnBtn = tkinter.ttk.Button(self, text='Выбрать папку снова', style='BtnStyle.TButton',
                                         command=self._callback)
        self.agnBtn.grid(row=1, column=0, sticky='s')
        data = filedialog.askdirectory()
        if data == '':
            pass
        else:
            if data:
                files = os.listdir(data)
                for file in files:
                    file_format = str(file.split('.')[-1])
                    if file_format == 'html':
                        self.files_dict.append(file)

            if str(self.files_dict) == '[]':
                self._show_error()
            else:
                self._check_info()
                self.update_idletasks()
                self.open_pages_thread = threading.Thread(target=open_pages, args=(data, self.files_dict, self.lsb))
                self.open_pages_thread.start()

    def _open_url(self, url: str):
        """ Функция для открытия киберссылок """
        webbrowser.open_new(url)

    def _destroy_widgets(self):
        """ Функция удаления виджетов (для освобождения памяти) """
        try:
            self.mainLbl.destroy()
            self.rootBtn.destroy()
            self.infoBtn.destroy()
        except EX as ex:
            print(ex)

        try:
            self.infoLbl.destroy()
            self.backBtn.destroy()
            self.extBtn.destroy()
        except EX as ex:
            print(ex)

        try:
            self.chsLbl.destroy()
            self.backBtn.destroy()
            self.extBtn.destroy()
            self.agnBtn.destroy()
        except EX as ex:
            print(ex)

    def _check_info(self):
        """ Показываем пользователю что мы загрузили """
        self.lsbFont = tkinter.font.Font(self, family='Colibri', size=12)
        self._destroy_widgets()
        _infoLabel = tkinter.ttk.Label(self, text='Ждите, мы начали сбор информации. Это достаточно долгий \n'
                                                  'долгий процесс. Мы вам сообщим, как закончим сбор.',
                                       style='StandartLabel.TLabel', font=self.font)
        _infoLabel.grid(row=0, column=0, sticky='n')

        self.lsb = tkinter.Listbox(self, width=56, height=30, selectmode=tkinter.MULTIPLE, font=self.lsbFont,
                                   fg='white', bg='gray16', selectbackground='gray2', selectforeground='white smoke',
                                   exportselection=0)
        self.lsb.grid(row=1, column=0, sticky='w')

        _exBtn = tkinter.ttk.Button(self, text='Свернуть приложение', style='BtnStyle.TButton', command=self._exit)
        _exBtn.grid(row=3, column=0, sticky='ws')

        hsy = tkinter.ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.lsb.yview)
        self.lsb['yscrollcommand'] = hsy.set
        hsy.grid(row=1, column=1, sticky='wns')
        hsy = tkinter.ttk.Scrollbar(self, orient=tkinter.HORIZONTAL, command=self.lsb.xview)
        self.lsb['xscrollcommand'] = hsy.set
        hsy.grid(row=2, column=0, sticky='wen')

    def _show_error(self):
        """ Выводим ошибку, если в папке отсутствуют файлы с форматом .html """
        tkinter.messagebox.showerror('html файл отсутствует', 'В указанной папке отсутствуют файлы с расширением html.')

    def _exit(self):
        """ Функция сворачивания приложения """
        question = tkinter.messagebox.askyesno('Прочтите внимательно!', 'ПРОЧИТАЙТЕ ВНИМАТЕЛЬНО! Вы уверены что хотите '
                                                                        'свернуть это окно? Процесс сбора информации '
                                                                        'продолжится, но вы больше не сможете открыть '
                                                                        'это окно с информацией!')
        if question:
            root.destroy()
            self.open_pages_thread.join()


root = tkinter.Tk()
app = Application(master=root)
root.mainloop()

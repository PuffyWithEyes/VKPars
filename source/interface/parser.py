import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import os
import tkinter


""" Создаём путь для папок """
all_root = os.getcwd()
all_root = list(all_root.split('\\')[:-1])
zero_string = ''
print('0', zero_string)
for root in all_root:
    zero_string += root + '\\'
    print('1', zero_string)
try:
    os.mkdir(f"{zero_string}\\data (VKPars)")
    zero_string += 'data (VKPars)' + '\\'
    print('2', zero_string)
except:
    zero_string += 'data (VKPars)' + '\\'
    print('3', zero_string)


useragent = fake_useragent.UserAgent().random
headers = {
    'User-Agent': useragent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


def create_direct():
    """ Создаём папки с данными """
    paths = [f"{zero_string}gallery", f"{zero_string}voices", f"{zero_string}other"]
    try:
        for path in paths:
            os.mkdir(path)
    except OSError:
        pass


def open_pages(direct, datas, label):
    """ Парсим данные """
    create_direct()
    count = 0
    for data in datas:
        try:
            with open(f"{direct}/{data}") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            get_info_time = soup.find_all('div', class_='item')
            for info in get_info_time:
                try:
                    try:
                        get_all_attachment = info.find_all('div', class_='attachment')
                        for i in get_all_attachment:
                            get_attachment = i.find('a', class_='attachment__link').get('href')

                            try:
                                get_who = info.find('div', class_='message__header').get('a').text
                                get_time = info.find('div', class_='message__header').text
                                all_info = get_who + get_time.replace(':', '-').replace(
                                    ' ', '-').replace(',', '-')

                            except:
                                all_info = info.find('div', class_='message__header').text.replace(':', '-').replace(
                                    ' ', '-').replace(',', '-')

                            download_data(get_attachment=get_attachment, all_info=all_info, count=count, label=label)
                            count += 1

                    except:
                        get_attachment = info.find('a', class_='attachment__link').get('href')

                        try:
                            get_who = info.find('div', class_='message__header').get('a').text
                            get_time = info.find('div', class_='message__header').text
                            all_info = get_who + get_time.replace(':', '-').replace(
                                ' ', '-').replace(',', '-')

                        except:
                            all_info = info.find('div', class_='message__header').text.replace(':', '-').replace(
                                ' ', '-').replace(',', '-')

                        download_data(get_attachment=get_attachment, all_info=all_info, count=count, label=label)
                        count += 1

                except:
                    continue
        except Exception as ex:
            label.insert(tkinter.END, f"[INFO] Process finished with: {ex}")


def download_data(get_attachment, all_info, count, label):
    """ Расфасовываем данные по папкам """
    r = requests.get(url=get_attachment, headers=headers)
    file_format = str(get_attachment.split('.')[-1])
    if file_format == 'jpg':
        with open(f"{zero_string}gallery/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    elif file_format == 'ogg':
        with open(f"{zero_string}voices/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    elif file_format == 'jpeg':
        with open(f"{zero_string}gallery/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    elif file_format == 'png':
        with open(f"{zero_string}gallery/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    elif file_format == 'gif':
        with open(f"{zero_string}gallery/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    elif file_format == 'mp3':
        with open(f"{zero_string}voices/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)
    else:
        with open(f"{zero_string}other/id_{count}___{all_info}.{file_format}", 'wb') as file:
            file.write(r.content)

    time.sleep(0.5)
    t = time.localtime()
    now = time.strftime('%H:%M:%S', t)
    label.insert(tkinter.END, f'''[INFO: {now}] From "{all_info}" downloaded file with extension ".{file_format}"
and id "{count}!"''')

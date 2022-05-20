import os
import webbrowser
from threading import Thread
import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication
from pytube import YouTube
import sys
from design import *

progresso = 0


class Baixar(Thread):
    def __init__(self, link, botao, status, texto):
        self.link = link
        self.lbl_status = status
        self.btn = botao
        self.texto = texto

        super().__init__()

    def run(self):
        print(self.link)
        self.yt_download(urls=self.link)
        self.lbl_status.showMessage('')
        self.btn.setEnabled(True)
        self.btn.setText('Baixar Videos')
        os.startfile(os.getcwd())
        # limpa o plaintextedit
        self.texto.clear()

    def on_progress(self, stream, chunk, bytes_remaining):
        global progresso
        #print(f'inicio {progresso}')
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        liveprogress = int(bytes_downloaded / total_size * 100)
        if liveprogress > progresso:
            #print(progresso, liveprogress, sep='|')
            progresso = liveprogress
            self.lbl_status.showMessage(f'Baixando {progresso}%')
        else:
            progresso = 0

    def yt_download(self, urls):
        try:
            for url in urls:
                yt = YouTube(url)
                self.lbl_status.showMessage(f'\nBaixando agora : {yt.title}')
                yt.register_on_progress_callback(self.on_progress)

                tudo = yt.streams.all()
                yt.streams.get_highest_resolution().download()

        except Exception as e:
            print("Ocorreu um erro!   " + str(e))


class Novo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        btn = self.btn_downloader.clicked.connect(self.baixar)

        # muda o titulo do programa
        self.setWindowTitle('Youtube Downloader 2022')
        self.comboBox.setVisible(False)
        self.label_2.setVisible(False)

    def verifica_link(self):
        urls = self.edit_links.toPlainText()
        url = [y for y in (x.strip() for x in urls.splitlines()) if y]
        links = []
        for i in url:
            if 'youtube.com' in i:
                links.append(i)
        return links

    def baixar(self):
        try:
            self.btn_downloader.setText('Baixando os vídeos')
            self.btn_downloader.setEnabled(False)

            links = self.verifica_link()
            ytDown = Baixar(link=links, botao=self.btn_downloader,
                            status=self.statusbar, texto=self.edit_links)
            retorno = ytDown.start()

        except Exception as e:
            print(f'Ocorreu um erro {e}')


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    novo = Novo()
    novo.show()
    qt.exec_()

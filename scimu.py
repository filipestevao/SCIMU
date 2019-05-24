#!/usr/bin/env python3

"""
Programa de Captura de Foto para Laboratório de Metalografia da UNIFESP
Câmera Nikon S3100
UNIFESP São José dos Campos
Campus Parque Tecnológico
Autor: Filipe Estevão de Freitas
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import shlex
import time
import sys

class JanelaPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(JanelaPrincipal, self).__init__(parent)
        self.setWindowTitle('SCIMU')
        self.setWindowIcon(QIcon('figuras/icon.svg'))
        self.setGeometry(0, 0, 0, 525)
        # self.setFixedSize(500, 525)
        self.setFixedWidth(500)
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        # Funçoẽs
        self.barraMenu()
        self.criaTitulo()
        self.localSalvar()
        self.nomeArquivo()
        self.selecionaAumento()
        self.botaoCapturar()
        self.criaProgressBar()


    def barraMenu(self):
        # Ação detectarCam do menu 'Arquivo'
        detectarCam = QAction(QIcon('figuras/find.svg'), 'Detectar câmera', self)
        detectarCam.setShortcut('Ctrl+D')
        detectarCam.setStatusTip('Detecta se a câmera está conectada.')
        detectarCam.triggered.connect(self.detectaCamera)
        # Ação sair do menu 'Arquivo'
        sair = QAction(QIcon('figuras/exit.svg'), 'Sair', self)
        sair.setShortcut('Ctrl+Q')
        sair.setStatusTip('Sair do aplicativo.')
        sair.triggered.connect(self.fecharApp)
        # Ação limparSD do menu 'Configuração'
        limparSD = QAction(QIcon('figuras/trash.svg'),'Limpar cartão SD', self)
        limparSD.setShortcut('Ctrl+R')
        limparSD.setStatusTip('Remover todas as fotos do cartão SD.')
        limparSD.triggered.connect(self.removeTudo)
        # Ação ajuda do menu 'Ajuda'
        ajuda = QAction('Ajuda', self)
        ajuda.setShortcut('F1')
        ajuda.setStatusTip('Manual do aplicativo.')
        # ajuda.triggered.connect()
        # Ação sobreApp do menu 'Ajuda'
        sobreApp = QAction(QIcon('figuras/about.svg'),'Sobre o SCIMU', self)
        sobreApp.setStatusTip('Informações sobre o aplicativo.')
        sobreApp.triggered.connect(self.mensSobreApp)
        sobreQt = QAction(QIcon('figuras/Qt.svg'), 'Sobre o Qt', self)
        sobreQt.setStatusTip('Informações sobre a ferramenta Qt.')
        sobreQt.triggered.connect(self.mensSobreQt)
        self.statusBar()
        # Menu principal
        mainMenu = self.menuBar()
        # Menu Arquivo
        fileMenu = mainMenu.addMenu('&Arquivo')
        fileMenu.addAction(detectarCam)
        fileMenu.addAction(limparSD)
        fileMenu.addSeparator()
        fileMenu.addAction(sair)
        # Menu Ajuda
        helpMenu = mainMenu.addMenu('&Sobre')
        # helpMenu.addAction(ajuda)
        helpMenu.addAction(sobreApp)
        helpMenu.addAction(sobreQt)


    def criaTitulo(self):
        self.titulo = QLabel(self)
        self.titulo.setText('Software de Captura de Imagens\nLaboratório de Metalografia - UNIFESP')
        fonte = self.titulo.font()
        fonte.setPointSize(14)
        self.titulo.setFont(fonte)
        self.titulo.setAlignment(Qt.AlignHCenter)
        self.titulo.resize(self.titulo.minimumSizeHint())
        self.titulo.move(self.geometry().width()/2 - self.titulo.size().width()/2, 30)


    def localSalvar(self):
        # Cria grupo
        self.grupoSalvar = QGroupBox(self)
        # Cria widgets
        self.botaoCaminho = QPushButton(QIcon('figuras/folder.svg'), ' Selecionar pasta', self)
        self.botaoCaminho.clicked.connect(self.selecionaPasta)
        labelSalvar = QLabel('Local onde serão salvas as imagens:')
        labelSalvar.setAlignment(Qt.AlignHCenter)
        # Cria layout
        layout = QVBoxLayout()
        layout.addWidget(labelSalvar)
        layout.addWidget(self.botaoCaminho)
        self.grupoSalvar.setLayout(layout)
        self.grupoSalvar.resize(self.geometry().width(), self.grupoSalvar.minimumSizeHint().height())
        y = 20 + self.titulo.size().height()
        self.grupoSalvar.move(0, y)
        # self.grupoSalvar.setStyleSheet("QGroupBox {background-color: #EFF0F1; border: 0px}")


    def nomeArquivo(self):
        # Cria grupo
        self.grupoNome = QGroupBox(self)
        # Cria widgets
        labelArquivo = QLabel('Nome da imagem:')
        self.entryArquivo = QLineEdit()
        labelJpg = QLabel('.jpg')
        # Cria layout
        layout = QHBoxLayout()
        layout.addWidget(labelArquivo)
        layout.addWidget(self.entryArquivo)
        layout.addWidget(labelJpg)
        self.grupoNome.setLayout(layout)
        self.grupoNome.resize(self.geometry().width(), self.grupoNome.minimumSizeHint().height())
        y = +10 + self.titulo.size().height() + self.grupoSalvar.size().height()
        self.grupoNome.move(0,y)


    def selecionaAumento(self):
        # Cria grupo
        self.grupoAumento = QGroupBox(self)
        # Cria widgets
        labelAumento = QLabel('Selecionar o aumento:')
        self.radioButton1 = QRadioButton('Nenhum')
        self.radioButton2 = QRadioButton('100x')
        self.radioButton3 = QRadioButton('200x')
        self.radioButton4 = QRadioButton('500x')
        self.radioButton5 = QRadioButton('1000x')
        self.radioButton1.setChecked(True)
        # Cria layout
        layout = QVBoxLayout()
        layout.addWidget(labelAumento)
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addWidget(self.radioButton3)
        layout.addWidget(self.radioButton4)
        layout.addWidget(self.radioButton5)
        layout.addStretch(1)
        self.grupoAumento.setLayout(layout)
        self.grupoAumento.resize(self.grupoAumento.minimumSizeHint())
        y = self.titulo.size().height() + self.grupoSalvar.size().height() + self.grupoNome.size().height()
        self.grupoAumento.move(self.geometry().width()/2 - self.grupoAumento.minimumSizeHint().width()/2, y)


    def botaoCapturar(self):
        self.btnCapturar = QPushButton('Capturar foto', self)
        self.btnCapturar.clicked.connect(self.verificaErro)
        self.btnCapturar.setDefault(True)
        self.btnCapturar.resize(120, 30)
        y =  15+self.titulo.size().height() + self.grupoSalvar.size().height() + self.grupoNome.size().height() + self.grupoAumento.size().height()
        self.btnCapturar.move(self.geometry().width()/2 - self.btnCapturar.size().width()/2, y)
        font = QFont()
        font.setBold(True)
        self.btnCapturar.setFont(font)
        # Para apenas avançar a barra de progresso: descomentar linhas e comentar 'clicked' acima
        # self.btnCapturar.clicked.connect(self.advanceProgressBar)
        # self.last_call = 0


    def criaProgressBar(self):
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        self.progressBar.resize(self.geometry().width() - 20, 30)
        y = 60 + self.titulo.size().height() + self.grupoSalvar.size().height() + self.grupoNome.size().height() + self.grupoAumento.size().height()
        self.progressBar.move(10, y)


    def detectaCamera(self):
        cmd = 'gphoto2 --auto-detect'
        saida = subprocess.getoutput(cmd).splitlines()
        try:
            QMessageBox.information(self, 'Câmera', saida[2].split('usb')[0])
        except IndexError:
            self.erroSemCamera()


    def erroSemCamera(self):
        return QMessageBox.warning(self, 'Erro', 'Nenhuma câmera localizada.')


    def verificaErro(self):
        try:
            # Detecta se cãmera foi conectada
            cmd = 'gphoto2 --auto-detect'
            saida = subprocess.getoutput(cmd).splitlines()
            saida[2].split('usb')[0]
        except IndexError:
            self.erroSemCamera()
        else:
            try:
                # Detecta se pasta foi selecionada
                isinstance(self.folder, str)
                if self.folder == '':
                    raise AttributeError
            except (AttributeError, NameError):
                QMessageBox.warning(self, 'Erro', 'Selecione uma pasta.')
            else:
                # Obtem o nome do arquivo e verifica se está em branco
                self.arquivo = self.entryArquivo.displayText().replace(' ', '') + '.jpg'
                if self.arquivo == '.jpg':
                    QMessageBox.warning(self, 'Erro', 'Digite o nome da imagem.')
                else:
                    # Verifica se o arquivo já existe na pasta
                    localizaImgExiste = 'ls %s' % self.folder
                    if self.arquivo in subprocess.getoutput(localizaImgExiste):
                        QMessageBox.warning(self, 'Erro', 'A imagem "%s" já existe na pasta "%s".' % (self.arquivo, self.folder))
                    else:
                        # Verifica se existe processo do gphoto2 e mata
                        if 'gphoto2' in subprocess.getoutput('ps aux | grep gphoto'):
                            subprocess.run(shlex.split('pkill -f gphoto2'))
                            self.tiraFoto()
                        else:
                            self.tiraFoto()


    def tiraFoto(self):
        # Desativa widgets
        self.grupoSalvar.setDisabled(True)
        self.grupoNome.setDisabled(True)
        self.grupoAumento.setDisabled(True)
        self.btnCapturar.setDisabled(True)
        # Avança a barra de progresso
        for i in range(1,11):
            self.progressBar.setValue(i)
            time.sleep(0.02)
        # Tira a foto
        cmd1 = 'gphoto2 --trigger-capture'
        subprocess.run(shlex.split(cmd1))
        # Avança a barra de progresso e espera 10 segundos
        for i in range(11,61):
            self.progressBar.setValue(i)
            time.sleep(0.2)
        # time.sleep(10) # Espera 10 segundos
        cmd2 = 'gphoto2 --list-files'
        saida_cmd2 = subprocess.getoutput(cmd2).splitlines()
        ultima_linha_cmd2 = saida_cmd2[len(saida_cmd2)-1].split() # lista
        # Avança a barra de progresso
        for i in range(61,76):
            self.progressBar.setValue(i)
            time.sleep(0.02)
        # Salva a imagem
        self.arquivo = self.folder + '/' + self.arquivo
        cmd3 = 'gphoto2 --get-file=' + ultima_linha_cmd2[0].strip('#') + ' --filename=' + self.arquivo
        subprocess.run(shlex.split(cmd3))
        # Avança a barra de progresso
        for i in range(76,91):
            self.progressBar.setValue(i)
            time.sleep(0.02)
        # Corta imagem
        corta_foto = 'convert %s -crop 2300x2080+1045+760 %s' % (self.arquivo, self.arquivo)
        subprocess.run(shlex.split(corta_foto))
        # Verifica qual escala foi selecionada
        verificaRadioBtn = (self.radioButton2.isChecked(), self.radioButton3.isChecked(), self.radioButton4.isChecked(), self.radioButton5.isChecked())
        if verificaRadioBtn[0]: # 100x
            escala = 'composite -geometry +1500+1858 escala/100x.png %s %s' % (self.arquivo, self.arquivo)
        elif verificaRadioBtn[1]: # 200x
            escala = 'composite -geometry +1490+1864 escala/200x.png %s %s' % (self.arquivo, self.arquivo)
        elif verificaRadioBtn[2]: # 500x
            escala = 'composite -geometry +1490+1864 escala/500x.png %s %s' % (self.arquivo, self.arquivo)
        elif verificaRadioBtn[3]: # 1000x
            escala = 'composite -geometry +1490+1864 escala/1000x.png %s %s' % (self.arquivo, self.arquivo)
        # Coloca escala
        if any(verificaRadioBtn):
            subprocess.run(shlex.split(escala))
        # Avança a barra de progresso
        for i in range(91,101):
            self.progressBar.setValue(i)
            time.sleep(0.02)
        time.sleep(0.5)
        self.progressBar.setValue(0)
        # Ativa widgets
        self.grupoSalvar.setDisabled(False)
        self.grupoNome.setDisabled(False)
        self.grupoAumento.setDisabled(False)
        self.btnCapturar.setDisabled(False)


    def removeTudo(self):
        escolha = QMessageBox.question(self, 'Apagar', "Tem certeza que deseja apagar\n    todas as fotos da câmera?",
                                            QMessageBox.Yes | QMessageBox.No)
        remove = 'gphoto2 -r "/store_00010001/DCIM/100NIKON"'
        # Verifica se existe processo no gphoto2 e mata
        if 'gphoto2' in subprocess.getoutput('ps aux | grep gphoto'):
            subprocess.run(shlex.split('pkill -f gphoto2'))
        # Verifica se câmera está conectada
        if escolha == QMessageBox.Yes:
            if 'Erro' in subprocess.getoutput(remove):
                self.erroSemCamera()
            else:
                # Remove as fotos
                subprocess.run(shlex.split(remove))
                QMessageBox.information(self, 'Apagar', 'Todas as fotos foram apagadas!')


    def fecharApp(self):
        choice = QMessageBox.question(self, 'Sair', "Tem certeza que deseja sair?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()


    def selecionaPasta(self):
        self.folder = str(QFileDialog.getExistingDirectory(self))
        self.botaoCaminho.setText(' ' + self.folder)


    def mensSobreQt(self):
        QMessageBox.aboutQt(self, 'Sobre o Qt')


    def mensSobreApp(self):
        texto = "<p align='center'><b>SCIMU</b><br><b>S</b>oftware de <b>C</b>aptura de <b>I</b>magens<br>"
        texto += "Laboratório de <b>M</b>etalografia da <b>U</b>NIFESP</par>"
        texto += "<p align='center'>Autor: <b>Filipe Estevão de Freitas</b><br> "
        texto += "(<a href='mailto:filipe.estevao@gmail.com'>filipe.estevao@gmail.com</a>)</par>"
        texto += "<p align='justify'>Esse aplicativo foi desenvolvido para Laboratório de Metalografia "
        texto += "da UNIFESP São José dos Campos (Campus Parque Tecnológico) em março/2019 "
        texto += "com o objetivo de facilitar a captura de imagens do microscópio óptico "
        texto += "utilizando uma câmera digital Nikon S3100.</par>"
        texto += "<p align='justify'>O aplicativo é um <i>front-end</i> escrito em Python3 utilizando a interface gráfica PyQt5 "
        texto += "(ver <b>Sobre o Qt</b> no menu Sobre) para comunicação entre os programas gphoto2 "
        texto += "(para o controle da máquina digital) e ImageMagick (para processamento da imagem). "
        texto += "Todos os programas utilizados são gratuitos.</par><br><br>"
        texto += "Python - <a href='https://www.python.org/'>www.python.org</a><br>"
        texto += "gphoto2 - <a href='http://www.gphoto.org/'>www.gphoto.org</a><br>"
        texto += "ImageMagick - <a href='https://www.imagemagick.org/'>www.imagemagick.org</a><br>"
        QMessageBox.about(self, 'Sobre o aplicativo', texto)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    root = JanelaPrincipal()
    root.show()
    sys.exit(app.exec_())

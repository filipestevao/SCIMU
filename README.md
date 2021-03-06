# SCIMU

Software de Captura de Imagens - Laboratório de Metalografia da UNIFESP

## Descrição

Programa desenvolvido para o Laboratório de Metalografia da UNIFESP (Campus São José dos Campos) com o objetivo de faciliar a captura de fotos utilizando uma câmera Nikon S3100.

## Captura de tela

![Screenshot1](./screenshot-scimu.jpg)

## Dependências

* [Python3](https://www.python.org/)
* [PyQt5](https://pypi.org/project/PyQt5/)
* [gphoto2](http://gphoto.org/)
* [ImageMagick](https://imagemagick.org/)

### Instalação das dependências

Para Ubuntu e derivados:
```
sudo apt install gphoto2 imagemagick python3-pyqt5
```

Para o Fedora:
```
sudo dnf install gphoto2 ImageMagick
pip3 install --user pyqt5
```

## Instalação do SCIMU

Baixar e executar o arquivo `scimu.py`. Segue os comandos:

```
git clone https://github.com/filipestevao/SCIMU.git
cd SCIMU
chmod +x scimu.py
./scimu.py
```

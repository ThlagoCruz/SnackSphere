@echo off
color 1
REM Instalar Python
echo Instalando Python...
curl -O https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe
start /wait python-3.10.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
echo Python instalado com sucesso.

REM Instalar pip se não estiver disponível
python -m ensurepip

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências
echo Instalando dependências do projeto...
pip install tkinter pandas numpy colorama tabulate smtplib

echo Todas as dependências foram instaladas com sucesso!
pause

#!/usr/bin/env bash

if ! command -v python3 $> /dev/null
then
  echo "Error: the command 'python3' does not exist (is python installed?)"
  exit
fi

if ! command -v pip $> /dev/null
then
  echo "Error: the command 'pip' does not exist (is pip installed?)"
  exit
fi

if ! command -v pyinstaller $> /dev/null
then
  echo "Error: the command 'pyinstaller' does not exist (can be installed with 'sudo pip install pyinstaller')"
  exit
fi

if ! command -v virtualenv $> /dev/null
then
  echo "Error: the command 'virtualenv' does not exist (can be installed with 'sudo apt install python3-virtualenv')"
  exit
fi

echo "Info: Creating virtualenv"
virtualenv venv

echo "Info: Activating virtualenv"
source ./venv/bin/activate

echo "Info: Installing dependencies from ../requirements.txt"
pip install -r ../requirements.txt

echo "Info: Running PyInstaller"
pyinstaller --noconfirm main-onefile.spec

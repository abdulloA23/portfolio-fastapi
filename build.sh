#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка системных зависимостей
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng

# Установка Python зависимостей
pip install --upgrade pip
pip install -r requirements.txt
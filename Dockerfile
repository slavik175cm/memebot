FROM python

RUN apt update && apt-get install -y myspell-ru git

RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN apt-get install -y libenchant1c2a
RUN apt-get install -y tesseract-ocr libtesseract-dev

RUN wget https://github.com/tesseract-ocr/tessdata/raw/master/rus.traineddata && mv rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata

WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip
RUN cd /app && pip3 install -r requirements.txt

CMD ["/bin/bash", "-c", "python3 main.py"]
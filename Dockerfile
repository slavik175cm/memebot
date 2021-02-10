FROM python

RUN apt update && apt-get install myspell-ru git

RUN wget https://github.com/tesseract-ocr/tessdata/raw/master/rus.traineddata && mv rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata

RUN git clone https://github.com/slavik175cm/memebot && cd memebot && pip install -r requirements.txt

CMD ["python main.py"]
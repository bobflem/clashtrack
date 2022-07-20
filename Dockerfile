FROM python:3

LABEL org.opencontainers.image.source "https://github.com/bobflem/clashtrack"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ClashTrack.py" ]
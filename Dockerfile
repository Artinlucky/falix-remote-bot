FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    xvfb ca-certificates --no-install-recommends

# Install Google Chrome v114
RUN mkdir -p /opt/chrome && \
    wget -O /tmp/chrome.zip https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome.zip -d /opt/chrome && \
    ln -s /opt/chrome/chrome-linux64/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome.zip

# Install ChromeDriver v114
RUN mkdir -p /opt/chromedriver && \
    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /opt/chromedriver && \
    mv /opt/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip

ENV DISPLAY=:99

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
CMD ["./start.sh"]

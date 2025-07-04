FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    xvfb ca-certificates --no-install-recommends

# Install Google Chrome v114 and matching ChromeDriver (guaranteed compatible)
RUN mkdir -p /opt/chrome && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip -d /opt/chrome && \
    rm chrome-linux64.zip && \
    ln -s /opt/chrome/chrome-linux64/chrome /usr/bin/google-chrome

RUN mkdir -p /opt/chromedriver && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip -d /opt/chromedriver && \
    rm chromedriver-linux64.zip && \
    mv /opt/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

ENV DISPLAY=:99

# Setup app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh
CMD ["./start.sh"]

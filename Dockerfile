FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    xvfb ca-certificates --no-install-recommends

# Install Chrome + ChromeDriver from single bundled zip
RUN mkdir -p /opt/chrome && \
    wget -O /tmp/chrome-bundle.zip https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome-bundle.zip -d /opt/chrome && \
    ln -s /opt/chrome/chrome-linux64/chrome /usr/bin/google-chrome && \
    cp /opt/chrome/chrome-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chrome-bundle.zip

ENV DISPLAY=:99

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
CMD ["./start.sh"]

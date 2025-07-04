FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcb-dri3-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    xvfb ca-certificates --no-install-recommends

# Install latest Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-key.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver matching Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.' | head -1) && \
    CHROMEDRIVER_URL=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json \
        | grep -A 6 "\"version\": \"$CHROME_VERSION" | grep "chromedriver_linux64" | grep "url" | cut -d '"' -f 4) && \
    wget -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

ENV DISPLAY=:99

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh
CMD ["./start.sh"]

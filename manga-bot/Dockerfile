FROM python:3.11.0-slim

# Cài Chromium và các dependencies hệ thống
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates \
    chromium chromium-driver \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 libxss1 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường cho undetected_chromedriver biết Chrome
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_BIN=/usr/bin/chromium

# Tạo thư mục làm việc
WORKDIR /app

# Cài dependencies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở cổng Flask app
EXPOSE 3001

# Chạy Flask bằng Gunicorn cho production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3001", "main:app"]

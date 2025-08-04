# Cài Tor

1. Cập nhật hệ thống:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Cài đặt Tor:
   ```bash
   sudo apt install tor -y
   ```

- Sau khi cài, Tor sẽ tự chạy và mở SOCKS5 proxy ở:
  ```
  127.0.0.1:9050
  ```

3. Kiểm tra trạng thái Tor:

   ```bash
   systemctl status tor
   ```

   Nếu Tor đang chạy, bạn sẽ thấy thông báo "active (running)".

4. Mở cấu hình Tor
   ```bash
   sudo nano /etc/tor/torrc
   ```
   - Đảm bảo dòng `SocksPort 9050` không bị comment (bỏ dấu `#` ở đầu dòng).
5. Bật Control Port để quản lý Tor:
   - Thêm dòng sau vào cuối file `torrc`:
     ```
     ControlPort 9051
     HashedControlPassword <HASH>
     CookieAuthentication 0
     ```
   - Lưu và thoát (Ctrl + O, Enter, Ctrl + X).
   - Lấy hash mật khẩu:
     ```bash
     tor --hash-password <YOUR_PASSWORD>
     ```
   - Thay `<HASH>` bằng giá trị hash bạn nhận được.
6. Khởi động lại Tor để áp dụng cấu hình mới:
   ```bash
   sudo systemctl restart tor
   ```
7. Kiểm tra IP của Tor:
   - Sử dụng lệnh sau để kiểm tra IP:
     ```bash
     curl --socks5 127.0.0.1:9050 http://ipinfo.io/ip
     ```

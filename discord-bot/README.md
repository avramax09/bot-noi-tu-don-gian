# 🎮 Bot Nối Từ Discord

Bot Discord chơi game nối từ tiếng Việt — người chơi nối tiếp nhau bằng cách dùng từ cuối của từ trước làm từ đầu của từ mới.

---

## 📋 Tính năng

- Bắt đầu / dừng game bằng lệnh
- Kiểm tra từ đã dùng, không cho dùng lại
- Không cho cùng một người chơi 2 lượt liên tiếp
- Tính điểm và xem bảng xếp hạng top 10
- Lưu điểm vĩnh viễn vào file JSON

---

## 🗂️ Cấu trúc hệ thống

```
discord-bot/
├── noitu.py              # File chính — khởi động bot
├── config.py             # Đọc cấu hình từ biến môi trường
├── requirements.txt      # Danh sách thư viện Python cần thiết
├── .gitignore            # Loại trừ file nhạy cảm và cache
├── cogs/
│   └── commands.py       # Xử lý lệnh !start, !stop, !rank và logic nối từ
├── utils/
│   ├── game.py           # Quản lý trạng thái game (từ hiện tại, người chơi...)
│   ├── text.py           # Chuẩn hóa chuỗi, lấy từ đầu/cuối
│   └── database.py       # Đọc/ghi điểm vào file JSON
└── data/
    └── scores.json       # Lưu điểm người chơi (tự tạo khi chạy)
```

---

## ⚙️ Yêu cầu hệ thống

- Python **3.10+**
- Tài khoản [Discord Developer Portal](https://discord.com/developers/applications)
- Bot Token từ Discord

---

## 🚀 Hướng dẫn cài đặt

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/discord-bot
```

### 2. Cài thư viện

```bash
pip install -r requirements.txt
```

### 3. Tạo file `.env`

Tạo file `.env` trong thư mục `discord-bot/`:

```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
TIMEOUT_SECONDS=30
```

> **Lưu ý:** Không bao giờ commit file `.env` lên GitHub. File `.gitignore` đã loại trừ nó.

### 4. Bật Message Content Intent

Vào [Discord Developer Portal](https://discord.com/developers/applications):

1. Chọn ứng dụng bot của bạn
2. Vào tab **Bot**
3. Bật **Message Content Intent** trong phần *Privileged Gateway Intents*
4. Nhấn **Save Changes**

### 5. Mời bot vào server

Trong Developer Portal → **OAuth2** → **URL Generator**:

- Tích **bot** trong Scopes
- Tích quyền: `Send Messages`, `Read Message History`, `Add Reactions`
- Copy URL và mở trên trình duyệt để mời bot

### 6. Chạy bot

```bash
python noitu.py
```

---

## 🕹️ Lệnh sử dụng

| Lệnh     | Mô tả                          |
|----------|-------------------------------|
| `!start` | Bắt đầu game nối từ           |
| `!stop`  | Dừng game                     |
| `!rank`  | Xem bảng xếp hạng top 10      |

---

## 📜 Luật chơi

1. Bot đưa ra từ đầu tiên
2. Người chơi tiếp theo gõ **cụm 2 từ trở lên**, bắt đầu bằng **từ cuối** của từ trước
3. Không được dùng lại từ đã xuất hiện
4. Không được chơi 2 lượt liên tiếp
5. Nối từ đúng → được **1 điểm**

**Ví dụ:**
```
Bot:      học sinh
Người A:  sinh viên
Người B:  viên chức
Người A:  chức năng
...
```

---

## 🛠️ Biến môi trường

| Biến               | Mô tả                        | Mặc định |
|--------------------|------------------------------|----------|
| `DISCORD_TOKEN`    | Token bot Discord (bắt buộc) | —        |
| `PREFIX`           | Prefix lệnh                  | `!`      |
| `TIMEOUT_SECONDS`  | Thời gian chờ (chưa dùng)   | `30`     |

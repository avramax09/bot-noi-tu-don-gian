# 🎮 Bot Nối Từ Discord

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
</p>

> Bot Discord tổ chức game **nối từ tiếng Việt** — người chơi lần lượt nối tiếp nhau bằng cách dùng từ cuối của cụm từ trước làm từ đầu của cụm từ mới. Ai nối sai hoặc dùng từ đã xuất hiện sẽ bị loại lượt. Điểm được lưu lại và xếp hạng theo thời gian thực.

---

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Luật chơi](#-luật-chơi)
- [Cấu trúc hệ thống](#-cấu-trúc-hệ-thống)
- [Luồng hoạt động](#-luồng-hoạt-động)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [Biến môi trường](#-biến-môi-trường)
- [Lệnh sử dụng](#-lệnh-sử-dụng)
- [Bảo mật](#-bảo-mật)
- [Đóng góp](#-đóng-góp)
- [License](#-license)

---

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 🎯 Game nối từ | Tự động kiểm tra và xác nhận từ hợp lệ |
| 🚫 Chống gian lận | Không cho dùng lại từ đã xuất hiện trong ván |
| 👤 Chống lượt liên tiếp | Một người không được chơi 2 lượt liên tiếp |
| 🏆 Bảng xếp hạng | Top 10 người chơi nhiều điểm nhất |
| 💾 Lưu điểm | Điểm được lưu vĩnh viễn vào file JSON |
| ⚡ Phản hồi nhanh | Dùng reaction ✅ để xác nhận từ hợp lệ |
| 🔧 Dễ cấu hình | Tùy chỉnh prefix và timeout qua file `.env` |

---

## 📜 Luật chơi

1. Dùng lệnh `!start` để bắt đầu — bot sẽ đưa ra từ đầu tiên
2. Người chơi tiếp theo gõ **cụm gồm 2 từ trở lên**, phải bắt đầu bằng **từ cuối** của cụm từ trước đó
3. Không được dùng lại từ đã xuất hiện trong ván
4. Không được chơi 2 lượt liên tiếp (phải chờ người khác chơi)
5. Nối từ đúng → bot thả ✅ và cộng **1 điểm**
6. Nối từ sai → bot thông báo lỗi, lượt tiếp tục với từ cũ

**Ví dụ một ván chơi:**

```
🤖 Bot:      học sinh
👤 Người A:  sinh viên       ✅ (+1 điểm)
👤 Người B:  viên chức       ✅ (+1 điểm)
👤 Người A:  chức năng       ✅ (+1 điểm)
👤 Người C:  năng lượng      ✅ (+1 điểm)
👤 Người B:  lượng tử        ✅ (+1 điểm)
...
```

---

## 🗂️ Cấu trúc hệ thống

```
discord-bot/
│
├── noitu.py                  # Entrypoint — khởi tạo bot và load cogs
├── config.py                 # Đọc cấu hình từ biến môi trường (.env)
├── requirements.txt          # Danh sách thư viện Python cần thiết
├── .gitignore                # Loại trừ file nhạy cảm và __pycache__
│
├── cogs/                     # Discord Cogs (nhóm lệnh và listener)
│   ├── __init__.py
│   └── commands.py           # Lệnh !start, !stop, !rank + listener on_message
│
├── utils/                    # Các module tiện ích
│   ├── __init__.py
│   ├── game.py               # GameManager — lưu trạng thái ván đang chơi
│   ├── text.py               # normalize(), get_first_word(), get_last_word()
│   └── database.py           # Đọc/ghi điểm từ data/scores.json
│
└── data/
    └── scores.json           # Lưu điểm người chơi (tự tạo nếu chưa có)
```

### Vai trò từng file

| File | Vai trò |
|------|---------|
| `noitu.py` | Khởi động bot, đăng ký intents, load extension `cogs.commands` |
| `config.py` | Đọc `DISCORD_TOKEN`, `PREFIX`, `TIMEOUT_SECONDS` từ môi trường |
| `cogs/commands.py` | Xử lý toàn bộ lệnh và logic kiểm tra từ nối |
| `utils/game.py` | Class `GameManager` — singleton lưu trạng thái game trong RAM |
| `utils/text.py` | Chuẩn hóa chuỗi (lowercase, strip), tách từ đầu/cuối |
| `utils/database.py` | Load/save file `scores.json`, cộng điểm, trả về top |
| `data/scores.json` | Dữ liệu điểm dạng `{"user_id": score, ...}` |

---

## 🔄 Luồng hoạt động

```
Người dùng gõ tin nhắn
        │
        ▼
  on_message() nhận tin
        │
        ├─ Bot? → Bỏ qua
        ├─ Game chưa bắt đầu? → Bỏ qua
        ├─ Cụm từ < 2 từ? → Bỏ qua
        │
        ▼
  Kiểm tra người chơi
        │
        ├─ Cùng người lượt trước? → ❌ Thông báo lỗi
        │
        ▼
  Kiểm tra từ đã dùng
        │
        ├─ Đã dùng rồi? → ❌ Thông báo lỗi
        │
        ▼
  Kiểm tra nối từ
        │
        ├─ Từ đầu ≠ từ cuối của từ trước? → ❌ Thông báo lỗi
        │
        ▼
  Hợp lệ → Lưu từ mới, cộng điểm, react ✅
```

---

## ⚙️ Yêu cầu hệ thống

- **Python** 3.10 trở lên
- **pip** (đi kèm Python)
- Tài khoản [Discord Developer Portal](https://discord.com/developers/applications)
- Bot Token từ Discord
- **Message Content Intent** được bật trong Developer Portal

---

## 🚀 Hướng dẫn cài đặt

### Bước 1 — Tạo bot trên Discord Developer Portal

1. Vào [discord.com/developers/applications](https://discord.com/developers/applications)
2. Nhấn **New Application** → đặt tên → **Create**
3. Vào tab **Bot** → nhấn **Add Bot**
4. Kéo xuống **Privileged Gateway Intents** → bật **Message Content Intent**
5. Nhấn **Save Changes**
6. Nhấn **Reset Token** → copy token (sẽ dùng ở bước 4)

### Bước 2 — Clone repository

```bash
git clone https://github.com/avramax09/bot-noi-tu-don-gian.git
cd bot-noi-tu-don-gian/discord-bot
```

### Bước 3 — Cài thư viện

```bash
pip install -r requirements.txt
```

### Bước 4 — Tạo file `.env`

Tạo file `.env` trong thư mục `discord-bot/`:

```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
TIMEOUT_SECONDS=30
```

> ⚠️ **Quan trọng:** Không bao giờ commit file `.env` lên GitHub. File `.gitignore` đã loại trừ nó sẵn.

### Bước 5 — Mời bot vào server

1. Trong Developer Portal → tab **OAuth2** → **URL Generator**
2. Tích **bot** trong mục *Scopes*
3. Tích các quyền: `Send Messages`, `Read Message History`, `Add Reactions`
4. Copy URL được tạo ra → mở trên trình duyệt → chọn server → **Authorize**

### Bước 6 — Chạy bot

```bash
python noitu.py
```

Nếu thành công, terminal sẽ hiển thị:
```
Đăng nhập: <tên bot>#XXXX
```

---

## 🛠️ Biến môi trường

| Biến | Bắt buộc | Mô tả | Mặc định |
|------|----------|-------|----------|
| `DISCORD_TOKEN` | ✅ | Token xác thực bot Discord | — |
| `PREFIX` | ❌ | Ký tự prefix cho lệnh | `!` |
| `TIMEOUT_SECONDS` | ❌ | Thời gian chờ (dùng cho tính năng mở rộng sau) | `30` |

---

## 🕹️ Lệnh sử dụng

| Lệnh | Quyền | Mô tả |
|------|-------|-------|
| `!start` | Mọi người | Bắt đầu một ván nối từ mới |
| `!stop` | Mọi người | Dừng ván đang chơi |
| `!rank` | Mọi người | Hiển thị bảng xếp hạng top 10 |

---

## 🔐 Bảo mật

- **Không** lưu token vào code — luôn dùng biến môi trường
- File `.env` đã được thêm vào `.gitignore`
- Thư mục `data/` (chứa điểm) cũng không được commit lên git
- Nếu token bị lộ: vào Developer Portal → **Reset Token** ngay lập tức

---

## 🤝 Đóng góp

Pull request luôn được chào đón! Nếu muốn thêm tính năng:

1. Fork repo này
2. Tạo branch mới: `git checkout -b feat/ten-tinh-nang`
3. Commit thay đổi: `git commit -m "feat: mô tả tính năng"`
4. Push lên branch: `git push origin feat/ten-tinh-nang`
5. Mở Pull Request

**Một số ý tưởng mở rộng:**
- ⏱️ Giới hạn thời gian trả lời mỗi lượt
- 📊 Lệnh `!score @user` xem điểm một người cụ thể
- 🔄 Lệnh `!reset` reset điểm toàn bộ
- 🗄️ Chuyển lưu điểm sang database thay vì JSON
- 🌐 Dashboard web hiển thị leaderboard

---

## 📄 License

Dự án được phát hành dưới [MIT License](LICENSE).

---

<p align="center">Made with ❤️ for the Vietnamese Discord community</p>

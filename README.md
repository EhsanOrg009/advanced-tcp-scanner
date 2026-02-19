# 🚀 Advanced TCP Scanner

A powerful Python-based TCP scanner with multi-threading, banner grabbing, and TCP ping support.

---

## 📌 Features

- 🔍 Fast multi-threaded port scanning
- 📡 TCP Ping (latency measurement)
- 🧠 Banner grabbing (service detection)
- 🎯 Custom port ranges (e.g. 1-1000, 80,443)
- ⚙️ Adjustable timeout & threads
- 💾 Save scan results to file
- 🌐 Supports domain & IP targets

---

## ▶️ Usage

```pytohn
python main.py example.com -p 1-1000 -t 200 --timeout 1 --ping 3 -o result.txt
```

---

## 🧠 How It Works

- Uses socket.connect_ex() to test TCP connections
- Multi-threading speeds up port scanning using ThreadPoolExecutor
- Attempts to grab banners from open ports (if service responds)
- Calculates latency using TCP handshake for TCP Ping feature
- Supports both IP addresses and domain names

---

## ⚠️ Notes

- Some systems may block scanning or rate-limit requests
- Banner grabbing depends on service response
- Results may vary based on network conditions
- Use responsibly and only on authorized targets

---

## 🛠 Requirements

- Python 3.10+
- No external libraries required

---

## 📄 License
- This project is open-source and available under the MIT License.

---

## 📦 Installation

```bash
git clone https://github.com/EhsanOrg009/tcp-ping-tool.git
cd tcp-ping-tool

```

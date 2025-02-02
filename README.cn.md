# 🚀 Botix - 远程 Linux Shell

<div align="center">
    <img src="./src/logo.png" width="500" alt="Botix - Remote Linux Shell" />
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot-Enabled-blue?style=flat-square)
![License](https://img.shields.io/badge/License-Restricted-red?style=flat-square)

## 🌍 语言
[**🇰🇷 한국어**](README.md) | [**🇺🇸 English**](README.en.md) | [**🇨🇳 中文**](README.cn.md) | [**🇯🇵 日本語**](README.ja.md)

</div>

## 🛠 技术栈
- **语言:** Python 3.x 🐍
- **框架:** python-telegram-bot
- **依赖:**
  - `python-dotenv`
  - `urllib3`
- **操作系统:** Linux 🐧

## 📌 功能
- 🚀 通过 Telegram 远程执行 Linux Shell 命令
- 🔒 使用预定义的用户 ID 进行安全访问控制
- ⚡ 通过环境变量轻松配置

## 📥 安装方法
克隆存储库并安装所需的依赖项:
```sh
git clone https://github.com/yourusername/Botix.git
cd Botix
pip install -r requirements.txt
```

## ⚙️ 配置
创建 `.env` 文件并设置以下环境变量:
```sh
Bot_Token="YOUR_TELEGRAM_BOT_TOKEN"  # str
U_Number= Set_ALLOWED_User_Number,1,2,3...  # int
```

## 🚀 使用方法
运行 Bot:
```sh
python bot.py
```
在 Telegram 中发送以下命令以远程执行 Shell 命令:
```sh
/s [your_command]
```

## 📜 许可证
本项目受 **限制性许可** 保护。允许个人修改使用，但**严禁重新分发或商业用途**。

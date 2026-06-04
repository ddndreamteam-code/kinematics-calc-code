Markdown
# 🤖 Robot Kinematics Telegram Bot

A Python-based Telegram bot that solves the **Forward Kinematics** problem for a 2-DOF (Degree of Freedom) robotic arm manipulator. Created as part of my engineering portfolio for university admission.

## 📌 Features
* **Real-time Kinematics Calculation:** Computes $(X, Y)$ coordinates of the robot's end-effector based on links length and joints angles.
* **Robust Input Validation:** Built-in error handling via Python `try-except` blocks to manage invalid user inputs (e.g., text instead of numbers) without crashing the bot.
* **Secure Configuration:** Uses environment variables (`.env`) to isolate sensitive data like Telegram API tokens from the source code.

## 📐 Math & Logic Behind the Project
The bot solves the standard forward kinematics equations for a two-link planar manipulator, where the second joint angle $\beta$ is relative to the first link:

$$X = L_1 \cdot \cos(\alpha) + L_2 \cdot \cos(\alpha + \beta)$$
$$Y = L_1 \cdot \sin(\alpha) + L_2 \cdot \sin(\alpha + \beta)$$

*The Python `math` module is utilized to convert user input from degrees to radians before performing trigonometric operations.*

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **API Framework:** `pyTelegramBotAPI` (telebot)
* **Environment Management:** `python-dotenv`
* **Core Concepts:** Forward Kinematics, Trigonometry, Process Automation, State Handling

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ddndreamteam-code/robot-kinematics-bot.git](https://github.

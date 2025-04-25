<img src="https://1.bp.blogspot.com/-N-XwxleEyOo/WYQEtqUZGnI/AAAAAAAAwRI/Klh5vIblR_EzyXjHsm1zh5WP3hWZMaciACLcBGAs/s1600/SRM%2BLogo.png" height=70>

# AI-Based Stock Market Investment Advisor 📈🤖





## 📌 Overview

An AI-powered stock prediction system that forecasts **NSE stock prices** using **LSTM neural networks**. It features a **Tkinter GUI** for real-time visualizations, portfolio recommendations, and secure user management via **MySQL**.

> **Note**: This project was developed as part of the **Artificial Intelligence** subject project during the **4th semester** of the **Bachelor of Technology** program at **SRM Institute of Science and Technology**, under the guidance of the course curriculum.





## 📌 Table of Contents

1. [Key Features](#key-features)
2. [Installation Guide](#installation-guide)
3. [User Manual](#user-manual)
4. [System Architecture](#system-architecture)
5. [Technical Stack](#technical-stack)
6. [License](#license)
7. [Author](#author)





## 🚀 Key Features

- **Real-Time Data**: Fetches **NSE stock data** using the `yfinance` library (TCS.NS, RELIANCE.NS, INFY.NS, etc.).
- **AI Predictions**: Utilizes a **dual-layer LSTM model** for **10-day price forecasts** with RMSE of 2.34 and MAE of 1.89.
- **Portfolio Recommendations**: Performs **risk-return analysis** and provides **probability scoring** for stock recommendations.
- **Interactive Dashboard**:
  - Single stock prediction graphs.
  - Investment amount calculator.
  - Historical performance tracking.
- **Secure Authentication**: User management with **MySQL-backed accounts** and **prediction history** tracking.





## 🛠️ Installation Guide

### Prerequisites

- **Python**: 3.8+
- **MySQL Server**: 8.0+
- **RAM**: Minimum 4GB

### Features

- User authentication system.
- Single stock price prediction.
- Investment recommendations.
- Prediction history tracking.
- Interactive visualizations.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/1sanemax/stock-prediction-system.git
   cd stock-prediction-system
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL database**:
   ```bash
   mysql -u root -p < database_schema.sql
   ```

4. **Update database credentials** in `db.py`:
   ```python
   connection = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       database="stock_prediction"
   )
   ```

5. **Run the application**:
   ```bash
   python interface.py
   ```





## 🖥️ User Manual

### Login Screen

- **New users** can register with **email/password**.
- **Existing users** can log in to access the dashboard.

### Dashboard Features

1. **Single Stock Prediction**:
   - Select from 5 NSE stocks.
   - View a **10-day price forecast** with historical comparison.

2. **Portfolio Advisor**:
   - Enter an **investment amount** (₹1,000 - ₹1,00,000).
   - Set a **time horizon** (7-90 days).
   - Get **AI-ranked stock recommendations** based on risk-return analysis.

3. **Prediction History**:
   - Track all previous forecasts.
   - Filter by **date/stock/profitability**.





## 🏗️ System Architecture

### Frontend:
- **Tkinter** (GUI framework)
- **Matplotlib** (Visualization)

### Backend:
- **Python 3.8**
- **TensorFlow 2.13** (AI Model)

### Database:
- **MySQL 8.0** (for user management and prediction history)

### Data Sources:
- **yFinance API** (for fetching real-time stock data)





## 🛠️ Technical Stack

- **Frontend**: Tkinter, Matplotlib
- **Backend**: Python 3.8, TensorFlow 2.13
- **Database**: MySQL 8.0
- **Data Sources**: yFinance API





## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





## ✨ Author

- **[Aaditya Gupta RA2311003011388](https://github.com/1sanemax)**
- **[Yash Chauhan RA2311003011362](https://github.com/Yashchauhan-07)**


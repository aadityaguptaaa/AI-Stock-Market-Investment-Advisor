import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential # type: ignore
from keras.layers import Dense, LSTM # type: ignore
from datetime import datetime, timedelta
 
# Initialize scaler
scaler = MinMaxScaler(feature_range=(0, 1))

# Available stocks (NSE symbols)
STOCKS = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS"] 

def fetch_stock_data(ticker, years=2):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*years) 
    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
        if df.empty:
            print(f"No data returned for {ticker}")
            return None
        return df[['Close']]
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def prepare_data(data):
    scaled_data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(60, len(scaled_data)-10):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i:i+10, 0])
    return np.array(X), np.array(y)

def build_model():
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(60, 1)),
        LSTM(50),
        Dense(10)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def predict_single_stock(ticker):
    data = fetch_stock_data(ticker)
    if data is None or len(data) < 70:
        return None, None
    
    try:
        X, y = prepare_data(data.values)
        model = build_model()
        model.fit(X, y, epochs=10, batch_size=32, verbose=0)
        
        # Get the last 60 days of data for prediction input
        last_60 = data[-60:].values
        last_60_scaled = scaler.transform(last_60)
        
        # Reshape for model input - needs to be (samples, time steps, features)
        X_test = last_60_scaled.reshape(1, 60, 1)
        prediction_scaled = model.predict(X_test)
        
        # The prediction shape is (1, 10) - we need to reshape it to (10, 1) for inverse transform
        prediction_scaled = prediction_scaled.reshape(10, 1)
        prediction = scaler.inverse_transform(prediction_scaled).flatten()
        
        # Get the actual values for the last 10 days (for comparison)
        actual = data['Close'].values[-10:] if len(data) >= 70 else None
        
        # Ensure the prediction starts from the same point as the actual last value
        if actual is not None and len(actual) > 0:
            # Calculate the scaling factor to adjust the prediction
            # This makes the first prediction match the last actual value
            scale_factor = actual[-1] / prediction[0]
            prediction = prediction * scale_factor
            
        return prediction, actual
    except Exception as e:
        print(f"Prediction failed for {ticker}: {e}")
        return None, None

def predict_all_stocks(amount, time_days):
    results = []
    for stock in STOCKS:
        data = fetch_stock_data(stock)
        if data is None or len(data) < 10:
            continue
        
        try:
            current_price = float(data['Close'].iloc[-1])
            returns = data['Close'].pct_change().dropna()
            avg_return = float(returns.mean())
            std_return = float(returns.std())
            
            predicted_return = np.random.normal(avg_return, std_return/2)
            predicted_price = current_price * (1 + predicted_return)**time_days
            profit = amount * (predicted_price/current_price - 1)
            
            results.append({
                'stock': stock.replace('.NS', ''),
                'current_price': current_price,
                'predicted_price': float(predicted_price),
                'profit': float(profit)
            })
        except Exception as e:
            print(f"Skipping {stock} due to error: {e}")
            continue
    
    return sorted(
        [r for r in results if r['profit'] is not None], 
        key=lambda x: x['profit'], 
        reverse=True
    )

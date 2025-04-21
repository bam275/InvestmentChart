import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

 # ***Issue with charting when a specified company was non-existent at desired time frame***
        # Chart becomes adjusted to nearest date

def growth_chart(ticker, day, month, year, day2, month2, year2, interval):
  
  # Calculate returns
  # ticker = ["aapl", nvda]

  if interval == "Daily":
        time = "1d"
  elif interval == "Monthly":
        time = "1mo"
  elif interval == "Quarterly":
        time = "3mo"

  data = yf.download(ticker, interval=time, auto_adjust=True, start = year+"-"+month+"-"+day, end = year2+"-"+month2+"-"+day2)
  returns = data["Close"].pct_change().dropna()
  cum_returns = (1 + returns).cumprod()
  
  # Graph
  fig, ax = plt.subplots(figsize=(16,9))

  for i in ticker:
    plt.plot(cum_returns[i], label = i)

  ax.set_xlabel('Date', size = 20)
  ax.set_ylabel('Cumulative Value', size = 16)
  ax.set_title('Growth of $1 Investment', size = 16)
  ax.legend(loc = "upper left")
  
  return fig



def download(ticker, day, month, year, day2, month2, year2, interval):
      if interval == "Daily":
        time = "1d"
      elif interval == "Monthly":
        time = "1mo"
      elif interval == "Quarterly":
        time = "3mo"

      data = yf.download(ticker, interval=time, auto_adjust=True, start = year+"-"+month+"-"+day, end = year2+"-"+month2+"-"+day2)

      return data
import Williams_R as wr
import exponential_moving_average as ema
import WilliamsR_strategy as WR_strategy
import pandas as pd
import numpy as np
import project_utils as utils
import matplotlib.pyplot as plt

# arguments
period = 131   # exponential moving average period
ctrl_ticks = 0       # minimum amount of ticks a triggerred signal must pass before buying/selling
stop_loss = 10
take_profit = 10
bear_open = -20
bear_close = -80
bull_open = -50
bull_close = -20
init_budget = 10000  # initial user budget
weight = 15  # volume of item bought on trade
expenses = 0.01   # expenses on each trade

# load data from csv file
csv_data = utils.load_data('xauusd_m10_data1.csv', "%Y.%m.%d %H:%M:%S")
dates = pd.to_datetime(csv_data.index.values, format="%Y.%m.%d %H:%M:%S")

# apply williams %r indicator
wr_data = wr.williams_r(csv_data, 14)
wr_data = wr_data[['Close', '%R']]
wr_data['EMA'] = ema.exponential_moving_average(csv_data['Close'], period)

# opt_period, opt_bear_open, opt_bear_close, opt_bull_open, opt_bull_close = WR_strategy.optimize_strategy2(wr_data, dates, init_budget, weight, expenses)
# profits, bull_buys, bull_sales, bear_buys, bear_sales, stop_loss_trades, take_profit_trades = \
#     WR_strategy.wr_strategy(True, wr_data, dates, opt_period, ctrl_ticks, stop_loss, take_profit, opt_bear_open, opt_bear_close, opt_bull_open, opt_bull_close, init_budget, weight, expenses)
# print("Optimal period: ", opt_period, ", bear open: ", opt_bear_open, ", bear close: ", opt_bear_close, ", bull open: ", opt_bull_open, ", bull close: ", opt_bull_close)


profits, bull_buys, bull_sales, bear_buys, bear_sales, stop_loss_trades, take_profit_trades = \
    WR_strategy.wr_strategy(True, wr_data, dates, period, ctrl_ticks, stop_loss, take_profit,
                            bear_open, bear_close, bull_open, bull_close, init_budget, weight, expenses)

# create array of dates array length
x = np.arange(len(dates))

profit_fig, ax = plt.subplots(1, 1)
ax.plot(x, profits)
utils.equidate_ax(profit_fig, ax, dates, fmt="%dd. %H:%M")
profit_fig.show()
plt.close()

# create subplot figure variable
fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(25, 15))


# plot closing price data
ax1.plot(x, wr_data['Close'], 'r-')
ax1.set_xticks(np.arange(min(x), max(x) + 1, len(x) / 20))
ax1.grid(True)
ax1.set_title('EURUSD Close Price + 100 period EMA')
ax1.set_ylabel('Closing price')

# plot ema data on top of closing price
ax1.plot(np.arange(period, len(dates)), wr_data['EMA'].iloc[period:], 'b-')

# ax1.plot(x[bearish_engulfing_mask], wr_data['Close'][bearish_engulfing_mask], 'b*')
ax1.plot(x[bear_sales], wr_data['Close'][bear_sales], 'c*')
ax1.plot(x[bear_buys], wr_data['Close'][bear_buys], 'b*')
# ax1.plot(x[bullish_engulfing_mask], wr_data['Close'][bullish_engulfing_mask], 'y*')
ax1.plot(x[bull_buys], wr_data['Close'][bull_buys], 'r*')
ax1.plot(x[bull_sales], wr_data['Close'][bull_sales], 'g*')
ax1.plot(x[stop_loss_trades], wr_data['Close'][stop_loss_trades], 'm*')
ax1.plot(x[take_profit_trades], wr_data['Close'][take_profit_trades], 'k*')

# plot williams %r data
ax2.plot(x, wr_data['%R'], 'b-', linewidth=1)
ax2.set_xticks(np.arange(min(x), max(x) + 1, len(x) / 30))
ax2.grid(True)
ax2.set_title('Williams %R')
ax2.set_ylabel('%R')

# plot a horizontal line at the middle of the plot
ax2.axhline(y=-20, color='r', linestyle='--', linewidth=0.5)
ax2.axhline(y=-50, color='r', linestyle='-', linewidth=1)
ax2.axhline(y=-80, color='r', linestyle='--', linewidth=0.5)

# show x axis labels as dates
utils.equidate_ax(fig, ax2, dates, fmt="%dd. %H:%M")

# show the figure
fig.show()

# close the figure
plt.close()
import matplotlib.pyplot as plt
import pandas as pd
import mpl_finance as fplt
import accumulation_distribution_line as adl
import exponential_moving_average as ema
import project_utils as utils


def chaikin_oscillator(data):
    data_copy = data.copy()
    data_copy['ADL'] = adl.accumulation_distribution_line(data_copy)
    data_copy['3 day EMA of ADL'] = ema.exponential_moving_average(data_copy['ADL'], 3)
    data_copy['10 day EMA of ADL'] = ema.exponential_moving_average(data_copy['ADL'], 10)
    data_copy['CHO'] = data_copy['3 day EMA of ADL'] - data_copy['10 day EMA of ADL']
    return data_copy


def test_indicator(file_name, start_date, end_date, figure_title, candlestick_width):
    date_format = "%Y.%m.%d %H:%M:%S"
    csv_data = pd.read_csv(file_name)
    csv_data['Time'] = pd.to_datetime(csv_data['Time'], format=date_format)
    csv_data = csv_data.set_index('Time')
    csv_data = csv_data.iloc[::-1]

    print("Sample data:")
    print(csv_data.head(10))

    data_CHO = chaikin_oscillator(csv_data)

    print("")
    print(data_CHO.tail(20))

    ax1_data = data_CHO.drop(['Volume', 'ADL', '3 day EMA of ADL', '10 day EMA of ADL', 'CHO'], 1)
    ax1_data = ax1_data.loc[start_date:end_date]

    ax2_data = data_CHO.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'CHO'], 1)
    ax2_data = ax2_data.loc[start_date:end_date]

    ax3_data = data_CHO['CHO'].loc[start_date:end_date]

    # fig1.suptitle('Hourly OHLC data') <- figure title

    df1_tuples = utils.candlestick_tuples(ax1_data)

    fig1, ax1 = plt.subplots(1, 1)
    ax1.xaxis_date()
    ax1.set_ylabel('OHLC', color='g')
    ax1.set_title(figure_title)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)
    for t1 in ax1.get_yticklabels():
        t1.set_color('g')
    ax1.grid()
    fplt.candlestick_ochl(ax1, df1_tuples, width=candlestick_width, colorup='g', colordown='r')

    ax2 = ax1.twinx()
    ax2.plot(ax3_data, 'b-')
    ax2.set_ylabel('%R', color='b')
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')
    fig1.show()

    fig2 = plt.figure(2)
    plt.plot(ax2_data)
    plt.title('ADL vs EMAs')
    plt.legend(['ADL', '3 day EMA of ADL', '10 day EMA of ADL'])
    plt.xlabel('Laikas')
    plt.ylabel('ADL')
    plt.grid()
    plt.xticks(rotation=90)
    fig2.show()

    plt.close()

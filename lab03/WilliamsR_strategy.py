import pandas as pd
import numpy as np


def wr_strategy(print_log, wr_data, dates, ema_period, control_ticks, stop_loss, take_profit, bear_open_bound, bear_close_bound, bull_open_bound, bull_close_bound, initial_budget, trade_weight, trade_expenses):
    # strategy dataframes
    # bearish_engulfing_mask = (wr_data['Close'] < wr_data['EMA']) & (wr_data['%R'] < -50)[ema_period:]
    # bullish_engulfing_mask = (wr_data['Close'] > wr_data['EMA']) & (wr_data['%R'] > -50)[ema_period:]

    # values to return
    profits = pd.Series(np.zeros(len(wr_data)))
    profits[0] = initial_budget
    bull_buys = pd.Series(np.full(len(wr_data), False), index=dates)
    bull_sales = pd.Series(np.full(len(wr_data), False), index=dates)
    bear_buys = pd.Series(np.full(len(wr_data), False), index=dates)
    bear_sales = pd.Series(np.full(len(wr_data), False), index=dates)
    stop_loss_trades = pd.Series(np.full(len(wr_data), False), index=dates)
    take_profit_trades = pd.Series(np.full(len(wr_data), False), index=dates)

    # helper variables
    bear_signal = False
    bear_mark = 0
    bear_stop_loss = 0
    bear_take_profit = 0
    bull_stop_loss = 0
    bull_take_profit = 0
    bull_signal = False
    bull_mark = 0

    # trade counters (returned)
    minusas = 0
    pliusas = 0
    stop_loss_counter = 0
    take_profit_counter = 0

    for i in range(ema_period, len(wr_data)):
        current_close_price = wr_data['Close'][i]
        if not bear_signal:
            bearish_open_signal = (wr_data['Close'][i] < wr_data['EMA'][i]) & (wr_data['%R'][i] < bear_open_bound)
            if bearish_open_signal:
                bear_signal = True
                bear_mark = i + control_ticks
                # bear_mark = i
                # bear_stop_loss = current_close_price - stop_loss
                # bear_take_profit = current_close_price + take_profit
        if bear_signal:
            bearish_close_signal = (wr_data['Close'][i] > wr_data['EMA'][i]) | (wr_data['%R'][i] > bear_close_bound)
            if bearish_close_signal and i < bear_mark:
                bear_signal = False
            elif i == bear_mark:
                if bearish_close_signal:
                    bear_signal = False
                else:
                    bear_stop_loss = current_close_price - stop_loss
                    bear_take_profit = current_close_price + take_profit
            elif bearish_close_signal and i > bear_mark:
                bear_signal = False
                bear_buys.iat[i] = True
                bear_sales.iat[bear_mark] = True
                trade_value = (wr_data['Close'][bear_mark] - current_close_price) * trade_weight - trade_expenses
                bear_stop_loss = 0
                bear_take_profit = 0
                profits[i] = trade_value
                if print_log:
                    if wr_data['Close'][bear_mark] < current_close_price:
                        print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; MINUSAS {5}; bear mark: {6}; i: {7}".format(
                            dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                            trade_value, bear_mark, i))
                        minusas += 1
                    else:
                        print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; PLIUSAS {5}; bear mark: {6}; i: {7}".format(
                            dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                            trade_value, bear_mark, i))
                        pliusas += 1
            elif current_close_price >= bear_take_profit and i > bear_mark:
                bear_signal = False
                bear_sales.iat[bear_mark] = True
                take_profit_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bear_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; TAKE PROFIT {5}".format(
                        dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    take_profit_counter += 1
            elif current_close_price <= bear_stop_loss and i > bear_mark:
                bear_signal = False
                bear_sales.iat[bear_mark] = True
                stop_loss_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bear_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; STOP LOSS {5}".format(
                        dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    stop_loss_counter += 1

        if not bull_signal:
            bullish_open_signal = (wr_data['Close'][i] > wr_data['EMA'][i]) & (wr_data['%R'][i] > bull_open_bound)
            if bullish_open_signal:
                bull_signal = True
                bull_mark = i + control_ticks
                # bull_mark = i
                # bull_stop_loss = current_close_price - stop_loss
                # bull_take_profit = current_close_price + take_profit
        if bull_signal:
            bullish_close_signal = (wr_data['Close'][i] < wr_data['EMA'][i]) | (wr_data['%R'][i] < bull_close_bound)
            if bullish_close_signal and i < bull_mark:
                bull_signal = False
            elif i == bull_mark:
                if bullish_close_signal:
                    bull_signal = False
                else:
                    bull_stop_loss = current_close_price - stop_loss
                    bull_take_profit = current_close_price + take_profit
            elif bullish_close_signal and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                bull_sales.iat[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    if current_close_price < wr_data['Close'][bull_mark]:
                        print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; MINUSAS {5}; bull mark: {6}; i: {7}".format(
                            dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                            trade_value, bull_mark, i))
                        minusas += 1
                    else:
                        print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; PLIUSAS {5}; bull mark: {6}; i: {7}".format(
                            dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                            trade_value, bull_mark, i))
                        pliusas += 1
            elif current_close_price >= bull_take_profit and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                take_profit_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; TAKE PROFIT {5}".format(
                        dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    take_profit_counter += 1
            elif current_close_price <= bull_stop_loss and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                stop_loss_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; STOP LOSS {5}".format(
                        dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    stop_loss_counter += 1

    profits = profits.cumsum()

    if print_log:
        print("Minusai: ", minusas, "; pliusai: ", pliusas)
        print("Stop losses: ", stop_loss_counter, "; take profits: ", take_profit_counter)

    return profits, bull_buys, bull_sales, bear_buys, bear_sales,  stop_loss_trades, take_profit_trades


def wr_strategy_backup(print_log, wr_data, dates, ema_period, control_ticks, stop_loss, take_profit, initial_budget, trade_weight, trade_expenses):
    # strategy dataframes
    bearish_engulfing_mask = (wr_data['Close'] < wr_data['EMA']) & (wr_data['%R'] < -50)[ema_period:]
    bearish_open_signal = (bearish_engulfing_mask != bearish_engulfing_mask.shift(1)) & (bearish_engulfing_mask == True)[ema_period:]
    bearish_close_signal = (bearish_engulfing_mask != bearish_engulfing_mask.shift(1)) & (bearish_engulfing_mask == False)[ema_period:]
    bullish_engulfing_mask = (wr_data['Close'] > wr_data['EMA']) & (wr_data['%R'] > -50)[ema_period:]
    bullish_open_signal = (bullish_engulfing_mask != bullish_engulfing_mask.shift(1)) & (bullish_engulfing_mask == True)[ema_period:]
    bullish_close_signal = (bullish_engulfing_mask != bullish_engulfing_mask.shift(1)) & (bullish_engulfing_mask == False)[ema_period:]

    # values to return
    profits = pd.Series(np.zeros(len(wr_data)))
    profits[0] = initial_budget
    bull_buys = pd.Series(np.full(len(wr_data), False), index=dates)
    bull_sales = pd.Series(np.full(len(wr_data), False), index=dates)
    bear_buys = pd.Series(np.full(len(wr_data), False), index=dates)
    bear_sales = pd.Series(np.full(len(wr_data), False), index=dates)
    stop_loss_trades = pd.Series(np.full(len(wr_data), False), index=dates)
    take_profit_trades = pd.Series(np.full(len(wr_data), False), index=dates)

    # helper variables
    bear_signal = False
    bear_mark = 0
    bear_stop_loss = 0
    bear_take_profit = 0
    bull_stop_loss = 0
    bull_take_profit = 0
    bull_signal = False
    bull_mark = 0

    # trade counters (returned)
    minusas = 0
    pliusas = 0
    stop_loss_counter = 0
    take_profit_counter = 0

    for i in range(ema_period, len(wr_data)):
        current_close_price = wr_data['Close'][i]
        if not bear_signal:
            if bearish_open_signal.iloc[i]:
                bear_signal = True
                bear_mark = i + control_ticks
                # bear_mark = i
                # bear_stop_loss = current_close_price - stop_loss
                # bear_take_profit = current_close_price + take_profit
        if bear_signal:
            if bearish_close_signal.iloc[i] and i < bear_mark:
                bear_signal = False
            elif i == bear_mark:
                if bearish_close_signal.iloc[i]:
                    bear_signal = False
                else:
                    bear_stop_loss = current_close_price - stop_loss
                    bear_take_profit = current_close_price + take_profit
            elif bearish_close_signal.iloc[i] and i > bear_mark:
                bear_signal = False
                bear_buys.iat[i] = True
                bear_sales.iat[bear_mark] = True
                trade_value = (wr_data['Close'][bear_mark] - current_close_price) * trade_weight - trade_expenses
                bear_stop_loss = 0
                bear_take_profit = 0
                profits[i] = trade_value
                if print_log:
                    if wr_data['Close'][bear_mark] < current_close_price:
                        print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; MINUSAS {5}".format(
                            dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                            trade_value))
                        minusas += 1
                    else:
                        print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; PLIUSAS {5}".format(
                            dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                            trade_value))
                        pliusas += 1
            elif current_close_price >= bear_take_profit and i > bear_mark:
                bear_signal = False
                bear_sales.iat[bear_mark] = True
                take_profit_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bear_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; TAKE PROFIT {5}".format(
                        dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    take_profit_counter += 1
            elif current_close_price <= bear_stop_loss and i > bear_mark:
                bear_signal = False
                bear_sales.iat[bear_mark] = True
                stop_loss_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bear_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pardavėm už {1}; {2}: pirkom už {3}. Kiekis: {4}; STOP LOSS {5}".format(
                        dates[bear_mark], wr_data['Close'][bear_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    stop_loss_counter += 1

        if not bull_signal:
            if bullish_open_signal.iloc[i]:
                bull_signal = True
                bull_mark = i + control_ticks
                # bull_mark = i
                # bull_stop_loss = current_close_price - stop_loss
                # bull_take_profit = current_close_price + take_profit
        if bull_signal:
            if bullish_close_signal.iloc[i] and i < bull_mark:
                bull_signal = False
            elif i == bull_mark:
                if bullish_close_signal.iloc[i]:
                    bull_signal = False
                else:
                    bull_stop_loss = current_close_price - stop_loss
                    bull_take_profit = current_close_price + take_profit
            elif bullish_close_signal.iloc[i] and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                bull_sales.iat[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    if current_close_price < wr_data['Close'][bull_mark]:
                        print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; MINUSAS {5}".format(
                            dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                            trade_value))
                        minusas += 1
                    else:
                        print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; PLIUSAS {5}".format(
                            dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                            trade_value))
                        pliusas += 1
            elif current_close_price >= bull_take_profit and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                take_profit_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; TAKE PROFIT {5}".format(
                        dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    take_profit_counter += 1
            elif current_close_price <= bull_stop_loss and i > bull_mark:
                bull_signal = False
                bull_buys.iat[bull_mark] = True
                stop_loss_trades[i] = True
                trade_value = (current_close_price - wr_data['Close'][bull_mark]) * trade_weight - trade_expenses
                profits[i] = trade_value
                if print_log:
                    print("{0}: pirkom už {1}; {2}: pardavėm už {3}. Kiekis: {4}; STOP LOSS {5}".format(
                        dates[bull_mark], wr_data['Close'][bull_mark], dates[i], current_close_price, trade_weight,
                        trade_value))
                    stop_loss_counter += 1

    profits = profits.cumsum()

    if print_log:
        print("Minusai: ", minusas, "; pliusai: ", pliusas)
        print("Stop losses: ", stop_loss_counter, "; take profits: ", take_profit_counter)

    return profits, bull_buys, bull_sales, bear_buys, bear_sales,  stop_loss_trades, take_profit_trades


def strategy_profits(wr_data, dates, ema_period, control_ticks, stop_loss, take_profit, initial_budget, trade_weight, trade_expenses):
    tmp_profits, temp_bull_buys, tmp_bull_sales, tmp_bear_buys, tmp_bear_sales, tmp_sl, tmp_tp = \
        wr_strategy(False, wr_data, dates, ema_period, control_ticks, stop_loss, take_profit,
                    -50, -50, -50, -50, initial_budget, trade_weight, trade_expenses)
    return tmp_profits


def strategy_profits2(wr_data, dates, ema_period, control_ticks, bear_open, bear_close, bull_open, bull_close, initial_budget, trade_weight, trade_expenses):
    tmp_profits, temp_bull_buys, tmp_bull_sales, tmp_bear_buys, tmp_bear_sales, tmp_sl, tmp_tp = \
        wr_strategy(False, wr_data, dates, ema_period, control_ticks, 10, 10, bear_open, bear_close, bull_open,
                    bull_close, initial_budget, trade_weight, trade_expenses)
    return tmp_profits


def strategy_profits3(wr_data, dates, ema_period, control_ticks, stop_loss, take_profit, bear_open, bear_close, bull_open, bull_close, initial_budget, trade_weight, trade_expenses):
    tmp_profits, temp_bull_buys, tmp_bull_sales, tmp_bear_buys, tmp_bear_sales, tmp_sl, tmp_tp = \
        wr_strategy(False, wr_data, dates, ema_period, control_ticks, stop_loss, take_profit, bear_open, bear_close,
                    bull_open, bull_close, initial_budget, trade_weight, trade_expenses)
    return tmp_profits


def strategy_profits4(wr_data, dates, ema_period, bear_open, bear_close, bull_open, bull_close, initial_budget, trade_weight, trade_expenses):
    tmp_profits, temp_bull_buys, tmp_bull_sales, tmp_bear_buys, tmp_bear_sales, tmp_sl, tmp_tp = \
        wr_strategy(False, wr_data, dates, ema_period, 0, 10, 10, bear_open, bear_close, bull_open,
                    bull_close, initial_budget, trade_weight, trade_expenses)
    return tmp_profits


def optimize_strategy(wr_data, dates, initial_budget, trade_weight, trade_expenses):
    max_profit = 0
    opt_period = 100
    opt_ctrl_ticks = 1
    opt_stop_loss = 1
    opt_take_profit = 2
    for ema_period in range(100, 150):
        for ctrl_ticks in range(3, 7):
            for stop_loss in np.arange(0.4, 1.0, 0.1):
                for take_profit in np.arange(1.6, 2.4, 0.1):
                    print("testing period: ", ema_period, "; control ticks: ", ctrl_ticks, "; stop loss: ", stop_loss,
                          "; take profit: ", take_profit, "optimal: period: ", opt_period, "; optimal control ticks: ",
                          opt_ctrl_ticks, "; optimal stop loss: ", opt_stop_loss, "; optimal take profit: ",
                          opt_take_profit, "; max profits: ", max_profit)
                    profits = strategy_profits(wr_data, dates, ema_period, ctrl_ticks, stop_loss, take_profit,
                                               initial_budget, trade_weight, trade_expenses)
                    if profits.iloc[-1] > max_profit:
                        max_profit = profits.iloc[-1]
                        opt_period = ema_period
                        opt_ctrl_ticks = ctrl_ticks
                        opt_stop_loss = stop_loss
                        opt_take_profit = take_profit
    return opt_period, opt_ctrl_ticks, opt_stop_loss, opt_take_profit


def optimize_strategy2(wr_data, dates, initial_budget, trade_weight, trade_expenses):
    max_profit = 0
    opt_period = 100
    opt_bear_open_bound = 50
    opt_bear_close_bound = 50
    opt_bull_open_bound = 50
    opt_bull_close_bound = 50
    for ema_period in range(30, 90):
        for bear_open_bound in np.arange(-20, -81, -30):
            for bear_close_bound in np.arange(-20, -81, -30):
                for bull_open_bound in np.arange(-20, -81, -30):
                    for bull_close_bound in np.arange(-20, -81, -30):
                        print("testing period: ", ema_period, "; bear open: ", bear_open_bound,
                              "; bear close: ", bear_close_bound, "; bull open: ", bull_open_bound, "; bull close: ", bull_close_bound,
                              "optimal period: ", opt_period, "; optimal bear open: ", opt_bear_open_bound, "; optimal bear close: ",
                              opt_bear_close_bound, "; optimal bull open: ", opt_bull_open_bound, "; optimal bull close: ",
                              opt_bull_close_bound, "; max profits: ", max_profit)
                        profits = strategy_profits4(wr_data, dates, ema_period, bear_open_bound,
                                                   bear_close_bound, bull_open_bound, bull_close_bound,
                                                   initial_budget, trade_weight, trade_expenses)
                        if profits.iloc[-1] > max_profit:
                            max_profit = profits.iloc[-1]
                            opt_period = ema_period
                            opt_bear_open_bound = bear_open_bound
                            opt_bear_close_bound = bear_close_bound
                            opt_bull_open_bound = bull_open_bound
                            opt_bull_close_bound = bull_close_bound
    return opt_period, opt_bear_open_bound, opt_bear_close_bound, opt_bull_open_bound, opt_bull_close_bound

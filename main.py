from risk_functions import fetch_data, compute_log_returns, compute_historical_var, plot_returns_with_var


def main():
    # --- Konfiguracja użytkownika: ---
    tickers = [
    "ASML",   # ASML Holding
    "VOO",    # Vanguard S&P 500 ETF
    "MSFT",   # Microsoft Corporation
    "TSLA",   # Tesla Inc.
        ]
    period = '6mo'
    interval = '1d'
    var_level = 0.05
    plot_mode = 'subplots'  # 'separate', 'subplots', 'combined'
    # ----------------------------------

    prices = fetch_data(tickers, period=period, interval=interval)
    returns = compute_log_returns(prices)
    var = compute_historical_var(returns, level=var_level)
    plot_returns_with_var(returns, var, level=var_level, mode=plot_mode)

if __name__ == '__main__':
    main()

"""
Moduł funkcji do pobierania danych, obliczania zwrotów i VaR oraz rysowania wykresów.
"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ui_utils import maximize_window


def fetch_data(tickers, period='1y', interval='1d'):
    """Pobiera historyczne ceny zamknięcia dla listy tickerów."""
    data = yf.download(tickers, period=period, interval=interval)['Close']
    return data


def compute_log_returns(price_df):
    """Oblicza dzienne zwroty logarytmiczne."""
    returns = np.log(price_df / price_df.shift(1)).dropna()
    return returns


def compute_historical_var(returns_df, level=0.05):
    """Oblicza VaR historyczne dla każdego tickeru na zadanym poziomie."""
    var = returns_df.quantile(level)
    return var


def plot_returns_with_var(returns_df, var_series, level=0.05, mode='combined'):
    """
    Rysuje histogram i KDE zwrotów z linią VaR.
    mode: 'separate' — osobne okna dla każdego tickera
          'subplots' — jedno okno, wiele wykresów
          'combined' — wszystkie zwroty na jednym wykresie
    """
    tickers = returns_df.columns

    if mode == 'separate':
        for t in tickers:
            fig, ax = plt.subplots()
            maximize_window(fig)
            sns.kdeplot(returns_df[t], fill = False, ax=ax, label=t)
            ax.axvline(var_series[t], color='red', linestyle='--', label=f'VaR {level*100:.0f}% = {var_series[t]:.2%}')
            ax.set_title(f'{t} zwroty i VaR')
            ax.set_xlabel(None)
            ax.legend()
            plt.show()

    elif mode == 'subplots':
        n = len(tickers)
        fig, axes = plt.subplots(n, 1, figsize=(8, 4*n))
        maximize_window(fig)
        axes_list = np.array(axes).ravel()
        min_x = returns_df.min().min()
        max_x = returns_df.max().max()
        for ax, t in zip(axes_list, tickers):
            sns.kdeplot(returns_df[t], fill = False, ax=ax, label=t)
            ax.axvline(var_series[t], color='red', linestyle='--', label=f'VaR {level*100:.0f}% = {var_series[t]:.2%}')
            ax.set_xlim(min_x, max_x)
            ax.set_title(f'{t} zwroty i VaR')
            ax.set_xlabel(None)
            ax.legend()
        plt.tight_layout()
        plt.show()

    elif mode == 'combined':
        palette = sns.color_palette(n_colors=len(tickers))
        fig, ax = plt.subplots()
        maximize_window(fig)
        for i, t in enumerate(tickers):
            sns.kdeplot(returns_df[t], fill=False, ax=ax, label=t, color=palette[i])
            ax.axvline(var_series[t], linestyle='--', color=palette[i], label=f'{t} VaR = {var_series[t]:.2%}')
        ax.set_title('Porównanie zwrotów i VaR')
        ax.set_xlabel(None)
        ax.legend()
        plt.show()

    else:
        raise ValueError("Nieznany tryb rysowania: wybierz 'separate', 'subplots' lub 'combined'.")


import sys
import os
sys.path.append(os.path.dirname(__file__))

from fetch_data import fetch_prices, compute_returns, compute_correlation
from visualize import plot_heatmap, plot_top_correlations

if __name__ == "__main__":
    print("\n🚀 Starting Stock Correlation Analysis\n" + "="*40)

    prices = fetch_prices(period="1y")
    returns = compute_returns(prices)
    corr_matrix = compute_correlation(returns)

    print("\n📊 Correlation Matrix:")
    print(corr_matrix.round(2).to_string())

    plot_heatmap(corr_matrix)
    plot_top_correlations(corr_matrix)

    print("\n✅ Done! Check outputs/charts/ for your heatmap.")

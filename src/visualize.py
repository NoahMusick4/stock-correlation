import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from fetch_data import STOCKS

DARK_BG = "#0f0f1a"
CARD_BG = "#1a1a2e"
GREEN   = "#00e676"
RED     = "#ff5252"

def plot_heatmap(corr_matrix, output_path="../outputs/charts/correlation_heatmap.png"):
    ticker_to_name = {v: k for k, v in STOCKS.items()}
    corr_matrix.columns = [ticker_to_name.get(c, c) for c in corr_matrix.columns]
    corr_matrix.index = [ticker_to_name.get(i, i) for i in corr_matrix.index]

    fig, ax = plt.subplots(figsize=(14, 11))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor="#0f0f1a",
        ax=ax,
        annot_kws={"size": 9, "color": "black"},
        cbar_kws={"shrink": 0.8},
    )

    ax.set_title("Stock Return Correlation Matrix\n1 Year of Daily Returns",
                 color="white", fontsize=15, fontweight="bold", pad=20)
    ax.tick_params(colors="white", labelsize=9)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")
    cbar.set_label("Correlation", color="white", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    print(f"Heatmap saved to {output_path}")
    plt.show()


def plot_top_correlations(corr_matrix, output_path="../outputs/charts/top_correlations.png"):
    ticker_to_name = {v: k for k, v in STOCKS.items()}

    pairs = []
    cols = corr_matrix.columns.tolist()
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append({
                "Pair": f"{ticker_to_name.get(cols[i], cols[i])} / {ticker_to_name.get(cols[j], cols[j])}",
                "Correlation": round(corr_matrix.iloc[i, j], 4)
            })

    pairs_df = pd.DataFrame(pairs).sort_values("Correlation", ascending=False)
    top5 = pairs_df.head(5)
    bottom5 = pairs_df.tail(5)
    combined = pd.concat([top5, bottom5])

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    colors = [GREEN if v >= 0 else RED for v in combined["Correlation"]]
    bars = ax.barh(combined["Pair"], combined["Correlation"], color=colors, edgecolor="none", height=0.6)

    for bar, val in zip(bars, combined["Correlation"]):
        x_pos = val + 0.01 if val >= 0 else val - 0.01
        ha = "left" if val >= 0 else "right"
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                f"{val:+.2f}", va="center", ha=ha,
                color="white", fontsize=9, fontweight="bold")

    ax.axvline(0, color="white", linewidth=0.8, alpha=0.4)
    ax.set_title("Top 5 Most and Least Correlated Stock Pairs",
                 color="white", fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors="white", labelsize=9)
    ax.spines[:].set_visible(False)
    ax.set_xlim(-1.2, 1.2)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    print(f"Top correlations chart saved to {output_path}")
    plt.show()

import matplotlib.pyplot as plt
import pandas as pd
"""
NOT WORKING YET NOT TESTED YET 3/18
"""

def plot_comparison(results_df):
    """Plot model comparison metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Model Comparison')

    metrics = ['MAE', 'MSE', 'RMSE', 'R²']
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightblue']

    for ax, metric, color in zip(axes.flatten(), metrics, colors):
        results_df.plot(kind='bar', x='Model', y=metric, ax=ax, color=color, legend=False)
        ax.set_title(metric)
        ax.set_ylabel(metric)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Call the visualization function
results_df = pd.read_csv("../data/model_comparison_results.csv") #UNSURE
plot_comparison(results_df)

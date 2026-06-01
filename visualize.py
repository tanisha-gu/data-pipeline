import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

class DataVisualizer:
    """Handles data visualization with matplotlib"""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = "output/visualizations"):
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def line_plot(self, x_col: str, y_col: str, title: str = None, filename: str = None):
        """Create a line plot"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.df[x_col], self.df[y_col], linewidth=2, color='#1f77b4')
        
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title or f"{y_col} over {x_col}", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        self._save_and_show(filename or f"line_{y_col}.png")
    
    def histogram(self, column: str, bins: int = 30, title: str = None, filename: str = None):
        """Create a histogram"""
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[column], bins=bins, color='#2ca02c', edgecolor='black', alpha=0.7)
        
        plt.xlabel(column, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.title(title or f"Distribution of {column}", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        self._save_and_show(filename or f"histogram_{column}.png")
    
    def scatter_plot(self, x_col: str, y_col: str, title: str = None, filename: str = None):
        """Create a scatter plot"""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[x_col], self.df[y_col], alpha=0.6, s=50, color='#d62728')
        
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title or f"{y_col} vs {x_col}", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        self._save_and_show(filename or f"scatter_{x_col}_vs_{y_col}.png")
    
    def bar_chart(self, x_col: str, y_col: str, title: str = None, filename: str = None, top_n: int = None):
        """Create a bar chart"""
        data = self.df[[x_col, y_col]].groupby(x_col).sum().sort_values(y_col, ascending=False)
        
        if top_n:
            data = data.head(top_n)
        
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(data)), data[y_col].values, color='#ff7f0e', edgecolor='black')
        plt.xticks(range(len(data)), data.index, rotation=45, ha='right')
        
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title or f"{y_col} by {x_col}", fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        self._save_and_show(filename or f"bar_{x_col}.png")
    
    def box_plot(self, columns: list, title: str = None, filename: str = None):
        """Create a box plot"""
        plt.figure(figsize=(10, 6))
        self.df[columns].boxplot()
        
        plt.title(title or "Distribution Comparison", fontsize=14, fontweight='bold')
        plt.ylabel("Values", fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        self._save_and_show(filename or "boxplot.png")
    
    def heatmap_correlation(self, numeric_cols: list = None, title: str = None, filename: str = None):
        """Create correlation heatmap"""
        import numpy as np
        
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        corr_matrix = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        plt.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        plt.colorbar(label='Correlation')
        
        plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45, ha='right')
        plt.yticks(range(len(numeric_cols)), numeric_cols)
        plt.title(title or "Correlation Matrix", fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        self._save_and_show(filename or "heatmap_correlation.png")
    
    def _save_and_show(self, filename: str):
        """Save figure and display"""
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
        plt.show()
    
    def summary_statistics(self):
        """Print summary statistics"""
        print("\n📈 Summary Statistics:")
        print(self.df.describe())

import pandas as pd
import numpy as np

class DataCleaner:
    """Handles data cleaning and transformation"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_shape = df.shape
    
    def remove_duplicates(self, subset=None) -> 'DataCleaner':
        """Remove duplicate rows"""
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset)
        after = len(self.df)
        print(f"✓ Removed {before - after} duplicate rows")
        return self
    
    def handle_missing_values(self, strategy: str = "drop") -> 'DataCleaner':
        """
        Handle missing values
        
        Args:
            strategy: 'drop' to remove rows, 'fill' to use forward fill
        """
        before = self.df.isnull().sum().sum()
        
        if strategy == "drop":
            self.df = self.df.dropna()
        elif strategy == "fill":
            self.df = self.df.fillna(method='ffill').fillna(method='bfill')
        
        after = self.df.isnull().sum().sum()
        print(f"✓ Handled {before - after} missing values (strategy: {strategy})")
        return self
    
    def remove_outliers(self, column: str, threshold: float = 3.0) -> 'DataCleaner':
        """Remove outliers using z-score method"""
        if column not in self.df.columns:
            print(f"⚠ Column '{column}' not found")
            return self
        
        before = len(self.df)
        z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
        self.df = self.df[z_scores < threshold]
        after = len(self.df)
        print(f"✓ Removed {before - after} outliers from {column}")
        return self
    
    def convert_dtypes(self, type_mapping: dict = None) -> 'DataCleaner':
        """
        Convert column data types
        
        Args:
            type_mapping: Dict of {column: dtype}
        """
        if type_mapping:
            for col, dtype in type_mapping.items():
                if col in self.df.columns:
                    try:
                        self.df[col] = self.df[col].astype(dtype)
                        print(f"✓ Converted {col} to {dtype}")
                    except Exception as e:
                        print(f"✗ Could not convert {col}: {str(e)}")
        return self
    
    def strip_whitespace(self) -> 'DataCleaner':
        """Remove leading/trailing whitespace from all string columns"""
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].str.strip()
        print(f"✓ Stripped whitespace from {len(string_cols)} columns")
        return self
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return the cleaned DataFrame"""
        print(f"\n✓ Cleaning complete: {self.original_shape} → {self.df.shape}")
        return self.df
    
    def summary(self):
        """Print summary statistics"""
        print("\n📊 Data Summary:")
        print(f"Shape: {self.df.shape}")
        print(f"\nMissing values:\n{self.df.isnull().sum()}")
        print(f"\nData types:\n{self.df.dtypes}")
        return self

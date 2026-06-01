import pandas as pd
import os
from pathlib import Path

class DataIngestor:
    """Handles reading CSV files from a directory"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def ingest_csv(self, filename: str) -> pd.DataFrame:
        """
        Read a single CSV file
        
        Args:
            filename: Name of CSV file (with extension)
            
        Returns:
            DataFrame with the CSV data
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File {filename} not found in {self.data_dir}")
        
        try:
            df = pd.read_csv(filepath)
            print(f"✓ Ingested {filename}: {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            print(f"✗ Error reading {filename}: {str(e)}")
            raise
    
    def ingest_all_csv(self) -> pd.DataFrame:
        """
        Read all CSV files from directory and combine them
        
        Returns:
            Combined DataFrame from all CSV files
        """
        csv_files = list(self.data_dir.glob("*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.data_dir}")
        
        dfs = []
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                dfs.append(df)
                print(f"✓ Ingested {csv_file.name}: {len(df)} rows")
            except Exception as e:
                print(f"✗ Error reading {csv_file.name}: {str(e)}")
        
        if not dfs:
            raise ValueError("No CSV files could be read")
        
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"\n✓ Combined: {len(combined_df)} total rows")
        return combined_df

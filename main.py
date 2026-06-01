#!/usr/bin/env python3
"""
Data Pipeline: CSV → Clean → MySQL → Visualize
Main orchestrator script
"""

from ingest import DataIngestor
from clean import DataCleaner
from load import MySQLLoader
from visualize import DataVisualizer
import argparse
import sys

def run_pipeline(
    csv_dir: str = "data/raw",
    csv_file: str = None,
    table_name: str = "processed_data",
    skip_db: bool = False,
    visualizations: list = None
):
    """
    Run the complete data pipeline
    
    Args:
        csv_dir: Directory containing CSV files
        csv_file: Specific CSV file to process (optional)
        table_name: MySQL table name for loaded data
        skip_db: Skip MySQL loading step
        visualizations: List of visualization types to generate
    """
    
    print("=" * 60)
    print("🚀 DATA PIPELINE: INGEST → CLEAN → LOAD → VISUALIZE")
    print("=" * 60)
    
    try:
        # Step 1: Ingest
        print("\n📥 STEP 1: INGESTING DATA")
        print("-" * 60)
        ingestor = DataIngestor(csv_dir)
        
        if csv_file:
            df = ingestor.ingest_csv(csv_file)
        else:
            df = ingestor.ingest_all_csv()
        
        # Step 2: Clean
        print("\n🧹 STEP 2: CLEANING DATA")
        print("-" * 60)
        cleaner = DataCleaner(df)
        df = (cleaner
              .remove_duplicates()
              .handle_missing_values(strategy="drop")
              .strip_whitespace()
              .get_dataframe())
        
        cleaner.summary()
        
        # Step 3: Load to MySQL
        if not skip_db:
            print("\n💾 STEP 3: LOADING TO MYSQL")
            print("-" * 60)
            try:
                loader = MySQLLoader()
                loader.connect()
                loader.load_data(df, table_name, drop_if_exists=True)
                loader.disconnect()
            except Exception as e:
                print(f"⚠ Warning: MySQL loading failed: {str(e)}")
                print("Continuing with visualization...")
        else:
            print("\n⏭ STEP 3: SKIPPED (--skip-db)")
        
        # Step 4: Visualize
        print("\n📊 STEP 4: CREATING VISUALIZATIONS")
        print("-" * 60)
        visualizer = DataVisualizer(df)
        
        # Generate default visualizations if none specified
        if visualizations is None:
            visualizations = ["summary"]
        
        for viz in visualizations:
            try:
                if viz == "summary":
                    visualizer.summary_statistics()
                elif viz == "correlation" and len(df.select_dtypes(include=['number']).columns) > 1:
                    visualizer.heatmap_correlation()
                else:
                    print(f"⚠ Visualization '{viz}' not supported or no numeric columns")
            except Exception as e:
                print(f"⚠ Error creating visualization '{viz}': {str(e)}")
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Processed: {len(df)} rows × {len(df.columns)} columns")
        print(f"📁 Output directory: output/visualizations/")
        if not skip_db:
            print(f"🗄️  MySQL table: {table_name}")
        
    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Data Pipeline: Ingest → Clean → MySQL → Visualize"
    )
    parser.add_argument(
        "--csv-dir",
        default="data/raw",
        help="Directory containing CSV files (default: data/raw)"
    )
    parser.add_argument(
        "--csv-file",
        help="Specific CSV file to process (optional)"
    )
    parser.add_argument(
        "--table-name",
        default="processed_data",
        help="MySQL table name (default: processed_data)"
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip MySQL loading step"
    )
    parser.add_argument(
        "--visualizations",
        nargs="+",
        default=["summary"],
        help="Visualization types: summary, correlation (default: summary)"
    )
    
    args = parser.parse_args()
    
    run_pipeline(
        csv_dir=args.csv_dir,
        csv_file=args.csv_file,
        table_name=args.table_name,
        skip_db=args.skip_db,
        visualizations=args.visualizations
    )


if __name__ == "__main__":
    main()

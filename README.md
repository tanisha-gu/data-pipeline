# 🚀 Data Pipeline

A production-ready data pipeline that ingests CSV files, cleans the data, loads it into MySQL, and generates visualizations with matplotlib.

## 📋 Pipeline Flow

```
CSV Files → Data Ingest → Data Cleaning → MySQL Load → Visualizations
```

## 🛠️ Tech Stack

- **Python 3.8+**
- **Pandas** - Data manipulation and analysis
- **MySQL** - Relational database
- **Matplotlib** - Data visualization

## 📦 Installation

### 1. Clone or setup project
```bash
cd data-pipeline
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=data_pipeline
```

### 5. Create MySQL database (if not exists)
```bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS data_pipeline;
```

## 📂 Project Structure

```
data-pipeline/
├── main.py                 # Main pipeline orchestrator
├── ingest.py              # CSV ingestion module
├── clean.py               # Data cleaning module
├── load.py                # MySQL loading module
├── visualize.py           # Visualization module
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
├── data/
│   └── raw/               # Place your CSV files here
├── output/
│   └── visualizations/    # Generated charts and plots
└── logs/                  # Pipeline logs (optional)
```

## 🚀 Quick Start

### 1. Prepare your CSV data
Place your CSV files in `data/raw/` directory:
```bash
mkdir -p data/raw
cp your_data.csv data/raw/
```

### 2. Run the pipeline
```bash
python main.py
```

### 3. View results
- **Visualizations**: Check `output/visualizations/` for generated charts
- **Database**: Query your MySQL database for the loaded data

## 📖 Usage Examples

### Process all CSV files in directory
```bash
python main.py --csv-dir data/raw
```

### Process a specific CSV file
```bash
python main.py --csv-file data.csv --table-name my_table
```

### Skip MySQL loading (just clean and visualize)
```bash
python main.py --skip-db
```

### Generate specific visualizations
```bash
python main.py --visualizations summary correlation
```

### Complete example with custom parameters
```bash
python main.py \
  --csv-dir data/raw \
  --table-name sales_data \
  --visualizations summary correlation \
  --csv-file sales_2024.csv
```

## 🔧 Module Reference

### DataIngestor (`ingest.py`)
```python
from ingest import DataIngestor

ingestor = DataIngestor("data/raw")
df = ingestor.ingest_csv("data.csv")           # Single file
df = ingestor.ingest_all_csv()                 # All CSV files
```

### DataCleaner (`clean.py`)
```python
from clean import DataCleaner

cleaner = DataCleaner(df)
df = (cleaner
    .remove_duplicates()
    .handle_missing_values(strategy="drop")
    .strip_whitespace()
    .get_dataframe())
```

### MySQLLoader (`load.py`)
```python
from load import MySQLLoader

loader = MySQLLoader()
loader.connect()
loader.load_data(df, "table_name", drop_if_exists=True)
loader.disconnect()
```

### DataVisualizer (`visualize.py`)
```python
from visualize import DataVisualizer

viz = DataVisualizer(df)
viz.line_plot("date", "value")
viz.histogram("column_name")
viz.scatter_plot("x", "y")
viz.bar_chart("category", "amount", top_n=10)
viz.heatmap_correlation()
```

## 🐛 Troubleshooting

### "No CSV files found" error
```bash
# Make sure CSV files are in the correct directory
ls data/raw/
```

### MySQL connection error
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1"

# Verify credentials in .env
cat .env
```

### "Column not found" in visualization
```bash
# Check available columns in your data
python -c "import pandas as pd; print(pd.read_csv('data/raw/your_file.csv').columns)"
```

## 🎨 Customization

### Add custom cleaning logic
Edit `clean.py` and add methods to `DataCleaner` class:
```python
def custom_clean(self) -> 'DataCleaner':
    # Your cleaning logic
    return self
```

### Add new visualization types
Edit `visualize.py` and add methods to `DataVisualizer` class:
```python
def custom_viz(self, column: str):
    # Your visualization logic
    self._save_and_show("custom.png")
```

### Modify data types for MySQL
In `load.py`, update the `create_table` method to match your data:
```python
if column_name == "special_column":
    col_type = "DECIMAL(10,2)"  # Custom type
```

## 📊 Example CSV Format

Your CSV should be formatted like:
```csv
date,product,sales,region
2024-01-01,Widget A,1500,North
2024-01-02,Widget B,2300,South
2024-01-03,Widget A,1800,East
```

## 🔐 Security Notes

- **Never commit `.env`** to version control - it contains passwords
- Use `.gitignore` to exclude sensitive files:
```
.env
data/raw/*
output/*
venv/
__pycache__/
```

- For production, use environment variables from your deployment system

## 📝 Logging

To enable detailed logging, add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Production Deployment

For production use:
1. Use connection pooling in `load.py`
2. Add error handling and retries
3. Implement data validation
4. Set up logging and monitoring
5. Use secrets manager for credentials
6. Schedule with cron or task scheduler

## 📚 Resources

- [Pandas Documentation](https://pandas.pydata.org/)
- [MySQL Connector Documentation](https://dev.mysql.com/doc/connector-python/en/)
- [Matplotlib Documentation](https://matplotlib.org/)

## 📄 License

MIT License - feel free to use and modify

## 💬 Support

For issues or questions, check the troubleshooting section or create an issue.

---

**Happy data processing! 🎉**

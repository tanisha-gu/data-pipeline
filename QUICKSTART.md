# Quick Start Guide

## 🎯 Get running in 5 minutes

### Windows Users:
```bash
setup.bat
```

### Mac/Linux Users:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure MySQL credentials
cp .env.example .env
# Edit .env with your MySQL details

# Create directories
mkdir -p data/raw output/visualizations logs
```

---

## 🚀 Run Your First Pipeline

### With Sample Data (No MySQL needed for testing):
```bash
# Skip database loading to test the pipeline
python main.py --skip-db --csv-file data/raw/sample_data.csv
```

### With Full MySQL Integration:
```bash
# First, ensure MySQL is running and .env is configured
# Then run the full pipeline
python main.py --csv-file data/raw/sample_data.csv --table-name sales_data
```

---

## 📊 What You'll Get

After running the pipeline, you'll have:

1. **Cleaned Data** - Duplicates removed, missing values handled, whitespace stripped
2. **MySQL Table** - Data loaded into your database (unless --skip-db)
3. **Visualizations** - Charts saved in `output/visualizations/`:
   - Summary statistics
   - Correlation heatmap
   - And more as configured

---

## 💡 Common Use Cases

### 1. Clean and Analyze CSV without Database:
```bash
python main.py --skip-db --visualizations summary correlation
```

### 2. Load Multiple CSV Files to Database:
```bash
python main.py --csv-dir data/raw --table-name combined_data
```

### 3. Process Specific File with Custom Table:
```bash
python main.py --csv-file sales_2024.csv --table-name sales_2024
```

### 4. Advanced - Custom Visualizations:
Edit `visualize.py` and add your own visualization methods, then:
```bash
python main.py --visualizations summary custom_viz
```

---

## 🔧 Customization Examples

### Modify Cleaning Logic:
Edit `clean.py` - Add methods to the `DataCleaner` class:
```python
def remove_outliers(self, column: str, threshold: float = 3.0) -> 'DataCleaner':
    # Custom outlier removal logic
    return self
```

### Add New Visualizations:
Edit `visualize.py` - Add methods to the `DataVisualizer` class:
```python
def custom_chart(self, x_col: str, y_col: str):
    # Your matplotlib code here
    self._save_and_show("custom_chart.png")
```

### Change MySQL Table Schema:
Edit `load.py` - Modify the `create_table` method:
```python
if dtype == 'object':
    col_type = "VARCHAR(500)"  # Custom length
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No CSV files found" | Ensure CSV files are in `data/raw/` |
| MySQL connection error | Check MySQL is running: `mysql -u root -p` |
| Missing columns error | Check CSV headers match your code |
| Module not found | Run `pip install -r requirements.txt` |

---

## 📚 Next Steps

1. **Read** the full [README.md](README.md) for comprehensive documentation
2. **Explore** the module files to understand the pipeline flow
3. **Customize** the pipeline for your specific data needs
4. **Deploy** to production with proper error handling and logging

---

## 🎓 Learning Resources

- Study `ingest.py` to understand CSV loading
- Check `clean.py` for data transformation patterns
- Review `load.py` for database integration
- Examine `visualize.py` for matplotlib usage

---

Happy Data Processing! 🎉

For detailed documentation, see [README.md](README.md)

import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLLoader:
    """Handles loading data to MySQL database"""
    
    def __init__(self, host: str = None, user: str = None, password: str = None, database: str = None):
        """
        Initialize MySQL connection
        
        Args:
            host: MySQL host (default from .env)
            user: MySQL user (default from .env)
            password: MySQL password (default from .env)
            database: Database name (default from .env)
        """
        self.host = host or os.getenv("MYSQL_HOST", "localhost")
        self.user = user or os.getenv("MYSQL_USER", "root")
        self.password = password or os.getenv("MYSQL_PASSWORD", "")
        self.database = database or os.getenv("MYSQL_DATABASE", "data_pipeline")
        self.connection = None
    
    def connect(self):
        """Establish MySQL connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Connected to MySQL database: {self.database}")
            return self
        except Error as e:
            print(f"✗ Connection failed: {str(e)}")
            raise
    
    def create_table(self, df: pd.DataFrame, table_name: str, drop_if_exists: bool = False):
        """
        Create table from DataFrame schema
        
        Args:
            df: Source DataFrame
            table_name: Name of table to create
            drop_if_exists: Drop table if it already exists
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            if drop_if_exists:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"✓ Dropped existing table: {table_name}")
            
            # Create column definitions
            col_defs = []
            for col_name, dtype in zip(df.columns, df.dtypes):
                if dtype == 'object':
                    col_type = "VARCHAR(255)"
                elif dtype == 'int64':
                    col_type = "BIGINT"
                elif dtype == 'float64':
                    col_type = "FLOAT"
                elif dtype == 'datetime64[ns]':
                    col_type = "DATETIME"
                else:
                    col_type = "VARCHAR(255)"
                
                col_defs.append(f"`{col_name}` {col_type}")
            
            create_statement = f"CREATE TABLE {table_name} ({', '.join(col_defs)})"
            cursor.execute(create_statement)
            self.connection.commit()
            print(f"✓ Created table: {table_name}")
        except Error as e:
            print(f"✗ Error creating table: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def insert_data(self, df: pd.DataFrame, table_name: str, batch_size: int = 1000):
        """
        Insert DataFrame into MySQL table
        
        Args:
            df: DataFrame to insert
            table_name: Target table name
            batch_size: Number of rows to insert per batch
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            columns = ", ".join([f"`{col}`" for col in df.columns])
            placeholders = ", ".join(["%s"] * len(df.columns))
            insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                data = [tuple(row) for row in batch.values]
                cursor.executemany(insert_statement, data)
                self.connection.commit()
                print(f"✓ Inserted {min(batch_size, len(batch))} rows ({i+len(batch)}/{len(df)})")
            
            print(f"✓ Successfully inserted {len(df)} rows into {table_name}")
        except Error as e:
            print(f"✗ Error inserting data: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def load_data(self, df: pd.DataFrame, table_name: str, drop_if_exists: bool = False):
        """
        Complete workflow: create table and insert data
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            drop_if_exists: Drop existing table before creating new one
        """
        if not self.connection:
            self.connect()
        
        self.create_table(df, table_name, drop_if_exists)
        self.insert_data(df, table_name)
    
    def disconnect(self):
        """Close MySQL connection"""
        if self.connection:
            self.connection.close()
            print("✓ Disconnected from MySQL")

import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db

# Set up logging
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def show_all_tables(conn):
    """Show all tables and preview first 5 rows of each table"""
    try:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';", conn
        )
        logging.info("All tables in the database:\n%s", tables)
        print("Tables in database:")
        print(tables)

        # Preview first 5 rows of each table
        for table in tables['name']:
            print(f"\nPreview of table '{table}':")
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5;", conn)
                print(df)
            except Exception as e:
                print(f"Could not preview table '{table}': {e}")

    except Exception as e:
        logging.error(f"Error fetching tables: {e}")
        print(f"Error fetching tables: {e}")

def create_vendor_summary(conn):
    """This function merges different tables to get the overall vendor summary"""
    try:
        vendor_sales_summary = pd.read_sql_query("""
        WITH FreightSummary AS (
            SELECT 
                VendorNumber,
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),
        PurchaseSummary AS (
            SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp
            ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
        ),
        SalesSummary AS (
            SELECT 
                VendorNo,
                Brand,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )
        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.PurchasePrice,
            ps.ActualPrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo
            AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
        """, conn)

        logging.info("Vendor summary created successfully")
        return vendor_sales_summary

    except Exception as e:
        logging.error(f"Error creating vendor summary: {e}")
        return None

def clean_data(df):
    """Clean data and add calculated columns"""
    df['Volume'] = df['Volume'].astype(float)
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    return df

if __name__ == '__main__':
    # Create database connection
    conn = sqlite3.connect('inventory.db')

    # Show all tables and preview
    show_all_tables(conn)

    logging.info('Creating Vendor Summary Table.....')
    summary_df = create_vendor_summary(conn)
    logging.info("\n" + str(summary_df.head()))
    print("\nVendor Summary Preview:")
    print(summary_df.head())

    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info("\n" + str(clean_df.head()))
    print("\nCleaned Vendor Summary Preview:")
    print(clean_df.head())

    logging.info('Ingesting data.....')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Completed')

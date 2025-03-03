import pandas as pd
import sqlite3
import os

def import_excel_to_db(excel_file, db_path, table_name):
    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 将DataFrame导入到数据库表中
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # 关闭数据库连接
    conn.close()

if __name__ == "__main__":
    # 定义Excel文件和对应的表名
    files_and_tables = {
        'c2301.xlsx': 'c2301',
        'c2302.xlsx': 'c2302',
        'c2303.xlsx': 'c2303',
        'c2304.xlsx': 'c2304',
        'c2305.xlsx': 'c2305',
        'c2306.xlsx': 'c2306',
        'c2307.xlsx': 'c2307',
        'c2308.xlsx': 'c2308',
        'c2309.xlsx': 'c2309',
        'c2310.xlsx': 'c2310',
        'c2311.xlsx': 'c2311',
        'c2312.xlsx': 'c2312'
        # 添加更多文件和表名
    }

    db_path = 'b2c.db'  # 替换为你的数据库路径

    for excel_file, table_name in files_and_tables.items():
        if os.path.exists(excel_file):
            import_excel_to_db(excel_file, db_path, table_name)
            print(f"Successfully imported {excel_file} to {table_name} in {db_path}")
        else:
            print(f"File {excel_file} does not exist.")

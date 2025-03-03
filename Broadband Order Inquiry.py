import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

def query_city_monthly_orders(db_path, table_name):
    """查询每个地市和月份的宽带订单数量"""
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 执行SQL查询
        query = f'''
            SELECT 地市, strftime('%m', 订单时间) AS 订单月份, COUNT(*) AS 订单数量
            FROM {table_name}
            WHERE 产品类型 = '宽带'
            GROUP BY 地市, 订单月份
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        # 转换为DataFrame
        df = pd.DataFrame(results, columns=['地市', '订单月份', '订单数量'])

        # 将月份列的值转换为带有“月”字的格式
        df['订单月份'] = df['订单月份'].astype(int).astype(str) + '月'

        return df

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = 'b2c.db'  # 替换为你的数据库路径
    table_name = 'A2023'  # 要查询的表名

    df = query_city_monthly_orders(db_path, table_name)

    # 计算每个地市1-12月的订单合计
    city_totals = df.groupby('地市')['订单数量'].sum().reset_index()
    city_totals['订单月份'] = '总计'
    df = pd.concat([df, city_totals], ignore_index=True)

    # 计算每个月所有地市的订单合计
    month_totals = df.groupby('订单月份')['订单数量'].sum().reset_index()
    month_totals['地市'] = '总计'
    df = pd.concat([df, month_totals], ignore_index=True)

    # 生成透视表
    pivot_table = df.pivot_table(index='地市', columns='订单月份', values='订单数量', fill_value=0)

    # 指定地市排序顺序
    city_order = ['哈尔滨', '齐齐哈尔', '牡丹江', '佳木斯', '绥化', '大庆', '鸡西', '黑河', '伊春', '双鸭山', '鹤岗', '七台河', '大兴安岭', '总计']
    pivot_table = pivot_table.reindex(city_order)

    # 指定月份排序顺序
    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '总计']
    pivot_table = pivot_table[month_order]

    # 打印结果
    print(pivot_table)

    # 生成当前日期和时间的字符串
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 生成文件名
    file_name = f"{current_datetime}.csv"
    # 保存结果到CSV文件
    pivot_table.to_csv(file_name)
    print(f"结果已保存到文件: {file_name}")

    # 设置中文字体
    font_path = 'C:/Windows/Fonts/simhei.ttf'  # 替换为你系统中支持中文的字体路径
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # 绘制热力图
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': '订单数量'})
    plt.title('2023年分地市宽带订单', fontproperties=font_prop)
    plt.xlabel('Month', fontproperties=font_prop)
    plt.ylabel('City', fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)
    plt.tight_layout()
    plt.show()

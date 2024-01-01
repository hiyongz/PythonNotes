import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows
# 创建数据集
data = {'城市': ['北京', '上海', '广州', '深圳'],
        '销量': [100, 200, 300, 400]}
df = pd.DataFrame(data)
 
# 将数据写入Excel文件
wb = Workbook()
ws = wb.active
for r in dataframe_to_rows(df, index=False):
    ws.append(r)
 
# 创建条形图
bar_chart = BarChart()
values = Reference(ws, min_col=2, max_col=2, min_row=1, max_row=len(df))
categories = Reference(ws, min_col=1, max_col=1, min_row=2, max_row=len(df)+1)
bar_chart.add_data(values, titles_from_data=True)
bar_chart.set_categories(categories)
 
# 添加图表到工作表
sheet = wb['Sheet']
sheet.add_chart(bar_chart, "E5")
 
# 保存Excel文件
wb.save("output.xlsx")
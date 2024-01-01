from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font 
from openpyxl.styles import Alignment 

import pandas as pd

data = {
    "姓名": ["张三", "李四"],
    "性别": ["男", "女"],
    "年龄": [15, 25],
}
df = pd.DataFrame(data)


wb = Workbook()
ws = wb.active

for row in dataframe_to_rows(df, index=False, header=True):
    ws.append(row)
    
font = Font(name="微软雅黑",size=10, bold=True,italic=False,color="FF0000")
alignment = Alignment(horizontal="center",vertical="center")
    
for i in range(1,df.shape[1]+1):
    cell = ws.cell(row=1, column=i)
    print(cell.value)
    cell.font = font
    cell.alignment = alignment
    
wb.save("pandas.xlsx")
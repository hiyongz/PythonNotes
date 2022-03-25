import glob
import os
import time

import pandas as pd

class excelConvert():

    def __init__(self):
        self.path = os.getcwd()  # 当前工作路径
        xlsxdirname = "xlsx"
        xlsxpath = os.path.join(self.path, xlsxdirname)

        if not os.path.exists(xlsxpath):
            print(f"创建文件夹: {xlsxdirname}")
            os.makedirs(xlsxpath)
        self.xlsxpath = xlsxpath

    def batch_convert(self):
        xls_files = glob.glob(self.path + "/*.xls")
        if len(xls_files) != 0:
            print('当前目录下的xls格式文件：')
            for file in xls_files:
                print(os.path.basename(file))
                data = self.readxls(file)

                fname, _ = os.path.splitext(file)
                basename = os.path.basename(fname)
                xlsxpathname = os.path.join(self.xlsxpath, basename)
                self.saveasxlsx(data, xlsxpathname)
        else:
            print('该目录下无xls格式文件，即将退出...')
            time.sleep(2)
            os._exit(0)

    def readxls(self, filepath):
        data = pd.DataFrame(pd.read_excel(filepath))  # 读取xls文件
        return data

    def saveasxlsx(self, data, filename):
        data.to_excel(filename + '.xlsx', index=False)  # 保存为xlsx格式

if __name__=='__main__':
    excel = excelConvert()
    excel.batch_convert()
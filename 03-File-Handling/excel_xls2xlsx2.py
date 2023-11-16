import win32com.client as win32

fname = "D:\\pythonproj\\PythonNotes\\03-File-Handling\\11AX_beacon] 协议一致性.xls"
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(fname)

wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
wb.Close()                               #FileFormat = 56 is for .xls extension
excel.Application.Quit()
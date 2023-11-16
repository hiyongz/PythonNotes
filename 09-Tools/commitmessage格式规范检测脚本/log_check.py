import os
from time import sleep

class Log_Check():
    
    def __init__(self):
        self.NewChipModelList = []
        self.LogList = []
        self.ExcelName = ''
        self.NewModelOwnerList = []
        self.result = 0
        os.popen("python3 -m pip install xlrd-2.0.1.tar.gz").readlines()

    def getChipModel(self):
        # 切换至上层目录
        os.chdir('../')
        # 切换至build目录
        os.chdir('build')
        # 获取芯片方案目录
        ChipModelList = os.popen("ls -F | grep '/$'").readlines()
        for i in ChipModelList:
            i = i.replace('/','')
            i = i.strip('\n')
            # 生成处理好的芯片方案列表
            self.NewChipModelList.append(i)

    def getLog(self,args):
        # 获取最新一条git log日志
        LogListAll = os.popen("git log -n 1").readlines()
        # 取log日志中的第五段，即提交的log文本内容
        StrLogList = LogListAll[4]
        StrLogList = StrLogList.strip()
        # 检查Log中的'[]'对数是否满足9条
        # StrLogList = args
        self.strLensCheck(StrLogList)
        # 将获取到的文本中的']'删除，然后用'['进行数据分割
        NewStrLogList = StrLogList.replace(' ','')
        NewStrLogList = NewStrLogList.replace('[','')
        NewLogList = NewStrLogList.split(']')
        NewLogList = NewLogList[0:9]
        self.LogList = NewLogList

    # 对log日志中的[]对数进行检查
    def strLensCheck(self,args):
        ArgsList = list(args)
        if ArgsList.count('[') == 9 and ArgsList.count(']') == 9:
            return True
        else:
            StrLensError = 'Log日志中的[]数量应为9对，请检查'
            print(StrLensError)
            raise 

    def startLogCheck(self):
        print("##########################")
        print("# 开始日志检查")
        Counter = 0
        if self.LogList[0] == '技术项':
            print("# 0.触发动作检查通过")
            self.tecItemsCheck()
        elif self.LogList[0] == '方案导入':
            print("# 0.触发动作检查通过")
            self.tecItemsCheck()
        elif self.LogList[0] == '新需求':
            print("# 0.触发动作检查通过")
            self.tecItemsCheck()
        elif self.LogList[0] == '模块优化':
            print("# 0.触发动作检查通过")
            self.moduleOptimCheck()
        elif self.LogList[0] == 'Debug':
            print("# 0.触发动作检查通过")
            self.DebugCheck()
        elif self.LogList[0] == 'debug':
            print("# 0.触发动作检查通过")
            self.DebugCheck()
        elif self.LogList[0] == '版本发布':
            print("# 0.触发动作检查通过")
            self.releaseCheck()
        else:
            print("触发动作 %s 填写错误,请修改"%self.LogList[0])
            raise
        print("# 结束日志检查")
        print("##########################")
        return self.result
   
    # 技术项log字段检查
    def tecItemsCheck(self):
        Counter = 0
        # 判断模块名是否正确
        for i in self.NewModelOwnerList:
            if self.LogList[1] in i:
                Counter += 1
                print("# 1.模块检查通过")
                break
        else:
            print("当前log模块名错误,%s不在归属模块列表,请修改"%self.LogList[1])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断描述是否正确
        if self.LogList[2] != '':
            Counter += 1
            print("# 2.描述检查通过")
        else:
            print("当前log描述为空,请修改")
        # 判断责任田主是否正确
        # 将[田主:XXX] 分割为田主和XXX
        if ':' in self.LogList[3]:
            self.OwnerOrInspector = self.LogList[3].split(':')[0]
            self.LogList[3] = self.LogList[3].split(':')[1]
        elif '：':
            self.OwnerOrInspector = self.LogList[3].split('：')[0]
            self.LogList[3] = self.LogList[3].split('：')[1]
        else:
            print("此次应填写 [田主:XXX]")
        for i in self.NewModelOwnerList:
            if self.LogList[3] in i:
                if self.OwnerOrInspector == '田主':
                    Counter += 1
                    print("# 3.田主检查通过")
                    break
                else:
                    print("此次应填写 [田主:XXX]")
        else:
            print("当前log责任田主错误,%s不在责任田主列表,请修改"%self.LogList[3])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断模块和责任田主组合是否与 规范一致
        LogModelOwner = self.LogList[1]+'|'+self.LogList[3]
        if LogModelOwner in self.NewModelOwnerList:
            Counter += 1
        else:
            print("当前log模块和责任田主对应错误,%s,请修改"%LogModelOwner)
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        if 'Bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        elif 'bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        else:
            print("当前log Bugid字段错误,请修改")
            print("无Bugid时填写：[Bugid:]")
            print("有Bugid时填写：[Bugid:100]")
        if '原厂patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        elif '原厂Patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        else:
            print("当前log原厂patch字段错误,请修改")
            print("无原厂patch时填写：[原厂patch:]")
            print("有原厂patch时填写：[原厂patch:patch名]")
        # 判断芯片方案是否在芯片方案列表中
        if self.LogList[6] in self.NewChipModelList:
            Counter += 1
            print("# 6.芯片方案检查通过")
        else:
            print("当前log芯片方案错误,%s不在芯片方案列表,请修改"%self.LogList[6])
            print("已有芯片方案列表如下：\n%s"%self.NewChipModelList)
        if self.LogList[7] != '':
            Counter += 1
            print("# 7.产品字段检查通过")
        else:
            print("当前log产品为空,请填写")
        if self.LogList[8] != '':
            if not self.isEnglish(self.LogList[8]):
                if self.isChinese(self.LogList[8]):
                    Counter += 1
                    print("# 8.修改者字段检查通过")
                else:
                    print("请将修改者姓名填写为中文名")
            else:
                print("当前log修改者姓名为英文,请修改为中文")
        else:
            print("当前log修改者为空,此字段为必填字段，请填写修改者中文姓名")
        if Counter == 9:
            self.result = 1
            print("log日志检查通过")
        else:
            self.result = 0
            print("log日志未按要求填写，请完成修改")
    # 方案导入log字段检查
    def schemeImportCheck(self):
        pass
    
    # 新需求log字段检查
    def newDemandCheck(self):
        pass

    # 模块优化log字段检查
    def moduleOptimCheck(self):
        Counter = 0
        # 判断模块名是否正确
        for i in self.NewModelOwnerList:
            if self.LogList[1] in i:
                Counter += 1
                print("# 1.模块检查通过")
                break
        else:
            print("当前log模块名错误,%s不在归属模块列表,请修改"%self.LogList[1])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断描述是否正确
        if self.LogList[2] != '':
            Counter += 1
            print("# 2.描述检查通过")
        else:
            print("当前log描述为空,请修改")
        # 判断责任田主是否正确
        # 将[田主:XXX] 分割为田主和XXX
        if ':' in self.LogList[3]:
            self.OwnerOrInspector = self.LogList[3].split(':')[0]
            self.LogList[3] = self.LogList[3].split(':')[1]
        elif '：':
            self.OwnerOrInspector = self.LogList[3].split('：')[0]
            self.LogList[3] = self.LogList[3].split('：')[1]
        else:
            print("此次应填写 [田主:XXX]")
        for i in self.NewModelOwnerList:
            if self.LogList[3] in i:
                if self.OwnerOrInspector == '田主':
                    Counter += 1
                    print("# 3.田主检查通过")
                    break
                else:
                    print("此次应填写 [田主:XXX]")
        else:
            print("当前log责任田主错误,%s不在责任田主列表,请修改"%self.LogList[3])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断模块和责任田主组合是否与 规范一致
        LogModelOwner = self.LogList[1]+'|'+self.LogList[3]
        if LogModelOwner in self.NewModelOwnerList:
            Counter += 1
        else:
            print("当前log模块和责任田主对应错误,%s,请修改"%LogModelOwner)
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        if 'Bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        elif 'bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        else:
            print("当前log Bugid字段错误,请修改")
            print("无Bugid时填写：[Bugid:]")
            print("有Bugid时填写：[Bugid:100]")
        if '原厂patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        elif '原厂Patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        else:
            print("当前log原厂patch字段错误,请修改")
            print("无原厂patch时填写：[原厂patch:]")
            print("有原厂patch时填写：[原厂patch:patch名]")
        # 判断芯片方案
        if '芯片方案' in self.LogList[6]:
            Counter += 1
            print("# 6.芯片方案检查通过")
        else:
            print("当前log芯片方案为可选字段，填写格式为[芯片方案:],请修改")
        if self.LogList[7] != '':
            Counter += 1
            print("# 7.产品字段检查通过")
        else:
            print("当前log产品为空,请填写")
        if self.LogList[8] != '':
            if not self.isEnglish(self.LogList[8]):
                if self.isChinese(self.LogList[8]):
                    Counter += 1
                    print("# 8.修改者字段检查通过")
                else:
                    print("请将修改者姓名填写为中文名")
            else:
                print("当前log修改者姓名为英文,请修改为中文")
        else:
            print("当前log修改者为空,此字段为必填字段，请填写修改者中文姓名")
        if Counter == 9:
            self.result = 1
            print("log日志检查通过")
        else:
            self.result = 0
            print("log日志未按要求填写，请完成修改")

    # Debug log字段检查
    def DebugCheck(self):
        Counter = 0
        # 判断模块名是否正确
        for i in self.NewModelOwnerList:
            if self.LogList[1] in i:
                Counter += 1
                print("# 1.模块检查通过")
                break
        else:
            print("当前log模块名错误,%s不在归属模块列表,请修改"%self.LogList[1])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断描述是否正确
        if self.LogList[2] != '':
            Counter += 1
            print("# 2.描述检查通过")
        else:
            print("当前log描述为空,请修改")
        # 判断责任田主是否正确
        # 将[田主:XXX] 分割为田主和XXX
        if ':' in self.LogList[3]:
            self.OwnerOrInspector = self.LogList[3].split(':')[0]
            self.LogList[3] = self.LogList[3].split(':')[1]
        elif '：':
            self.OwnerOrInspector = self.LogList[3].split('：')[0]
            self.LogList[3] = self.LogList[3].split('：')[1]
        else:
            print("此次应填写 [田主:XXX]")
        for i in self.NewModelOwnerList:
            if self.LogList[3] in i:
                if self.OwnerOrInspector == '田主':
                    Counter += 1
                    print("# 3.田主检查通过")
                    break
                else:
                    print("此次应填写 [田主:XXX]")
        else:
            print("当前log责任田主错误,%s不在责任田主列表,请修改"%self.LogList[3])
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 判断模块和责任田主组合是否与 规范一致
        LogModelOwner = self.LogList[1]+'|'+self.LogList[3]
        if LogModelOwner in self.NewModelOwnerList:
            Counter += 1
        else:
            print("当前log模块和责任田主对应错误,%s,请修改"%LogModelOwner)
            print("已有归属模块和责任田主列表如下：\n%s"%self.NewModelOwnerList)
        # 检查bugid内容是否为空
        BugId = self.LogList[4]
        if ':' in BugId:
            BugId = BugId.split(':')[1]
        elif '：' in BugId:
            BugId = BugId.split(':')[1]
        else:
            print("Bugid必填时填写：[Bugid:xxx]")
        if BugId != '':
            Counter += 1
            print("# 4.Bugid检查通过")
        else:
            print("当前log Bugid字段为必填,请修改")
            print("Bugid必填时填写：[Bugid:xxx]")
        if '原厂patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        elif '原厂Patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        else:
            print("当前log原厂patch字段错误,请修改")
            print("无原厂patch时填写：[原厂patch:]")
            print("有原厂patch时填写：[原厂patch:patch名]")
        # 判断芯片方案是否在芯片方案列表中
        if self.LogList[6] in self.NewChipModelList:
            Counter += 1
            print("# 6.芯片方案检查通过")
        else:
            print("当前log芯片方案错误,%s不在芯片方案列表,请修改"%self.LogList[6])
            print("已有芯片方案列表如下：\n%s"%self.NewChipModelList)
        if self.LogList[7] != '':
            Counter += 1
            print("# 7.产品字段检查通过")
        else:
            print("当前log产品为空,请填写")
        if self.LogList[8] != '':
            if not self.isEnglish(self.LogList[8]):
                if self.isChinese(self.LogList[8]):
                    Counter += 1
                    print("# 8.修改者字段检查通过")
                else:
                    print("请将修改者姓名填写为中文名")
            else:
                print("当前log修改者姓名为英文,请修改为中文")
        else:
            print("当前log修改者为空,此字段为必填字段，请填写修改者中文姓名")
        if Counter == 9:
            self.result = 1
            print("log日志检查通过")
        else:
            self.result = 0
            print("log日志未按要求填写，请完成修改")

    # 版本发布log字段检查
    def releaseCheck(self):
        Counter = 0
        # 判断发布类型是否 为Release or Bootloder
        ModelList = ['Release','Bootloder']
        if self.LogList[1] in ModelList:
            Counter += 1
            print("# 1.发布类型检查通过")
        else:
            print("当前log发布类型%s不在%s中，请修改"%(self.LogList[1],ModelList))
        # 判断描述是否正确
        if self.LogList[2] != '':
            Counter += 1
            print("# 2.描述检查通过")
        else:
            print("当前log描述为空,请修改")
        # 判断主检视人否为中文
        # 将[主检视人:XXX] 分割为主检视人和XXX
        if ':' in self.LogList[3]:
            self.OwnerOrInspector = self.LogList[3].split(':')[0]
            self.LogList[3] = self.LogList[3].split(':')[1]
        elif '：':
            self.OwnerOrInspector = self.LogList[3].split('：')[0]
            self.LogList[3] = self.LogList[3].split('：')[1]
        else:
            print("此次应填写 [主检视人:XXX]")
        if self.isChinese(self.LogList[3]):
            if self.OwnerOrInspector == '主检视人':
                Counter += 1
                print("# 3.主检视人检查通过")
            else:
                print("此次应填写 [主检视人:XXX]")
        else:
            print("请将主检视人姓名填写为中文名")
        if 'Bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        elif 'bugid' in self.LogList[4]:
            Counter += 1
            print("# 4.Bugid检查通过")
        else:
            print("当前log Bugid字段错误,请修改")
            print("无Bugid时填写：[Bugid:]")
            print("有Bugid时填写：[Bugid:100]")
        if '原厂patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        elif '原厂Patch' in self.LogList[5]:
            Counter += 1
            print("# 5.原厂patch检查通过")
        else:
            print("当前log原厂patch字段错误,请修改")
            print("无原厂patch时填写：[原厂patch:]")
            print("有原厂patch时填写：[原厂patch:patch名]")
        # 判断芯片方案是否在芯片方案列表中
        if self.LogList[6] in self.NewChipModelList:
            Counter += 1
            print("# 6.芯片方案检查通过")
        else:
            print("当前log芯片方案错误,%s不在芯片方案列表,请修改"%self.LogList[6])
            print("已有芯片方案列表如下：\n%s"%self.NewChipModelList)
        if '产品'in self.LogList[7]:
            Counter += 1
            print("# 7.产品字段检查通过")
        else:
            print("当前log产品字段错误,请修改")
            print("无产品时填写：[产品:]")
            print("有产品时填写：[产品:产品名]")

        if self.LogList[8] != '':
            if not self.isEnglish(self.LogList[8]):
                if self.isChinese(self.LogList[8]):
                    Counter += 1
                    print("# 8.修改者字段检查通过")
                else:
                    print("请将修改者姓名填写为中文名")
            else:
                print("当前log修改者姓名为英文,请修改为中文")
        else:
            print("当前log修改者为空,此字段为必填字段，请填写修改者中文姓名")
        if Counter == 9:
            self.result = 1
            print("log日志检查通过")
        else:
            self.result = 0
            print("log日志未按要求填写，请完成修改")

    # 获取模块名和责任田主
    def readExcel(self):
        # 导入 xlrd 模块
        import xlrd
        # 切换至上层目录
        os.chdir('../')
        # 切换至build目录
        os.chdir('docs/source/ugw')
        Ex = xlrd.open_workbook(self.ExcelName)
        Wifi = Ex.sheet_by_name('WIFI')
        Km = Ex.sheet_by_name('KM')
        Cbb = Ex.sheet_by_name('CBB')
        Bsp = Ex.sheet_by_name('BSP')
        AllData = []
        # 获取wifi领域的模块和责任田
        for i in range(Wifi.nrows):
            if i > 1:
                WifiCells = Wifi.row_values(i)
                # 将模块名(第6列)和责任田主（第7列）的组合加入AllData
                AllData.append(WifiCells[5]+'|'+WifiCells[6])
            else:
                continue

        # 获取km领域的模块和责任田
        for i in range(Km.nrows):
            if i > 1:
                KmCells = Km.row_values(i)
                # 将模块名(第5列)和责任田主（第6列）的组合加入AllData
                AllData.append(KmCells[4]+'|'+KmCells[5])
            else:
                continue

        # 获取Cbb领域的模块和责任田
        for i in range(Cbb.nrows):
            if i > 1:
                CbbCells = Cbb.row_values(i)
                # 将模块名(第6列)和责任田主（第7列）的组合加入AllData
                AllData.append(CbbCells[5]+'|'+CbbCells[6])
            else:
                continue

        # 获取Bsp领域的模块和责任田
        for i in range(Bsp.nrows):
            if i > 1:
                BspCells = Bsp.row_values(i)
                # 将模块名(第6列)和责任田主（第7列）的组合加入AllData
                AllData.append(BspCells[5]+'|'+BspCells[6])
            else:
                continue
        # 对AllData进行去重
        self.NewModelOwnerList = list(set(AllData))

    def isChinese(self,character):
        '''判断是否存在为中文字符'''
        for cha in character:
            if  '\u0e00' <= cha <= '\u9fa5':
                return True
        else:
            return False

    def isEnglish(self,character):
        '''判断是否为英文字母'''
        for cha in character:
            if not 'A' <= cha <= 'Z' and not 'a' <= cha <= 'z':
                return False
        else:
            return True

if __name__ == '__main__':

    lc = Log_Check()
    lc.getChipModel()
    lc.ExcelName = 'UGW需求基线.xls'
    args = '[方案导入] [系统安全][子节点] [田主:熊相权][bugid：][原厂 patch：][bcm6750_6715_11ax_mesh] [MX15V1.0][钟博]'
    # args = input('input log:')
    lc.getLog(args)
    lc.readExcel()
    lc.startLogCheck()

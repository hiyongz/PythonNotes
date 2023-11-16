# encoding=gbk
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xlutils.copy import copy
from copy import deepcopy
import xlwt
import xlrd
import re
import os, sys, shutil
# from getpic import easyExcel, get_picture
import traceback

# ������ʽ
p = re.compile(r"<table.*>.*?</table>", re.S)
p_tr = re.compile(r"<tr.*?>.*?</tr>", re.S)
p_td = re.compile(r"<td.*?>(.*?)</td>", re.S)
# ����
titles = {0: u'ID', 1: u'������', 2: u'ժҪ', 3: u'''�ؼ�����(�ص���"��ʲô"��������"��ô��")''', 4: u"���Ե�", 5: u"Pri", 6: u"��ʽ",
          7: u'''��ʱ(�ֶ�=>�Զ���)''', 8: u"����Դ"}
# ���з�ʽ
execmap = {"1": u"�ֶ�", "2": u"�Զ�", '3': '����'}
# ���ȼ�
primap = {"1": u"��", "2": u"��", "3": u"��", "4": u"��"}
# �п�
widths = {0: 1, 1: 3, 2: 3, 3: 5, 4: 3, 5: 3, 6: 2, 7: 1}
replacement = {r"&amp;": r"&", r"&lt;": r"<", r"&gt;": r">", r"&apos;": r"'", r"&quot;": r'"'}
htmlchars = [r'<p>', r'</p>']
# ÿһ���������ڵ�����
idcol = 0
itemcol = 1
summcol = 2
actioncol = 3
casecol = 4
pricol = 5
execcol = 6
timecol = 7
datacol = 8
wunit = 2962
# ������
font = xlwt.Font()
font.name = u'����'
font.blod = True
font.size = 9

font0 = xlwt.Font()
font0.name = u'����'
font0.blod = True
font0.colour_index = 0x38
font0.size = 9

style = xlwt.XFStyle()
al = xlwt.Alignment()
# ���뷽ʽ
al.vert = xlwt.Alignment.VERT_CENTER
al.horz = xlwt.Alignment.HORZ_CENTER
style.alignment = al
style.font = font

stype_h_l = xlwt.XFStyle()
al_h_l = xlwt.Alignment()
al_h_l.horz = xlwt.Alignment.HORZ_LEFT
al_h_l.vert = xlwt.Alignment.VERT_CENTER
# �Զ��س�
al_h_l.wrap = xlwt.Alignment.WRAP_AT_RIGHT
stype_h_l.alignment = al_h_l
stype_h_l.font = font

stype_data_color = xlwt.XFStyle()
stype_data_color.alignment = al_h_l
stype_data_color.font = font0

style1 = xlwt.XFStyle()
al_1 = xlwt.Alignment()
al_1.wrap = xlwt.Alignment.WRAP_AT_RIGHT
style1.alignment = al_1
style1.font = font


# ����HTML��ʽ�� ����Դ�ı��


def tableparse(summary):
    tabledata = {}
    tabledata['data'] = {}
    tabledata['title'] = None
    ret = p.search(summary)
    tbdata = None
    if ret:
        tbdata = ret.group()
    else:
        return
    trs = p_tr.findall(tbdata)
    datalen = len(trs)
    titles = trs[1]
    titles = p_td.findall(titles)[4:]
    trs = trs[2:]
    index = 0
    for trdata in trs:
        tds = p_td.findall(trdata)
        tds = tds[4:]
        index += 1;
        tabledata['data'][index] = tds
    tabledata['title'] = titles
    return tabledata


# ͨ�õı�����������2ά���ֵ䣬������/�� ������
def table_case_parse(summary):
    tabledata = {}
    tabledata['data'] = {}
    tabledata['title'] = None
    if not summary:
        return None
    ret = p.search(summary)
    tbdata = None
    if ret:
        tbdata = ret.group()
    else:
        return
    trs = p_tr.findall(tbdata)
    datalen = len(trs)
    titles = trs[0]
    titles = p_td.findall(titles)
    for trdata in trs[1:]:
        tds = p_td.findall(trdata)
        tabledata['data'] = tds
    tabledata['title'] = titles
    return tabledata


def table2dict(tb):
    if not tb: return
    tabledata = {}
    ret = p.search(tb)
    if ret:
        tbdata = ret.group()
    else:
        return
    index_tr = 0
    index_td = 0
    trs = p_tr.findall(tbdata)
    for trdata in trs:
        tabledata[index_tr] = {}
        tds = p_td.findall(trdata)
        index_td = 0
        for td in tds:
            tabledata[index_tr][index_td] = td.strip()
            index_td += 1
        index_tr += 1
    return tabledata


def xml2excels(filename):
    tree = ElementTree(file=filename)
    root = tree.getroot()
    rootname = root.attrib.get('name')
    # if rootname!='':


def xml2excel(filename, targetname, addargs=None):
    # xlsname=filename+u".xls"
    xlsname = targetname
    # backfile(xlsname)
    # ��Excel,��ӹ�����
    w = xlwt.Workbook(encoding='gbk')
    ws = w.add_sheet(u'��������', cell_overwrite_ok=True)
    ws1 = w.add_sheet(u'����ͼ', cell_overwrite_ok=True)
    # ���ɱ���
    for (key, value) in titles.items():
        ws.write(0, key, value)
    # ���ÿ��
    wunit = 1962
    for (key, value) in widths.items():
        ws.col(key).width = value * wunit
    # ��XML�ļ����д���
    # 1. ȥ��HTML�ַ�
    # replacement={r"&amp;":r"&",r"&lt;":r"<",r"&gt;":r">",r"&apos;"��r"'",r"&quot;":r'"'}
    # htmlchars=[r'<p>',r'</p>']
    # 2. ת�������ַ�
    # filefd = open(filename,encoding='utf-8')
    # file_content = filefd.read()
    # # for (key,value) in replacement.items():
    # # file_content=file_content.replace(key,value)
    # for char in htmlchars:
    #     file_content = file_content.replace(char, '')
    # filefd.close()
    # filefd = open(filename, 'w')
    # filefd.write(file_content)
    # filefd.close()
    # ��ʼ����XML
    print(u'��ʼ����')
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    rootname = root.attrib.get('name')
    rootindex = rootname.split("]")[0]
    root_detail = None
    # if rootindex.find(".")==-1:
    if not re.search('\.[A-Z]', rootindex):
        test_suites = root.findall('.//testsuite')
    elif len(rootindex.split('.')) == 2:
        test_suites = (root,)
    else:
        print(u"����Ĳ�Σ�ֻ���� һ�����߶���ģ�鵼��XML")
        return False
    row_begin = 1;
    images = ''
    data_source_max = 0;
    for sub_model in test_suites:
        childrens = sub_model.getchildren()
        tss = {}
        # ����xml��ʽ�����ݣ����浽tss�ֵ��ʽ��
        for children in childrens:
            # ������testsuite
            if children.tag == "details":
                root_detail = children.text
            if children.tag != 'testsuite': continue
            test_suite = children
            tsname = test_suite.attrib.get('name')
            tsname_short = tsname[:tsname.find("]")]
            tsname_short_index = tsname_short[tsname_short.rfind(".") + 1:]
            # ��ȡ���Լ� ��Ϣ
            tss[tsname_short_index] = {}
            tss[tsname_short_index]['name'] = tsname
            tss[tsname_short_index]['index'] = tsname_short_index
            tss[tsname_short_index]['details'] = test_suite.find('.//details').text
            tss[tsname_short_index]['case'] = {}
            test_cases = test_suite.findall('.//testcase')
            # ��ȡ����������Ϣ
            for test_case in test_cases:
                tcname = test_case.attrib.get('name')
                if tcname.find('Sum]') != -1:
                    tcname_index = 'Sum'
                    # print("tcname_index:",tcname_index)
                    tss[tsname_short_index]['case'][tcname_index] = {}
                    stepsobj = test_case.find('.//steps')
                    preobj = test_case.find('.//preconditions')
                    pretext = ""
                    if preobj is not None:
                        pretext = preobj.text
                    if pretext:
                        images += pretext;
                    # if pretext:
                    # print(pretext)
                    # ��ȡ���Բ�����Ϣ
                    steps = []
                    if stepsobj is not None:
                        # expects=[]
                        for stepobj in stepsobj:
                            steps.append(stepobj.find('.//actions').text)
                            # expects.append(stepobj.find('.//expectedresults').text)
                    tss[tsname_short_index]['case'][tcname_index]['steps'] = deepcopy(steps)
                    # tss[tsname_short_index]['case'][tcname_index]['expects']=deepcopy(expects)
                    tcname_index_1 = tcname.split(".")[-2]
                    # ��ȡժҪ��Ϣ����html table ��ʽ����� ����Դ
                    if tcname_index_1 != "0" and tcname_index_1 != "c":
                        summaryobj = test_case.find('.//summary')
                        summary = summaryobj.text
                        tss[tsname_short_index]['case'][tcname_index]['summary'] = summary
                # ����ÿһ��������������Ϣ
                else:
                    tcname_index = tcname.split(")")[0].split(".")[-1]
                    tss[tsname_short_index]['case'][tcname_index] = {}
                    tss[tsname_short_index]['case'][tcname_index]['exectype'] = test_case.find('execution_type').text
                    tss[tsname_short_index]['case'][tcname_index]['importance'] = test_case.find('importance').text
                    if test_case.find('auto_exec_duration'):
                        tss[tsname_short_index]['case'][tcname_index]['auto_exec_duration'] = test_case.find(
                            'auto_exec_duration').text
                    else:
                        tss[tsname_short_index]['case'][tcname_index]['auto_exec_duration'] = "1"

                    if test_case.find('estimated_exec_duration'):
                        tss[tsname_short_index]['case'][tcname_index]['estimated_exec_duration'] = test_case.find(
                            'estimated_exec_duration').text
                    else:
                        tss[tsname_short_index]['case'][tcname_index]['estimated_exec_duration'] = "1"
                    tss[tsname_short_index]['case'][tcname_index]['summary'] = test_case.find('summary').text
                tss[tsname_short_index]['case'][tcname_index]['name'] = tcname
                tss[tsname_short_index]['case'][tcname_index]['index'] = tcname_index

        tss_keys = tss.keys()
        if not tss: continue
        if "C" in tss_keys:
            tss_keys.remove("C")
        tss_keys.sort(key=lambda x: int(x))
        tss_keys.append("C")
        # д�뵽excel�ļ���
        for ts in tss_keys:
            tsname = tss[ts]['name'].strip()
            tsindex = tss[ts]['index']
            tssummary = tss[ts]['details']

            # д��case 0
            if tsindex == '0':
                ws.write(row_begin, idcol, tsindex, style)
                ws.write(row_begin, itemcol, tsname, style)
                # ����
                steps = "\n".join(tss[ts]['case']['Sum']['steps'])
                # expects="\n".join(tss[ts]['case']['Sum']['expects'])
                ws.write(row_begin, actioncol, steps, stype_h_l)
                # ws.write(row_begin,expectcol,expects,stype_h_l)
                ws.write(row_begin, casecol, u'0) ģ�黷������', stype_h_l)

                # ��ʼ����ͼƬ

                row_begin += 2
            if tsindex != '0' and tsindex != 'C' and tsindex != 'c':
                # д��case
                cases = tss[ts]['case'].keys()
                cases.sort()
                casecount = len(cases)
                row_end = row_begin + casecount + 1
                ws.write_merge(row_begin, row_end - 1, idcol, idcol, tsindex, stype_h_l)
                ws.write_merge(row_begin, row_end - 1, itemcol, itemcol, tsname, stype_h_l)
                ws.write_merge(row_begin, row_end - 1, summcol, summcol, tssummary, stype_h_l)
                if 'Sum' not in tss[ts]['case']:
                    print(u"����û��.Sum�벹��")
                    steps = tss[ts]['case']['Sum']['steps']
                    keyword = "//Before"
                    try:
                        bfind = False;
                        index_keyword = 0;
                        for step in steps:
                            if step.find(keyword) != -1:
                                bfind = True
                                break
                            index_keyword += 1;
                        if bfind:
                            before_index_steps = index_keyword;
                        else:
                            before_index_steps = 1;
                    except:
                        print("steps", "\n".join(steps), tsindex)
                        traceback.print_exc()
                        return False
                    # before_index_expects=expects.index(keyword)
                    before_steps = steps[1:before_index_steps]
                    # before_expects=expects[1:before_index_expects]
                    ws.write(row_begin, actioncol, "\n".join(before_steps), stype_h_l)
                    # ws.write(row_begin,expectcol,"\n".join(before_expects),stype_h_l)
                    ws.write(row_begin, casecol, u"0) //BeforItem", stype_h_l)

                    # ���AfterItem���⴦��
                    After_col = row_begin + casecount
                    print("tsname=", tsname)
                    print("steps=", steps)

                    after_index_steps = steps.index('//AfterItem')
                    # after_index_expects=expects.index('//AfterItem')
                    after_steps = steps[after_index_steps + 1:]
                    # after_expects=expects[after_index_expects+1:]
                    ws.write(After_col, actioncol, "\n".join(after_steps), stype_h_l)
                    # ws.write(After_col,expectcol,"\n".join(after_expects),stype_h_l)
                    ws.write(After_col, casecol, u"C) //AfterItem", stype_h_l)
                    # ������������
                    steps = steps[before_index_steps:after_index_steps]
                    # expects=expects[before_index_steps:after_index_steps]
                    steps = "\n".join(steps)
                    # expects="\n".join(expects)
                    if After_col - row_begin > 2:
                        ws.write_merge(row_begin + 1, After_col - 1, actioncol, actioncol, steps, stype_h_l)
                    else:
                        ws.write(row_begin + 1, actioncol, steps, stype_h_l)
                    # ws.write_merge(row_begin+1,After_col-1,expectcol,expectcol,expects,stype_h_l)
                    currindex = 1
                    dataindex = 1;
                    # ��ȡ����ֵ
                    for case in cases:
                        casename = tss[ts]['case'][case]['name']
                        if casename.endswith("Sum]") or casename.endswith("Sum)"):
                            summary = tss[ts]['case'][case]['summary']
                            # ����Դ�Ĵ���
                            # tabledata=tableparse(summary.encode('gbk'))
                            # if tabledata:
                            # datatitle=tabledata['title'];
                            # datavalue=tabledata['data'];
                            # ws.write_merge(0,0,datacol,datacol+len(datatitle),u"����Դ")
                            # for i in range(len(datatitle)):
                            # ws.write(row_begin,datacol+i,datatitle[i],stype_data_color)
                            # for key in datavalue:
                            # datarow=row_begin+dataindex
                            # dataindex+=1
                            # for k in range(len(datavalue[key])):
                            # ws.write(datarow,datacol+k,datavalue[key][k],stype_data_color)
                    cases.remove('Sum')
                    cases.sort(key=lambda x: int(x))

                    case_summary = tss[ts]['case'][cases[0]]['summary']
                    case_data = table_case_parse(case_summary)
                    if case_data:
                        for i in range(len(case_data['title'])):
                            ws.write(row_begin, datacol + i, case_data['title'][i], stype_data_color)
                    for case in cases:
                        # д�����������Ϣ
                        caseindex = tss[ts]['case'][case]['index']
                        caseid = caseindex.split(".")[-1]
                        casename = tss[ts]['case'][case]['name']
                        casename = caseid + ")" + ")".join(casename.split(")")[1:])
                        execution_type = tss[ts]['case'][case]['exectype']
                        pri = tss[ts]['case'][case]['importance']
                        auto_exec = tss[ts]['case'][case]['auto_exec_duration']
                        estimated_exec = tss[ts]['case'][case]['estimated_exec_duration']
                        ws.write(row_begin + currindex, casecol, casename, stype_h_l)
                        ws.write(row_begin + currindex, pricol, primap[pri], stype_h_l)
                        ws.write(row_begin + currindex, execcol, execmap[execution_type], stype_h_l)
                        if estimated_exec and auto_exec:
                            ws.write(row_begin + currindex, timecol, estimated_exec + "=>" + auto_exec, stype_h_l)
                        else:
                            ws.write(row_begin + currindex, timecol, "", stype_h_l)
                        # ��������Դ
                        case_summary = tss[ts]['case'][case]['summary']
                        case_data = table_case_parse(case_summary)
                        if case_data:
                            for i in range(len(case_data['title'])):
                                ws.write(row_begin + currindex, datacol + i, case_data['data'][i], stype_data_color)
                            if data_source_max < len(case_data['title']):
                                data_source_max = len(case_data['title'])
                        if case_summary:
                            pass
                        currindex += 1;
                    row_begin = row_end + 1;
                    # д�� �����������Ϣ
            if "C" in tss:
                ts = "C"
                tsname = tss[ts]['name']
                tsindex = tss[ts]['index']
                ws.write(row_begin, idcol, tsindex, style)
                ws.write(row_begin, itemcol, tsname, style)
                steps = "\r\n".join(tss[ts]['case']['Sum']['steps'])
                ws.write(row_begin, actioncol, steps, stype_h_l)
                ws.write(row_begin, casecol, u'C) ģ�黷������', stype_h_l)
                row_begin += 2;
        if data_source_max > 1:
            ws.write_merge(0, 0, 8, 8 + data_source_max - 1, u"����Դ", stype_h_l)
        w.save(xlsname)
        # myExcel = easyExcel(xlsname)  # ʵ����һ��easyExcel��
        # try:
        #     if images:
        #         get_picture(images, myExcel, 2)
        #     myExcel.setserial(1, {pricol + 1: u'��,��,��,��', execcol + 1: u'�ֶ�,�Զ�,����'})
        # except Exception as e:
        #     print(u"��������ͼʱ�����˴���:", str(e))
        #     traceback.print_exc()
        #     return False
        # finally:
        #     myExcel.save()
        #     myExcel.close()
        # if xlsname.endswith('.bak'):
        #     print(u"����ת��Excel���\n", xlsname[:-4])
        # else:
        #     print(u"����ת��Excel���\n", xlsname)
        return True

xml2excel('testsuite-_5G����.xml', 'testsuite-_ 5G����.xls')
print("666")

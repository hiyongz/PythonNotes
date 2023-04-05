#-*-coding:utf-8-*-
# @Time:    2021/10/1 22:26
# @Author:  hiyongz
# @File:    img_style_convert.py
import datetime
import logging
import os,re
import sys
import time
import glob


class Loggers():
    """日志记录器

    记录日志，支持命令行窗口和保存到文件。
    Attributes:
        console_level: 输出到控制台最低的日志严重级别
        file_level: 保存到文件最低的日志严重级别
        fmt: 日志格式化输出样式
        datefmt: 时间格式化
    """
    def __init__(self, console_level = logging.INFO, file_level = logging.INFO, fmt = '%(asctime)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%Y%m%d-%H:%M:%S'):
        self.filename = 'log_' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
        logpath = os.path.join(abspath, 'log') # 日志保存路径
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        self.logname  = os.path.join(logpath, self.filename)
        self.fmt      = fmt
        self.datefmt  = datefmt
        self.console_level = console_level
        self.file_level    = file_level

    def myLogger(self):
        # 创建自定义 logger
        logging.root.setLevel(logging.NOTSET)
        self.logger = logging.getLogger() 
        # 创建处理器 handlers
        console_handler = logging.StreamHandler() # 输出到控制台
        file_handler    = logging.FileHandler(self.logname, mode='w') # 输出到文件
        console_handler.setLevel(self.console_level)
        file_handler.setLevel(self.file_level)
        # 设置日志格式
        format_str  = logging.Formatter(self.fmt, self.datefmt)  # 设置日志格式
        # 将格式器添加到处理器中
        console_handler.setFormatter(format_str)
        file_handler.setFormatter(format_str)
        # 将处理器添加到logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        return self.logger

class blogConvert():
    def __init__(self):
        self.logger = Loggers().myLogger()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))

    def img_convert(self, file):
        self.logger.info('\n当前文件：%s'%file)
        reg_img = r'(?<=src=\").*?(?=\")'# 图片名称
        reg_img2 = r'(?<=!\[).*?(?=\]\()'
        reg_img3 = r'(?<=]\().*?(?=\))'# 图片名称
        reg_img4 = r'<center><b>.*<b></center>'# 图片名称
        reg_heading = r'^#'# 标题

        with open(file, 'r', encoding='utf-8') as f:
            lines = []  # 创建了一个空列表，里面没有元素
            filename = file.split("\\")[-1]
            filename = filename.split(".md")[0]
            for line in f.readlines():
                if re.search("^<img.*/>$", line):
                    img_name = re.findall(reg_img, line)[0]  # 图片名称
                    self.logger.info(line)
                    line1 = f"![]({filename}/{img_name})\n"
                    self.logger.info(line1)
                    lines.append(line1)
                    continue
                if re.search(reg_img2, line):
                    img_name = re.findall(reg_img3, line)[0]  # 图片名称
                    self.logger.info(line)
                    line2 = f"![]({filename}/{img_name})\n"
                    lines.append(line2)
                    self.logger.info(line2)
                    continue
                if re.search(reg_img4, line):
                    lines.append("\n")
                    continue
                if re.search(reg_heading, line):
                    lines.append('#' + line)
                    continue
                lines.append(line)
            f.close()
        with open(file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write('%s' % line)
            f.close()

    def headline_edit(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            reg_title = r"(?<=title: ).*"
            title_block = []
            lines = []
            index = 0
            flag = 0
            for line in f.readlines():
                if len(title_block) == 2 and flag == 0:
                    lines.append(f"# {title_name}\n")
                    flag = 1
                    continue
                elif flag == 1:
                    lines.append(line)
                    continue
                if line == '---\n':
                    title_block.append(index)
                if re.search(reg_title, line):
                    title_name = re.findall(reg_title, line)[0]  # 图片名称
                    self.logger.info(title_name)
                index += 1

            f.close()
        if len(lines) != 0:
            with open(file, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write('%s' % line)
                f.close()

    def appMain(self):
        md_file = []
        if len(sys.argv) < 2:            
            md_file = glob.glob(self.dirpath + "/*.md")
            self.logger.info(md_file)
            if len(md_file) != 0:
                self.logger.info('当前目录下的Markdown文件：')
                for file in md_file:
                    self.logger.info(file)
            else:
                self.logger.warning('该目录下无Markdown文件，即将退出...')
                time.sleep(2)
                os._exit(0)
        else:
            md_file[0] = sys.argv[1]

        for file in md_file:
            if os.path.exists(file) and os.path.isfile(file):
                self.img_convert(file)
                self.headline_edit(file)
            else:
                msg = "未找到文件"
                self.logger.warning(msg)


if __name__=='__main__':
    bg = blogConvert()
    bg.appMain()

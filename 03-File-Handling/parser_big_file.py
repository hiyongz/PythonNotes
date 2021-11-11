

import re
from functools import reduce

class ParserFile():
    def parser_file(self):
        reg1 = "REBOOT-TESTERR"
        # reg2 = r"([0-9a-fA-F]{2})(([/\s:][0-9a-fA-F]{2}){5})"
        reg2 = r"([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})"
        res_list = []
        with open('output.xml', encoding='UTF-8') as file:
            # for line,index in file:
            for index, line in enumerate(file):
                res1 = re.findall(reg1, line)
                res2 = re.findall(reg2, line)
                if res1:
                    res_list.append(res1[0])
                if res2:
                    res_list.append(res2[0][0])
                    # print(res1)
                # print(res_list)
            err_mac_list = []
            for index, content in enumerate(res_list):
              if content == "REBOOT-TESTERR":
                err_mac_list.append(res_list[index+1])
            print(err_mac_list)
            print(len(err_mac_list))
            self._err_mac_save(err_mac_list)

    def _err_mac_save(self, data, path="err-mac.log"):
        with open(path, 'w') as f:
            for line in data:
                f.write('%s\n' % line)

if __name__ == '__main__':
    xp = ParserFile()
    xp.parser_file()
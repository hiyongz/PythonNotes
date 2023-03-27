import configparser
import os


path          = os.path.dirname(os.path.realpath(__file__))
configpath    = os.path.join(path, 'config.ini')
config   = configparser.ConfigParser() # 类实例化
config.read(configpath)
config.items('DUT')
ip = config.get("DUT", "router_ip")
print(ip)

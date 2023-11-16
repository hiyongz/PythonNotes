import re


def ipv6_eui64(mac_address):
    """
    根据MAC生成IPv6 EUI-64接口ID。

    : mac_address:   接口地址。

    返回EUI-64接口ID

    eg:

    | ${eui64} | ipv6_eui64 | 50:2B:73:02:F9:81 | 

    """
    # 判断传参是否正确
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    
    if not bool(pattern.match(mac_address)):
        raise RuntimeError('关键字ipv6_eui64传入的参数值应为正确的MAC地址！')

    def binary_to_hex(binary_str):
        "将2进制字符串转为16进制字符串"
        return hex(int(binary_str, 2))[2:]
        
    # 将MAC地址转2进制
    hex_list = mac_address.split(':')
    mac_address = ''.join([bin(int(hex_num, 16))[2:].zfill(8) for hex_num in hex_list])
    
    # EUI-64定义在MAC地址中间位置插入十六进制数FFFE
    insertfffe = mac_address[:24] + '1111111111111110' + mac_address[24:]
    
    # 从高位开始的第7位 设置为 1
    str64 = insertfffe[:6] + '1' + insertfffe[7:]

    # 转为ipv6地址，分两步：
    # ① 将64位2进制数按照16位的长度切割为列表
    eui64_list = [str64[i:i+16] for i in range(0, len(str64), 16)]
    # ② 遍历列表并将每一项转为16进制，用':'连接起来。
    eui64 = ':'.join([binary_to_hex(i) for i in eui64_list])
    
    return eui64

# eui64 = ipv6_eui64('50:2b:73:02:f9:80')
eui64 = ipv6_eui64('50-2b-73-02-f9-80')
print(eui64)
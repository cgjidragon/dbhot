# 导入pysnmp和tkinter库
from pysnmp.hlapi import *
import tkinter as tk
import radom

# 定义一个函数，用于发送SNMP GET请求并显示响应
def snmp_get(target_ip, public_mib, oid):
    # 创建一个SNMP GET请求
    get_request = getCmd(SnmpEngine(),
                         CommunityData(public_mib),
                         UdpTransportTarget((target_ip, 161)),
                         ContextData(),
                         ObjectType(ObjectIdentity(oid)))

    # 发送请求并获取响应
    errorIndication, errorStatus, errorIndex, varBinds = next(get_request)

    # 检查是否有错误
    if errorIndication:
        result = errorIndication
    elif errorStatus:
        result = '%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
    else:
        # 获取响应中的OID的值
        result = ' = '.join([x.prettyPrint() for x in varBinds[0]])

    # 返回结果
    return result

# 定义一个函数，用于发送SNMP WALK请求并显示响应
def snmp_walk(target_ip, public_mib, oid):
    # 创建一个SNMP WALK请求
    walk_request = nextCmd(SnmpEngine(),
                           CommunityData(public_mib),
                           UdpTransportTarget((target_ip, 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity(oid)),
                           lexicographicMode=False)

    # 发送请求并获取响应
    result = ""
    for (errorIndication, errorStatus, errorIndex, varBinds) in walk_request:

        # 检查是否有错误
        if errorIndication:
            result = errorIndication
            break
        elif errorStatus:
            result = '%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            break
        else:
            # 获取响应中的OID的值，并拼接到结果字符串中
            for varBind in varBinds:
                result += ' = '.join([x.prettyPrint() for x in varBind]) + "\n"

    # 返回结果
    return result

# 定义一个函数，用于根据操作类型和OID发送SNMP请求并显示响应
def snmp_request():
    # 获取目标设备的IP地址和公共MIB
    target_ip = entry_ip.get()
    public_mib = entry_mib.get()

    # 获取操作类型和OID
    operation = var_operation.get()
    oid = entry_oid.get()

    # 根据操作类型调用相应的函数，并获取结果
    if operation == "get":
        result = snmp_get(target_ip, public_mib, oid)
    elif operation == "walk":
        result = snmp_walk(target_ip, public_mib, oid)
    else:
        result = "Invalid operation"

    # 显示结果在文本框中
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result)

# 创建一个窗口
window = tk.Tk()
window.title("SNMP GUI")

# 创建一些标签，输入框和按钮
label_ip = tk.Label(window, text="Target IP:")
label_ip.grid(row=0, column=0)
entry_ip = tk.Entry(window)
entry_ip.grid(row=0, column=1)

label_mib = tk.Label(window, text="Public MIB:")
label_mib.grid(row=1, column=0)
entry_mib = tk.Entry(window)
entry_mib.grid(row=1, column=1)

label_oid = tk.Label(window, text="OID:")
label_oid.grid(row=2, column=0)
entry_oid = tk.Entry(window)
entry_oid.grid(row=2, column=1)

var_operation = tk.StringVar()
var_operation.set("get")
radio_get = tk.Radiobutton(window, text="Get", variable=var_operation,
                           value="get")
radio_get.grid(row=3, column=0)
radio_walk = tk.Radiobutton(window, text="Walk", variable=var_operation,
                            value="walk")
radio_walk.grid(row=3, column=1)

button_request = tk.Button(window,
                           text="Send Request",
                           command=snmp_request)
button_request.grid(row=4, column=0, columnspan=2)

text_result = tk.Text(window)
text_result.grid(row=5, column=0, columnspan=2)

# 启动窗口
window.mainloop()

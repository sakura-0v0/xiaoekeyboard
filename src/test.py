from typing import List

from xiaoe_keyboard import Keyboard, HotkeyType

'''示例用法'''

"""====    完整使用示例    =================================="""
def full_use():

    import tkinter as tk
    win = tk.Tk()
    DEFAULT_KEYS1 = ['D']
    DEFAULT_KEYS2 = ['ctrl_l', 'D']
    DEFAULT_KEYS3 = [None, None, None]
    def down_fun(n=None):  # 按下热键执行的方法
        if n is None:
            n='第三个'
        print(n,'你按下了热键！')

    def up_fun(n=None):  # 松开热键执行的方法
        if n is None:
            n='第三个'
        print(n,'你松开了热键！')


    hotkey_list: List[HotkeyType] = [
        {'name': '热键示例0', 'value': set(DEFAULT_KEYS1), 'down_fun': lambda :down_fun(0), 'up_fun': lambda :up_fun(0), },
        {'name': '热键示例1', 'value': set(DEFAULT_KEYS2), 'down_fun': lambda :down_fun(1)},
        {'name': '热键示例2', 'value': set(DEFAULT_KEYS3),                                  'up_fun': up_fun}
    ]  # 存储热键的字典列表                                                   (可以不用写lambda)
    #             热键名字(必选)         热键值（集合，必选）         按下触发函数（可选）              松开触发函数（可选）


    def save_fun(name,value):
        """保存热键配置"""
        btn_index=int(name[-1])
        btn_list[btn_index].config(text='设置热键')
        print("\n保存热键配置成功：",name,value)
        #在这里保存热键配置到文件或数据库等

    will_save_hotkey = dict()#热键暂存，支持批量设置批量保存

    def validate_keys_fun(name,value):
        """预处理热键"""
        will_save_hotkey[name] = value
        print(f"\n\n请点击保存按钮保存热键：new    name:{name}  value:{value}")
        for key,value in will_save_hotkey.items():
            print(f"即将保存的热键：name:{key}  value:{value}")
        print("\n")
        #在这里对热键值进行暂存（若不填validate_keys_fun，则直接保存）

    keyboard = Keyboard(
        hotkey_list,  # 热键配置信息
        run_fun_callback=lambda func: win.after(0, func), # 提供回调函数
        save_fun=save_fun, # 保存回调函数
        validate_keys_fun=validate_keys_fun, # 预处理回调函数（松手触发。置空则松手直接保存）,
        is_read_mouse=True, # 开启鼠标识别
        is_read_mouse_right=True, # 开启鼠标右键识别
        is_read_mouse_scroll=True, # 开启鼠标滚轮识别
    )
    def button_fun(n):
        """触发修改"""
        print(will_save_hotkey)
        if keyboard.get_hotkey_setting() is None:
            print(f'正在设置：热键示例{n}...')
            btn_list[n].config(text='取消设置')
            keyboard.set_hotkey_setting(f'热键示例{n}')#发送信号，开启识别热键功能（目标热键名字，只能同时设置一个）
        else:
            print('取消设置')
            btn_list[n].config(text=f'设置热键{n}')
            keyboard.set_hotkey_setting(None)#再次按下按钮，发送信号，关闭识别热键功能


    set_button0 = tk.Button(win, text='设置热键0', command=lambda :button_fun(0))
    set_button0.pack(pady=15)

    set_button1 = tk.Button(win, text='设置热键1', command=lambda :button_fun(1))
    set_button1.pack(pady=15)

    set_button2 = tk.Button(win, text='设置热键2', command=lambda :button_fun(2))
    set_button2.pack(pady=15)

    btn_list=[set_button0,set_button1,set_button2]

    def call_save():
        """通知保存"""
        if will_save_hotkey:
            for name,value in will_save_hotkey.items():#批量保存
                keyboard.set_one_hotkey_dict(name,value)
            will_save_hotkey.clear()

    save_button = tk.Button(win, text='保存热键', command=call_save)
    save_button.pack(pady=30)

    win.geometry(f'300x300+{win.winfo_screenwidth()//2-150}+{win.winfo_screenheight()//2-150}')

    try:
        win.mainloop()
    finally:
        print('exit')

"""====    最小使用示例    =================================="""
def simple():
    def fun99():
        print('你按下了热键99！')

    hotkey=['ctrl_l', 'R']

    hotkey_list: List[HotkeyType] = [
        {'name': '热键示例99', 'value': set(hotkey),'down_fun': fun99},
    ]

    Keyboard(hotkey_list)

    while True:
        if input('输入quit退出...')=='quit':
            break

if __name__ == "__main__":
    """====    运行示例    ===="""
    run = 0

    #0：完整使用示例   1：最小使用示例(固定热键：ctrl_l + R)


    if run==0:
        full_use()
    elif run==1:
        simple()








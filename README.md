# Xiaoe Keyboard 🎹

一个轻量、精准的 Python 全局热键管理器。基于 `pynput` 封装，专为需要处理**复杂组合键**和 **UI 线程安全**的桌面应用设计。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

## ✨ 为什么选择它？

- **🧠 智能组合键匹配**：底层使用 `set` 子集算法匹配按键，**完全无视用户按下组合键的先后顺序**。
- **🎯 贪心精准触发**：同时注册 `Ctrl+D` 和 `Ctrl+Shift+D` 时，只会精准触发匹配度最高的那个，不会发生冲突。
- **🎛️ 完美的“预览-保存”交互**：支持 `validate_keys_fun` 拦截机制。用户按下快捷键后，可以先在 UI 上预览（如："你即将设置为 Ctrl+C"），用户点“确认”后再真正应用保存，体验极其优雅。也可以不设置 `validate_keys_fun` ，用户松手后立刻触发保存。传入你的保存方法 `save_fun` ，比如说将按键存储在配置文件中，它将在触发保存后调用。

## 📦 安装

```bash
pip install xiaoe-keyboard
```

## 🚀 快速上手

只需三步，即可监听全局快捷键：

```python
from xiaoe_keyboard import Keyboard

def my_action():
    print("你按下了 Ctrl + D！")

# value 必须是 set 类型
hotkey_list = [
    {'name': '我的热键', 'value': {'ctrl_l', 'd'}, 'down_fun': my_action}
]

# 启动监听
kb = Keyboard(hotkey_list)

input("按回车键退出程序...\n")
```

## 📖 进阶用法：动态设置热键（配合 Tkinter）

在实际桌面开发中，我们经常需要让用户“自定义快捷键”。以下演示了如何配合 Tkinter 实现完美的交互流程：

```python
import tkinter as tk
from typing import List

from xiaoe_keyboard import Keyboard, HotkeyType

config = {
    '操作a': ['ctrl_l', 'D']
}

win = tk.Tk()
win.geometry("300x200")

# 1. 定义初始热键
hotkey_list: List[HotkeyType] = [
    {'name': '测试热键', 'value': set(config['操作a']), 'down_fun': lambda: print("执行了操作a！"), 'up_fun': lambda: print("松开了操作a！")}
]
def flash_get_now_key_label():
    """用于更新标签按键值"""
    label.config(text = f"当前热键: 【{'】+【'.join(config['操作a'])}】")
    
def update_btn_status(is_change):
    """用于更新按钮文字"""
    if is_change:
        text = "修改热键"
    else:
        text = "取消设置"
    btn.config(text=text)


# 2. 定义保存和预处理函数
def save_fun(name, value):
    """保存按键时的操作"""
    value = list(value)
    print(f"[已保存] {name} -> {value}")
    config['操作a'] = value.copy()
    flash_get_now_key_label()
    update_btn_status(True)

will_save_hotkey = {}

def validate_keys_fun(name, value):
    """用户松手后，先触发这里，用于在界面上展示预览"""
    will_save_hotkey[name] = value
    label.config(text=f"即将设置为: {value} (请点保存)")

# 3. 实例化 Keyboard，传入调用回调的函数 run_fun_callback 保证线程安全
kb = Keyboard(
    hotkey_list, 
    run_fun_callback=lambda func: win.after(0, func), 
    save_fun=save_fun, 
    validate_keys_fun=validate_keys_fun
)

# 4. UI 交互逻辑
label = tk.Label(win)
flash_get_now_key_label()
label.pack(pady=10)

def start_setting():
    if kb.get_hotkey_setting() is None and not will_save_hotkey:
        update_btn_status(False)
        label.config(text="请按下你要设置的组合键...")
        kb.set_hotkey_setting('测试热键') # 开启读取模式
    else:
        update_btn_status(True)
        kb.set_hotkey_setting(None)      # 关闭读取模式
        flash_get_now_key_label()
        will_save_hotkey.clear()


btn = tk.Button(win, command=start_setting)
update_btn_status(True)
btn.pack(pady=5)

def do_save():
    if will_save_hotkey:
        for name, value in will_save_hotkey.items():
            kb.set_one_hotkey_dict(name, value) # 确认应用并触发 save_fun
        will_save_hotkey.clear()

save_btn = tk.Button(win, text="保存设置", command=do_save)
save_btn.pack(pady=5)

win.mainloop()
```

## 📝 核心参数说明

- `hotkey_list`: 热键配置列表，字典格式。`value` 必须是 `set`。如果需要解绑按键，设置{None}即可忽略该按键。
- `run_fun_callback`: 传入能在UI线程调用回调函数的函数。
```python
# tkinter:
run_fun_callback=lambda func: win.after(0, func)

# qt(这里使用传递字典信号的方式):
class App(QWidget):
    run_signal = QtCore.pyqtSignal(dict)
    def __init__(self):
        self.run_signal.connect(
            lambda func_dict: func_dict['func']()
        )
    def run_func(self, func):
        run_signal.emit({'func': func})
app = App()
run_fun_callback=app.run_func # 传入xiaoe_keyboard的参数
```
- `save_fun`: 当热键被成功应用/保存时触动的回调。
- `validate_keys_fun`: 如果提供此项，用户松开按键时**不会立刻保存**，而是触发此函数。你需要自行在 UI 上暂存数据，并在用户点击“确认”后手动调用 `set_one_hotkey_dict()`。如果你不提供该参数，当用户松开第一个按键后会立刻触发保存。

## 📄 开源协议

基于 [MIT License](./LICENSE) 开源，自由使用，保留署名即可。

---
**Author**: 一只黄小娥  
**Url**: [https://www.yzhxe.cn/]

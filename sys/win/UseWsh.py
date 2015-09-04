'''
python创建Wscript.Shell进行自动化2008-04-17 13:02

object.SendKeys(string) 
参数 
object 
WshShell 对象。 
string 
表示要发送的键击（一个或多个）的字符串值。 
说明 
使用 SendKeys 方法可以将键击发送到无自动化界面的应用程序中。多数键盘字符都可用一个键击表示。
某些键盘字符由多个键击组合而成（例如，CTRL+SHIFT+ HOME）。
要发送单个键盘字符，请将字符本身作为 string 参数发送。例如，要发送字母 x，则请发送 string 参数 "x"。 

注意 要发送空格，则请发送字符串 " "。 
可使用 SendKeys 同时发送多个键击。为此，可将每个键击按顺序排列在一起，以此来创建表示一系列键击的复合字符串参数。
例如，要发送键击 a、b 和 c，则需要发送字符串参数 "abc"。
SendKeys 方法将某些字符用作字符的修饰符（而不使用其本身的含义）。这组特殊的字符可包括圆括号、中括号、大括号，以及： 

加号 "+"、 
插入记号 "^"、 
百分号 "%"、 
和“非”符号 "~"。 
用大括号 "{}" 括起这些字符可以发送它们。例如，要发送加号，请使用字符串参数 "{+}"。
SendKeys中使用的中括号 "[ ]" 无任何特殊含义，但是必须把它们括在大括号中，
以便容纳确实要赋予其特殊含义的应用程序（例如，对于动态数据交换 (DDE) 就是这样）。 

要发送左中括号字符，请发送字符串参数 "{[]"；要发送右中括号字符，请发送字符串参数 "{]}"。 
要发送左大括号字符，请发送字符串参数 "{{}"；要发送右大括号字符，请发送字符串参数 "{}}"。 
某些键击不生成字符（如 ENTER 和 TAB）。某些键击表示操作（如 BACKSPACE 和 BREAK）。要发送这些类型的键击，请发送下表中列出的参数： 

键 参数 
退格键 {BACKSPACE}、{BS} 或 {BKSP} 
BREAK {BREAK} 
CAPS LOCK {CAPSLOCK} 
DEL 或 DELETE {DELETE} 或 {DEL} 
向下键 {DOWN} 
END {END} 
ENTER {ENTER} 或 ~ 
ESC {ESC} 
HELP {HELP} 
HOME {HOME} 
INS 或 INSERT {INSERT} 或 {INS} 
向左键 {LEFT} 
NUM LOCK {NUMLOCK} 
PAGE DOWN {PGDN} 
PAGE UP {PGUP} 
PRINT SCREEN {PRTSC} 
向右键 {RIGHT} 
SCROLL LOCK {SCROLLLOCK} 
TAB {TAB} 
向上键 {UP} 
F1 {F1} 
F2 {F2} 
F3 {F3} 
F4 {F4} 
F5 {F5} 
F6 {F6} 
F7 {F7} 
F8 {F8} 
F9 {F9} 
F10 {F10} 
F11 {F11} 
F12 {F12} 
F13 {F13} 
F14 {F14} 
F15 {F15} 
F16 {F16} 

要发送由常规键击和 SHIFT、CTRL 或 ALT 组合而成的键盘字符，请创建表示该键击组合的复合字符串参数。
可通过在常规键击之前添加一个或多个以下特殊字符来完成上述操作： 

键 特殊字符 
SHIFT + 
CTRL ^ 
ALT % 

注意 这样使用时，不用大括号括起这些特殊字符。 
要指定在按下多个其他键时，按下 SHIFT、CTRL 和 ALT 的组合，请创建复合字符串参数，用括号括起其中的组合键。
例如，要发送的组合键指定： 

如果在按 e 和 c 的同时按 SHIFT 键，则发送字符串参数 "+(ec)"。 
如果在按 e 时只按 c（而不按 SHIFT），则发送字符串参数 "+ec"。 
可使用 SendKeys 方法发送一种在一行内重复按键的键击。为此，要创建复合字符串参数，以指定要重复的键击，并在其后指定重复次数。
可使用 {键击 数字} 形式的复合字符串参数来完成上述操作。例如，如果要发送 10 次 "x"，则需要发送字符串参数 "{x 10}"。
请确保在键击和数字之间有一个空格。
'''

import win32com.client
import time

execpath = 'cmd.exe'
wsh = win32com.client.Dispatch("Wscript.Shell")
#wshe = wsh.Exec(execpath)
wshe = wsh.run('cmd')
pid = wshe.ProcessID
wsh.AppActivate(pid)
time.sleep(splashsec)
wsh.SendKeys("{ENTER}")
wsh.SendKeys("%n")#alt+n
wsh.SendKeys("%a")
wsh.SendKeys("10.0.0.1")
wsh.SendKeys("{CAPSLOCK}")

wsh.run('calc')
wsh.AppActivate('计算器')
wsh.AppActivate('Windows Live Messenger')


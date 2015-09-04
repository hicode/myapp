# http://www.pyregex.com/   https://www.debuggex.com/


##### ��ʹ�� re ģ��֮ǰ���ȿ���һ����������Ƿ�����ø��졢���򵥵��ַ��������������

import re
p = re.compile('ab*')
print p

# RegexObject
p = re.compile('ab*', re.IGNORECASE)
p = re.compile('[a-z]+')

# MatchObject
p.match("")  # match() �ӵ�һ���ַ���ʼ����Ҫ�ܹ�ƥ�䵽ģʽ
m = p.match( 'tempo')
m.group()
m.start()
m.end()
m.span()

# MatchObject
m = p.search('::: message')  # search() ���Դ�����λ�ÿ�ʼƥ�䣬��ƥ�䵽��һ��ƥ����ʱ�˳�
m.group()
m.span()

p = re.compile('\d+')
p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')   # findall�᷵���ַ���������ƥ���ƥ�����

iterator = p.finditer('12 drummers drumming, 11 ... 10 ...')
for match in iterator:
  print match.span()


# ��һ��Ҫ���� `RegexObject` ���ٵ����䷽����reģ���ж������������� match()��search()��sub() �ȡ�ʹ�� RE �ַ�����Ϊ��һ������������Ĳ�������Ӧ `RegexObject` �ķ���������ͬ������None��һ�� `MatchObject`
print re.match(r'From\s+', 'Fromage amk')
re.match(r'From\s+', 'From amk Thu May 14 19:12:10 1998')


###########################################################################################################
# ���飬�޲������������
p = re.compile('(ab)*')
print p.match('ababababab').span()

p = re.compile('(a)b')
m = p.match('ab')
m.group()
m.group(0)

p = re.compile('(a(b)c)d')
m = p.match('abcd')
m.group(0)
m.group(1)
m.group(2)

m.group(2,1,2)
m.groups()

p = re.compile(r'(\b\w+)\s+\1')
p.search('Paris in the the spring').group()


p = re.compile(r'(?P<word>\b\w+\b)')
m = p.search( '(((( Lots of punctuation )))' )
m.group('word')
m.group(1)



contactInfo = 'Doe, John: 555-1212'
re.search(r'\w+, \w+: \S+', contactInfo)
match = re.search(r'(\w+), (\w+): (\S+)', contactInfo)  # ʹ��������ס������ʽ��ĳЩ���ֽ��з���
match.group(1)  # ��Щ�������ʹ�� group() ����ȡ�ã��������Դ�ַ���������ƥ���˳�������ֽ��б�ţ���1��ʼ��
match.group(2)
match.group(3)
match.group(0)  # ��� 0 ������������ƥ����

# ʹ�����Ʒ���
match = re.search(r'(?P<last>\w+), (?P<first>\w+): (?P<phone>\S+)', contactInfo) 
match.group('last')
match.group('first')
match.group('phone')

# fetchall() ����ͬ������ʹ�÷��飬���������� match ������Ƿ���һ��Ԫ���б�Ԫ���е�ÿ��Ԫ�ض�Ӧ������ʽ����Ӧ�ķ���
����

re.findall(r'(\w+), (\w+): (\S+)', contactInfo)  # findall() ����ʱ���ǲ���ʹ�÷�������


###########################################################################################################
paragraph = \
'''
<p>
This is a paragraph.
It has multiple lines.
</p>
'''

match = re.search(r'<p>.*</p>', paragraph, re.DOTALL)
match.group(0)

# ^ �� $ ͨ��ƥ�������ַ��������׺���β��ͨ��MULTILINEģʽ���ĳһ�ض��еĿ�ʼ�ͽ���������ƥ��,
match = re.search(r'^It has.*', paragraph, re.MULTILINE)



# ̰��ƥ��ͷ�̰��ƥ��
htmlSnippet = '<h1>This is the Title</h1>'
re.findall(r'<.*>', htmlSnippet) # ̰��ƥ��
re.findall(r'<.*?>', htmlSnippet) # ��̰��ƥ��


re.sub(r'\w+', 'word', 'This phrase contains 5 words')
re.sub(r'(?P<firstLetter>\w)\w*', r'\g<firstLetter>', 'This phrase contains 5 words')  # �÷������������е�ƥ��


###########################################################################################################
# ����ʽ���ı�ת��ΪPython�б���ʽ��<name>, <birth-date>, <description>��'description'�ɻ��У�ÿ����Ϣʹ��һ���������ָ�
rawProfiles = '''
Tim Fake, 1982/03/21, I like to
eat, sleep and
relax

Lisa Test, 1990/05/12, I like long
walks of the beach, watching sun-sets,
and listening to slow jazz
'''

profilesList = re.split(r'\n{2,}', rawProfiles)
profilesList = [ re.sub(r'\n', ' ', profile) for profile in profilesList ]
profilesList = [ re.split(r',', profile, maxsplit=2) for profile in profilesList ]
profilesList = [ map(str.strip, profile) for profile in profilesList ]


m = re.search("[abc]","abc")
m1 = re.search("(abc)","abc")
m2 = re.search("([abc])","abc")
m3 = re.search("[(abc)]","abc")
m.group(0)
m.group(1)
m.groups()
m1.group(0)
m1.group(1)
m1.groups()
m2.group(0)
m2.group(1)
m2.groups()
m3.group(0)
m3.group(1)
m3.groups()

m = re.match("([abc])+", "abc")
m.groups()
m = re.match("(?:[abc])+", "abc")
m.groups()
m = re.findall("([abc])+", "abc")
m = re.findall("([abc])", "abc")
m = re.findall("[(abc)]", "abc")


s="""var hq_str_sz160125="�Ϸ����,0.951,0.951,0.962,0.966,0.950,0.962,0.963,16589128,15919488.608,146836,0.962,132900,0.961,86800,0.960,75000,0.959,83600,0.958,22500,0.963,126400,0.964,30000,0.965,71800,0.966,61200,0.967,2015-08-04,15:05:54,00";
var hq_str_sh510900="H��ETF,1.077,1.074,1.089,1.092,1.073,1.088,1.089,115032200,124612305,946200,1.088,140700,1.087,123000,1.086,585000,1.085,558800,1.084,280200,1.089,643900,1.090,1126700,1.091,1341900,1.092,150900,1.093,2015-08-04,15:03:05,00";
var hq_str_sz002594="���ǵ�,57.88,57.78,59.66,60.48,55.19,59.66,59.67,26199893,1528937750.25,77388,59.66,11034,59.65,17100,59.64,9000,59.63,7400,59.62,9500,59.67,1700,59.68,500,59.69,10200,59.70,400,59.71,2015-08-04,15:05:54,00";
"""
res = re.findall(r'="(.*)";', s)
res = re.findall(r'="(.*)";', s, re.DOTALL)
res = re.search(r'="(.*)"', s, re.DOTALL)
res = re.search(r'="(.*)"', s, re.MULTILINE)


s1 = 'text=cssPath:"<a href="http://imgcache.qq.com/ptlogin/v4/style/32"" target="_blank">http://imgcache.qq.com/ptlogin/v4/style/32"</a>,sig:"OvL7F1OQEojtPkn5x2xdj1*uYPm*H3mpaOf3rs2M",clientip:"82ee3af631dd6ffe",serverip:"",version:"201404010930"'
res = re.findall(r'sig:"([^"]+)"',s1)



s2='''({val:"600000",val2:"�ַ�����",val3:"pfyx"});
_t.push({val:"600004",val2:"���ƻ���",val3:"byjc"});
_t.push({val:"600005",val2:"��ֹɷ�",val3:"wggf"});
_t.push({val:"600006",val2:"��������",val3:"dfqc"});
_t.push({val:"600007",val2:"�й���ó",val3:"zggm"});
_t.push({val:"600008",val2:"�״��ɷ�",val3:"scgf"});
_t.push({val:"600009",val2:"�Ϻ�����",val3:"shjc"});
'''
res = re.findall(r'{(.*)}', s2)

from urllib2 import Request, urlopen
url = "http://finance.yahoo.com/d/quotes.csv?s=160125.sz&f=l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7"
req = Request( url )
resp = urlopen(req)
r1 = resp.read()



 
preg_match( ' /< h1> .< /h1> /' ' < h1> ����һ�����⡣< /h1> 
< h1> ������һ����< /h1> ' $matches ) 

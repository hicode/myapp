# coding=utf-8

todo = '基金申赎代码  深交所下载代码中的深B深AB 000033'

def Submarket(market, code):  # A股 B股  如何区分基金是场内还是场外？
    errDict = {'SH':['939988'], 'SZ':['159900'], 'HK':['01183', '01291', '01350', '01352', '01392', '01403', '01407', '01436', '01437', '01441', '01453', '01493', ]} 
    if market.upper()=='SH':   # 939988
        if code in errDict['SH']:
            return 'ERR'
        if code[0]=='6':
            return 'SHS'
        elif code[0]=='9':
            return 'SHSB'
        elif code[0:3]=='500':
            return 'SHFC'
        elif code[0:3]=='510':
            return 'SHF'
        elif code[0:3]=='000':
            return 'SHI'
        else:
            #raise
            print '!!!!!!!!ERROR SH CODE!!!!', code
            return ''
    elif market.upper()=='SZ':
    # (A股(主板SZA 中小板SZAZ 创业板SZAC) B股SZB 开放式基金SZF 封闭式基金SZFC)
        if code in errDict['SZ']:
            return 'ERR'
        if code[0:2]=='15' or code[0:2] == '16':
            return 'SZF'
        if code[0:2]=='18':
            return 'SZFC'
        elif code[0]=='2':
            return 'SZSB'
        elif code[0:2]=='30':
            return 'SZSC'
        elif code[0:2]=='39':  # 399
            return 'SZI'
        elif code[0:3]=='002':
            return 'SZSZ'
        elif code[0:3]<'002':
            return 'SZS'
        else:
            #raise
            print '!!!!!!!!ERROR SZ CODE!!!!', code
            return ''
    #def HkSubmarket(code):  # (主板 创业板 权证/牛熊证)
    elif market.upper()=='HK':
        if code in errDict['HK']:
            return 'ERR'
        elif code[0:2]=='08':
            return 'HKSC'   # STOCK CHUANGYE
        elif code[0:2]<'08':
            return 'HKS'   # STOCK
        elif code[0] in ['1', '2']:
            return 'HKDW'  # DERIVATIVE WARRANT
        elif code[0] > '6':
            return 'HKDCB'  #DERIVATIVE cow bear
        else:
            #raise
            print '!!!!!!!!ERROR HK CODE!!!!'
    else:
        print '!!!!!!!!ERROR market!!!!', market
        return ''


def MapSubmarket2Table(submarket):  # A股 B股  如何区分基金是场内还是场外？
    # mapSubmarket2Table = {'SZI': 'CNS'}
    if submarket in ['SHS', 'SHSB', 'SZS', 'SZSB', 'SZSZ', 'SZSC']:
        return 'CNS'
    elif submarket in ['SHI', 'SZI']:
        return 'CNI'
    elif submarket in ['HKS', 'HKSC']:
        return 'HKS'
    elif submarket in ['HKI']:
        return 'HKI'
    else:
        print '!!!!!!!!ERROR submarket!!!!', submarket
        return ''
    '''
    elif submarket in ['', '', '', '', '', ]:
        return 'CNF'
    elif submarket in ['', '', '', '', '', ]:
        return 'CND'
    elif submarket in ['HKDW', '', '', '', '', ]:
        return 'HKD'
    elif submarket in ['', '', '', '', '', ]:
        return 'HKF'
    '''



'''
   确保历史数据库中最大日期和最小日期之间是完整连续的
'''

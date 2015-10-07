def addPreClose(conn):
    df_cns = pd.read_sql_query('select * from myapp_kDaily_cns', conn)
    df_hks = pd.read_sql_query('select * from myapp_kDaily_hks', conn)
    df_cni = pd.read_sql_query('select * from myapp_kDaily_cni', conn)
    df_hki = pd.read_sql_query('select * from myapp_kDaily_hki', conn)
    dfl = [df_cns, df_cni, df_hks, df_hki]
    df = pd.concat(dfl, ignore_index=True)

    cur = conn.cursor()
    for key in prodDict8Submarket:
        tblName = MapSubmarket2Table( key ).lower()
        if tblName <> 'cns' and tblName <> 'hks' and tblName <> 'cni' and tblName <> 'hki':
            continue 
        for prod in prodDict8Submarket[key]:
            if prod.dateHistEnd == None:
                continue
            elif prod.ratioFrwdBegin == None:
                sys.stdout.write(  'dateHistEnd is not Null but ratioFrwdBegin isnull:' + prod.code+'.'+prod.submarket + '\r\n' )
                continue

            try:
                cur.execute( "update myapp_kdaily_%s set ratioBack=%s/ratioFrwd where product_id = %s" % (tblName, prod.ratioFrwdBegin, prod.id) )
            except db.Error,e:
                sys.stdout.write(  'except while execute update:' + prod.code+'.'+prod.submarket + ' Error: ' + str(e) + '\r\n' )
    conn.commit()

def moreK(conn, fld):
    dfD = pd.read_sql_query('select * from myapp_kDaily', conn)
    grouped = dfD.groupby([dfD['product_id'], dfD['year'], dfD[fld]])
    h=grouped['h'].max()
    l=grouped['l'].min()
    o=grouped['o'].first()
    c=grouped['c'].last()

def groupK(conn, fld):

def intdate(int):
    return datetime.strptime(str(int), '%Y%m%d')

    t = time.clock()
    #dfD = pd.read_sql_query('select * from myapp_kDaily where product_id = 8838 ', conn)
    dfD = pd.read_sql_query('select * from myapp_kDaily', conn)
    print('read_sql_query time: %.03f' % (time.clock()-t) )
    
    t = time.clock()
    grouped = dfD.groupby([dfD['product_id'], dfD['year'], dfD[fld]])
    h=grouped['h'].max()
    l=grouped['l'].min()
    o=grouped['o'].first()
    c=grouped['c'].last()
    startD=grouped['date'].min()
    ih=grouped['h'].idxmax()
    hD=dfD.iloc[ih]['date']
    hD.name='hDate'
    hD.index=o.index
    il=grouped['l'].idxmin()
    lD=dfD.iloc[il]['date']
    lD.name='lDate'
    lD.index=o.index
    #dfM = pd.merge( pd.DataFrame(startD), pd.DataFrame(o), on=['product_id', 'year', fld] )
    rsltDf = pd.DataFrame(startD).join( [pd.DataFrame(o), pd.DataFrame(h), pd.DataFrame(l), pd.DataFrame(c), pd.DataFrame(hD), pd.DataFrame(lD) ] )
    print('group month time: %.03f' % (time.clock()-t) )
    return rsltDf


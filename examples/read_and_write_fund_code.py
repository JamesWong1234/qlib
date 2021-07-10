# coding=utf-8

import demjson,re
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from toolkit import get_HTML_content


def main():
    df = get_all_fund_code_df()
    write_fund_code_into_DB(df)
    df = read_fund_code_from_DB()
    print(df.head())

def get_all_fund_code_df():
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    content = get_HTML_content(url)
    _ = re.sub("\|", "  ", content[8:-1])
    d = demjson.decode(_)
    code_list = []
    ename_list = []
    cname_list = []
    type_list = []

    for i in d:
        code_list.append(i[0])
        ename_list.append(i[1])
        cname_list.append(i[2])
        type_list.append(i[3])

    data = {'code': code_list,
            'ename': ename_list,
            'cname':cname_list,
            'type':type_list}

    df: DataFrame = pd.DataFrame(data,
                      columns=['code','ename','cname','type'])
    return df

def write_fund_code_into_DB(df):
    connect = create_engine('mysql+pymysql://root:Aa821124@localhost:3306/fund_data?charset=utf8')
    df.to_sql('fund_code', connect, schema='fund_data', if_exists='replace') #'fail' 'append'

def read_fund_code_from_DB():
    connect = create_engine('mysql+pymysql://root:Aa821124@localhost:3306/fund_data?charset=utf8')
    sql_cmd = "SELECT * FROM fund_code"
    df = pd.read_sql(sql=sql_cmd, con=connect)
    return df

if __name__ == '__main__':
    main()


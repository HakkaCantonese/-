# 函数功能:将json数据一条一条地导入MySQL数据库

import pymysql
import json
import time

def main():
    # 从文件中读取json数据
    filename = 'update.json'
    try:
        with open(filename,'r',encoding='utf-8') as f:
            res = json.load(f)
        print('load ok!')
    except:
        print('read json file done!')


    #建立与数据库之间的连接,注意编码是utf8,不是utf-8
    mysql = pymysql.connect(host='localhost',user='root',passwd='password',db='usersinfo',charset='utf8')

    #新建游标
    cur = mysql.cursor()
    #记录的条数
    n = len(res)

    print('开始插入!')
    for i in range(n):
        r_n,e_p_n,e_t_i = res[i]['REPORT_NUM'],res[i]['EVENT_PROPERTY_NAME'],res[i]['EVENT_TYPE_ID']
        e_t_n,e_s_n = res[i]['EVENT_TYPE_NAME'],res[i]['EVENT_SRC_NAME']
        d_i,i_a_n,s_t_i,d_n = res[i]['DISTRICT_ID'],res[i]['INTIME_ARCHIVE_NUM'],res[i]['SUB_TYPE_ID'],res[i]['DISTRICT_NAME']
        c_i,r_i,s_i = res[i]['COMMUNITY_ID'],res[i]['REC_ID'],res[i]['STREET_ID']
        o_a_n,o_n,d_u_i = res[i]['OVERTIME_ARCHIVE_NUM'],res[i]['OPERATE_NUM'],res[i]['DISPOSE_UNIT_ID']
        s_n,c_t,e_s_i = res[i]['STREET_NAME'],res[i]['CREATE_TIME'],res[i]['EVENT_SRC_ID']
        i_t_a,s_t_n,e_p_i,o_p = res[i]['INTIME_TO_ARCHIVE_NUM'],res[i]['SUB_TYPE_NAME'],res[i]['EVENT_PROPERTY_ID'],res[i]['OCCUR_PLACE']
        c_n,d_u_n,m_t_n,m_t_t = res[i]['COMMUNITY_NAME'],res[i]['DISPOSE_UNIT_NAME'],res[i]['MAIN_TYPE_NAME'],res[i]['MAIN_TYPE_ID']

        sql = "insert into lifedata2 (REPORT_NUM,EVENT_PROPERTY_NAME,EVENT_TYPE_ID,EVENT_TYPE_NAME,EVENT_SRC_NAME,\
                DISTRICT_ID,INTIME_ARCHIVE_NUM,SUB_TYPE_ID,DISTRICT_NAME,COMMUNITY_ID,REC_ID,STREET_ID,\
                OVERTIME_ARCHIVE_NUM,OPERATE_NUM,DISPOSE_UNIT_ID,STREET_NAME,CREATE_TIME,EVENT_SRC_ID,\
                INTIME_TO_ARCHIVE_NUM,SUB_TYPE_NAME,EVENT_PROPERTY_ID,OCCUR_PLACE,COMMUNITY_NAME,DISPOSE_UNIT_NAME,\
                MAIN_TYPE_NAME,MAIN_TYPE_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (r_n,e_p_n,e_t_i,e_t_n,e_s_n,d_i,i_a_n,s_t_i,d_n,c_i,r_i,s_i,o_a_n,o_n,d_u_i,s_n,c_t,e_s_i,i_t_a,s_t_n,e_p_i,o_p,c_n,d_u_n,m_t_n,m_t_t)
        cur.execute(sql,values)
        mysql.commit()
        print("success!")
        time.sleep(0.5)
    cur.close()
    mysql.close()

if __name__ == '__main__':
    main()

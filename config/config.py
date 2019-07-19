"""
一些常用的通用配置，如User-Agent，Cookie
"""
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) ' \
             'Chrome/22.0.1207.1 Safari/537.1'

Mongodb_uri = 'mongodb://localhost:27017/'

image_path = r'D:\Pictures\weibo'

Cookie = 'SINAGLOBAL=5586490899717.181.1536913818826; UM_distinctid=169b38928b096b-06981a967f761-9333061-1fa400-169b38928b16eb; un=1304169736@qq.com; _s_tentry=login.sina.com.cn; Apache=7633642948419.628.1563419233797; ULV=1563419233803:233:14:4:7633642948419.628.1563419233797:1563329939504; login_sid_t=fc60f649b1425d7d4a1f6e06ee085312; cross_origin_proto=SSL; SSOLoginState=1563419241; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF5SSkZaQym.hgJRur5llA05JpX5KMhUgL.Fo2Ne0MES0qESKM2dJLoIpBLxKnLBKeLBonLxK-LBKBL129KKntt; ALF=1595044551; SCF=AsshEl09dCx_bI0moyWocHGC9rAJa92BpoUfT7WNWbMNfeI9-V4kWYEHVP2_ZJxUR28vKJhZqD-QRwsdssW6Ous.; SUB=_2A25wNU8YDeRhGedJ6FUT9yjOzjuIHXVTQyfQrDV8PUNbmtBeLXTwkW9NVjU2Ynsp0_KbabwnvRoLIjTC_JfW3q0w; SUHB=0LcDCmk4zfAMDJ; UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1563508709978%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

headers = {'User-Agent': User_Agent,
           'Cookie': Cookie}
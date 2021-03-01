import pandas as pd
# 显示所有的列，方便查看数据
from pandas._testing import assert_frame_equal

pd.set_option('display.max_columns', None)
# # 设置显示10列
# pd.set_option('display.max_columns', 10)
data=pd.read_csv('/Users/zhouya/Desktop/02/customer_behavior.csv',encoding='utf-8')
# print(data.head())
#'cust_id'用户ID,'prod_id'产品id,'group_id'产品类目,'be_type'操作类型,'day_id'具体到分的时间,'buy_time'具体到天的时间
data=data[['cust_id','prod_id','group_id','be_type','day_id','buy_time']]
# print(data.isnull().any())
# print(data.count())
# 数据清洗，筛选出11月5号到11月13号之间的数据，去除不符合条件的数据
# 异常数据的处理
data1=data[(data.buy_time>='2019-11-05')& (data.buy_time<='2019-11-13')]
print(len(data))
print(len(data1))
#下面两种方法都可以看某一列有哪些值
print(data1['be_type'].drop_duplicates())
print(data1['be_type'].value_counts())
#查看数据格式
print(data1.dtypes)
#将day_id转化为时间格式
data1['day_id']=pd.to_datetime(data1['day_id'],format='%Y-%m-%d')
data1['month']=data1['day_id'].dt.month
data1['buy_time']=data1['day_id'].dt.date
data1['times']=data1['day_id'].dt.time
data1['hours']=data1['day_id'].dt.hour
data1['weekday']=data1['day_id'].dt.dayofweek+1
print(data1.head())
behavior_count=data1.groupby('be_type')['cust_id'].count()
print(behavior_count.head())
#数据整体，计算pv，uv、跳失率：只有点击行为的用户数/总用户数，总用户数即uv
pv=behavior_count['pv']
uv=len(data1['cust_id'].unique())
data_pv=data1.loc[data1['be_type']=='pv',['cust_id']]
data_fav=data1.loc[data1['be_type']=='fav',['cust_id']]
data_cart=data1.loc[data1['be_type']=='cart',['cust_id']]
data_buy=data1.loc[data1['be_type']=='buy',['cust_id']]
#集合相减，获取只有进入页面没有做其他任何操作的的用户数
data_pv_only=set(data_pv['cust_id'])-set(data_fav['cust_id'])-set(data_cart['cust_id'])-set(data_buy['cust_id'])
pv_only=len(data_pv_only)
print('跳失率为：%.2f%%'%(pv_only/uv*100))
#按照时间分段查看pv，uv，获取流量信息
#按天
pv_day=data1[data1['be_type']=='pv'].groupby('buy_time')['cust_id'].count()
uv_day=data1[data1['be_type']=='pv'].drop_duplicates(['buy_time','cust_id']).groupby('buy_time')['cust_id'].count()






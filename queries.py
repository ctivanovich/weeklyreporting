# -*- coding: utf-8 -*-
#地区
REGION = 'sh-lawson'
AREACODE = '19000'

#本周
STARTDATE = '20180625'
ENDDATE = '20180701'

STARTTIME = '2018-06-25 00:00:00'
ENDTIME = '2018-07-01 23:59:59'

#上周-计算流失会员
LOSTSTART = '20180618'
LOSTEND = '20180624'

LOSTBEGINTIME = '2018-06-18 00:00:00'
LOSTENDTIME = '2018-06-24 23:59:59'


QUERIES = {
'q1' : '''
select
case user_origin
	when "WX" then "微信"
	when "AP" then "支付宝"
    when "LW" then "门店注册"
    when "MR" then "无人POS注册"
	else "APP下载"
	end as category, count(DISTINCT barcode)
from t_user
where region_block_code = '{0}'
and create_date <= '{1}'
and del_flg = '0'
GROUP BY 1
with rollup;
'''.format(REGION, ENDTIME).replace('\n', ' ').replace('\t', ' '),

#q2 : 'formula',

# 累计活跃会员
'q3' : '''
select
	case
		d.consuming_origin
		when "0" then "app原生"
		when "1" then "微信卡包"
	    when "2" then "微信小程序"
	    when "3" then "支付宝卡包"
	    when "4" then "动态支付码"
	    when "5" then "门店报手机"
	    when "6" then "火星兔子"
		else "others"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
LEFT JOIN yoren_user_level c on a.USER_ID = c.USER_ID
LEFT JOIN t_consuming_origin_recode d on a.region_block_code = d.region_block_code and a.user_id = d.user_id and a.deal_time = d.deal_time
where a.purchase_date <= '{0}'
  and c.LEVEL_1805 != 'L7'
	and c.LEVEL_1805 != ''  # 更新Level_日期
  and a.region_block_code = '{1}'
group by 1
with rollup
;'''.format(ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

# 4 formula


# 5  本周活跃会员数
'q5_1' : '''
select
	case
		d.consuming_origin
		when 0 then "APP"
		when 1 then "微信卡包"
	    when 2 then "微信小程序"
	    when 3 then "支付宝卡包"
	    when 4 then "动态支付码"
	    when 5 then "门店报手机"
	    when 6 then "火星兔子"
		else "others"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
LEFT JOIN yoren_user_level c on a.USER_ID = c.USER_ID
LEFT JOIN t_consuming_origin_recode d on a.region_block_code = d.region_block_code and a.user_id = d.user_id and a.deal_time = d.deal_time
where a.purchase_date BETWEEN '{0}' and '{1}'
  and c.LEVEL_1805 != 'L7'
	and c.LEVEL_1805 != ''  # 更新Level_日期
  and a.region_block_code = '{2}'
group by 1
;'''.format(STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

'q5_2' :
'''
SELECT consuming_origin,count(*)
from t_consuming_origin_recode
where deal_time BETWEEN '{0}' and '{1}'
and region_block_code = '{2}'
GROUP BY 1
with rollup;
'''.format(STARTTIME, ENDTIME, REGION).replace('\n', ' ').replace('\t', ' '),
}

{
'q5_3' :
'''
SELECT count(*)
from t_consuming_origin_recode
where deal_time BETWEEN '{0}' and '{1}';
'''.format(STARTTIME, ENDTIME).replace('\n', ' ').replace('\t', ' '),


# 6 formula

# 7 formula
#支付方式

'q7' :
'''
select
CASE
payment_method1
when 01 then '现金'
when 50 then '微信'
when 51 then '支付宝'
when 55 then '翼支付'
else '其他'
end as payment_method ,count(*)
from t_pos_purchase_log a
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between '{0}' and '{1}'
  and b.LEVEL_1805 != 'L7'
	and b.LEVEL_1805 != ''
GROUP BY 1
;'''.format(STARTDATE, ENDDATE).replace('\n', ' ').replace('\t', ' '),

# 8 formula

# 9 formula
#会员销售额 包含L7
'q9' : '''
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
where purchase_date between '{0}' and '{1}'
and region_block_code = '{2}'
;'''.format(STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

# 10 formula
#会员交易次数 包含L7
'q10' : '''
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,a.DEAL_TIME))
from t_pos_purchase_log a
where purchase_date between '{0}' and '{1}'
and region_block_code = '{2}'
;'''.format(STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),


# 11 #老会员的总消费金额
'q11' : '''
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between '{0}' and '{1}'
and a.region_block_code = '{2}'
and b.region_block_code = '{2}'
and b.LEVEL_1805 != 'L7'
and b.LEVEL_1805 != ''
and c.create_date < '{3}'
;'''.format(STARTDATE, ENDDATE, REGION, STARTTIME).replace('\n', ' ').replace('\t', ' '),

# 12 #老会员的总交易次数
'q12' : '''
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,a.DEAL_TIME))
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between '{0}' and '{1}'
and a.region_block_code = '{2}'
and b.region_block_code = '{2}'
and b.LEVEL_1805 != 'L7'
and b.LEVEL_1805 != ''
and c.create_date < '{3}'
;'''.format(STARTDATE, ENDDATE, REGION, STARTTIME).replace('\n', ' ').replace('\t', ' '),

# 13 #老会员的客单价
# formula


# 14 #会员的总交易次数
'q14' : """
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,a.DEAL_TIME))
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between '{0}' and '{1}'
and a.region_block_code = '{2}'
and b.region_block_code = '{2}'
and b.LEVEL_1805 != 'L7'
and b.LEVEL_1805 != ''
;""".format(STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

#20元以上的总交易次数
'q20' : """
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,a.DEAL_TIME))
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between '{0}' and '{1}'
and a.region_block_code = '{2}'
and b.region_block_code = '{2}'
and b.LEVEL_1805 != 'L7'
and b.LEVEL_1805 != ''
and (total_payment - COLLECTING_AMOUNT) >=20
;""".format(STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

# 16 ##新会员注册
'q16' : '''
select
	case user_origin
		when "WX" then "微信"
		when "AP" then "支付宝"
	    when "LW" then "门店注册"
	    when "MR" then "无人POS注册"
		else "APP下载"
		end as category,
	count(DISTINCT barcode)
from t_user
where CREATE_DATE between '{0}' and '{1}'
and region_block_code = '{2}'
GROUP BY 1;'''.format(STARTTIME, ENDTIME, REGION).replace('\n', ' ').replace('\t', ' '),

# 17 formula

# 18 #新会员活跃人数
'q18' : '''
select
	case
		d.consuming_origin
		when 0 then "APP"
		when 1 then "微信卡包"
    when 2 then "微信小程序"
    when 3 then "支付宝卡包"
    when 4 then "动态支付码"
    when 5 then "门店报手机"
    when 6 then "火星兔子"
		else "others"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
LEFT JOIN t_consuming_origin_recode d on a.region_block_code = d.region_block_code and a.user_id = d.user_id and a.deal_time = d.deal_time
where a.purchase_date BETWEEN '{0}' and '{1}'
  and a.region_block_code = '{2}'
  and d.region_block_code = '{2}'
  and b.CREATE_DATE between '{3}' and '{4}'
group by 1
;
'''.format(STARTDATE, ENDDATE, REGION, STARTTIME, ENDTIME).replace('\n', ' ').replace('\t', ' '),
# 19 formula

# 20 formula

# 21 #上周新会员流失人数
'q21' : '''
select
	case
		b.user_origin
		when "WX" then "微信"
		when "AP" then "支付宝"
    when "LW" then "门店注册"
    when "MR" then "无人POS注册"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
where a.PURCHASE_DATE between '{0}' and '{1}'##上周活跃
and b.create_date between '{2}' and '{3}'
and a.user_barcode not in
(
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between '{4}' and '{5}'
	)
 and a.region_block_code = '{6}'
group by 1
;'''.format(LOSTSTART, LOSTEND, LOSTBEGINTIME, LOSTENDTIME, STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),

# 22 formula
#
# 23 formula


#老会员的活跃人数
'q22' : '''
select
	case
		d.consuming_origin
		when 0 then "APP"
		when 1 then "微信卡包"
    when 2 then "微信小程序"
    when 3 then "支付宝卡包"
    when 4 then "动态支付码"
    when 5 then "门店报手机"
    when 6 then "火星兔子"
		else "others"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
LEFT JOIN t_consuming_origin_recode d on a.region_block_code = d.region_block_code and a.user_id = d.user_id and a.deal_time = d.deal_time
where a.purchase_date BETWEEN '{0}' and '{1}'
  and a.region_block_code = '{2}'
  and d.region_block_code = '{2}'
  and b.CREATE_DATE < '{3}'
group by 1
;'''.format(STARTDATE, ENDDATE, REGION, STARTTIME).replace('\n', ' ').replace('\t', ' '),

#老会员的流失人数
'q23' : '''
select
	case
		b.user_origin
		when "WX" then "微信"
		when "AP" then "支付宝"
    when "LW" then "门店注册"
    when "MR" then "无人POS注册"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
left join yoren_user_level c on a.user_id = c.user_id
where a.PURCHASE_DATE between '{0}' and '{1}'##上周活跃
and b.create_date < '{2}'
and a.user_barcode not in
(
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between '{3}' and '{4}'
	)
and a.region_block_code = '{5}'
and c.LEVEL_1805 != 'L7'
and c.LEVEL_1805 != ''
group by 1;
'''.format(LOSTSTART, LOSTEND, LOSTBEGINTIME, STARTDATE, ENDDATE, REGION).replace('\n', ' ').replace('\t', ' '),
}

postgre_queries = {
'q1':'select asdasdfsadf from users limit 100',
'q2':'select * from users limit 100',
'q3':'select count(*) from users',
'q4':'select count(*) from users',
'q5':'select count(*) from receipts',
'q6':'select count(*) from users',
'q7':'select count(*) from users',
'q8':'select count(*) from receipts',
'q9':'select count(*) from users',
'q10':'select count(*) from users',
'q11':'select count(*) from receipts',
'q12':'select count(*) from users',
}

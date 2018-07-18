queries = {'set_attributes': [
    "set @region = 'sh-lawson';",
    "set @areacode = '19000';",
    #本周
    "set @begin = '20180625';",
    "set @end = '20180701';",
    "set @begintime = '2018-06-25 00:00:00';",
    "set @endtime = '2018-07-01 23:59:59';",
    #上周-计算流失会员
    "set @lostbegin = '20180618';",
    "set @lostend = '20180624';",
    "set @lostbegintime = '2018-06-18 00:00:00';",
    "set @lostendtime = '2018-06-24 23:59:59';"
    ],
#
#
# 1 #会员占比（金额）
# formula
#
# 2 #会员占比（客数）
# formula
#
# 3 #会员总销售额 包含L7
'q3': """
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
where purchase_date between @begin and @end
and region_block_code = @region;
""",

# 4 #POS周销售额
# Lawson提供

# 5 #会员总交易次数 包含L7
'q5':
"""
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
from t_pos_purchase_log a
where purchase_date between @begin and @end
and region_block_code = @region
;""",

# 6 #POS周交易次数
# Lawson提供

# 7 #会员总销量
'q7':
"""
select sum(sells_count)
from t_pos_purchase_commodity_log a
left join yoren_user_level c on a.user_id = c.user_id
where a.region_block_code = @region
  and c.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.drcr_type = 1
  and c.level_1805 != 'L7';
""",

# 8 #WAU
'q8':
"""
select
	case
		b.user_origin
		when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
left join t_user b on a.user_id = b.user_id
LEFT JOIN yoren_user_level c on a.USER_ID = c.USER_ID
where a.purchase_date between @begin and @end
  and c.LEVEL_1805 != 'L7'
  and a.region_block_code = @region
  and c.region_block_code = @region
group by 1;
""",

# 9 #WAU渠道结构比
# formula
#
# 10 #累计会员人数
'q10':
"""
select
case
		user_origin
	  when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,count(DISTINCT barcode)
from t_user
where region_block_code = @region
and create_date <= @endtime
and del_flg = '0'
GROUP BY 1;
""",

# 11 # 2018年累计活跃人数
'q11':
"""
select
	case
		b.user_origin
		when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_id )
from t_pos_purchase_log a
left join t_user b on a.user_id = b.user_id
#LEFT JOIN yoren_user_level c on a.USER_ID = c.USER_ID
where a.purchase_date between '20180101' and @end
  and b.del_flg = '0'
  and a.region_block_code = @region
  #and c.region_block_code = @region
group by 1;
""",


# 12 #年活跃率
# formula


# 13~17 # PV UU
# 没写


# 18 #人均消费金额-老会员
'q18' :
"""
select sum(total_payment - COLLECTING_AMOUNT)/count(DISTINCT a.user_id)
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
and c.create_date < @begintime;
""",

# 19 #人均来店频次-老会员
'q19':
"""
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))	/count(DISTINCT a.user_id)
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
and c.create_date < @begintime;
""",

# 20 #客单价-老会员
'q20':
"""
select avg(total_payment - COLLECTING_AMOUNT )
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
and c.create_date < @begintime;
""",

# 21 # 高客单占比%
'q21':
"""
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
from t_pos_purchase_log a
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
and (total_payment - COLLECTING_AMOUNT) >= 20
;
""",
# formula （除以第五行）


# 22 # 新会员注册人数
'q22':
"""
select
case
		user_origin
    when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,count(DISTINCT barcode)
from t_user
where CREATE_DATE between @begintime and @endtime
and region_block_code = @region
GROUP BY 1;
""",

# 23 # 新会员渠道结构比
# formula
#
# 24 # 新会员活跃人数
'q24':
"""
select
	case
		b.user_origin
		when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
where a.purchase_date between @begin and @end
	and b.CREATE_DATE between @begintime and @endtime
and a.region_block_code = @region
group by 1;
""",

# 25 # 新会员活跃率
# formula

# 26 # 新会员活跃渠道结构比
# formula


# 27 # 新会员流失人数
'q27':
"""
select
	case
		b.user_origin
		when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
where a.PURCHASE_DATE between @lostbegin and @lostend##上周活跃
and b.create_date between @lostbegintime and @lostendtime
and a.user_barcode not in
(
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between @begin and @end
	)
 and a.region_block_code = @region
group by 1
;
""",

# 28 # 新会员流失率
# formula



# 29 # 老会员活跃人数
'q29':
"""
select
	case
		b.user_origin
    when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
where a.purchase_date between @begin and @end
	and b.CREATE_DATE < @begintime
and a.region_block_code = @region
group by 1;
""",

# 30 # 老会员活跃率
# formula



# 31 # 老会员流失人数
'q31':
"""
select
	case
		b.user_origin
	  when "WX" then "微信卡包"
    when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
    when "LW" then "门店报手机"
    when "MR" then "火星兔子"
		else "APP下载"
	end as category,
	count( distinct a.user_barcode )
from t_pos_purchase_log a
left join t_user b on a.user_barcode = b.barcode
left join yoren_user_level c on a.user_id = c.user_id
where a.PURCHASE_DATE between @lostbegin and @lostend##上周活跃
and b.create_date < @lostbegintime
and a.user_barcode not in
(
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between @begin and @end
	)
and a.region_block_code = @region
and c.LEVEL_1805 != 'L7'
group by 1
;
""",

# 32 # 老会员流失率
# formula



# 33 # 会员购买售价总额
'q33':
"""
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
;
""",


# 34 # 含L7总销售额(含税)
'q34':
"""
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
where purchase_date between @begin and @end
and region_block_code = @region
;
""",

# 35 # L7销售额
'q35':
"""
select sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log a
inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
left join yoren_user_level b on a.user_id = b.user_id
where purchase_date between @begin and @end
and a.region_block_code = @region
and b.region_block_code = @region
and b.LEVEL_1805 != 'L7'
;
""",

# 36 # L7销售额占比
# formula

# 37# 每周40次以上金额
'q37':
"""
SELECT sum(total_payment - COLLECTING_AMOUNT)
from t_pos_purchase_log
where user_id in
(
select DISTINCT a.USER_ID
from t_pos_purchase_log a
where a.purchase_date between @begin and @end
and a.REGION_BLOCK_CODE =@region
and user_id != ''
group by 1
having count(*) >= 40   # 消费总次数
)
and purchase_date between @begin and @end
and REGION_BLOCK_CODE =@region
;
""",

# 38 # 总发行积分
'q38':
"""
select sum(point_num)
from t_point_history
where region_block_code = @region
;
""",

# 39 # 总被使用积分
'q39':
"""
select sum(used_point)
from t_point_used
where region_block_code = @region
;
""",

# 40 # 2018年年底过期积分
'q40':
"""
select sum(remain_point)
from t_point_history
where region_block_code = @region
and point_end_date = '2018-12-31'
;
""",

# 41 # 总使用率
# formula


# 42 # 剩余积分
# formula

# 43 # 剩余积分换算金额
# formula

# 44 # 已过期积分
'q44':
"""
select sum(remain_point)
from t_point_history
where region_block_code = @region
and point_end_date < '2018-12-31'
;
""",


# 45 # 本周发行积分个数
'q45':
"""
select sum(point_num)
from t_point_history
where region_block_code = @region
and create_date between @begintime and @endtime
;
""",

# 46 # 本周被兑换积分个数
'q46':
"""
select sum(used_point)
from t_point_used
where region_block_code = @region
and create_date between @begintime and @endtime;
""",

# 47 # 会员商品SKU数
'q47':
"""
SELECT count(DISTINCT commodity_cd)
from t_discount
where region_block_code = @region
and publish_date_from <= @endtime
and publish_date_to >= @begintime
;
""",

# 48 # 会员商品购买人数
'q48':
"""
select count(distinct a.user_id)
from t_pos_purchase_commodity_log a
left join yoren_user_level d on a.user_id = d.user_id and a.region_block_code = d.region_block_code
where a.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.PROMOTION_FLG = '1'
  and d.level_1805 != 'L7';
""",


# 49 # 会员商品销量
'q49':
"""
select sum(sells_count)
from t_pos_purchase_commodity_log a
left join yoren_user_level d on a.user_id = d.user_id  and a.region_block_code = d.region_block_code
where a.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.PROMOTION_FLG = '1'
  and d.level_1805 != 'L7';
""",

# 50 # 会员商品销量占比
# formula

# 51 # 会员商品销售额
'q51':
"""
select sum(DISCOUNT_TAX_INCLUSIVE_PRICE )
from t_pos_purchase_commodity_log a
left join yoren_user_level d on a.user_id = d.user_id
where a.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.PROMOTION_FLG = '1'
  and d.level_1805 != 'L7';
""",


# 52 # 会员商品销售额占比
# formula


# 53 # 集点对象SKU数 --对象是分类商品的 没有考虑,如何添加
'q53':
"""
SELECT count(*)
FROM t_activity_commodity a
WHERE  ACTIVITY_ID in
(
SELECT DISTINCT campaign_id
FROM t_campaign a
where region_block_code = @region
and campaign_date_from <= @endtime
and campaign_date_to >= @begintime);
""",

# 54 # 集点参与人数
'q54':
"""
SELECT count(DISTINCT user_id)
FROM t_user_stamp
WHERE  campaign_id in
(
SELECT DISTINCT campaign_id
FROM t_campaign a
where region_block_code = @region
and campaign_date_from <= @endtime
and campaign_date_to >= @begintime);
""",

# 55 # 集点对象商品销量
'q55':
"""
SELECT sum(stamp_num)
FROM t_user_stamp
WHERE  campaign_id in
(
SELECT DISTINCT campaign_id
FROM t_campaign a
where region_block_code = @region
and campaign_date_from <= @endtime
and campaign_date_to >= @begintime);
""",

# 56 # 集点对象商品销量占比
# formula



# 57 # 集点对象商品销售额 --有点复杂,且没有包含分类集点商品
'q57':
"""
SELECT
	sum(DISCOUNT_TAX_INCLUSIVE_PRICE)
FROM
	t_pos_purchase_commodity_log
WHERE
	region_block_code = @region
AND purchase_date BETWEEN @BEGIN AND @END
AND commodity_cd IN (
	SELECT
		commodity_cd
	FROM
		t_activity_commodity a
	WHERE
		ACTIVITY_ID IN (
			SELECT DISTINCT
				campaign_id
			FROM
				t_campaign a
			WHERE
				region_block_code = @region
			AND campaign_date_from <= @endtime
			AND campaign_date_to >= @begintime));
""",

# 58 # 集点对象商品销售额占比



# 59 # 实际发出礼券张数
'q59':
"""
select
CASE
c.send_type
when 0 then '一般发送'
when 1 then 'PUSH发送'
when 2 then '集点礼券'
when 3 then '活动派发（扫码/电子码）'
when 4 then '积分商城兑换'
when 5 then '红包'
when 6 then '注册'
when 7 then '购买'
else 'others'
end as 'type' ,count(*)
from t_user_coupon  a
left join yoren_user_level b on a.user_id = b.user_id
LEFT JOIN t_coupon c on a.coupon_id = c.coupon_id
where b.region_block_code = @region
  and c.region_block_code = @region
  and binding_date between @begintime and @endtime
  and level_1805 != 'L7'
GROUP BY 1;
""",
# 签到获得
# 抽奖获得
# 每日福利获得   都是活动派发


# 60 # 积分兑换礼券使用张数
'q60':
"""
select count(*)
from t_user_coupon  a
left join yoren_user_level b on a.user_id = b.user_id
LEFT JOIN t_coupon c on a.coupon_id = c.coupon_id
where c.region_block_code = @region
  and b.region_block_code = @region
  and use_date between @begintime and @endtime
  and level_1805 != 'L7'
  and c.send_type = '4';
""",

# 61 # 积分兑换礼券使用率
# formula

# 62 # 会员退货率
# formula

# 63 # 会员退货次数
'q63':
"""
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
from t_pos_purchase_commodity_log a
left join yoren_user_level c on a.user_id = c.user_id
where a.region_block_code = @region
  and c.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.business_flg = 'A'
  and c.level_1707 != 'L7';
""",

# 64 # 会员活动商品退货次数
'q64':
"""
select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
from t_pos_purchase_commodity_log a
left join yoren_user_level c on a.user_id = c.user_id
where a.region_block_code = @region
  and c.region_block_code = @region
  and a.purchase_date between @begin and @end
  and a.business_flg = 'A'
  and c.level_1707 != 'L7'
  and a.promotion_flg in ('1', '2', '3');
"""
}
# 65 # QR页面浏览总次数
# 66 # 下载罗森点点次数

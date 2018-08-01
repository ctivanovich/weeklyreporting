# -*- coding: utf-8 -*-
import datetime

NOW = datetime.datetime.now()

begin = (NOW - datetime.timedelta(days=7)).strftime("%Y%m%d")
end = (NOW - datetime.timedelta(days=1)).strftime("%Y%m%d")
begintime = (NOW - datetime.timedelta(days=7)).strftime("%Y-%m-%d 00:00:00")
endtime = (NOW - datetime.timedelta(days=1)).strftime("%Y-%m-%d 11:59:59")
lostbegin = (NOW - datetime.timedelta(days=14)).strftime("%Y%m%d")
lostend = (NOW - datetime.timedelta(days=8)).strftime("%Y%m%d")
lostbegintime = (NOW - datetime.timedelta(days=14)).strftime("%Y%m%d  00:00:00")
lostendtime = (NOW - datetime.timedelta(days=8)).strftime("%Y%m%d 23:59:59")

def get_queries(region):
    queries = {
    'q3':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    where purchase_date between '{begin}' and '{end}'
    and region_block_code = '{region}';
    """,

    # 4 #POS周销售额
    # Lawson提供

    # 5 #会员总交易次数 包含L7
    'q5':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_log a
    where purchase_date between '{begin}' and '{end}'
    and region_block_code = '{region}'
    ;""",

    # 6 #POS周交易次数
    # Lawson提供

    # 7 #会员总销量
    'q7':
    f"""
    select sum(sells_count)
    from t_pos_purchase_commodity_log a
    left join yoren_user_level c on a.user_id = c.user_id
    where a.region_block_code = '{region}'
      and c.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.drcr_type = 1
      and c.level_1805 != 'L7';
    """,

    # 8 #WAU
    'q8':
    f"""
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
    where a.purchase_date between '{begin}' and '{end}'
      and c.LEVEL_1805 != 'L7'
      and a.region_block_code = '{region}'
      and c.region_block_code = '{region}'
    group by 1;
    """,

    # 9 #WAU渠道结构比
    # formula
    #
    # 10 #累计会员人数
    'q10':
    f"""
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
    where region_block_code = '{region}'
    and create_date <= '{endtime}'
    and del_flg = '0'
    GROUP BY 1;
    """,

    # 11 # 2018年累计活跃人数
    'q11':
    f"""
    select case
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
    where a.purchase_date between '20180101' and '{end}'
      and b.del_flg = '0'
      and a.region_block_code = '{region}'
      #and c.region_block_code = '{region}'
    group by 1;
    """,


    # 12 #年活跃率
    # formula


    # 13~17 # PV UU
    # 没写


    # 18 #人均消费金额-老会员
    'q18' :
    f"""
    select case
		user_origin
        when "WX" then "微信卡包"
        when "WM" then "微信小程序"
        when "AP" then "支付宝卡包"
        when "LW" then "门店报手机"
        when "MR" then "火星兔子"
        	else "APP下载"
        end as category,
        sum(total_payment - COLLECTING_AMOUNT)/count(DISTINCT a.user_id)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    and c.create_date < '{begintime}';
    """,

    # 19 #人均来店频次-老会员
    'q19':
    f"""
    select case
		user_origin
        when "WX" then "微信卡包"
        when "WM" then "微信小程序"
        when "AP" then "支付宝卡包"
        when "LW" then "门店报手机"
        when "MR" then "火星兔子"
        	else "APP下载"
        end as category,
        count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))	/count(DISTINCT a.user_id)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    and c.create_date < '{begintime}';
    """,

    # 20 #客单价-老会员
    'q20':
    f"""
    select case
		user_origin
        when "WX" then "微信卡包"
        when "WM" then "微信小程序"
        when "AP" then "支付宝卡包"
        when "LW" then "门店报手机"
        when "MR" then "火星兔子"
        	else "APP下载"
        end as category,
        avg(total_payment - COLLECTING_AMOUNT )
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    and c.create_date < '{begintime}';
    """,

    # 21 # 高客单占比%
    'q21':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_log a
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    and (total_payment - COLLECTING_AMOUNT) >= 20
    ;
    """,
    # formula （除以第五行）


    # 22 # 新会员注册人数
    'q22':
    f"""
    select
    case user_origin
        when "WX" then "微信卡包"
        when "WM" then "微信小程序"
    	when "AP" then "支付宝卡包"
        when "LW" then "门店报手机"
        when "MR" then "火星兔子"
    	else "APP下载"
    	end as category,
        count(DISTINCT barcode)
    from t_user
    where CREATE_DATE between '{begintime}' and '{endtime}'
    and region_block_code = '{region}'
    GROUP BY 1;
    """,

    # 23 # 新会员渠道结构比
    # formula
    #
    # 24 # 新会员活跃人数
    'q24':
    f"""
    select case
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
    where a.purchase_date between '{begin}' and '{end}'
    	and b.CREATE_DATE between '{begintime}' and '{endtime}'
    and a.region_block_code = '{region}'
    group by 1;
    """,

    # 25 # 新会员活跃率
    # formula

    # 26 # 新会员活跃渠道结构比
    # formula


    # 27 # 新会员流失人数
    'q27':
    f"""
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
    where a.PURCHASE_DATE between '{lostbegin}' and '{lostend}'##上周活跃
    and b.create_date between '{lostbegintime}' and '{lostendtime}'
    and a.user_barcode not in
    (
    		select distinct user_barcode
    		from t_pos_purchase_log
    		where PURCHASE_DATE between '{begin}' and '{end}'
    	)
     and a.region_block_code = '{region}'
    group by 1
    ;
    """,

    # 28 # 新会员流失率
    # formula



    # 29 # 老会员活跃人数
    'q29':
    f"""
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
    where a.purchase_date between '{begin}' and '{end}'
    	and b.CREATE_DATE < '{begintime}'
    and a.region_block_code = '{region}'
    group by 1;
    """,

    # 30 # 老会员活跃率
    # formula



    # 31 # 老会员流失人数
    'q31':
    f"""
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
    where a.PURCHASE_DATE between '{lostbegin}' and '{lostend}'##上周活跃
    and b.create_date < '{lostbegintime}'
    and a.user_barcode not in
    (
    		select distinct user_barcode
    		from t_pos_purchase_log
    		where PURCHASE_DATE between '{begin}' and '{end}'
    	)
    and a.region_block_code = '{region}'
    and c.LEVEL_1805 != 'L7'
    group by 1
    ;
    """,

    # 32 # 老会员流失率
    # formula



    # 33 # 会员购买售价总额
    'q33':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    ;
    """,


    # 34 # 含L7总销售额(含税)
    'q34':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    where purchase_date between '{begin}' and '{end}'
    and region_block_code = '{region}'
    ;
    """,

    # 35 # L7销售额
    'q35':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id and a.REGION_BLOCK_CODE = c.region_block_code
    left join yoren_user_level b on a.user_id = b.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.region_block_code = '{region}'
    and b.LEVEL_1805 != 'L7'
    ;
    """,

    # 36 # L7销售额占比
    # formula

    # 37# 每周40次以上金额
    'q37':
    f"""
    SELECT sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log
    JOIN
    (
    SELECT a.USER_ID
    from t_pos_purchase_log a
    where a.purchase_date between '{begin}' and '{end}'
    and a.REGION_BLOCK_CODE ='{region}'
    and user_id > 0
    group by 1
    HAVING count(*) > 40 # 消费总次数
    ) sub1 ON sub1.user_id = t_pos_purchase_log.user_id
    WHERE purchase_date between '{begin}' and '{end}'
    and REGION_BLOCK_CODE = '{region}';
    """,

    # 38 # 总发行积分
    'q38':
    f"""
    select sum(point_num)
    from t_point_history
    where region_block_code = '{region}'
    ;
    """,

    # 39 # 总被使用积分
    'q39':
    f"""
    select sum(used_point)
    from t_point_used
    where region_block_code = '{region}'
    ;
    """,

    # 40 # 2018年年底过期积分
    'q40':
    f"""
    select sum(remain_point)
    from t_point_history
    where region_block_code = '{region}'
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
    f"""
    select sum(remain_point)
    from t_point_history
    where region_block_code = '{region}'
    and point_end_date < '2018-12-31'
    ;
    """,


    # 45 # 本周发行积分个数
    'q45':
    f"""
    select sum(point_num)
    from t_point_history
    where region_block_code = '{region}'
    and create_date between '{begintime}' and '{endtime}'
    ;
    """,

    # 46 # 本周被兑换积分个数
    'q46':
    f"""
    select sum(used_point)
    from t_point_used
    where region_block_code = '{region}'
    and create_date between '{begintime}' and '{endtime}';
    """,

    # 47 # 会员商品SKU数
    'q47':
    f"""
    SELECT count(DISTINCT commodity_cd)
    from t_discount
    where region_block_code = '{region}'
    and publish_date_from <= '{endtime}'
    and publish_date_to >= '{begintime}'
    ;
    """,

    # 48 # 会员商品购买人数
    'q48':
    f"""
    select count(distinct a.user_id)
    from t_pos_purchase_commodity_log a
    left join yoren_user_level d on a.user_id = d.user_id and a.region_block_code = d.region_block_code
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1'
      and d.level_1805 != 'L7';
    """,


    # 49 # 会员商品销量
    'q49':
    f"""
    select sum(sells_count)
    from t_pos_purchase_commodity_log a
    left join yoren_user_level d on a.user_id = d.user_id  and a.region_block_code = d.region_block_code
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1'
      and d.level_1805 != 'L7';
    """,

    # 50 # 会员商品销量占比
    # formula

    # 51 # 会员商品销售额
    'q51':
    f"""
    select sum(DISCOUNT_TAX_INCLUSIVE_PRICE )
    from t_pos_purchase_commodity_log a
    left join yoren_user_level d on a.user_id = d.user_id
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1'
      and d.level_1805 != 'L7';
    """,


    # 52 # 会员商品销售额占比
    # formula


    # 53 # 集点对象SKU数 --对象是分类商品的 没有考虑,如何添加
    'q53':
    f"""
    SELECT count(*)
    FROM t_activity_commodity a
    WHERE  ACTIVITY_ID in
    (
    SELECT DISTINCT campaign_id
    FROM t_campaign a
    where region_block_code = '{region}'
    and campaign_date_from <= '{endtime}'
    and campaign_date_to >= '{begintime}');
    """,

    # 54 # 集点参与人数
    'q54':
    f"""
    SELECT count(DISTINCT user_id)
    FROM t_user_stamp
    WHERE  campaign_id in
    (
    SELECT DISTINCT campaign_id
    FROM t_campaign a
    where region_block_code = '{region}'
    and campaign_date_from <= '{endtime}'
    and campaign_date_to >= '{begintime}');
    """,

    # 55 # 集点对象商品销量
    'q55':
    f"""
    SELECT sum(stamp_num)
    FROM t_user_stamp
    WHERE  campaign_id in
    (
    SELECT DISTINCT campaign_id
    FROM t_campaign a
    where region_block_code = '{region}'
    and campaign_date_from <= '{endtime}'
    and campaign_date_to >= '{begintime}');
    """,

    # 56 # 集点对象商品销量占比
    # formula



    # 57 # 集点对象商品销售额 --有点复杂,且没有包含分类集点商品
    'q57':
    f"""
    SELECT
    	sum(DISCOUNT_TAX_INCLUSIVE_PRICE)
    FROM
    	t_pos_purchase_commodity_log
    WHERE
    	region_block_code = '{region}'
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
    				region_block_code = '{region}'
    			AND campaign_date_from <= '{endtime}'
    			AND campaign_date_to >= '{begintime}'));
    """,

    # 58 # 集点对象商品销售额占比



    # 59 # 实际发出礼券张数
    'q59':
    f"""
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
    where b.region_block_code = '{region}'
      and c.region_block_code = '{region}'
      and binding_date between '{begintime}' and '{endtime}'
      and level_1805 != 'L7'
    GROUP BY 1;
    """,
    # 签到获得
    # 抽奖获得
    # 每日福利获得   都是活动派发


    # 60 # 积分兑换礼券使用张数
    'q60':
    f"""
    select count(*)
    from t_user_coupon  a
    left join yoren_user_level b on a.user_id = b.user_id
    LEFT JOIN t_coupon c on a.coupon_id = c.coupon_id
    where c.region_block_code = '{region}'
      and b.region_block_code = '{region}'
      and use_date between '{begintime}' and '{endtime}'
      and level_1805 != 'L7'
      and c.send_type = '4';
    """,

    # 61 # 积分兑换礼券使用率
    # formula

    # 62 # 会员退货率
    # formula

    # 63 # 会员退货次数
    'q63':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_commodity_log a
    left join yoren_user_level c on a.user_id = c.user_id
    where a.region_block_code = '{region}'
      and c.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.business_flg = 'A'
      and c.level_1707 != 'L7';
    """,

    # 64 # 会员活动商品退货次数
    'q64':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_commodity_log a
    left join yoren_user_level c on a.user_id = c.user_id
    where a.region_block_code = '{region}'
      and c.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.business_flg = 'A'
      and c.level_1707 != 'L7'
      and a.promotion_flg in ('1', '2', '3');
    """}
    return queries

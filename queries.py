import datetime

NOW = datetime.datetime.now()
#NOW = datetime.datetime.strptime("20181224", "%Y%m%d") #for debugging

#set Yoren user level for the L7 query (quert 35)
last_ym = (NOW.replace(day=1) - datetime.timedelta(days=1)).strftime("%y%m")
yoren_user_level = "level_" + last_ym

#get datetime values for one week and 2 weeks ago
begin = (NOW - datetime.timedelta(days=7)).strftime("%Y%m%d")
end = (NOW - datetime.timedelta(days=1)).strftime("%Y%m%d")
begintime = (NOW - datetime.timedelta(days=7)).strftime("%Y-%m-%d 00:00:00")
endtime =  (NOW - datetime.timedelta(days=1)).strftime("%Y-%m-%d 23:59:59")
#上周-计算流失会员

lostbegin = (NOW - datetime.timedelta(days=14)).strftime("%Y%m%d")
lostend = (NOW - datetime.timedelta(days=8)).strftime("%Y%m%d")

lostbegintime = (NOW - datetime.timedelta(days=14)).strftime("%Y-%m-%d 00:00:00")
lostendtime = (NOW - datetime.timedelta(days=8)).strftime("%Y-%m-%d 23:59:59")


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
    select count(DISTINCT CONCAT(a.SHOP_ID,
    a.POS_NO ,
    serial_number,a.DEAL_TIME))
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
    where a.purchase_date between '{begin}' and '{end}'
      and a.region_block_code = '{region}'
      and a.drcr_type = 1;
    """,

    # 8 #WAU
    'q8':
    f"""
    select
    	case b.user_origin
        	when "WX" then "微信卡包"
            when "WM" then "微信小程序"
        	when "AP" then "支付宝卡包"
            when "LW" then "门店报手机"
            when "MR" then "火星兔子"
            when "FI" then "刷脸"
        	else "APP"
    	end as category,
    	count( distinct a.user_id )
    from t_pos_purchase_log a
    left join t_user b on a.user_id = b.user_id
    where a.purchase_date between '{begin}' and '{end}'
      and a.region_block_code = '{region}'
      and b.del_flg = '0'
    group by 1;
    """,

    # 9 #WAU渠道结构比
    # formula
    #
    # 10 #累计会员人数
    'q10':
    f"""
    select
    case user_origin
    	when "WX" then "微信卡包"
        when "WM" then "微信小程序"
		when "AP" then "支付宝卡包"
        when "LW" then "门店报手机"
        when "MR" then "火星兔子"
        when "FI" then "刷脸"
		else "APP"
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
        when "FI" then "刷脸"
		      else "APP"
    	end as category,
    	count( distinct a.user_id )
    from t_pos_purchase_log a
    left join t_user b on a.user_id = b.user_id
    where a.purchase_date between '20180101' and '{end}'
      and b.del_flg = '0'
      and a.region_block_code = '{region}'
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
        when "FI" then "刷脸"
        	else "APP"
        end as category,
        sum(total_payment - COLLECTING_AMOUNT)/count(DISTINCT a.user_id)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and c.create_date < '{begintime}'
    and c.del_flg = '0'
    GROUP BY 1;
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
        when "FI" then "刷脸"
        	else "APP"
        end as category,
        count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))	/count(DISTINCT a.user_id)
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and c.create_date < '{begintime}'
    and c.del_flg = '0'
    GROUP BY 1;
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
        when "FI" then "刷脸"
        	else "APP"
        end as category,
        avg(total_payment - COLLECTING_AMOUNT )
    from t_pos_purchase_log a
    inner JOIN t_user c on a.USER_ID = c.user_id
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and c.create_date < '{begintime}'
    and c.del_flg = '0'
    GROUP BY 1;
    """,

    # 21 # 高客单订单笔数
    'q21':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_log a
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and (total_payment - COLLECTING_AMOUNT) >= 20;
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
            when "FI" then "刷脸"
        	else "APP"
    	end as category,
    count(DISTINCT barcode)
    from t_user
    where CREATE_DATE between '{begintime}' and '{endtime}'
    and region_block_code = '{region}'
    and del_flg = '0'
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
        when "FI" then "刷脸"
    		else "APP"
    	end as category,
    	count( distinct a.user_barcode )
    from t_pos_purchase_log a
    left join t_user b on a.user_barcode = b.barcode
    where a.purchase_date between '{begin}' and '{end}'
    	and b.CREATE_DATE between '{begintime}' and '{endtime}'
    and a.region_block_code = '{region}'
    and b.del_flg = '0'
    group by 1;
    """,

    # 25 # 新会员活跃率
    # formula

    # 26 # 新会员活跃渠道结构比
    # formula


    # 27 # 新会员继续活跃人数
    'q27':
    f"""
    select
    	case b.user_origin
        	when "WX" then "微信卡包"
            when "WM" then "微信小程序"
        	when "AP" then "支付宝卡包"
            when "LW" then "门店报手机"
            when "MR" then "火星兔子"
            when "FI" then "刷脸"
    		else "APP"
    	end as category,
    	count( distinct a.user_barcode )
    from t_pos_purchase_log a
    left join t_user b on a.user_barcode = b.barcode
    inner join (
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between '{begin}' and '{end}'
        and region_block_code = '{region}'
    	) c on a.user_barcode = c.user_barcode
    where a.PURCHASE_DATE between '{lostbegin}' and '{lostend}'
    and b.create_date between '{lostbegintime}' and '{lostendtime}'
     and a.region_block_code = '{region}'
    and b.del_flg = '0'
    group by 1;

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
            when "FI" then "刷脸"
    		else "APP"
    	end as category,
    	count( distinct a.user_id )
    from t_pos_purchase_log a
    left join t_user b on a.user_id = b.user_id
    where a.purchase_date between '{begin}' and '{end}'
      and a.region_block_code = '{region}'
      and b.CREATE_DATE < '{begintime}'
      and b.del_flg = '0'
    group by 1;
    """,

    # 30 # 老会员活跃率
    # formula



    # 31 # 老会员继续活跃人数
    'q31':
    f"""
    select
    	case b.user_origin
        	when "WX" then "微信卡包"
            when "WM" then "微信小程序"
        	when "AP" then "支付宝卡包"
            when "LW" then "门店报手机"
            when "MR" then "火星兔子"
            when "FI" then "刷脸"
        	else "APP"
    	end as category,
    	count( distinct a.user_barcode )
    from t_pos_purchase_log a
    left join t_user b on a.user_barcode = b.barcode
    inner join (
		select distinct user_barcode
		from t_pos_purchase_log
		where PURCHASE_DATE between '{begin}' and '{end}'
        and region_block_code = '{region}'
    	) d on a.user_barcode = d.user_barcode
    where a.PURCHASE_DATE between '{lostbegin}' and '{lostend}'##上周活跃
        and b.create_date < '{lostbegintime}'
        and a.region_block_code = '{region}'
        and b.del_flg = '0'
    group by 1;
    """,

    # 32 # 老会员流失率
    # formula



    # 33 # 会员购买售价总额
    'q33':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    ;
    """,


    # 34 # 含L7总销售额(含税)
    'q34':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log
    where purchase_date between '{begin}' and '{end}'
    and region_block_code = '{region}'
    ;""",

	# 35 # L7人群的消费额(含税)
    'q35':
    f"""
    select sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    left join yoren_user_level b on a.user_id = b.user_id and a.region_block_code = b.REGION_BLOCK_CODE
    where purchase_date between '{begin}' and '{end}'
    and a.region_block_code = '{region}'
    and b.{yoren_user_level} = 'L7'
    ;""",

    # 36 # L7销售额占比
    # formula

    # 37# 每周40次以上金额
    'q37':
    f"""
    SELECT sum(total_payment - COLLECTING_AMOUNT)
    from t_pos_purchase_log a
    JOIN
    (
    SELECT DISTINCT a.USER_ID
    from t_pos_purchase_log a
    where a.purchase_date between '{begin}' and '{end}'
    and a.REGION_BLOCK_CODE ='{region}'
    and user_id != ''
    group by 1
    HAVING count(*) >= 40 # 消费总次数
    ) sub1 ON sub1.user_id = a.user_id
    and purchase_date between '{begin}' and '{end}'
    and REGION_BLOCK_CODE = '{region}';
    """,

    # 38 # 总发行积分
    'q38':
    f"""
    select sum(point_num)
    from t_point_history
    where region_block_code = '{region}'
    and create_date between '2017-01-01 00:00:00' and '{endtime}';
    """,

    # 39 # 总被使用积分
    # 'q39':
    # f"""
    # select sum(used_point)
    # from t_point_used
    # where region_block_code = '{region}'
    # and create_date <= '{endtime}';
    # """,

    # 40 # 2018年年底过期积分
    'q40':
    f"""
    select sum(remain_point)
    from t_point_history
    where region_block_code = '{region}'
    and create_date between '2017-01-01' and '{endtime}'
    ;
    """,

    # 41 # 总使用率
    # formula


    # 42 # 剩余积分
    # formula

    # 43 # 剩余积分换算金额
    # formula

    # 44 # 已过期积分
    # 'q44':
    # f"""
    # select sum(remain_point)
    # from t_point_history
    # where region_block_code = '{region}'
    # and point_end_date < '2018-12-31'
    # and create_date <= '{endtime}'
    # ;
    # """,


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
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1';
    """,


    # 49 # 会员商品销量
    'q49':
    f"""
    select sum(sells_count)
    from t_pos_purchase_commodity_log a
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1';
    """,

    # 50 # 会员商品销量占比
    # formula

    # 51 # 会员商品销售额
    'q51':
    f"""
    select sum(DISCOUNT_TAX_INCLUSIVE_PRICE )
    from t_pos_purchase_commodity_log a
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.PROMOTION_FLG = '1';
    """,


    # 52 # 会员商品销售额占比
    # formula


    # 53 # 集点对象SKU数 --对象是分类商品的 没有考虑,如何添加
    'q53':
    f"""
    SELECT count(distinct commodity_cd)
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
    SELECT count(distinct user_barcode)
    FROM t_real_purchase_campaign_log a
    INNER JOIN t_real_purchase_log b on a.real_purchase_id = b.real_purchase_id
    WHERE campaign_id in
    (
        SELECT DISTINCT campaign_id
        FROM t_campaign a
        where region_block_code = '{region}'
        and campaign_date_from <= '{endtime}'
        and campaign_date_to >= '{begintime}'
    )
    and b.create_date BETWEEN '{begintime}' and '{endtime}';
    """,

    # 55 # 集点对象商品销量
    'q55':
    f"""
    SELECT sum(stamp_num)
    FROM t_real_purchase_campaign_log a
    INNER JOIN t_real_purchase_log b on a.real_purchase_id = b.real_purchase_id
    WHERE campaign_id in
        (
        SELECT DISTINCT campaign_id
        FROM t_campaign a
        where region_block_code = '{region}'
        and campaign_date_from <= '{endtime}'
        and campaign_date_to >= '{begintime}'
        )
    and b.create_date BETWEEN '{begintime}' and '{endtime}'
    ;""",
    
    # 56 # 集点对象商品销量占比
    # formula

    # 57 # 实际发出礼券张数
    'q57':
    f"""
    select
    CASE
        c.send_type
        when 0 then '一般发送'
        when 2 then '集点礼券'
        when 3 then '活动派发（扫码/电子码）'
        when 9 then '活动派发（扫码/电子码）'
        when 4 then '积分商城兑换'
        when 6 then '注册'
        when 7 then '购买'
    END AS type,
    count(*)
    from t_user_coupon  a
    LEFT JOIN t_coupon c on a.coupon_id = c.coupon_id
    where c.region_block_code = '{region}'
      and binding_date between '{begintime}' and '{endtime}'
    GROUP BY 1;
    """,
    # 签到获得
    'q57f':
    f"""
    SELECT count(*)
    FROM t_signed_history a
    LEFT JOIN
    (
        SELECT DISTINCT signed_id ,region_block_code
        FROM t_signed
        where region_block_code = '{region}'
            and signed_start_datetime <= '{endtime}'
            and signed_end_datetime >= '{begintime}'
    ) b on a.signed_id = b.signed_id
    WHERE create_date BETWEEN '{begintime}' and '{endtime}'
        and b.region_block_code = '{region}'
        and coupon_id !='';
    """,
    # 抽奖获得
    'q57g':
    f"""
    SELECT count(*)
    FROM t_lottery_history a
    LEFT JOIN
    (
        SELECT DISTINCT lottery_id ,region_block_code
        FROM t_lottery
        where region_block_code = '{region}'
        and lottery_start_datetime <= '{endtime}'
        and lottery_end_datetime >= '{begintime}'
    ) b on a.lottery_id = b.lottery_id
    WHERE create_date BETWEEN '{begintime}' and '{endtime}'
    and b.region_block_code = '{region}'
    and coupon_id !=''
    and receive_flg = 1;
    """,

    # 每日福利获得   都是活动派发
    'q57h':
    f"""
    SELECT count(*)
    FROM t_mission_history a
    LEFT JOIN
    (
        SELECT DISTINCT mission_id ,region_block_code
        FROM t_mission
        where region_block_code = '{region}'
        and mission_start_datetime <= '{endtime}'
        and mission_end_datetime >= '{begintime}'
    ) b on a.mission_id = b.mission_id
    WHERE create_date BETWEEN '{begintime}' and '{endtime}'
    and b.region_block_code = '{region}'
    and coupon_id !=''
    and receive_flg = 1;
    """,

    # 58 # 积分兑换礼券使用张数
    'q58':
    f"""
    select count(*)
    from t_user_coupon  a
    LEFT JOIN t_coupon c on a.coupon_id = c.coupon_id
    where c.region_block_code = '{region}'
      and use_date between '{begintime}' and '{endtime}'
      and c.send_type = '4';
    """,

    # 61 # 积分兑换礼券使用率
    # formula

    # 62 # 会员退货率
    # formula

    # 63 # 会员退货次数
    'q61':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_commodity_log a
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.business_flg = 'A';
    """,

    # 64 # 会员活动商品退货次数
    'q62':
    f"""
    select count(DISTINCT CONCAT(a.SHOP_ID, a.POS_NO ,serial_number,a.DEAL_TIME))
    from t_pos_purchase_commodity_log a
    where a.region_block_code = '{region}'
      and a.purchase_date between '{begin}' and '{end}'
      and a.business_flg = 'A'
      and a.promotion_flg in ('1', '2', '3');
    """}

    return queries

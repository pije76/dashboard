import operator
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from collections import Counter

from .models import Order, Article, MonthlySalesProduct, MonthlySalesBrand, Customer, ShopviewChannel
from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractWeekDay
from django.db import connection
from django.db.models import Count
from calendar import monthrange


def chart_day(filter_options, countries, channels, articles, products, brands, type, start_time, end_time):
    cursor = connection.cursor()
    res = Counter(filter_options.values())
    return_val = []

    if res[True] == 4:
        if type == "Article":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(articles))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                            left join order_detail on orders.order_id=order_detail.order_id
                            left join shopview_channel on shopview_channel.shopview = orders.shop_view
                            left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                            where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                            	and order_detail.article_id in ({}) and article.brand in ({})
                                and orders.date between '{}' and '{}'
                            group by day order by day""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(articles) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif type == "Product":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(products))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                	and article.product_name in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(products) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
    elif res[True] == 3:
        if filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
    								select article_id, case
    									when brand='Paket' then 'Braineffect'
    									else brand
    									end as brand
    								from article
    							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                	and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(articles)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    	and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(products)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    	and article.brand in ({}) and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders1, placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)

        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({})
                                	and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.channel in ({})
                                    	and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)

        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True and filter_options['Country'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({})
                                	and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({})
                                    	and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 2:
        if filter_options['Country'] is True and filter_options['Channel'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(day from date) as day, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview=orders.shop_view
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1]),
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
    							left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join article on article.article_id=order_detail.article_id
    							left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
    								select article_id, case
    									when brand='Paket' then 'Braineffect'
    									else brand
    									end as brand
    								from article
    							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders1, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by day order by day""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, product_name, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by day order by day""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 1:
        if filter_options['Country'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            raw_query = """select extract(day from date) as day, sum(total_product_net_after_discount) as discount from orders
                            left join shopview_channel on shopview_channel.shopview=orders.shop_view
                            where orders.status='complete' and shopview_channel.land in ({}) and date between ('{}') and ('{}')
                            group by day order by day""".format(placeholders1, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    where order_detail.article_id in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by day order by day""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join article.article_id=order_detail.article_id
                                    where article.product_name in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by day order by day""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(day from date) as day, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where shopview_channel.channel in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by day order by day""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where article.brand in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by day order by day""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(brands))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
    start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
    number_of_days = int(monthrange(start_time.year, start_time.month)[1])
    output = {'number_of_days': number_of_days, 'reports': return_val}
    return_val = json.dumps(output)
    return return_val

# extract(dow from date) as week,


def chart_week(filter_options, countries, channels, articles, products, brands, type, start_time, end_time):
    cursor = connection.cursor()
    res = Counter(filter_options.values())
    return_val = []

    if res[True] == 4:
        if type == "Article":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(articles))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                            left join order_detail on orders.order_id=order_detail.order_id
                            left join shopview_channel on shopview_channel.shopview = orders.shop_view
                            left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                            where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                            	and order_detail.article_id in ({}) and article.brand in ({})
                                and orders.date between '{}' and '{}'
                            group by week order by week""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(articles) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif type == "Product":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(products))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                	and article.product_name in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(products) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
    elif res[True] == 3:
        if filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
    								select article_id, case
    									when brand='Paket' then 'Braineffect'
    									else brand
    									end as brand
    								from article
    							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                	and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(articles)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    	and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(products)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    	and article.brand in ({}) and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders1, placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)

        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({})
                                	and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.channel in ({})
                                    	and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)

        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True and filter_options['Country'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({})
                                	and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({})
                                    	and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 2:
        if filter_options['Country'] is True and filter_options['Channel'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(dow from date) as week, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview=orders.shop_view
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1]),
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
    							left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join article on article.article_id=order_detail.article_id
    							left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
    								select article_id, case
    									when brand='Paket' then 'Braineffect'
    									else brand
    									end as brand
    								from article
    							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders1, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by week order by week""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
        								select article_id, product_name, case
        									when brand='Paket' then 'Braineffect'
        									else brand
        									end as brand
        								from article
        							) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by week order by week""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 1:
        if filter_options['Country'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            raw_query = """select extract(dow from date) as week, sum(total_product_net_after_discount) as discount from orders
                            left join shopview_channel on shopview_channel.shopview=orders.shop_view
                            where orders.status='complete' and shopview_channel.land in ({}) and date between ('{}') and ('{}')
                            group by week order by week""".format(placeholders1, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    where order_detail.article_id in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by week order by week""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join article.article_id=order_detail.article_id
                                    where article.product_name in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by week order by week""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(dow from date) as week, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where shopview_channel.channel in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by week order by week""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join (
								select article_id, case
									when brand='Paket' then 'Braineffect'
									else brand
									end as brand
								from article
							) as article on article.article_id=order_detail.article_id
                                where article.brand in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by week order by week""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(brands))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)

    months = ['Sunday', 'Monday', 'Tuesday',
              'Wednesday', 'Thursday', 'Friday', 'Saturday']
    resp = []
    for item in return_val:
        dict_elem = {
            "day": months[item['day']],
            "total_discount": item['total_discount']
        }
        resp.append(dict_elem)
    return_val = json.dumps(resp)
    return return_val

# extract(month from date) as month


def chart_month(filter_options, countries, channels, articles, products, brands, type, start_time, end_time):
    cursor = connection.cursor()
    res = Counter(filter_options.values())
    return_val = []

    if res[True] == 4:
        if type == "Article":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(articles))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                            left join order_detail on orders.order_id=order_detail.order_id
                            left join shopview_channel on shopview_channel.shopview = orders.shop_view
                            left join (
                                select article_id, case
                                    when brand='Paket' then 'Braineffect'
                                    else brand
                                    end as brand
                                from article
                            ) as article on article.article_id=order_detail.article_id
                            where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                and order_detail.article_id in ({}) and article.brand in ({})
                                and orders.date between '{}' and '{}'
                            group by month order by month""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(articles) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif type == "Product":
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders3 = ', '.join(['%s'] * len(products))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                select article_id, case
                                    when brand='Paket' then 'Braineffect'
                                    else brand
                                    end as brand
                                from article
                            ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    and article.product_name in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders2, placeholders3, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) +
                tuple(products) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
    elif res[True] == 3:
        if filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                    select article_id, case
                                        when brand='Paket' then 'Braineffect'
                                        else brand
                                        end as brand
                                    from article
                                ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(articles)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                        and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders1, placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(channels) +
                    tuple(products)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                        and article.brand in ({}) and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders1, placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)

        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({})
                                    and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.channel in ({})
                                        and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders2, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)

        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True and filter_options['Country'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({})
                                    and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
                                        select article_id, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({})
                                        and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders1, placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) +
                    tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 2:
        if filter_options['Country'] is True and filter_options['Channel'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(month from date) as month, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview=orders.shop_view
                                where orders.status='complete' and shopview_channel.land in ({}) and shopview_channel.channel in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(channels))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1]),
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders1 = ', '.join(['%s'] * len(countries))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and shopview_channel.land in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders1, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(countries) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and order_detail.article_id in ({}) and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders2 = ', '.join(['%s'] * len(channels))
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join article on article.article_id=order_detail.article_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.product_name in ({}) and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders2, placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(channels) + tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Country'] is True and filter_options['Brand'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                    select article_id, case
                                        when brand='Paket' then 'Braineffect'
                                        else brand
                                        end as brand
                                    from article
                                ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.land in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders1, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Channel'] is True and filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            placeholders4 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                select article_id, case
                                    when brand='Paket' then 'Braineffect'
                                    else brand
                                    end as brand
                                from article
                            ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and shopview_channel.channel in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders2, placeholders4, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels) + tuple(brands)
            )
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True and filter_options['Brand'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                left join (
                                select article_id, case
                                    when brand='Paket' then 'Braineffect'
                                    else brand
                                    end as brand
                                from article
                            ) as article on article.article_id=order_detail.article_id
                                where orders.status='complete' and order_detail.article_id in ({}) and article.brand in ({})
                                    and orders.date between '{}' and '{}'
                                group by month order by month""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                placeholders4 = ', '.join(['%s'] * len(brands))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                    left join (
                                        select article_id, product_name, case
                                            when brand='Paket' then 'Braineffect'
                                            else brand
                                            end as brand
                                        from article
                                    ) as article on article.article_id=order_detail.article_id
                                    where orders.status='complete' and article.product_name in ({}) and article.brand in ({})
                                        and orders.date between '{}' and '{}'
                                    group by month order by month""".format(placeholders3, placeholders4, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products) + tuple(brands)
                )
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
    elif res[True] == 1:
        if filter_options['Country'] is True:
            placeholders1 = ', '.join(['%s'] * len(countries))
            raw_query = """select extract(month from date) as month, sum(total_product_net_after_discount) as discount from orders
                            left join shopview_channel on shopview_channel.shopview=orders.shop_view
                            where orders.status='complete' and shopview_channel.land in ({}) and date between ('{}') and ('{}')
                            group by month order by month""".format(placeholders1, start_time, end_time)
            cursor.execute(
                raw_query, tuple(countries))
            res_val = cursor.fetchall()

            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['ArticleProduct'] is True:
            if type == "Article":
                placeholders3 = ', '.join(['%s'] * len(articles))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    where order_detail.article_id in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by month order by month""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(articles))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
            elif type == "Product":
                placeholders3 = ', '.join(['%s'] * len(products))
                raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                    left join order_detail on orders.order_id=order_detail.order_id
                                    left join article.article_id=order_detail.article_id
                                    where article.product_name in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                    group by month order by month""".format(placeholders3, start_time, end_time)
                cursor.execute(
                    raw_query, tuple(products))
                res_val = cursor.fetchall()

                for val in res_val:
                    dict_elem = {
                        "day": int(val[0]),
                        "total_discount": float(val[1])
                    }
                    return_val.append(dict_elem)
        elif filter_options['Channel'] is True:
            placeholders2 = ', '.join(['%s'] * len(channels))
            raw_query = """select extract(month from date) as month, sum(total_product_net_after_discount) as discount from orders
                                left join shopview_channel on shopview_channel.shopview = orders.shop_view
                                where shopview_channel.channel in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by month order by month""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(channels))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)
        elif filter_options['Brand'] is True:
            placeholders2 = ', '.join(['%s'] * len(brands))
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                                left join order_detail on orders.order_id=order_detail.order_id
                                left join (
                                select article_id, case
                                    when brand='Paket' then 'Braineffect'
                                    else brand
                                    end as brand
                                from article
                            ) as article on article.article_id=order_detail.article_id
                                where article.brand in ({}) and orders.date between '{}' and '{}' and orders.status='complete'
                                group by month order by month""".format(placeholders2, start_time, end_time)
            cursor.execute(
                raw_query, tuple(brands))
            res_val = cursor.fetchall()
            for val in res_val:
                dict_elem = {
                    "day": int(val[0]),
                    "total_discount": float(val[1])
                }
                return_val.append(dict_elem)

    return_val = json.dumps(return_val)
    return return_val


def search_articles(request, path=''):
    if request.method == 'POST':

        # get post data (filter articles, start date and finish date)
        filtered_articles = request.POST.get('filtered_articles', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
        end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
        filtered_articles = json.loads(filtered_articles)
        # filtered_articles = ["4260460480200", "4260460481689"]
        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(filtered_articles))
        raw_query = """select r2.total_sales as total_sales, article.article_name as article_name from
                        (select r1.article_id, sum(sales) as total_sales from
                            (
                                SELECT order_detail.article_id, date, order_detail.price * order_detail.quantity as sales FROM orders
                                LEFT JOIN order_detail ON orders.order_id = order_detail.order_id
                                WHERE (order_detail.article_id IN ({}))
                                AND (date BETWEEN '{}' AND '{}') AND (status='complete')
                            ) as r1 GROUP BY r1.article_id) as r2, article
                            where r2.article_id = article.article_id""".format(placeholders, start_time, end_time)
        cursor.execute(
            raw_query, tuple(filtered_articles))
        articles = cursor.fetchall()
        res_val = []
        for article in articles:
            dict_elem = {
                "article_name": article[1],
                "total_sales": float(article[0])
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def search_by_daterange_for_week_sales(request, path=''):
    if request.method == 'POST':

        # get post data (start day and finish day)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        articles = request.POST.get('filtered_articles', None)
        articles = json.loads(articles)
        placeholders = ', '.join(['%s'] * len(articles))
        cursor = connection.cursor()
        if len(articles) == 0:
            raw_query = """select extract(dow from date) as week, sum(total_product_net_after_discount) as total_discount from orders
                    where date between '{}' and '{}' and status='complete'
                    group by week order by week asc""".format(start_time, end_time)
            cursor.execute(
                raw_query)
        else:
            raw_query = """select extract(dow from date) as week, sum(order_detail.price * order_detail.quantity) as total_discount from orders
                    left join order_detail on orders.order_id=order_detail.order_id
                    where date between '{}' and '{}' and order_detail.article_id in ({}) and status='complete'
                    group by week order by week asc""".format(start_time, end_time, placeholders)
            cursor.execute(
                raw_query, tuple(articles))

        reports = cursor.fetchall()
        res_val = []
        for report in reports:
            dict_elem = {
                "week_number": calendar.day_name[int(report[0]) - 1],
                "total_discount": float(report[1])
            }
            res_val.append(dict_elem)

        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def search_by_daterange_for_country_sales(request, path=''):
    if request.method == 'POST':
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        countries = request.POST.get('countries', None)
        articles = request.POST.get('filtered_articles', None)
        articles = json.loads(articles)
        countries = json.loads(countries)

        cursor = connection.cursor()
        placeholders1 = ', '.join(['%s'] * len(articles))
        placeholders2 = ', '.join(['%s'] * len(countries))
        if len(countries) == 0:
            placeholders2 = "' '"
        if len(articles) == 0:
            raw_query = """select sum(orders.total_product_net_after_discount) as discount, customers.land as land from orders
                            left join customers on orders.customer_id=customers.id
                            where orders.date between '{}' and '{}' and customers.land in ({}) and orders.status='complete'
                            group by customers.land""".format(start_time, end_time, placeholders2)
            cursor.execute(
                raw_query, tuple(countries))
        else:
            raw_query = """select sum(order_detail.price * order_detail.quantity) as discount, customers.land as land from orders
                            left join customers on orders.customer_id=customers.id
                            left join order_detail on orders.order_id=order_detail.order_id
                            where orders.date between '{}' and '{}' and customers.land in ({}) and order_detail.article_id in ({}) and orders.status='complete'
                            group by customers.land""".format(start_time, end_time, placeholders2, placeholders1)
            cursor.execute(
                raw_query, tuple(countries) + tuple(articles))
        reports = cursor.fetchall()
        res_val = []
        for report in reports:
            dict_elem = {
                "country": report[1],
                "total_discount": float(report[0]),
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def search_by_daterange_for_shopview_sales(request, path=''):
    if request.method == 'POST':
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        shopviews = request.POST.get('shopviews', None)
        articles = request.POST.get('filtered_articles', None)
        articles = json.loads(articles)
        shopviews = json.loads(shopviews)
        placeholders1 = ', '.join(['%s'] * len(articles))
        placeholders2 = ', '.join(['%s'] * len(shopviews))
        cursor = connection.cursor()
        if len(shopviews) == 0:
            placeholders2 = "' '"
        if len(articles) == 0:
            raw_query = """select sum(total_product_net_after_discount) as discount, shop_view as shopview from orders
                                where date between '{}' and '{}' and shop_view in ({}) and status='complete'
                                group by shop_view""".format(start_time, end_time, placeholders2)
            cursor.execute(
                raw_query, tuple(shopviews))
        else:
            raw_query = """select sum(order_detail.price * order_detail.quantity) as discount, orders.shop_view as shopview from orders
                            left join order_detail on orders.order_id=order_detail.order_id
                            where orders.date between '{}' and '{}' and orders.shop_view in ({}) and order_detail.article_id in ({}) and orders.status='complete'
                            group by orders.shop_view""".format(start_time, end_time, placeholders2, placeholders1)
            cursor.execute(
                raw_query, tuple(shopviews) + tuple(articles))
        reports = cursor.fetchall()
        res_val = []
        for report in reports:
            dict_elem = {
                "shop_view": report[1],
                "total_discount": float(report[0])
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def search_by_year_for_month_sales(request, path=''):
    if request.method == 'POST':
        year = request.POST.get('year', None)
        filtered_articles = request.POST.get('filtered_articles', None)
        articles = json.loads(filtered_articles)

        placeholders = ', '.join(['%s'] * len(articles))
        cursor = connection.cursor()
        if len(articles) == 0:
            raw_query = """select extract(month from date) as month, sum(total_product_net_after_discount) as discount from orders
                    where extract(year from date)={} and status='complete'
                    group by month order by month asc""".format(year)
            cursor.execute(
                raw_query)
        else:
            raw_query = """select extract(month from date) as month, sum(order_detail.price * order_detail.quantity) as discount from orders
                    left join order_detail on orders.order_id=order_detail.order_id
                    where extract(year from date)={} and order_detail.article_id in ({}) and orders.status='complete' and orders.status='complete'
                    group by month order by month asc""".format(year, placeholders)
            cursor.execute(
                raw_query, tuple(articles))

        reports = cursor.fetchall()
        res_val = []
        for report in reports:
            dict_elem = {
                "month_number": calendar.month_abbr[int(report[0])],
                "total_discount": float(report[1]),
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def search_by_monthyear_for_day_sales(request, path=''):
    if request.method == 'POST':

        filtered_articles = request.POST.get('filtered_articles', None)
        filtered_articles = json.loads(filtered_articles)
        # filtered_articles = ["4260460480200", "4260460481689"]

        year = request.POST.get('mon_year', None)
        start_day = datetime.strptime(year, '%Y-%m')
        number_of_days = int(monthrange(start_day.year, start_day.month)[1])
        end_day = start_day + relativedelta(months=1, days=-1)

        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(filtered_articles))
        if len(filtered_articles) == 0:
            raw_query = """select extract(day from date) as day, sum(total_product_net_after_discount) as discount from orders
                        where date between '{}' and '{}' and status='complete'
                        group by day""".format(start_day.strftime('%Y-%m-%d'), end_day.strftime('%Y-%m-%d'))
            cursor.execute(raw_query)

        else:
            raw_query = """select extract(day from date) as day, sum(order_detail.price * order_detail.quantity) as discount from orders
                        left join order_detail on orders.order_id=order_detail.order_id
                        where date between '{}' and '{}' and order_detail.article_id in ({}) and orders.status='complete'
                        group by day""".format(start_day.strftime('%Y-%m-%d'), end_day.strftime('%Y-%m-%d'), placeholders)
            cursor.execute(
                raw_query, tuple(filtered_articles))
        articles = cursor.fetchall()
        res_val = []
        for article in articles:
            dict_elem = {
                "day_number": article[0],
                "total_discount": float(article[1])
            }
            res_val.append(dict_elem)
        return_val = {"day_numbers": number_of_days, "reports": res_val}
        res_val = json.dumps(return_val)
        # return results
        return HttpResponse(res_val)


def filter_by_month_year(request, path=''):
    if request.method == 'POST':
        month_year = request.POST.get('mon_year', None)
        cursor = connection.cursor()
        raw_query = """SELECT article.article_name AS article_name, T1.brand, T1.units_sold, T1.total_material_cost, T1.total_product_sales, quote FROM monthly_sales_product AS T1
                        LEFT JOIN article ON article.article_id=T1.article_id WHERE T1.month_year='{}'""".format(month_year)
        cursor.execute(raw_query)
        monthly_sales_info = cursor.fetchall()
        res_val = []
        for info in monthly_sales_info:
            dict_elem = {
                "article_name": info[0],
                "brand": info[1],
                "units_sold": info[2],
                "total_material_cost": info[3],
                "total_article_sales": info[4],
                "quote": info[5],
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)
        # return results
        return HttpResponse(res_val)


@login_required(login_url='/accounts/login/')
def index(request):
    # load template
    template = loader.get_template('dashboard.html')
    _end_day = datetime.today()
    _start_day = _end_day + relativedelta(years=-1)
    start_day = _start_day.strftime('%Y-%m-%d')
    end_day = _end_day.strftime('%Y-%m-%d')
    start_day_month = datetime(_end_day.year, _end_day.month, 1)
    end_day_month = start_day_month + relativedelta(months=1, days=-1)
    # get total sales and total revenue value by day using query
    report_by_day = Order.objects.filter(date__range=[start_day_month.strftime('%Y-%m-%d'),
                                                      end_day_month.strftime('%Y-%m-%d')]).filter(status='complete').annotate(day=ExtractDay('date')).values('day').order_by('day').annotate(
        total_discount=Sum('total_product_net_after_discount'))
    # get total sales and total revenue value by week using query
    report_by_week = Order.objects.filter(date__range=[start_day, end_day]).filter(status='complete').annotate(weekday=ExtractWeekDay('date')).values('weekday').order_by('weekday').annotate(
        total_discount=Sum('total_product_net_after_discount')).order_by('weekday')

    # # get total sales and total revenue value by month using query
    report_by_month = Order.objects.filter(date__year=_end_day.strftime('%Y')).filter(status='complete').annotate(month=ExtractMonth('date')).values('month').order_by('month').annotate(
        total_discount=Sum('total_product_net_after_discount'))

    # get total sales and total revenue value by country using query
    report_country = Order.objects.filter(date__range=[start_day, end_day]).filter(status='complete').values('customer_id__land').order_by('customer_id__land').annotate(
        total_discount=Sum('total_product_net_after_discount')).values('customer_id__land', 'total_discount')
    countries = Customer.objects.values(
        'land').annotate(dcount=Count('land'))

    # get total sales and total revenue value by shop view using query
    report_shop_view = Order.objects.filter(date__range=[start_day, end_day]).filter(status='complete').values('shop_view').order_by('shop_view').annotate(
        total_discount=Sum('total_product_net_after_discount'))
    shopviews = Order.objects.filter(status='complete').values(
        'shop_view').annotate(dcount=Count('shop_view'))

    # get all available articles from database
    articles = Article.objects.all()
    number_of_days = monthrange(_end_day.year, _end_day.month)[1]

    # render template with parameters
    context = {
        'report_day': [{'day_number': report['day'], 'total_discount': report['total_discount']} for report in report_by_day],
        'report_week': [{'week_number': calendar.day_name[report['weekday'] - 2], 'total_discount': report['total_discount']} for report in report_by_week],
        'report_month': [{'month_number': calendar.month_abbr[report['month']], 'total_discount': report['total_discount']} for report in report_by_month],
        'report_country': [{'country': report['customer_id__land'], 'total_discount': report['total_discount']} for report in report_country],
        'report_shop_view': [{'shop_view': report['shop_view'], 'total_discount': report['total_discount']} for report in report_shop_view],
        'articles': articles,
        'start_day': _start_day,
        'end_day': _end_day,
        'year': _end_day.strftime('%Y'),
        'countries': countries,
        'shopviews': shopviews,
        'page': 'home',
        'numberof_days': number_of_days
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def monthly_sales_article_data(request):

    month_year_info = MonthlySalesProduct.objects.values(
        'month_year').annotate(dcount=Count('month_year'))
    month_year = request.GET.get('mon_year', None)
    if month_year is None:
        month_year = month_year_info[0]['month_year']
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_abbr) if num}
    cur_mon_year = "{}-{:02d}".format(month_year[:4],
                                      abbr_to_num[month_year[5:].capitalize()])
    # load template
    template = loader.get_template('monthly_sales_article.html')

    cursor = connection.cursor()
    raw_query = """SELECT article.article_name AS article_name, T1.brand, T1.units_sold, T1.total_material_cost, T1.total_product_sales, quote FROM monthly_sales_product AS T1
                    LEFT JOIN article ON article.article_id=T1.article_id WHERE T1.month_year='{}'""".format(month_year)
    cursor.execute(raw_query)

    monthly_sales_info = cursor.fetchall()
    # render template with parameters
    context = {
        'monthly_sales_info': [{'article_name': report[0], 'brand': report[1], 'units_sold': report[2], 'total_material_cost': report[3],
                                'total_article_sales': report[4], 'quote': report[5]} for report in monthly_sales_info],
        'month_year_info': month_year_info,
        'month_year': month_year,
        'page': 'article-table',
        'cur_mon_year': cur_mon_year
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def monthly_sales_product_data(request):

    month_year_info = MonthlySalesProduct.objects.values(
        'month_year').annotate(dcount=Count('month_year'))
    month_year = request.GET.get('mon_year', None)
    if month_year is None:
        month_year = month_year_info[0]['month_year']
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_abbr) if num}
    cur_mon_year = "{}-{:02d}".format(month_year[:4],
                                      abbr_to_num[month_year[5:].capitalize()])
    # load template
    template = loader.get_template('monthly_sales_product.html')

    cursor = connection.cursor()
    raw_query = """SELECT article.product_name AS product_name, sum(T1.units_sold) as units_sold, sum(T1.total_material_cost) as material_cost, sum(T1.total_product_sales) as product_sales, sum(quote) as quote FROM monthly_sales_product AS T1
                    LEFT JOIN article ON article.article_id=T1.article_id WHERE T1.month_year='{}' group by product_name order by product_name""".format(month_year)
    cursor.execute(raw_query)

    monthly_sales_info = cursor.fetchall()
    # render template with parameters
    context = {
        'monthly_sales_info': [{'product_name': report[0], 'units_sold': report[1], 'total_material_cost': report[2],
                                'total_article_sales': report[3], 'quote': report[4]} for report in monthly_sales_info],
        'month_year_info': month_year_info,
        'month_year': month_year,
        'page': 'product-table',
        'cur_mon_year': cur_mon_year
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def monthly_sales_brand_data(request):
    cursor = connection.cursor()
    month_year_info = MonthlySalesBrand.objects.values(
        'month_year').annotate(dcount=Count('month_year'))
    month_year = request.GET.get('mon_year', None)

    if month_year is None:
        month_year = month_year_info[0]['month_year']
    month_name = month_year[5:]
    year_name = month_year[:4]
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_abbr) if num}
    cur_mon_year = "{}-{:02d}".format(month_year[:4],
                                      abbr_to_num[month_year[5:].capitalize()])

    # load template
    template = loader.get_template('monthly_sales_brand.html')

    start_day_month = datetime(
        int(year_name), int(abbr_to_num[month_year[5:].capitalize()]), 1)
    end_day_month = start_day_month + relativedelta(months=1, days=-1)

    raw_query = """select sum(total_material_cost_of_brand), sum(umsatz), sum(anteil), sum(materialquoten), sum(cnt_brand) from (
                    select *, case when brand='Paket' then 'Braineffect' else brand end as new_brand
                    from (select total_material_cost_of_brand, umsatz, anteil, materialquoten, cnt_brand, T2.brand from monthly_sales_brand
                    left join (select brand, sum(units_sold) as cnt_brand from monthly_sales_product where month_year='{}' group by brand) as T2
                    on monthly_sales_brand.brand=T2.brand where month_year='{}') as T1 ) as T3""".format(month_year, month_year)
    cursor.execute(raw_query)

    total_info = cursor.fetchall()

    total_material_cost = MonthlySalesBrand.objects.filter(
        month_year=month_year).aggregate(Sum('total_material_cost_of_brand'))
    total_umsatz = MonthlySalesBrand.objects.filter(
        month_year=month_year).aggregate(Sum('umsatz'))
    total_anteil = MonthlySalesBrand.objects.filter(
        month_year=month_year).aggregate(Sum('anteil'))
    total_material_quoten = MonthlySalesBrand.objects.filter(
        month_year=month_year).aggregate(Sum('materialquoten'))
    raw_query = """select sum(total_material_cost_of_brand), sum(umsatz), sum(anteil), sum(materialquoten), sum(cnt_brand), new_brand from (
                    select *, case when brand='Paket' then 'Braineffect' else brand end as new_brand
                    from (select total_material_cost_of_brand, umsatz, anteil, materialquoten, cnt_brand, T2.brand from monthly_sales_brand
                    left join (select brand, sum(units_sold) as cnt_brand from monthly_sales_product where month_year='{}' group by brand) as T2
                    on monthly_sales_brand.brand=T2.brand where month_year='{}') as T1 ) as T3 group by T3.new_brand""".format(month_year, month_year)
    cursor.execute(raw_query)
    monthly_sales_info = cursor.fetchall()
    # render template with parameters
    if not float(total_info[0][1]) == 0:
        total_material_quoten = float(
            total_info[0][0]) / float(total_info[0][1]) * 100
    else:
        total_material_quoten = 0.0

    shopviews = Order.objects.filter(status='complete').values(
        'shop_view').annotate(dcount=Count('shop_view'))
    raw_query = """select orders.shop_view, sum(material_cost_{}.{} * order_detail.quantity) from orders
                    left join order_detail on orders.order_id=order_detail.order_id
                    left join material_cost_{} on material_cost_{}.article_id=order_detail.article_id
                    where orders.status='complete' and orders.date between ('{}') and ('{}')
                    group by orders.shop_view""".format(year_name, month_name, year_name, year_name, start_day_month, end_day_month)
    cursor.execute(raw_query)
    shopview_material = cursor.fetchall()
    context = {
        'monthly_sales_info': [{'total_material_cost_of_brand': "{:.2f}".format(info[0]), 'umsatz': "{:.2f}".format(info[1]),
                                'anteil': "{:.2f}".format(info[2]), 'materialquoten': "{:.2f}".format(info[3]), 'units': info[4], 'brand': info[5]} for info in monthly_sales_info],
        'month_year_info': month_year_info,
        'month_year': month_year,
        'total_material_cost': "{:.2f}".format(total_info[0][0]),
        'total_umsatz': "{:.2f}".format(total_info[0][1]),
        'total_anteil': "{:.2f}".format(total_info[0][2]),
        'total_material_quoten': "{:.2f}".format(total_material_quoten),
        'total_units': total_info[0][4],
        'page': 'brand-table',
        'cur_mon_year': cur_mon_year,
        'shopviews': shopviews,
        'shopview_material': [{'shopview': info[0], 'material': info[1]} for info in shopview_material]
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def charts(request):

    # load template
    template = loader.get_template('charts.html')

    cursor = connection.cursor()
    raw_query = """SELECT SUBSTRING(month_year,1,4) as year
                    FROM monthly_sales_brand group by year"""
    cursor.execute(raw_query)

    year_info = cursor.fetchall()

    year_info = [x[0] for x in year_info]

    raw_query = """select T1.month_num, T1.month_str, T1.total, T2.braineffect, T3.vitafair from (
                    select sum(umsatz) as total, month_str, min(month_number) as month_num from monthly_sales_brand
                                        left join months on LOWER(months.month_str)=substring(month_year, 6, 8)
                                        where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={}
                                        group by months.month_str order by month_num asc
                    	) as T1
                    left join (
                    	select sum(umsatz) as braineffect, min(month_number) as month_num from monthly_sales_brand
                    	left join months on LOWER(months.month_str)=substring(month_year, 6, 8)
                    	where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={} and (brand='Paket' or brand='Braineffect')
                    	group by months.month_str order by month_num asc
                    ) as T2 on T1.month_num = T2.month_num
                    left join (
                    	select sum(umsatz) as vitafair, min(month_number) as month_num from monthly_sales_brand
                    	left join months on LOWER(months.month_str)=substring(month_year, 6, 8)
                    	where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={} and brand='Vitafair'
                    	group by months.month_str order by month_num asc
                    ) as T3 on T1.month_num = T3.month_num""".format(2019, 1, 12, 2019, 1, 12, 2019, 1, 12)
    cursor.execute(raw_query)

    total_sales = cursor.fetchall()
    raw_query = """select sum(umsatz), substring(month_year, 1, 4) from monthly_sales_brand
                    left join months on months.month_str=substring(month_year, 6, 8)
                    group by substring(month_year, 1, 4)
                    order by substring(month_year, 1, 4) asc"""
    cursor.execute(raw_query)
    yearly_sales = cursor.fetchall()
    # render template with parameters
    context = {
        'year_info': year_info,
        'cur_year': 2019,
        'total_sales_info': [{'total_sales': report[2], 'month_name': report[1].capitalize(), 'braineffect': report[3], 'vitafair': report[4]} for report in total_sales],
        'yearly_sales': [{'sales': report[0], 'year_name': report[1]} for report in yearly_sales],
        'page': 'charts'
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def advanced_charts(request):

    # load template
    template = loader.get_template('advanced_charts.html')

    countries = Customer.objects.values('land').annotate(dcount=Count('land'))
    channels = ShopviewChannel.objects.values(
        'channel').annotate(dcount=Count('channel'))
    # get all available articles from database
    articles = Article.objects.all()
    products = Article.objects.values(
        'product_name').annotate(dcount=Count('product_name'))
    # render template with parameters
    context = {
        'countries': countries,
        'channels': channels,
        'articles': articles,
        'products': products,
        'page': 'advanced-charts'
    }
    return HttpResponse(template.render(context, request))


def filter_by_year_month_for_material_sales(request, path=''):
    if request.method == 'POST':
        year = request.POST.get('year', None)
        start_month = request.POST.get('start_month', None)
        end_month = request.POST.get('end_month', None)
        cursor = connection.cursor()
        raw_query = """select T1.month_num, T1.month_str, T1.total, T2.braineffect, T3.vitafair from (
                        select sum(umsatz) as total, month_str, min(month_number) as month_num from monthly_sales_brand
                                            left join months on months.month_str=substring(month_year, 6, 8)
                                            where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={}
                                            group by months.month_str order by month_num asc
                        	) as T1
                        left join (
                        	select sum(umsatz) as braineffect, min(month_number) as month_num from monthly_sales_brand
                        	left join months on months.month_str=substring(month_year, 6, 8)
                        	where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={} and (brand='Paket' or brand='Braineffect')
                        	group by months.month_str order by month_num asc
                        ) as T2 on T1.month_num = T2.month_num
                        left join (
                        	select sum(umsatz) as vitafair, min(month_number) as month_num from monthly_sales_brand
                        	left join months on months.month_str=substring(month_year, 6, 8)
                        	where substring(month_year, 1, 4)='{}' and month_number>={} and month_number<={} and brand='Vitafair'
                        	group by months.month_str order by month_num asc
                        ) as T3 on T1.month_num = T3.month_num""".format(year, start_month, end_month, year, start_month, end_month, year, start_month, end_month)
        cursor.execute(raw_query)
        total_sales_info = cursor.fetchall()
        res_val = []
        for info in total_sales_info:
            dict_elem = {
                "total_sales": info[2],
                "month_name": info[1],
                "vitafair": info[4],
                "braineffect": info[3]
            }
            res_val.append(dict_elem)
        res_val = json.dumps(res_val)

        # return results
        return HttpResponse(res_val)


def display_chart_by_filter_option(request, path=''):
    if request.method == 'POST':
        x_axis = request.POST.get('xaxis', None)
        filter_options = request.POST.get('filter_options', None)
        countries = request.POST.get('countries', None)
        channels = request.POST.get('channels', None)
        articles = request.POST.get('articles', None)
        products = request.POST.get('products', None)
        brands = request.POST.get('brands', None)
        type = request.POST.get('type', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)

        filter_options = json.loads(filter_options)
        countries = json.loads(countries)
        channels = json.loads(channels)
        articles = json.loads(articles)
        products = json.loads(products)
        brands = json.loads(brands)
        res_val = []
        if x_axis == 'day':
            res_val = chart_day(filter_options, countries,
                                channels, articles, products, brands, type, start_time, end_time)
        elif x_axis == 'week':
            res_val = chart_week(filter_options, countries,
                                 channels, articles, products, brands, type, start_time, end_time)
        elif x_axis == 'month':
            res_val = chart_month(filter_options, countries,
                                  channels, articles, products, brands, type, start_time, end_time)

        # return results
        return HttpResponse(res_val)


def materialcost_by_shopview(request, path=''):
    if request.method == 'POST':
        shopviews = request.POST.get('filtered_shopviews', None)
        mon_year = request.POST.get('mon_year', None)

        shopviews = json.loads(shopviews)
        print(shopviews)
        month_name = mon_year[5:]
        year_name = mon_year[:4]
        abbr_to_num = {name: num for num,
                       name in enumerate(calendar.month_abbr) if num}

        start_day_month = datetime(
            int(year_name), int(abbr_to_num[mon_year[5:].capitalize()]), 1)
        end_day_month = start_day_month + relativedelta(months=1, days=-1)

        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(shopviews))
        raw_query = """select orders.shop_view, sum(material_cost_{}.{} * order_detail.quantity) from orders
                        left join order_detail on orders.order_id=order_detail.order_id
                        left join material_cost_{} on material_cost_{}.article_id=order_detail.article_id
                        where orders.status='complete' and orders.shop_view in ({}) and orders.date between ('{}') and ('{}')
                        group by orders.shop_view""".format(year_name, month_name, year_name, year_name, placeholders, start_day_month, end_day_month)
        cursor.execute(raw_query, tuple(shopviews))
        print(cursor.query)
        shopview_material = cursor.fetchall()
        return_val = []
        for val in shopview_material:
            dict_elem = {
                "shopview": val[0],
                "material_cost": float(val[1])
            }
            return_val.append(dict_elem)
        return_val = json.dumps(return_val)
        print(return_val)
        return HttpResponse(return_val)

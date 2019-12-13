from django.urls import path
from sales_data import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('monthly-sales-article/',
         views.monthly_sales_article_data, name='monthly_sales_article_data'),
    path('monthly-sales-brand/',
         views.monthly_sales_brand_data, name='monthly_sales_brand_data'),
    path('monthly-sales-product/',
         views.monthly_sales_product_data, name='monthly_sales_product_data'),
    path('charts/',
         views.charts, name='charts'),
    path('advanced-charts',
         views.advanced_charts, name='advanced_charts'),
    path('search_article/', views.search_articles, name='search_articles'),
    path('search-by-daterange-for-week-sales/', views.search_by_daterange_for_week_sales,
         name='search_by_daterange_for_week_sales'),
    path('search-by-daterange-for-country-sales/', views.search_by_daterange_for_country_sales,
         name='search_by_daterange_for_country_sales'),
    path('search-by-daterange-for-shopview-sales/', views.search_by_daterange_for_shopview_sales,
         name='search_by_daterange_for_shopview_sales'),
    path('search-by-year-for-month-sales/', views.search_by_year_for_month_sales,
         name='search_by_year_for_month_sales'),
    path('search-by-monthyear-for-day-sales/', views.search_by_monthyear_for_day_sales,
         name='search_by_monthyear_for_day_sales'),
    path('filter-by-year-month-for-material-sales/', views.filter_by_year_month_for_material_sales,
         name='filter_by_year_month_for_material_sale'),
    path('display-chart-by-filter-option/', views.display_chart_by_filter_option,
         name='display_chart_by_filter_option'),
    path('materialcost-by-shopview/', views.materialcost_by_shopview,
         name='materialcost_by_shopview'),

]

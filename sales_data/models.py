from django.db import models


# customers table
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    stadt = models.CharField(max_length=255)
    land = models.CharField(max_length=255)
    plz = models.CharField(max_length=255)
    shop_customer_id = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = "customers"


# orders table
class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=255)
    amazon_order_id = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    e_mail = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    shop_view = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    repeated_customer = models.CharField(max_length=255)
    total_gross_before_discount = models.FloatField(null=True)
    total_product_gross_before_discount = models.FloatField(null=True)
    shipping_net = models.FloatField(null=True)
    shipping_tax = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    total_gross_after_discount = models.FloatField(null=True)
    total_product_gross_after_discount = models.FloatField(null=True)
    total_tax = models.FloatField(null=True)
    total_product_tax = models.FloatField(null=True)
    total_product_net_after_discount = models.FloatField(null=True)
    total_net_after_discount = models.FloatField(null=True)
    total_product_net_before_discount = models.FloatField(null=True)
    product_tax_category_19 = models.FloatField(null=True)
    product_tax_category_7 = models.FloatField(null=True)
    coupon_code = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)

    class Meta:
        db_table = "orders"


# order_detail table
class Order_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # article_id = Column('article_id', String, ForeignKey("article.article_id"), nullable=False)
    article_id = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        db_table = "order_detail"


# article table
class Article(models.Model):

    article_id = models.CharField(primary_key=True, max_length=255)
    article_name = models.CharField(max_length=255)
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    variant = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    giveaway = models.CharField(max_length=255)

    class Meta:
        db_table = "article"


# monthly_sales_product table
class MonthlySalesProduct(models.Model):
    id = models.AutoField(primary_key=True)
    month_year = models.CharField(max_length=255)
    article_id = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True)
    units_sold = models.IntegerField(null=True)
    month_year_materialcost = models.FloatField(null=True)
    total_material_cost = models.FloatField(null=True)
    total_product_sales = models.FloatField(null=True)
    quote = models.FloatField(null=True)

    class Meta:
        db_table = "monthly_sales_product"


# monthly_sales_brand table
class MonthlySalesBrand(models.Model):
    id = models.AutoField(primary_key=True)
    month_year = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    total_material_cost_of_brand = models.FloatField(null=True)
    umsatz = models.FloatField(null=True)
    anteil = models.FloatField(null=True)
    materialquoten = models.FloatField(null=True)

    class Meta:
        db_table = "monthly_sales_brand"


class Withdrawl(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    article_id = models.CharField(max_length=255)
    units = models.IntegerField()

    class Meta:
        db_table = "withdrawls"


class ShopviewChannel(models.Model):
    shopview = models.CharField(max_length=255)
    channel = models.CharField(max_length=255)
    land = models.CharField(max_length=255)

    class Meta:
        db_table = "shopview_channel"

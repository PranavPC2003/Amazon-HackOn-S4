from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
import math
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img_path = "https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"
    profile_pic = models.ImageField(default=img_path, upload_to='profile_pics/', null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    
    country = models.CharField(max_length=15, null=True, blank=True)
    addr_FullName = models.CharField(max_length=30, null=True, blank=True)
    addr_Phone = models.CharField(max_length=10, blank=True, null=True) 
    Flat = models.CharField(max_length=100, null=True, blank=True)
    Area = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=6, null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True)

    amazon_pay_balance = models.IntegerField(default=0)

class Category(models.Model):
    TYPE_CHOICES = (
        ('CLOTHING', 'Clothing'),
        ('ELECTRONICS', 'Electronics'),
        ('GROCERY', 'Grocery'),
    )
    category_name = models.CharField(max_length=25, unique=True, choices = TYPE_CHOICES)

    def __str__(self):
        return self.category_name

class Items(models.Model):
    seller_name = models.CharField(max_length=30)
    seller_id = models.IntegerField()
    description = models.TextField()
    cost = models.IntegerField()
    item_title = models.CharField(max_length=50, blank=True, null=True)
    item_id = models.IntegerField()
    img_path = "https://static7.depositphotos.com/1056394/786/v/450/depositphotos_7867981-stock-illustration-vector-cardboard-box.jpg"
    item_photo = models.ImageField(default=img_path, upload_to='item_img/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_title

class Bank_Info(models.Model):
    BANK_CHOICES = (
        ('SBI', 'State Bank of India'),
        ('HDFC', 'HDFC Bank'),
        ('ICICI', 'ICICI Bank'),
        ('PAYTM', 'Paytm'),
        ('PHONEPE', 'PhonePe'),
        ('AMAZON_PAY', 'Amazon Pay'),
        ('CASH', 'Cash'),
    )
    bank_name = models.CharField(max_length=30, choices = BANK_CHOICES, null = True, blank = True)

    TYPE_CHOICES = (
        ('CARD', 'card payment'),
        ('UPI', 'upi'),
        ('CASH', 'cash'),
        ('AMAZON_WALLET', 'Amazon wallet'),
    )

    type = models.CharField(max_length=20, choices = TYPE_CHOICES, default='CASH')
    perc_discount = models.IntegerField(default=0, null = True, blank = True)
    perc_cashback = models.IntegerField(default=0, null = True, blank = True)

    def __str__(self):
        return self.bank_name

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    order_items = models.ManyToManyField(Items)
    total_cost = models.IntegerField(default=0, blank=True)

    Bank_Details = models.ForeignKey(Bank_Info, on_delete=models.CASCADE)

    discounted_cost = models.IntegerField(default=0, null = True, blank = True)
    savings = models.IntegerField(default=0, null = True, blank = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_cost = sum(item.cost for item in self.order_items.all())
        discount = 0
        cashback = 0

        if self.Bank_Details.perc_discount > 0:
            discount = self.Bank_Details.perc_discount / 100

        elif self.Bank_Details.perc_cashback > 0:
            cashback = self.Bank_Details.perc_cashback / 100

        self.discounted_cost = max(math.ceil(self.total_cost - (self.total_cost * discount) - (self.total_cost * cashback)),0)
        self.savings = self.total_cost - self.discounted_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user}: {self.Bank_Details}"

class Set_Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()   
    amount = models.IntegerField(default = 0)

    clothing_perc = models.IntegerField(default = 0)
    electronics_perc = models.IntegerField(default = 0)
    grocery_perc = models.IntegerField(default = 0)

    clothing_amount = models.IntegerField(default = 0)
    electronics_amount = models.IntegerField(default = 0)
    grocery_amount = models.IntegerField(default = 0)

    month = models.IntegerField(default=datetime.datetime.now().month)

    def __str__(self):
        return f"{self.user}: {self.date.month}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.month = self.date.month

        self.clothing_amount = math.ceil((self.amount * self.clothing_perc) / 100)
        self.electronics_amount = math.ceil((self.amount * self.electronics_perc) / 100)
        self.grocery_amount = math.ceil((self.amount * self.grocery_perc) / 100)
        super().save(*args, **kwargs)


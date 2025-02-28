from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator
from django.utils.text import slugify
from django.utils import timezone
import uuid

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, validators=[EmailValidator()], null=True)
	
	class Meta:
		ordering = ['name']
		verbose_name = 'Customer'
		verbose_name_plural = 'Customers'

	def __str__(self):
		return str(self.name)

class Category(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True, blank=True)
	description = models.TextField(null=True, blank=True)
	
	class Meta:
		ordering = ['name']
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, unique=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	price = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
		validators=[MinValueValidator(0.01)]
	)
	digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(upload_to='products/', null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	date_added = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-date_added']
		verbose_name = 'Product'
		verbose_name_plural = 'Products'

	def __str__(self):
		return self.name
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	)

	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	
	class Meta:
		ordering = ['-date_ordered']
		verbose_name = 'Order'
		verbose_name_plural = 'Orders'

	def __str__(self):
		return str(self.transaction_id)
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if not i.product.digital:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date_added']
		verbose_name = 'Order Item'
		verbose_name_plural = 'Order Items'

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date_added']
		verbose_name = 'Shipping Address'
		verbose_name_plural = 'Shipping Addresses'

	def __str__(self):
		return f"{self.address}, {self.city}"

	def get_full_address(self):
		return f"{self.address}, {self.city}, {self.state} {self.zipcode}"
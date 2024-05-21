from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        if not password:
            raise ValueError('User must have a password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        user = self.create_user(email, password, **extra_fields)

        return user


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = None
    first_name = None
    last_name = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products', default='products/product_default.png')

    def __str__(self):
        return self.name


class CartItem(models.Model):  # 購物車中的商品
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        unique_together = ('user', 'product')


class Order(models.Model):
    order_no = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_status = models.BooleanField(default=False)  # False = Not Delivered, True = Delivered
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):  # 訂單中的商品
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.order} - {self.product}'

    class Meta:
        unique_together = ('order', 'product')

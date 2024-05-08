from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
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
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    description = models.TextField()
    image = models.ImageField(upload_to='products', default='products/product_default.png')

    def __str__(self):
        return self.name


class CartItem(models.Model):  # 購物車中的商品
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} - {self.product}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_status = models.BooleanField(default=False)  # False = Not Delivered, True = Delivered

    def __str__(self):
        return f'order_id:{self.id} - {self.user}'


class OrderItem(models.Model):  # 訂單中的商品ß
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f'order_id:{self.order.id} - {self.product}'

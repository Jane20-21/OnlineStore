from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(blank=True, default='static/images/default.png', verbose_name='Изображение')
    short_description = models.CharField(max_length=255, verbose_name='Короткое описание', default='')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name + ' ' + str(self.price) + '$'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.IntegerField(default=0, verbose_name='Количество')

    @property
    def total_price(self):
        total = self.product.price * self.count
        return total

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return self.product.name + ' - ' + str(self.count) + ' items $' + str(self.total_price)


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    cart_products = models.ManyToManyField(CartProduct, blank=True, verbose_name='Товары в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_price(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.product.price * cart_product.count
        return total

    is_bought = models.BooleanField(default=False, verbose_name='Куплена')

    @property
    def total_count(self):
        total = 0
        for cart_product in self.cart_products.all():
            total += cart_product.count
        return total

    def __str__(self):
        return self.user.username + ' - ' + str(self.total_count) + ' items ' + str(self.total_price) + '$'


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.user.username + ' ' + str(self.date)

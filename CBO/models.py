from django.db import models


class Product(models.Model):
  CATEGORY_CHOICES = [
      ('Casual', 'Casual Wear'),
      ('Formal', 'Formal & Office'),
      ('Kids', 'Kids & Accessories'),
  ]
  SIZE_CHOICES = [
      ('S', 'Small (S)'),
      ('M', 'Medium (M)'),
      ('L', 'Large (L)'),
      ('XL', 'Extra Large (XL)'),
      ('XXL', '2XL'),
      ('Free Size', 'Free Size'),
  ]

  name = models.CharField(max_length=100)
  category = models.CharField(
      max_length=50, choices=CATEGORY_CHOICES, default='Casual'
  )
  size = models.CharField(
      max_length=20, choices=SIZE_CHOICES, default='Free Size'
  )
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField(default=0)
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='products/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)  # Added for sorting latest arrivals

  def __str__(self):
    return self.name


class SizeGuide(models.Model):
  size_label = models.CharField(max_length=10)  # e.g., S, M, L, XL, XXL
  chest_inches = models.CharField(max_length=20)  # e.g., 36 – 38
  waist_inches = models.CharField(max_length=20)  # e.g., 28 – 30
  display_order = models.PositiveIntegerField(default=0)

  class Meta:
    ordering = ['display_order']

  def __str__(self):
    return f'{self.size_label} (Chest: {self.chest_inches})'


class StoreSettings(models.Model):
  heading = models.CharField(
      max_length=200, default='Quality Fashion for Every Wardrobe'
  )
  description = models.TextField()
  store_hours = models.CharField(
      max_length=150, default='Monday – Saturday, 8:30 AM – 7:00 PM'
  )
  exchange_policy = models.CharField(
      max_length=150, default='Accepted within 7 days with receipt'
  )

  class Meta:
    verbose_name_plural = 'Store Settings'

  def __str__(self):
    return self.heading

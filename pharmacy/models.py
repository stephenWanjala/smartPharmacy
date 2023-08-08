# Create your models here.
# pharmacy/models.py
from time import timezone

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import date


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Stock(models.Model):
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @staticmethod
    def remove_expired_medicines():
        today = date.today()
        expired_medicines = Stock.objects.filter(medicine__purchase__expiry_date__lt=today)

        for stock in expired_medicines:
            quantity_removed = stock.quantity
            stock.quantity = 0
            stock.save()

            # Log the removal for reference (You can customize this as per your needs)
            ExpiredMedicineLog.objects.create(medicine=stock.medicine, quantity_removed=quantity_removed)

    def __str__(self):
        return f"{self.medicine.name} - Quantity: {self.quantity}"


class Purchase(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_purchased = models.PositiveIntegerField()
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} - {self.purchase_date}"

    def save(self, *args, **kwargs):
        # Update stock quantity before saving the purchase
        self.update_stock_quantity()
        super().save(*args, **kwargs)

    def update_stock_quantity(self):
        # Get the stock object for the medicine
        stock, created = Stock.objects.get_or_create(medicine=self.medicine)
        # Increase stock quantity by the quantity purchased
        stock.quantity += self.quantity_purchased
        stock.save()


class ExpiredMedicineLog(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_removed = models.PositiveIntegerField()
    removal_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - Removed: {self.quantity_removed} - {self.removal_date}"

    @receiver(post_save, sender=Purchase)
    def check_medicine_expiration(sender, instance, **kwargs):
        stock, _ = Stock.objects.get_or_create(medicine=instance.medicine)
        if instance.expiry_date < date.today():
            stock.quantity -= instance.quantity_purchased
            stock.save()
            ExpiredMedicineLog.objects.create(medicine=instance.medicine, quantity_removed=instance.quantity_purchased)


class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_date = models.DateField(auto_now_add=True, )
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicine.name} - {self.sales_date}"

    def save(self, *args, **kwargs):
        if self.is_valid_sale():
            # Update stock quantity before saving the sale
            self.update_stock_quantity()
            super().save(*args, **kwargs)

    def is_valid_sale(self):
        # Check if the medicine is in stock and has been purchased
        stock = Stock.objects.filter(medicine=self.medicine).first()
        if not stock or stock.quantity < self.quantity_sold:
            return False
        return True

    # def update_stock_quantity(self):
    #     # Get the stock object for the medicine
    #     stock, created = Stock.objects.get_or_create(medicine=self.medicine)
    #     # Reduce stock quantity by the quantity sold
    #     stock.quantity -= self.quantity_sold
    #     # Ensure stock quantity does not go below zero
    #     stock.quantity = max(stock.quantity, 0)
    #     stock.save()
    def update_stock_quantity(self):
        # Get the stock object for the medicine
        stock, created = Stock.objects.get_or_create(medicine=self.medicine)
        # Reduce stock quantity by the quantity sold
        stock.quantity -= self.quantity_sold
        stock.save()

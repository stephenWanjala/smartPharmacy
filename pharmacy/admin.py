# Register your models here.

# pharmacy/admin.py

from django.contrib import admin

import pharmacy.models as myModels


@admin.register(myModels.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity_purchased', 'purchase_date', 'purchase_amount', 'supplier')
    actions = ['update_stock']

    def update_stock(self, request, queryset):
        for purchase in queryset:
            medicine = purchase.medicine
            quantity_purchased = purchase.quantity_purchased
            supplier = purchase.supplier

            # Check if the medicine already exists in the inventory
            existing_medicine = myModels.Medicine.objects.filter(name=medicine.name, supplier=supplier).first()

            if existing_medicine:
                existing_medicine.quantity += quantity_purchased
                existing_medicine.save()
            else:
                new_medicine = myModels.Medicine(
                    name=medicine.name,
                    category=medicine.category,
                    batch_number=medicine.batch_number,
                    expiration_date=medicine.expiration_date,
                    quantity=quantity_purchased,
                    cost_price=purchase.purchase_amount,
                    supplier=supplier,
                )
                new_medicine.save()

        self.message_user(request, f"Stocks updated for {queryset.count()} purchases.")

    update_stock.short_description = "Update Stock and Add New Medicines"


# Register other models as well
admin.site.register(myModels.Supplier)
admin.site.register(myModels.Category)
admin.site.register(myModels.Medicine)
admin.site.register(myModels.Stock)
admin.site.register(myModels.Sale)
admin.site.register(myModels.ExpiredMedicineLog)

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime, date

from pharmacy.forms.forms import MedicineCategoryForm, MedicineForm, PurchaseForm, SaleForm
from pharmacy.models import Sale, Stock, Category, Medicine, Purchase, ExpiredMedicineLog


# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
        #     return redirect(to='/admin')
        redirect(to='/home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            # if user.is_superuser:
            #     return redirect(to='/admin')
            return redirect(to='/home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {'messages': messages.get_messages(request), 'currentYear': datetime.now().year}
    return render(request=request, template_name='pharmacy/index.html', context=context)


def logout_view(request):
    logout(request)
    return redirect(to='login')


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Update stock and save the sale
            medicine = form.cleaned_data['medicine']
            quantity = form.cleaned_data['quantity_sold']
            # update_stock_on_sale(medicine, quantity)
            form.save()
            return redirect('home')

    else:
        form = SaleForm()
    today = date.today()
    total_sales = Sale.objects.filter(sales_date=today).count()
    total_amount_received = Sale.objects.filter(sales_date=today).aggregate(Sum('selling_price'))[
                                'selling_price__sum'] or 0
    total_sales_monthly = Sale.objects.filter(sales_date__year=today.year, sales_date__month=today.month).count()
    total_amount_received_monthly = \
        Sale.objects.filter(sales_date__year=today.year, sales_date__month=today.month).aggregate(Sum('selling_price'))[
            'selling_price__sum'] or 0

    stocks = Stock.objects.all()
    stock_status_list = []

    for stock in stocks:
        current_quantity = stock.quantity
        maximum_quantity = stock.medicine.purchase_set.aggregate(Sum('quantity_purchased'))[
                               'quantity_purchased__sum'] or 0
        if maximum_quantity > 0:
            stock_level = (current_quantity / maximum_quantity) * 100
        else:
            stock_level = 0

        stock_status_list.append({'medicine': stock.medicine, 'stock_level': stock_level})
        # Calculate the total quantity of each medicine sold today
    sales_today = Sale.objects.filter(sales_date=today)
    total_stock_sold = sales_today.aggregate(total_stock_sold=Sum('quantity_sold'))['total_stock_sold'] or 0

    # Calculate the total stock quantity available for all medicines
    total_stock_quantity = Stock.objects.aggregate(total_stock_quantity=Sum('quantity'))['total_stock_quantity'] or 0

    # Calculate the percentage of the total stock sold
    stock_sold_percentage = round(((total_stock_sold / total_stock_quantity) * 100 if total_stock_quantity > 0 else 0),
                                  2)

    sales = Sale.objects.filter()

    context = {'currentYear': datetime.now().year, 'total_sales': total_sales,
               'total_amount_received': total_amount_received, 'total_sales_monthly': total_sales_monthly,
               'total_amount_received_monthly': total_amount_received_monthly,
               'stock_status_list': stock_status_list, 'stock_sold_percentage': stock_sold_percentage,
               'sales': sales,
               'form': form}
    return render(request=request, template_name='pharmacy/home.html', context=context)


@login_required(login_url='login')
def category(request):
    if request.method == 'POST':
        # Check if the user is a superuser before saving the category
        if request.user.is_superuser:
            form = MedicineCategoryForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect('categories')

        # If it's a GET request, display the form and list of categories
    categories = Category.objects.all()

    form = MedicineCategoryForm()

    return render(request, 'pharmacy/Categories.html',
                  {'categories': categories, 'form': form, 'currentYear': datetime.now().year})


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = MedicineCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='categories')
    else:
        form = MedicineCategoryForm()
    return render(request, 'pharmacy/addCategory.html', {'form': form, 'currentYear': datetime.now().year})


@login_required(login_url='login')
def delete_category(request, category_id):
    if request.method == "POST":
        if request.user.is_superuser:
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            return redirect(to='categories')


@login_required(login_url='login')
def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return redirect('categories')


@login_required(login_url='login')
def medicines(request):
    # Check if the user is admin to handle medicine creation
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MedicineForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('medicines')

    medicines = Medicine.objects.all()
    form = MedicineForm()
    return render(request, 'pharmacy/medicines.html', {'medicines': medicines, 'form': form})


@login_required(login_url='login')
def delete_medicine(request, medicine_id):
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        medicine.delete()
        return redirect('medicines')


@login_required(login_url='login')
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='medicines')
    else:
        form = MedicineForm()
    return render(request, 'pharmacy/createMedicine.html', {'form': form, 'currentYear': datetime.now().year})


@login_required(login_url='login')
def purchases(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchases')

    else:
        form = PurchaseForm()

    purchases = Purchase.objects.all()
    return render(request, 'pharmacy/Purchases.html', {'form': form, 'purchases': purchases})


@login_required(login_url='login')
def view_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'pharmacy/view_stock.html', {'stocks': stocks})


@login_required(login_url='login')
def make_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Update stock and save the sale
            medicine = form.cleaned_data['medicine']
            quantity = form.cleaned_data['quantity_sold']
            # update_stock_on_sale(medicine, quantity)
            form.save()
            return redirect('home')

    else:
        form = SaleForm()

    return render(request, 'pharmacy/home.html', {'form': form})



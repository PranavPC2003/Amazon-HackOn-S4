from django.shortcuts import render, redirect, get_object_or_404
#from django.http import HttpResponse
from .models import Orders, Category, Items, Set_Budget
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import datetime
#from django.templatetags.static import static
#from django.conf import settings
#import os
from django.contrib.auth.decorators import login_required


def home(request):
    latest_items = Items.objects.all().order_by('-id')[:4]
    return render(request, 'server/home.html', {'latest_items': latest_items}  )

def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('auth_login')

    return render(request, 'server/auth_login.html')

def signout(request):
    logout(request)
    return redirect('home')

def exp_tracker_data(request):
    month = request.GET.get('month')
    user_orders = Orders.objects.filter(user=request.user, date__month=month)
    categories = Category.objects.all()

    expenditures = []
    for category in categories:
        category_expenditure = 0
        for order in user_orders:
            items_in_order = order.order_items.filter(category=category)
            for item in items_in_order:
                category_expenditure += item.cost
        expenditures.append([category.category_name, category_expenditure])

    total_expenditure = sum([x[1] for x in expenditures])
    # print(month)
    # print(expenditures)
    return JsonResponse({'expenditures': expenditures, 'total_expenditure': total_expenditure})

def expense_budget(request):
    option = request.GET.get('option')
    expenditures = [['Category', 'Amount'], ['Expense', 0], ['Budget_Left', 0]]
    current_month = datetime.datetime.now().month
    user_orders = Orders.objects.filter(user=request.user, date__month=current_month)
    
    if option == 'monthly':
        #print('monthly expense')
        budgets = Set_Budget.objects.filter(month=current_month)
        budget_amount = 0
        for budget in budgets:
            budget_amount = budget.amount

        for order in user_orders:
            item_in_order = order.order_items.filter()
            for item in item_in_order:
                expenditures[1][1] += item.cost
        budget_left = budget_amount - expenditures[1][1] 
        if (budget_left <= 0):
            expenditures[2][1] = 0
        else:
            expenditures[2][1] = budget_left


    elif option == 'yearly':
        print('yearly expense')


    return JsonResponse({'expenditures': expenditures})

@login_required()
def exp_tracker(request):
    date = datetime.datetime.now().date()
    user = request.user
    current_month = datetime.datetime.now().month
    date = datetime.datetime.now().date()
    try:
        budgets = Set_Budget.objects.get(user=user, month=current_month)
    except Set_Budget.DoesNotExist:
        budget_obj = Set_Budget(
            user=user,
            amount=0,
            clothing_perc=0,
            electronics_perc=0,
            grocery_perc=0,
            date=date
        )
        budget_obj.save()
         
    if request.method == 'POST':   
        amount = int(request.POST.get('budget_amount'))
        clothing_perc = int(request.POST.get('clothing_perc'))
        electronics_perc = int(request.POST.get('electronics_perc'))
        grocery_perc = int(request.POST.get('grocery_perc'))

        if budgets:
            budgets.amount = amount
            budgets.clothing_perc = clothing_perc
            budgets.electronics_perc = electronics_perc
            budgets.grocery_perc = grocery_perc
            budgets.user = user
            budgets.date = date
            budgets.save()

        else:
            budget_obj = Set_Budget(
                user=user,
                amount=amount,
                clothing_perc=clothing_perc,
                electronics_perc=electronics_perc,
                grocery_perc=grocery_perc,
                date=date
            )
            budget_obj.save()

        return redirect('exp_tracker')

    return render(request, 'server/expense_tracker.html', {'budgets': budgets})  


def payment_method_data(request):
    month = request.GET.get('month')
    user_orders = Orders.objects.filter(user=request.user, date__month=month)
    categories = Category.objects.all()

    expenditures = []
    for category in categories:
        category_expenditures = [category.category_name, 0, 0, 0, 0]
        for order in user_orders:
            payment_method = order.Bank_Details.type
            if payment_method == 'CARD':
                items_in_order = order.order_items.filter(category=category)
                for item in items_in_order:
                    category_expenditures[1] += item.cost

            elif payment_method == 'UPI':
                items_in_order = order.order_items.filter(category=category)
                for item in items_in_order:
                    category_expenditures[2] += item.cost

            elif payment_method == 'AMAZON_WALLET':
                items_in_order = order.order_items.filter(category=category)
                for item in items_in_order:
                    category_expenditures[3] += item.cost

            elif payment_method == 'CASH':
                items_in_order = order.order_items.filter(category=category)
                for item in items_in_order:
                    category_expenditures[4] += item.cost 

        expenditures.append(category_expenditures)
    return JsonResponse({'expenditures': expenditures})

def category_expenditure(request):
    selected_category = request.GET.get('selectedcategory')
    user_orders = Orders.objects.filter(user=request.user)
    categories = Category.objects.all()

    expenditures = [["January", 0], ["February", 0], ["March", 0], ["April", 0], ["May", 0], ["June", 0],
                    ["July", 0], ["August", 0], ["September", 0], ["October", 0], ["November", 0], ["December", 0]]
    
    for category in categories:
        for order in user_orders:
            for item in order.order_items.filter(category=category):
                if selected_category and item.category.category_name != selected_category:
                    continue           
                month = order.date.month
                expenditures[month-1][1] += item.cost
    return JsonResponse({'expenditures': expenditures})

@login_required()
def more_stats(request):
    return render(request, 'server/more_stats.html')

def payment_page(request):
    item_id = request.GET.get('item')
    item = None
    if item_id:
        item = Items.objects.get(item_id=item_id)
    else:
        return render(request, 'server/payment.html')
    
    return render(request, 'server/payment.html', {'item': item})

def savings_tracker_data(request):
    month = request.GET.get('month')
    user_orders = Orders.objects.filter(user=request.user, date__month=month)
    categories = Category.objects.all()

    savings = []
    for category in categories:
        category_expenditure = 0
        for order in user_orders:
            items_in_order = order.order_items.filter(category=category)
            for i in range(0, len(items_in_order)):
                category_expenditure += order.savings
        savings.append([category.category_name, category_expenditure])

    total_savings = sum([x[1] for x in savings])
    return JsonResponse({'savings': savings, 'total_savings': total_savings})

def savings_tracker(request):
    return render(request, 'server/savings_tracker.html')

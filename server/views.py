from django.shortcuts import render, redirect
from .models import Orders, Category, Items, Set_Budget, Bank_Info, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import datetime
from django.contrib.auth.decorators import login_required
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
import random


def home(request):
    latest_items = Items.objects.all().order_by('-id')[:8]
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

@login_required
def orders_page(request):
    user = request.user
    orders = Orders.objects.filter(user=user).order_by('-date')
    return render(request, 'server/orders.html', {'orders': orders})

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

def dynamic_order(request):
    bankDetails = request.GET.get('bankDetails')
    bank_obj = Bank_Info.objects.get(bank_name=bankDetails)
    disc_data = [0,0]

    if bank_obj:
        if bank_obj.perc_discount > 0:
            disc_data[0] = bank_obj.perc_discount
        if bank_obj.perc_cashback > 0:
            disc_data[1] = bank_obj.perc_cashback

    return JsonResponse({'disc_data': disc_data})

def payment_page(request):
    item_id = request.GET.get('item')
    item = None
    if item_id:
        item = Items.objects.get(item_id=item_id)
    else:
        return render(request, 'server/payment.html')
    
    if request.method == 'POST':
        bank_name = request.POST.get('paymentMethod')
        user = request.user
        bank_obj = None
        try:
            bank_obj = Bank_Info.objects.get(bank_name=bank_name)
        except:
            print('No bank_info')

        date = datetime.datetime.now()

        if bank_obj:
            order_obj = Orders(
                user=user,
                date=date,
                Bank_Details=bank_obj,
            )
            
            order_obj.save()
            order_obj.order_items.add(item)
            order_obj.save()

        try:
            budget_obj = Set_Budget.objects.get(month=(datetime.datetime.now().month))
            userProfileObj = UserProfile.objects.get(user=user)
        except:
            print('no budget')

        total_expense = 26895 #static for now
        if (total_expense+item.cost >= (budget_obj.amount*0.75) and budget_obj.above_75 == False):
            send_budget_alert(user.first_name, budget_obj.amount, total_expense+item.cost, userProfileObj.email)
            budget_obj.above_75 = True
            budget_obj.save()
        total_expense+=item.cost

        if (total_expense+item.cost >= (budget_obj.amount) and budget_obj.equal_100 == False):
            send_budget_alert(user.first_name, budget_obj.amount, total_expense+item.cost, userProfileObj.email)
            budget_obj.equal_100 = True
            budget_obj.save()
        total_expense+=item.cost

        return redirect(f'/exp_tracker/?payment=success')
    
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


def send_budget_alert(name, budget, expense,email):
    percent_spent = math.ceil(((expense / budget) * 100))

    # Email configuration
    sender_email = "ashwinnegi.an@gmail.com"
    receiver_email = email
    password = "ksgeqtyyrtthobzp"
    
    # Create the email content
    if percent_spent >= 75 and percent_spent < 100:
        subject = "Budget Alert"
        body = f"Dear {name},\n\nYou have spent {percent_spent:.2f}% of your total budget.\n\nRegards,\nBudget Alert System"

    elif percent_spent >= 100:
        subject = "Budget Alert"
        body = f"Dear {name},\n\nYou have spent 100% of your total budget and exhausted your budget limit of the month.\n\nRegards,\nBudget Alert System"        

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))

    # Create SMTP session for sending the mail
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace 'smtp.example.com' with the SMTP server of your email provider
            server.starttls()  # Enable security
            server.login(sender_email, password)  # Login with your email and password
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def ai_payment_method(request):
    product_price = request.GET.get('product_price')
    disc_data = [['', 0, 0], ['', 0, 0]]

    best_user_method, best_user_amount, best_overall_method, best_overall_amount = get_best_payment_method(user_data, payment_methods_data, int(product_price))
    best_user_method_bank = Bank_Info.objects.get(bank_name=best_user_method)

    if best_user_method_bank:
        disc_data[0][0] = best_user_method_bank.bank_name
        if best_user_method_bank.perc_discount > 0:
            disc_data[0][1] = best_user_method_bank.perc_discount
        if best_user_method_bank.perc_cashback > 0:
            disc_data[0][2] = best_user_method_bank.perc_cashback
        #print(disc_data[0][0], disc_data[0][1], disc_data[0][2])

    best_overall_method_bank = Bank_Info.objects.get(bank_name=best_overall_method)

    if best_overall_method_bank:
        disc_data[1][0] = best_overall_method_bank.bank_name
        if best_overall_method_bank.perc_discount > 0:
            disc_data[1][1] = best_overall_method_bank.perc_discount
        if best_overall_method_bank.perc_cashback > 0:
            disc_data[1][2] = best_overall_method_bank.perc_cashback
        #print(disc_data)

    return JsonResponse({'disc_data': disc_data})


def calculate_final_amount(price, cashback, max_discount=None):
    discount = price * cashback
    if max_discount is not None:
        discount = min(discount, max_discount)
    final_amount = price - discount
    return max(final_amount, 0)  # Ensure final_amount is not less than zero

def get_possible_payment_methods(saved_methods, transactions, amount):
    possible_methods = set(saved_methods)
    
    for transaction in transactions:
        if transaction["amount"] <= amount:
            possible_methods.add(transaction["method"])
    
    return list(possible_methods)

def get_best_payment_method(user_data, all_methods, price):
    saved_methods = user_data["saved_methods"]
    transactions = user_data["transactions"]
    
    # Get possible payment methods from user's history and saved methods
    possible_methods = get_possible_payment_methods(saved_methods, transactions, price)
    
    best_user_method = None
    best_user_amount = float('inf')
    
    for method in possible_methods:
        if method in all_methods:
            details = all_methods[method]
            if details["min_transaction"] <= price and details["success_rate"] >= 0.70:
                final_amount = calculate_final_amount(price, details["cashback"], details.get("max_discount"))
                if final_amount < best_user_amount:
                    best_user_amount = final_amount
                    best_user_method = method
    
    best_overall_method = None
    best_overall_amount = float('inf')
    
    for method, details in all_methods.items():
        if details["min_transaction"] <= price and details["success_rate"] >= 0.70:
            final_amount = calculate_final_amount(price, details["cashback"], details.get("max_discount"))
            if final_amount < best_overall_amount:
                best_overall_amount = final_amount
                best_overall_method = method
    
    return best_user_method, best_user_amount, best_overall_method, best_overall_amount

#mock data for running the algorithm
user_db = {
    "user_id": 1,
    "saved_methods": ["ICICI", "Paytm", "Amazon Wallet", "HDFC"],
    "transactions": [
        # High amounts (usually cards, sometimes UPI or Amazon Pay Wallet)
        {"amount": 5000, "method": "ICICI"},
        {"amount": 6000, "method": "HDFC"},
        {"amount": 7000, "method": "ICICI"},
        {"amount": 8000, "method": "HDFC"},
        {"amount": 9000, "method": "HDFC"},

        # Moderate amounts (usually UPI, sometimes cards or Amazon Pay Wallet)
        {"amount": 2000, "method": "Paytm"},
        {"amount": 2500, "method": "Paytm"},
        {"amount": 3000, "method": "PhonePe"},
        {"amount": 3500, "method": "PhonePe"},
        {"amount": 4000, "method": "Paytm"},

        # Low amounts (usually Amazon Pay Wallet, sometimes UPI or cards)
        {"amount": 500, "method": "Amazon Wallet"},
        {"amount": 600, "method": "Amazon Wallet"},
        {"amount": 700, "method": "Amazon Wallet"},
        {"amount": 800, "method": "Amazon Wallet"},
        {"amount": 900, "method": "PhonePe"},
        {"amount": 1000, "method": "Amazon Wallet"},
        {"amount": 1200, "method": "Paytm"},
        {"amount": 1500, "method": "PhonePe"},
        {"amount": 1800, "method": "Paytm"}
    ]
}

payment_methods_db = {
    "ICICI": {"type": "card", "success_rate": 0.98, "cashback": 0.02, "max_discount": 100, "min_transaction": 1000},
    "HDFC": {"type": "card", "success_rate": 0.67, "cashback": 0.03, "max_discount": 120, "min_transaction": 1500},
    "CITI": {"type": "card", "success_rate": 0.96, "cashback": 0.04, "max_discount": 150, "min_transaction": 500},
    "KOTAK": {"type": "card", "success_rate": 0.95, "cashback": 0.05, "max_discount": 180, "min_transaction": 500},
    "AMEX": {"type": "card", "success_rate": 0.99, "cashback": 0.06, "max_discount": 200, "min_transaction": 2000},
    "Amazon Pay": {"type": "upi", "success_rate": 0.98, "cashback": 0.05, "max_discount": 150, "min_transaction": 500},
    "Paytm": {"type": "upi", "success_rate": 0.53, "cashback": 0.04, "max_discount": 60, "min_transaction": 100},
    "PhonePe": {"type": "upi", "success_rate": 0.96, "cashback": 0.03, "max_discount": 70, "min_transaction": 100},
    "Amazon Wallet": {"type": "wallet", "success_rate": 0.97, "cashback": 0.03, "max_discount": 40, "min_transaction": 50},
    "Paytm Wallet": {"type": "wallet", "success_rate": 0.77, "cashback": 0.02, "max_discount": 45, "min_transaction": 50},
    "PhonePe Wallet": {"type": "wallet", "success_rate": 0.96, "cashback": 0.01, "max_discount": 50, "min_transaction": 50}
}


user_data = user_db
payment_methods_data = payment_methods_db
from django.shortcuts import render,redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import User, TempoBill, Owners, Bill

# Create your views here.


def index(request):
    return render(request, 'index.html')

def process(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['id'] = user.id
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return redirect('index')

def register(request):
    return render(request, 'register.html')

def register_process(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        user = User(name=name, username=username, password=password)
        user.save()
        return redirect('index')
    return redirect('register')

def logout(request):
    request.session.flush()

    return redirect('index')  


def home(request):
    session_id = request.session.get('id')
    sessionname = None

    if session_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM user WHERE id = %s", [session_id])
            row = cursor.fetchone()
            if row:
                sessionname = row[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM user")
        users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bill")
        bill = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM owners")
        client = cursor.fetchone()[0]

    context = {
        'sessionname': sessionname,
        'users': users,
        'bill': bill,
        'client': client,
    }

    return render(request, 'home.html', context)




def clients(request):
    session = request.session.get('id')
    sessionname = ""
    
    if session:
        user = Owners.objects.filter(id=session).first()
        if user:
            sessionname = user.name
    
    if request.method == 'POST':
        if 'add' in request.POST:
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            address = request.POST['address']
            contact = request.POST['contact']
            meterReader = request.POST['meterReader']
            
            Owners.objects.create(fname=fname, lname=lname, address=address, contact=contact)
            TempoBill.objects.create(client=fname, prev=meterReader)
    
    owners = Owners.objects.all()
    
    return render(request, 'clients.html', {'sessionname': sessionname, 'owners': owners})

def edit_owner(request):
    if request.method == 'POST':
        owner_id = request.POST.get('id')
        id = request.POST.get('id')
        lname = request.POST.get('lname')
        fname = request.POST.get('fname')
        address = request.POST.get('address')
        contact = request.POST.get('contact')

        if id and owner_id:
            owner = Owners.objects.get(id=owner_id)
            owner.id = id
            owner.lname = lname
            owner.fname = fname
            owner.address = address
            owner.contact = contact
            owner.save()
        
        return redirect('clients')
    
    return redirect('clients')

def delete_client(request, owner_id):
    owner = Owners.objects.get(id=owner_id)
    owner.delete()

    return redirect('clients')



def users(request):
    session = request.session.get('id')
    sessionname = ""

    if session:
        user = User.objects.filter(id=session).first()
        if user:
            sessionname = user.name

    if request.method == 'POST':
        if 'add' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            
            User.objects.create(username=username, password=password, name=name)
            
        
    users = User.objects.all()

    return render(request, 'users.html', {'users': users, 'sessionname': sessionname})

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.save()
        
        return redirect('users')
    
    return render(request, 'edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    
    return redirect('users')




def billing(request):
    session = request.session.get('id')
    sessionname = ""

    if session:
        user = User.objects.filter(id=session).first()
        if user:
            sessionname = user.name

    owners = Owners.objects.all()

    return render(request, 'billing.html', {'owners': owners, 'sessionname': sessionname})

def paybill(request, owner_id):
    owner = Owners.objects.get(id=owner_id)
    previous = TempoBill.objects.get(client=owner.fname).prev

    context = {
        'owner': owner,
        'previous': previous,
        'date': datetime.now().strftime('%y/%m/%d %H:%M:%S')
    }
    
    return render(request, 'paybill.html', context)

def addbill(request, owner_id):
    if request.method == 'POST':
        owners_id = request.POST['owners_id']
        prev = request.POST['prev']
        pres = request.POST['pres']
        totalcons = float(pres) - float(prev)
        price = request.POST['price']
        pricetotal = float(totalcons) * float(price)
        date = request.POST['date']

        try:
            tempo_bill = TempoBill.objects.get(client=owner_id)
            tempo_bill.prev = pres
            tempo_bill.save()
        except ObjectDoesNotExist:

         Bill.objects.create(
            owners_id=owners_id,
            prev=prev,
            pres=pres,
            price=pricetotal,
            date=date
        )

        return redirect('billing')

def view_bill(request, owner_id):
    session = request.session.get('id')
    sessionname = ""

    if session:
        user = User.objects.filter(id=session).first()
        if user:
            sessionname = user.name

    bills = Bill.objects.filter(owners_id=owner_id)

    for bill in bills:
        totalcons = float(bill.pres) - float(bill.prev)
        bill.bill_amount = totalcons * float(bill.price)

    return render(request, 'viewbill.html', {'bills': bills, 'sessionname': sessionname})

def view_payment(request, bill_id):
    session = request.session.get('id')

    if not session:
        return redirect('index') 

    bill = Bill.objects.filter(id=bill_id).first()
    if not bill:
        return HttpResponse("Error: Data not found..")

    owner = Owners.objects.filter(id=bill.owners_id).first()
    if not owner:
        return HttpResponse("Error: Data not found..")

    totalcons = float(bill.pres) - float(bill.prev)
    bill.bill_amount = totalcons * float(bill.price)

    context = {
        'bill': bill,
        'owner': owner,
    }

    return render(request, 'viewpayment.html', context)

def del_bill(request, bill_id):
    Bill.objects.filter(id=bill_id).delete()
    return redirect(request.META.get('HTTP_REFERER', ''))
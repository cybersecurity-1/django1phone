from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Register
from .models import Product
from .models import Cart
from .models import Order
from .models import Category


# Create your views here.
def index(request):
    cat = Category.objects.all().values()
    if 'search' in request.GET:
           search = request.GET['search']
           url = f"/product?search={search}"
           return HttpResponseRedirect(url)
    context = {
        'cat':cat
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def about(request):
             
    template = loader.get_template("about.html")
    return HttpResponse(template.render({},request))

def master(request):
    template = loader.get_template("masterpage.html")
    return HttpResponse(template.render({},request))


def account(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('login')
    template = loader.get_template("account.html")
    return HttpResponse(template.render({},request))

# ...................................................................................................................
# def login(request):
#     if 'usersession' in request.session:
#          return HttpResponseRedirect('/')  
#     if request.method=="POST":
#         log_id = request.POST['log_id']
#         log_psd = request.POST['log_psd']
    
#         login=Register.objects.filter(
#         reg_username=log_id,
#         reg_psw=log_psd
#         )

#         if login:
#             request.session['usersession'] = log_id
#             return HttpResponseRedirect('/')

#     template = loader.get_template("login.html")
#     return HttpResponse(template.render({},request))

def login(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/')  

    if request.method == "POST":
        log_id = request.POST['log_id']
        log_psd = request.POST['log_psd']
        
        # Check if the credentials are correct
        login = Register.objects.filter(
            reg_username=log_id,
            reg_psw=log_psd
        )

        if login:
            # Set the user session
            request.session['usersession'] = log_id
            
            # Restore the cart count from the database
            cart_count = Cart.objects.filter(cart_user=log_id).count()
            request.session['cart_count'] = cart_count
            
            # Redirect to the homepage
            return HttpResponseRedirect('/')

    # If not POST, render the login template
    template = loader.get_template("login.html")
    return HttpResponse(template.render({}, request))
# ......................................................................................................................

def register(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        cname = request.POST["name"]
        cemail = request.POST["email"]
        cphone = request.POST["phone"]
        cusername = request.POST["username"]
        cpsw = request.POST["psw"]
    
        con = Register(
            reg_cname = cname,
            reg_cemail = cemail,
            reg_cphone = cphone,
            reg_username = cusername,
            reg_psw = cpsw,

        )
        con.save()
    template = loader.get_template("register.html")
    return HttpResponse(template.render({},request))

def logout(request):
    if 'usersession' in request.session:
     del request.session['usersession']
    request.session.flush()
    return HttpResponseRedirect('/login')

def addproduct(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    category = Category.objects.all().values()
    if request.method == 'POST':
        pro_name = request.POST['pro_name']
        pro_price = request.POST['pro_price']
        pro_image = request.FILES['pro_image']
        p_catid = request.POST['pro_cats']

        pro_cat = Category.objects.get(id = p_catid)

        product = Product(
            pro_name=pro_name,
            pro_price=pro_price,
            pro_image=pro_image,
            pro_cats=pro_cat,
        )

        product.save()
    context={
        'category':category
    }
    template = loader.get_template("addproduct.html")
    return HttpResponse(template.render(context,request))

def product(request):
      if 'search' in request.GET:
           search = request.GET['search']
           products=Product.objects.filter(pro_name__contains = search)
      elif 'pro' in request.GET:
          id = request.GET['pro']
          products = Product.objects.filter(pro_cats = id)
      else:
        products=Product.objects.all().values()

      context={
          'products':products
      }

      template = loader.get_template("product.html")
      return HttpResponse(template.render(context,request))
# ..................................................................................................................
# def addtocart(request,id):
#     if 'usersession' not in request.session:
#         return HttpResponseRedirect('/login')

#     exist = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])
#     if exist:
#         exstcart = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])[0]
#         exstcart.cart_qty+=1
#         exstcart.cart_amount = exstcart.cart_qty * exstcart.cart_price
#         exstcart.save()
#     else:
#         pro = Product.objects.filter(id=id)[0]

#         cart = Cart(cart_user = request.session["usersession"],
#                     cart_proid = pro.id,
#                     cart_name = pro.pro_name,
#                     cart_price = pro.pro_price,
#                     cart_image = pro.pro_image,
#                     cart_qty=1,
#                     cart_amount =pro.pro_price)
#         cart.save()
#     return HttpResponseRedirect("/cart")

def addtocart(request, id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    exist = Cart.objects.filter(cart_proid=id, cart_user=request.session["usersession"])
    
    if exist:
        exstcart = exist.first()
        exstcart.cart_qty += 1
        exstcart.cart_amount = exstcart.cart_qty * exstcart.cart_price
        exstcart.save()
    else:
        pro = Product.objects.get(id=id)
        cart = Cart(
            cart_user=request.session["usersession"],
            cart_proid=pro.id,
            cart_name=pro.pro_name,
            cart_price=pro.pro_price,
            cart_image=pro.pro_image,
            cart_qty=1,
            cart_amount=pro.pro_price
        )
        cart.save()

    # Update the cart count in the session
    cart_count = Cart.objects.filter(cart_user=request.session["usersession"]).count()
    request.session['cart_count'] = cart_count
    request.session.modified = True

    return HttpResponseRedirect("/cart")

# .....................................................................................................................
def cart(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    #delete cart item
    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)[0]
        delcart.delete()

    #change cart quantity
    if 'q' in request.GET:
        q = request.GET['q']
        cp = request.GET['cp']
        cart3= Cart.objects.filter(id=cp)[0]
        if q =='inc':
            cart3.cart_qty+=1
        elif q =='dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1
        cart3.cart_amount = cart3.cart_qty * cart3.cart_price
        cart3.save() 
    user = request.session["usersession"]
    cart=Cart.objects.filter(cart_user=user).values() 
    cart2=Cart.objects.filter(cart_user=user)

    tot = 0
    for x in cart2:
        tot+=x.cart_amount

    shp = tot * 10/100
    gst = tot *18/100

    gtot = tot+shp+gst
    request.session["tot"] = tot
    request.session["gst"] = gst
    request.session["shp"] = shp
    request.session["gtot"] = gtot

    context={
        'cart':cart,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot
    }

    templpate = loader.get_template("cart.html")
    return HttpResponse(templpate.render(context,request))

def checkout(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    co = 0
    adrs = ptype =  ""
    #step4 : after order submit
    if 'div_adrs' in request.POST:
        adrs = request.POST["div_adrs"]
        ptype = request.POST["pay_type"]
        co=1

    user = request.session["usersession"]

    #step1 : delete old data from orders
    old_odr=Order.objects.filter(order_prouser=user,order_status=0)
    old_odr.delete()

    #step2 : add cart data to order table
    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(order_prouser = x.cart_user,
                    order_proname = x.cart_name,
                    order_proprice = x.cart_price,
                    order_proimage = x.cart_image,
                    order_proqty = x.cart_qty,
                    order_proamount = x.cart_amount,
                    order_address=adrs,
                    order_paytype=ptype,
                    order_status=0
                      )
        odr.save()

    #step3 : Display order data
    order=Order.objects.filter(order_prouser=user,order_status=0).values()

    tot = request.session["tot"]
    gst = request.session["gst"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]

    context={

        'order':order,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot,
        'co':co
        }  
         
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

def confirmorder(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    user = request.session["usersession"] 
    order = Order.objects.filter(order_prouser=user,order_status=0) 
    for x in order:
        x.order_status=1
        x.save()
    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))  
    
def myorders(request):
    user = request.session["usersession"]
    order=Order.objects.filter(order_prouser=user,order_status=1)
    context = {
        'order':order
    }
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))


def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())


# # ........................................................................................................
def delete_from_cart(request, id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    
    # Find the cart item by product ID and user session
    cart_item = Cart.objects.filter(cart_proid=id, cart_user=request.session['usersession']).first()
    
    if cart_item:
        # Delete the cart item
        cart_item.delete()
        
        # Update the cart count in the session
        cart_count = Cart.objects.filter(cart_user=request.session['usersession']).count()
        request.session['cart_count'] = cart_count
        request.session.modified = True
    
    # Redirect back to the cart page or index page
    return HttpResponseRedirect('/cart')



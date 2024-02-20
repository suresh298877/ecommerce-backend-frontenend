from django.shortcuts import render
from rest_framework import generics,permissions,authentication,pagination,viewsets
from . import serializers
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import IntegrityError
# Create your views here.

class VendorList(generics.ListCreateAPIView):
    queryset=models.Vendor.objects.all()
    serializer_class=serializers.VendorSerializer

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Vendor.objects.all()
    serializer_class=serializers.VendorDetailSerializer

@csrf_exempt
def vendor_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    address=request.POST.get('address')
    username=request.POST.get('username')
    password=request.POST.get('password')
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
        )
        user.set_password(password)
        user.save()
        if user :
            #Create Customer
            try:
                vendor=models.Vendor.objects.create(
                    user=user,
                    mobile=mobile,
                    address=address
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'vendor':vendor.id,
                    'msg':'Thank you for your registration. You can login now'
                }
            except IntegrityError:
                msg={
                'bool':False,
                'msg':'mobile already exist!!'
            }
        else:
            msg={
                'bool':False,
                'msg':'Oops... Something went wrong!!'
            }
    except IntegrityError:
        msg={
                'bool':False,
                'msg':'Username already exist!!!'
            }
    return JsonResponse(msg)

@csrf_exempt
def vendor_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    # print(user)
    if user :
        vendor=models.Vendor.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':vendor.id,
        }
    else:
        msg={
            'bool':False,
            'msg':'Invalid Username/Password!!'
        }
    return JsonResponse(msg)

class ProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        if 'category' in self.request.GET:
            category=self.request.GET['category']
            category=models.ProductCategory.objects.get(id=category)
            qs=qs.filter(category=category)
        if 'fetch_limit' in self.request.GET:
            limit=int(self.request.GET['fetch_limit'])
            qs=qs[:limit]
        return qs
    
class VendorProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        vendor_id=self.kwargs['vendor_id']
        qs=qs.filter(vendor_id=vendor_id)
        return qs
            
        # try:
        #     if self.request.GET['category'] is not None:
        #         category=self.request.GET['category']
        #         category=models.ProductCategory.objects.get(id=category)
        #         qs=qs.filter(category=category)
        #         return qs
        # except Exception as e:
        #     return qs



class ProductImgsList(generics.ListCreateAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProudctImageSerializer
    
class ProductImgsDetail(generics.ListCreateAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProudctImageSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        product_id=self.kwargs['product_id']
        qs=qs.filter(product__id=product_id)
        return qs


class ProductImgDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProudctImageSerializer
    

class TagProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        tag=self.kwargs['tag']
        qs=qs.filter(tags__icontains=tag)
        return qs
    

class ReletedProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        product_id=self.kwargs['pk']
        product=models.Product.objects.get(id=product_id)
        qs=qs.filter(category=product.category).exclude(id=product_id)
        return qs

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductDetailSerializer


#Customer
class CustomerList(generics.ListCreateAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerDetailSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.User.objects.all()
    serializer_class=serializers.UserSerializer

@csrf_exempt
def customer_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    # print(username,password)
    user=authenticate(username=username,password=password)
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaa',user)
    msg={}
    if user :
        try:
            customer=models.Customer.objects.get(user=user)
        except Exception as e:
            msg={
            'bool':False,
            'msg':'Invalid Username/Password!!'
            }
            return JsonResponse(msg)
        if customer:
            msg={
                'bool':True,
                'user':user.username,
                'id':customer.id,
            }
        else:
            msg={
            'bool':False,
            'msg':'Invalid Username/Password!!'
            }
            return msg
    else:
        msg={
            'bool':False,
            'msg':'Invalid Username/Password!!'
        }
    return JsonResponse(msg)


@csrf_exempt
def customer_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    username=request.POST.get('username')
    password=request.POST.get('password')
    print(first_name,last_name,email,mobile,username,password)
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
        )
        user.set_password(password)
        user.save()
        if user :
            #Create Customer
            try:
                customer=models.Customer.objects.create(
                    user=user,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':customer.id,
                    'msg':'Thank you for your registration. You can login now'
                }
            except IntegrityError:
                msg={
                'bool':False,
                'msg':'mobile already exist!!'
            }
        else:
            msg={
                'bool':False,
                'msg':'Oops... Something went wrong!!'
            }
    except IntegrityError:
        msg={
                'bool':False,
                'msg':'Username already exist!!!'
            }
    return JsonResponse(msg)

#Order
class OrderList(generics.ListCreateAPIView):
    queryset=models.Order.objects.all()
    serializer_class=serializers.OrderSerializer

    # def post(self,request,*args,**kwargs):
    #     return super().post(request,*args,**kwargs)
    

#Order Items
class OrderItemList(generics.ListCreateAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemSerializer

# customer order items
class CustomerOrderItemList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(order__customer__id=customer_id)
        return qs
    
class VendorCustomerOrderItemList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        vendor_id=self.kwargs['vendor_id']
        customer_id=self.kwargs['customer_id']
        qs=qs.filter(order__customer__id=customer_id,product__vendor__id=vendor_id)
        return qs


class VendorOrderItemList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        vendor_id=self.kwargs['pk']
        qs=qs.filter(product__vendor__id=vendor_id)
        return qs
    
class VendorDailyReport(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrdersSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        vendor_id=self.kwargs['pk']
        qs=qs.filter(product__vendor__id=vendor_id).annotate(count=Count('id'))
        return qs

class VendorCustomerList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        vendor_id=self.kwargs['pk']
        qs=qs.filter(product__vendor__id=vendor_id)
        return qs

###change this view question mark on video number 76 and at video time 14 03 
class OrderDetail(generics.ListAPIView):
    # queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderDetailSerializer
    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        order_items=models.OrderItems.objects.filter(order=order)
        return order_items


class OrderDelete(generics.RetrieveDestroyAPIView):
    queryset=models.Order.objects.all()
    serializer_class=serializers.OrderDetailSerializer
    # def get_queryset(self):
    #     order_id=self.kwargs['pk']
    #     order=models.Order.objects.get(id=order_id)
    #     order_items=models.OrderItems.objects.filter(order=order)
    #     return order_items
class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset=models.CustomerAddress.objects.all()
    serializer_class=serializers.CustomerAddressSerializer

class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.ProductRatingSerializer
    queryset=models.ProductRating.objects.all()



#Category List API
class CategoryList(generics.ListCreateAPIView):
    queryset=models.ProductCategory.objects.all()
    serializer_class=serializers.CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.ProductCategory.objects.all()
    serializer_class=serializers.CategoryDetailSerializer

class OrderModify(generics.RetrieveUpdateAPIView):
    queryset=models.Order.objects.all()
    serializer_class=serializers.OrderSerializer

@csrf_exempt
def update_order_status(request,order_id):
    if request.method=='POST':
        updateRes=models.Order.objects.filter(id=order_id).update(order_status=True)
        msg={
            'bool':False,
        }
        if updateRes:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)

@csrf_exempt
def update_product_download_count(request,product_id):
    if request.method=='POST':
        print('aaaaaaaaaaaaaaaaaaaaaaaa',product_id)
        product=models.Product.objects.get(id=product_id)
        totalDownloads=int(product.downloads)
        totalDownloads+=1
        if totalDownloads ==0:
            totalDownloads=1
        updateRes=models.Product.objects.filter(id=product_id).update(downloads=str(totalDownloads))
        msg={
            'bool':False,
        }
        if updateRes:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)


# wishlist

class WishList(generics.ListCreateAPIView):
    queryset=models.Wishlist.objects.all()
    serializer_class=serializers.WishlistSerializer

@csrf_exempt
def check_in_wishlist(request):
    if request.method=='POST':
        product_id=request.POST.get('product')
        customer_id=request.POST.get('customer')
        checkWishlist=models.Wishlist.objects.filter(product__id=product_id,customer__id=customer_id).count()
        msg={
            'bool':False,
        }
        if checkWishlist>0:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)


@csrf_exempt
def delete_customer_orders(request,customer_id):
    if request.method=='DELETE':
        orders=models.Order.objects.filter(customer__id=customer_id).delete()
        msg={
            'bool':False,
        }
        if orders:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)

#customer wish items
class CustomerWishItemList(generics.ListAPIView):
    queryset=models.Wishlist.objects.all()
    serializer_class=serializers.WishlistSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(customer__id=customer_id)
        return qs
    
@csrf_exempt
def remove_from_wishlist(request):
    if request.method=='POST':
        wishlist_id=request.POST.get('wishlist_id')
        # customer_id=request.POST.get('customer')
        res=models.Wishlist.objects.filter(id=wishlist_id).delete()
        msg={
            'bool':False,
        }
        if res:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)

class CustomerAddressList(generics.ListAPIView):
    queryset=models.CustomerAddress.objects.all()
    serializer_class=serializers.CustomerAddressSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(customer__id=customer_id).order_by('id')
        return qs
    
@csrf_exempt
def mark_default_address(request,pk):
    if request.method=='POST':
        address_id=request.POST.get('address_id')
        # customer_id=request.POST.get('customer')
        models.CustomerAddress.objects.all().update(default_address=False)
        res=models.CustomerAddress.objects.filter(id=address_id).update(default_address=True)
        msg={
            'bool':False,
        }
        if res:
            msg={
                'bool':True,
            }
    return JsonResponse(msg)

def customer_dashboard(request,pk):
    customer_id=pk
    # print(customer_id)
    # totalOrders=models.OrderItems.objects.filter(order=models.Order.objects.get(customer_id=customer_id).id).count()
    totalOrders=models.Order.objects.filter(customer_id=customer_id).count()
    totalWishList=models.Wishlist.objects.filter(customer_id=customer_id).count()
    totalAddress=models.CustomerAddress.objects.filter(customer_id=customer_id).count()
    # print(models.CustomerAddress.objects.get(customer_id=customer_id))
    print(totalOrders,totalWishList,totalAddress)
    msg={
        'totalOrders':totalOrders,
        'totalWishList':totalWishList,
        'totalAddress':totalAddress
    }
    return JsonResponse(msg)



def vendor_dashboard(request,pk):
    vendor_id=pk
    # print(customer_id)
    # totalOrders=models.OrderItems.objects.filter(order=models.Order.objects.get(customer_id=customer_id).id).count()
    totalProducts=models.Product.objects.filter(vendor__id=vendor_id).count()
    totalOrders=models.OrderItems.objects.filter(product__vendor__id=vendor_id).count()
    totalCustomers=models.OrderItems.objects.filter(product__vendor__id=vendor_id).values('order__customer').count()
    # print(models.CustomerAddress.objects.get(customer_id=customer_id))
    # print(totalOrders,totalWishList,totalAddress)
    msg={
        'totalProducts':totalProducts,
        'totalOrders':totalOrders,
        'totalCustomers':totalCustomers
    }
    return JsonResponse(msg)
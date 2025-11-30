from .views import UserView , ProductView ,OrderView , makepayment , verify_payment , CartItemView , PaymentHistory
from rest_framework.routers import DefaultRouter
from django.urls import path , include

routes = DefaultRouter()

routes.register("users" , UserView , basename="user")
routes.register("products" , ProductView , basename="products")
routes.register("cartitem" ,CartItemView , basename="cartitem" )
routes.register("order" , OrderView ,basename="order")
routes.register("paymenthistory" , PaymentHistory , basename="paymenthistory")
urlpatterns= [
    path("makepayment/<id>" , view=makepayment),
    path("verifypayment/" , view= verify_payment),
    path("" , include(routes.urls))
]
from django.shortcuts import render
from .paymenthook import paymentHook
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serial import UserSerial , ProductSerial , OrderSerial ,CartItemserial , PaymentSerial
from .models import User , Product , Order , Cart ,Payment
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
import os
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter 


class UserView(ModelViewSet):
    serializer_class = UserSerial
    queryset = User.objects.all()
    #permission_classes =[IsAuthenticated]
    
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerial
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
    def perform_create(self, serializer):
        serializer.save(seller = self.request.user)
        #return super().perform_create(serializer)
        


class CartItemView(ModelViewSet):
    serializer_class = CartItemserial

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        cart , created = Cart.objects.get_or_create(buyer = user)
        query = cart.items.all()
    
        return query
        



class OrderView(ModelViewSet):
    serializer_class = OrderSerial
    permission_classes= [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        query = Order.objects.filter(buyer = user)
        return query


class PaymentHistory(ModelViewSet):
    serializer_class = PaymentSerial
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        query = Payment.objects.filter(buyer = user)
        
        return query



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def makepayment(req , id):
    from uuid import uuid4
    order = Order.objects.get(id = id)
    amount = order.total_price()
    tx_ref = f"chewatatest-{uuid4()}"
    api_key = os.getenv("CHAPA")
    
    
    payment_data = paymentHook(amount=amount,req=req , tx_ref = tx_ref ,api_key= api_key)
    
    payment = Payment.objects.create(
        order = order,
        amount = amount,
        transaction_id = tx_ref,
        buyer = req.user
    )
    
    payment.save()
   
    
    return Response(payment_data, status=status.HTTP_200_OK)





def verify_payment(req):
    tx_ref= req.GET.get("tx_ref")
    payment = Payment.objects.get(transaction_id = tx_ref)
    payment.status = "SUCCESS"
    
    payment.save()
    
    return Response({"payment": "Success"} , status=status.HTTP_202_ACCEPTED)
    
    
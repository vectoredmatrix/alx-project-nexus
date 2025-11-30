from .models import User , Payment ,Review , Cart ,CartItem , Order ,OrderItem , Product
from django.contrib.auth.hashers import make_password

from rest_framework.serializers import ModelSerializer , SerializerMethodField , ImageField , UUIDField , ValidationError ,Serializer , IntegerField ,PrimaryKeyRelatedField

class UserSerial(ModelSerializer):
    dp = ImageField(required = True)
    
    class Meta:
        model = User
        fields = ["username" , 
                  "first_name" ,
                  "last_name",
                  "role",
                  "dp",
                  "phone",
                  "email",
                  "password"]
        extra_kwargs = {"password":{"write_only":True}}
        
        
    def create(self, validated_data):
        pword = validated_data.get("password" ,None)
        
        validated_data["password"] = make_password(pword)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
       
        fields = [
        "username",
        "first_name",
        "last_name",
        "role",
        "dp",
        "phone",
        "email",
        "password"
        ]
    
        for field in fields:
             setattr(instance, field, validated_data.get(field, getattr(instance, field)))
    

        pword = validated_data.get("password")
        
        if pword:
            instance.password = make_password(pword)
    
        instance.save()
        return instance
    


class ProductSerial(ModelSerializer):
    image = ImageField(required = True)
    seller = UserSerial(read_only = True)
    class Meta:
        model =Product
        fields = "__all__"
        
class CartItemserial(ModelSerializer):
    product = ProductSerial(read_only = True)
    product_id = UUIDField(write_only = True)
    cart = PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"
        
    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        
        try:
            product = Product.objects.get(id= product_id)
        
        except Product.DoesNotExist:
            raise ValidationError({"Product_id":"Invalid Product Id"})
        
        
        user = self.context["request"].user
        cart, created = Cart.objects.get_or_create(buyer=user)
        validated_data["cart"] = cart
        validated_data["product"] = product
        return super().create(validated_data)
        
        
class OrderItemInputSerializer(Serializer):
    product_id = UUIDField()
    quantity = IntegerField(min_value = 1)
    
    
class OrderItemSerial(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"    
    
class OrderSerial(ModelSerializer):
    items = OrderItemInputSerializer(write_only = True , many= True)
    orderedItems = OrderItemSerial(read_only = True , many= True , source = "items")
    
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id" , "buyer","created_at","status","orderedItems"]
        
    
    def create(self, validated_data):
        items = validated_data.pop("items")
        request = self.context.get("request")
        order = Order.objects.create(buyer = request.user)
        
        for item in items:
            try:
                product = Product.objects.get(id = item["product_id"])
            except Product.DoesNotExist:
                 raise ValidationError({"product_id":"Invalid Product Id"})
             
            
            OrderItem.objects.create(
                order = order,
                product = product,
                quantity = item["quantity"],
                price_at_purchase = product.price
            )
        
        return order
    
class PaymentSerial(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
        read_only_fields = [field.name for field in Payment._meta.fields]
        
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import CartItem
import shop.serializers as serializers


class CartItemView(generics.ListAPIView, APIView):
    serializer_class = serializers.CartItemSerializer

    def post(self, request):
        data = request.data.copy()
        data["user_id"] = request.user.id

        serialized_item = serializers.CartItemSerializer(data=data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()

        return Response(serialized_item.data, status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        CartItem.objects.filter(user_id=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user_id=user.id)


class SingleCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer


class CartItemQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = serializers.CartItemQuantitySerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

import shop.serializers as serializers
from shop.models import CartItem, Order, OrderItem
from shop.permissions import IsAdminOrReadOnly


class OrderView(generics.ListCreateAPIView, APIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def post(self, request):
        new_order = Order.objects.create(user_id=request.user.id)
        serialized_new_order = serializers.OrderSerializer(new_order)
        order_id = serialized_new_order.data['id']

        items_in_cart = CartItem.objects.filter(user_id=request.user.id)
        if items_in_cart.exists():
            for cart_item in items_in_cart:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=cart_item.product_id,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )
                order_item.save()
                cart_item.delete()
        else:
            return Response({'error': 'Cart is empty'}, status.HTTP_400_BAD_REQUEST)

        order_items = OrderItem.objects.filter(order_id=order_id)
        serialized_order_items = serializers.OrderItemSerializer(order_items, many=True)

        return Response(
            {
                'order': serialized_new_order.data,
                'order_items': serialized_order_items.data,
            },
            status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)


class SingleOrderView(generics.DestroyAPIView, APIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order_id=pk)

        if (request.user.id != order.user_id) and (not request.user.is_superuser):
            return Response(
                {'error': 'Unauthorized access to order details'},
                status.HTTP_403_FORBIDDEN,
            )

        serialized_order = serializers.OrderSerializer(order)
        serialized_order_items = serializers.OrderItemSerializer(order_items, many=True)

        return Response(
            {
                'order': serialized_order.data,
                'order_items': serialized_order_items.data,
            }
        )


class OrderDeliveryStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderDeliveryStatusSerializer
    permission_classes = [IsAdminOrReadOnly]

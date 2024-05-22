from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import shop.serializers as serializers
from shop.models import Order, OrderItem
from shop.permissions import IsAdminOrReadOnly


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)


class SingleOrderView(generics.DestroyAPIView, APIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
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
    permission_classes = [IsAdminUser]

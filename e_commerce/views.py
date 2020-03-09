from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, ColorOfItem, SizeOfItem, SortCategories, Order
from .serializers import ItemSerializer, ColorofItemSerializers, SizeOfItemSerializer, SortCategoriesSerializers, \
    ListBasketItemSerializer, OrderSerializer


class SortCategoriesViewSet(viewsets.ModelViewSet):
    queryset = SortCategories.objects.all()
    lookup_field = 'id'
    serializer_class = SortCategoriesSerializers


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    lookup_field = 'id'
    serializer_class = ItemSerializer


class ColorofItemViewSet(viewsets.ModelViewSet):
    queryset = ColorOfItem.objects.all()
    lookup_field = 'id'
    serializer_class = ColorofItemSerializers


class SizeOfItemViewSet(viewsets.ModelViewSet):
    queryset = SizeOfItem.objects.all()
    lookup_field = 'id'
    serializer_class = SizeOfItemSerializer


class ListProductToBasketViewSet(APIView):

    def get(self, request):
        basket = request.user.basket

        color_of_item = basket.color_basket.all()
        colors = []

        for color in color_of_item:
            colors.append(color.name)

        item_of_product = basket.item_basket.all()
        items = []

        for item in item_of_product:
            items.append(item.name)

        size_of_item = basket.size_basket.all()
        sizes = []

        for size in size_of_item:
            sizes.append(size)

        return Response([colors, items, sizes])

    def post(self, request):
        serializer = ListBasketItemSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            items = serializer.validated_data['item_basket']
            size_item = serializer.validated_data['size_basket']
            color_item = serializer.validated_data['color_basket']

            basket = user.basket

            for size in size_item:
                basket.size_basket.add(size)

            for color in color_item:
                basket.color_basket.add(color)

            for item in items:
                basket.item_basket.add(item)

            return Response({'items in basket': [g.id for g in basket.item_basket.all()],
                             'colors in basket': [q.id for q in basket.color_basket.all()],
                             'size in basket': [r.id for r in basket.size_basket.all()]},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(APIView):

    def get(self, request):
        queryset = request.user.basket.item_basket.all()
        product = []
        for item in queryset:
            product.append(item.name)
        return Response(product)

    def post(self, request, ):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            basket = request.user.basket
            items = basket.item_basket.all()
            colors = basket.color_basket.all()
            sizes = basket.size_basket.all()

            total_price = 0

            for item in items:
                total_price += item.price

            for color in colors:
                total_price += color.price

            for size in sizes:
                total_price += size.price

            order = Order.objects.create(delivery=serializer.validated_data['delivery'],
                                         total_price=total_price, basket=basket)

            return Response({'Total price': total_price,
                             'Delivery type': order.delivery,
                             'Identifier': order.slug})

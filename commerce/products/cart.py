from typing import Any


class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session-key')

        if 'session-key' not in self.session:
            cart = self.session['session-key'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['price'] += product.price
            # self.cart[product_id]['name'] = product.name
        else:
            self.cart[product_id] = {
                'price': product.price, 'name': product.name}

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def setPriceHT(self):
        priceHT = 0
        for product_id in self.cart:
            priceHT += self.cart[product_id]['price']
        return priceHT

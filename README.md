# Warehouse-purchase

A microservice with payment and inventory services.

Inventory service to store products and products' details.

Payment service to purchase products from the inventory service.

When products are purchased, an event is sent from the payment service, using redis stream, to the inventory service.

The event handles:
- updating the quantity of products available
- processing discount and fees
- updating the status of the purchase order

Both services use Redis JSON for database and Redis stream for the event driven architecture.


# Microservices

Two microservices.
Business.py is the payment microservice, buys from the inventory microservice, Stock.py

Stock.py stores inventory in a RedisJSON database.

Redis Streams sends events from one microservice to the other.

Redis was chosen because Redis has everything needed.
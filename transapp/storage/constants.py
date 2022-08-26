from django.db import models

DEFAULT_TIME_OPEN = [(8, 16), (8, 16), (8, 16), (8, 16), (8, 16)]
WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),]
SEND_EMAIL_URL = 'http://mail:8001/email-complain?provider={}'
BROKEN_ORDER_TEXT = "Twoje zamówienie o numerze {} uległo uszkodzeniu w trakcie transportu, reklamacja została złożona do firmy kurierskiej, a pieniądze zostaną zwrócone na twoje konto"
BROKEN_ORDERS_TEXT = "Twoje zamówienia o numerach {} uległy uszkodzeniu w trakcie transportu, reklamacja została złożona do firmy kurierskiej, a pieniądze zostaną zwrócone na twoje konto"
class StatusChoice(models.TextChoices):
    ''' Choices for delivery status in action model '''
    DELIVERED_BROKEN = 'delivered_broken', 'Delivered with broken products'
    DELIVERED = 'delivered' , 'Delivered with no problems'
    IN_PROGRESS = 'in_progress', 'In progress'
    UNREADY = 'unready', 'Not ready to action'



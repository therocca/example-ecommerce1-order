import enum


# TODO: possibly add generic typing for entity IDs


class OrderState(enum.Enum):
    """
    Enumeration for all possible state for an order, from creation to shipping and delivery.
    """

    CREATED = "CREATED"
    CHANGED = "CHANGED"
    CANCELLED = "CANCELLED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

    def __str__(self):
        return '%s' % self.value
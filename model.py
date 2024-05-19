from dataclasses import dataclass
from datetime import date
from typing import Optional


# order line is an immutable object, with no behavior
@dataclass(frozen=True)
class OrderLine:
    order_id : str
    sku : str
    quantity : int


@dataclass
class Batch:
    reference:int
    sku:str
    available_quantity : int
    state : Optional[date] 
    order_line = set()

    def allocate(self, order_line:OrderLine):
        if self.can_allocate(order_line):
            self.order_line.add(order_line)

    def deallocate(self, order_line:OrderLine):
        if order_line in self.order_line:
            self.order_line.remove(order_line)
    
    def can_allocate(self, order_line:OrderLine)->bool:
        return order_line.sku == self.sku and order_line.quantity <= self.availibale_quantity


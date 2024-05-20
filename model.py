from dataclasses import dataclass
from datetime import date
from typing import Optional
from typing import NewType

Quantity = NewType('Quantity', int)
Sku = NewType('Sku', str)
BatchReference = NewType('BatchReference', int)
OrderId = NewType('OrderId', int)
OrderReference = NewType('OrderReference', int)
ProductReference = NewType('ProductReference', int)
AvailibaleQuantity = NewType('AvailibaleQuantity', int)

# order line is an immutable object, with no behavior
@dataclass(frozen=True)
class OrderLine:
    orderid: OrderReference
    sku: ProductReference
    qty: Quantity

@dataclass
class Batch:
    reference: BatchReference
    sku: Sku
    available_quantity: AvailibaleQuantity
    state: Optional[date]
    order_line = set()

    def __gt__(self, other):
        if self.state is None:
            return False  
        if other.state is None:
            return True
        return self.state > other.state

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.order_line.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line in self.order_line:
            self.order_line.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return order_line.sku == self.sku and order_line.qty <= self.availibale_quantity

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self.order_line)

    @property
    def availibale_quantity(self) -> int:
        return self.available_quantity - self.allocated_quantity
    
def allocate(order_ine:OrderLine, batch: list[Batch]):
    batch = next(b for b in sorted(batch) if b.can_allocate(order_ine))
    batch.allocate(order_ine)
    return batch.reference

class OutOfStock(Exception):
    pass

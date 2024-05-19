from datetime import date, timedelta
import pytest

from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def make_batch_and_line(sku, batch_qty, line_qty): return (
        Batch("batch-001", sku, batch_qty, state=date.today()),
        OrderLine("order-123", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(order_line)
    assert batch.available_quantity == 20 - 2

def test_can_allocate_if_available_greater_than_required():
    batch , order_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    assert batch.can_allocate(order_line)

def test_cannot_allocate_if_available_smaller_than_required():
    batch, order_line = make_batch_and_line("SMALL-TABLE", 2, 3)
    assert not batch.can_allocate(order_line)

def test_can_allocate_if_available_equal_to_required():
    batch, order_line = make_batch_and_line("SMALL-TABLE", 2, 2)
    assert batch.can_allocate(order_line)

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, state=None) 
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10) 
    assert batch.can_allocate(different_sku_line) is False

def test_prefers_warehouse_batches_to_shipments():
    warehouse_batch = Batch("warehouse-batch", "SMALL-TABLE", 100, state=None)
    shipment_batch = Batch("shipment-batch", "SMALL-TABLE", 100, state=tomorrow)
    order_line = OrderLine("order-123", "SMALL-TABLE", 10)
    assert warehouse_batch.can_allocate(order_line)
    assert not shipment_batch.can_allocate(order_line)

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2) 
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_can_deallocate_allocated_lines():
    batch, order_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2) 
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 20


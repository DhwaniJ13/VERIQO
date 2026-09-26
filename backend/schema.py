from typing import List, Optional

from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class Invoice(BaseModel):
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None

    items: List[InvoiceItem] = Field(
        default_factory=list
    )

    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
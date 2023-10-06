from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class ReadingDate:
    target_date: str
    reason: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ReadingDate:
        return ReadingDate(
            target_date=data["readingdateTarget"],
            reason=data["readingreason"],
        )


@dataclass
class Price:
    name: str
    net: float
    gross: float
    unit: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Price:
        return Price(
            name=data["extensions"]["TEXT"],
            net=data["basePrice"]["net"],
            gross=data["basePrice"]["gross"],
            unit=data["extensions"]["EINHEIT"],
        )
    

@dataclass
class Product:
    name: str
    description: str
    prices: List[Price]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Product:
        return Product(
            name=data["product"],
            description=data["productText"],
            prices=[Price.from_dict(price) for price in data["prices"]],
        )


@dataclass
class Contract:
    number: str
    active: bool
    division: str
    description: str
    meteringType: str
    actualBillingPeriodLength: int
    onlineProduct: str
    moveOutMrState: str
    actualMeteringUnit: str
    installation: str
    premise: str
    pod: str
    intUi: str
    actualMeter: str
    actualEqunr: str
    meterClassification: str
    meterOperation: str
    moveinDate: str
    moveoutDate: str
    productText: str
    voltageLevel: str
    consumptionType: str
    collectiveInvoicing: bool
    loadprofileHeader: Any
    meterReadingDates: List[ReadingDate]
    product: Product

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Contract:
        return Contract(
            number=data["number"],
            active=data["active"],
            division=data["division"],
            description=data["description"],
            meteringType=data["meteringType"],
            actualBillingPeriodLength=data["actualBillingPeriodLength"],
            onlineProduct=data["onlineProduct"],
            moveOutMrState=data["moveOutMrState"],
            actualMeteringUnit=data["actualMeteringUnit"],
            installation=data["installation"],
            premise=data["premise"],
            pod=data["pod"],
            intUi=data["intUi"],
            actualMeter=data["actualMeter"],
            actualEqunr=data["actualEqunr"],
            meterClassification=data["meterClassification"],
            meterOperation=data["meterOperation"],
            moveinDate=data["moveinDate"],
            moveoutDate=data["moveoutDate"],
            productText=data["productText"],
            voltageLevel=data["voltageLevel"],
            consumptionType=data["consumptionType"],
            collectiveInvoicing=data["collectiveInvoicing"],
            loadprofileHeader=data["loadprofileHeader"],
            meterReadingDates=[ReadingDate.from_dict(reading_date) for reading_date in data["meterReadingDates"]],
            product=Product.from_dict(data["productData"]["current"]),
        )
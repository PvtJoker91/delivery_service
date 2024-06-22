from datetime import datetime

import pytest

from app.domain.entities.packages import Package, PackageType
from app.domain.entities.users import User
from app.domain.exceptions.packages import TitleTooLongException, WrongPriceValueException, WrongWeightValueException
from app.domain.values.packages import Title, PackageWeight, PackagePrice


def test_create_package_success(user_entity: User, package_type_entity: PackageType):
    title = Title('hello world')
    weight = PackageWeight(100.00)
    price = PackagePrice(300.1)
    package = Package(
        title=title,
        weight=weight,
        price=price,
        type_id=1,
        owner_id=1,
        owner=user_entity,
        type=package_type_entity
    )

    assert package.title == title
    assert package.weight == weight
    assert package.price == price
    assert package.created_at.date() == datetime.today().date()


def test_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title('title' * 200)


def test_wrong_price_value_type():
    with pytest.raises(WrongPriceValueException):
        PackagePrice('100')


def test_wrong_price_value_negative():
    with pytest.raises(WrongPriceValueException):
        PackagePrice(-100)


def test_wrong_weight_value_type():
    with pytest.raises(WrongWeightValueException):
        PackageWeight('100')


def test_wrong_weight_value_negative():
    with pytest.raises(WrongWeightValueException):
        PackageWeight(-100)

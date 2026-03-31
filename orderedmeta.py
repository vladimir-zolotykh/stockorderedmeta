#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import OrderedDict


class Typed:
    def __init__(self, name=None):
        self._name = name

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError(f"{value!r} must be of type {self._expected_type}")
        instance.__dict__[self._name] = value


class String(Typed):
    _expected_type = str


class Integer(Typed):
    _expected_type = int


class Float(Typed):
    _expected_type = float


class OrderedMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        d = dict(clsdict)
        order = []
        for attr, obj in clsdict.items():
            if isinstance(obj, Typed):
                order.append(attr)
            d[attr] = obj
        d["_order"] = order
        return super().__new__(mcls, clsname, bases, d)

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        return OrderedDict()


class Stock(metaclass=OrderedMeta):
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def as_csv(cls):
        for field, value in cls._order:
            print(f"{field = }, {value = }")

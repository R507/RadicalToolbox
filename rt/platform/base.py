"""Stuff"""
from rt.base.objects import Structure


class ManagerParameters(Structure):
    """Atm only the manager to execute itself"""
    def __init__(self, manager):
        self.manager = manager


# Errors raised by the service layer. The controllers turn them into messages for the UI.


class StoreError(Exception):
    """Base class of all business errors."""


class NotFoundError(StoreError):
    """The requested record does not exist."""


class BusinessRuleError(StoreError):
    """The action is not allowed (not enough stock, wrong order status, ...)."""

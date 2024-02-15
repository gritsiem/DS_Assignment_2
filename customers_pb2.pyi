from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InsertMessage(_message.Message):
    __slots__ = ("table_name", "columns", "values")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    columns: str
    values: str
    def __init__(self, table_name: _Optional[str] = ..., columns: _Optional[str] = ..., values: _Optional[str] = ...) -> None: ...

class UpdateMessage(_message.Message):
    __slots__ = ("table_name", "columns", "values", "condition_col", "condition_val")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    CONDITION_COL_FIELD_NUMBER: _ClassVar[int]
    CONDITION_VAL_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    columns: str
    values: str
    condition_col: str
    condition_val: int
    def __init__(self, table_name: _Optional[str] = ..., columns: _Optional[str] = ..., values: _Optional[str] = ..., condition_col: _Optional[str] = ..., condition_val: _Optional[int] = ...) -> None: ...

class SelectOneMessage(_message.Message):
    __slots__ = ("table_name", "column", "search_value")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    SEARCH_VALUE_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    column: str
    search_value: str
    def __init__(self, table_name: _Optional[str] = ..., column: _Optional[str] = ..., search_value: _Optional[str] = ...) -> None: ...

class SelectManyMessage(_message.Message):
    __slots__ = ("table_name", "columns", "search_values", "selected_columns")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_VALUES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    columns: str
    search_values: str
    selected_columns: str
    def __init__(self, table_name: _Optional[str] = ..., columns: _Optional[str] = ..., search_values: _Optional[str] = ..., selected_columns: _Optional[str] = ...) -> None: ...

class generalResponse(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class CreateAccountMessage(_message.Message):
    __slots__ = ("username", "password", "name")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    name: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class LoginMessage(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class SearchProductMessage(_message.Message):
    __slots__ = ("item_category", "keywords")
    ITEM_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    item_category: int
    keywords: str
    def __init__(self, item_category: _Optional[int] = ..., keywords: _Optional[str] = ...) -> None: ...

class AddToCartMessage(_message.Message):
    __slots__ = ("buyer_id", "product_id", "quantity")
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    product_id: int
    quantity: int
    def __init__(self, buyer_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ...) -> None: ...

class RemoveFromCartMessage(_message.Message):
    __slots__ = ("buyer_id", "product_id", "quantity")
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    product_id: int
    quantity: int
    def __init__(self, buyer_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ...) -> None: ...

class ClearCartMessage(_message.Message):
    __slots__ = ("buyer_id",)
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    def __init__(self, buyer_id: _Optional[int] = ...) -> None: ...

class DisplayCartMessage(_message.Message):
    __slots__ = ("buyer_id",)
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    def __init__(self, buyer_id: _Optional[int] = ...) -> None: ...

class MakePurchaseMessage(_message.Message):
    __slots__ = ("buyer_id", "credit_card")
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    CREDIT_CARD_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    credit_card: str
    def __init__(self, buyer_id: _Optional[int] = ..., credit_card: _Optional[str] = ...) -> None: ...

class PurchaseHistoryMessage(_message.Message):
    __slots__ = ("buyer_id",)
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    def __init__(self, buyer_id: _Optional[int] = ...) -> None: ...

class ProvideFeedbackMessage(_message.Message):
    __slots__ = ("buyer_id", "product_id", "feedback_type")
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_TYPE_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    product_id: int
    feedback_type: str
    def __init__(self, buyer_id: _Optional[int] = ..., product_id: _Optional[int] = ..., feedback_type: _Optional[str] = ...) -> None: ...

class GetSellerRatingMessage(_message.Message):
    __slots__ = ("seller_id",)
    SELLER_ID_FIELD_NUMBER: _ClassVar[int]
    seller_id: int
    def __init__(self, seller_id: _Optional[int] = ...) -> None: ...

class LogoutMessage(_message.Message):
    __slots__ = ("buyer_id",)
    BUYER_ID_FIELD_NUMBER: _ClassVar[int]
    buyer_id: int
    def __init__(self, buyer_id: _Optional[int] = ...) -> None: ...

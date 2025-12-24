from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HomeResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class GetTermRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SearchTermRequest(_message.Message):
    __slots__ = ("keyword",)
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    keyword: str
    def __init__(self, keyword: _Optional[str] = ...) -> None: ...

class CreateTermRequest(_message.Message):
    __slots__ = ("term", "description")
    TERM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    term: str
    description: str
    def __init__(self, term: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateTermRequest(_message.Message):
    __slots__ = ("id", "term", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    term: str
    description: str
    def __init__(self, id: _Optional[int] = ..., term: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class DeleteTermRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class Term(_message.Message):
    __slots__ = ("id", "term", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    term: str
    description: str
    def __init__(self, id: _Optional[int] = ..., term: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class TermResponse(_message.Message):
    __slots__ = ("id", "term", "description", "error")
    ID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    id: int
    term: str
    description: str
    error: str
    def __init__(self, id: _Optional[int] = ..., term: _Optional[str] = ..., description: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class GetAllResponse(_message.Message):
    __slots__ = ("terms",)
    class TermsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Term
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Term, _Mapping]] = ...) -> None: ...
    TERMS_FIELD_NUMBER: _ClassVar[int]
    terms: _containers.MessageMap[int, Term]
    def __init__(self, terms: _Optional[_Mapping[int, Term]] = ...) -> None: ...

class SearchTermResponse(_message.Message):
    __slots__ = ("results",)
    class ResultsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Term
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Term, _Mapping]] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.MessageMap[int, Term]
    def __init__(self, results: _Optional[_Mapping[int, Term]] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("message", "error")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    message: str
    error: str
    def __init__(self, message: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

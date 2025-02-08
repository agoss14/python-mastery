# tableformat\formatter.py

__all__ = [
    'create_formatter',
    'print_table',
]

from abc import ABC, abstractmethod

class TableFormatter(ABC):

    _formats = { }

    @classmethod
    def __init_subclass__(cls):
        name = cls.__module__.split('.')[-1]
        TableFormatter._formats[name] = cls

    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass

def print_table(records, fields, formatter):
    print(type(formatter))

    if not isinstance(formatter, TableFormatter):
        raise RuntimeError('Expected a TableFormatter')

    formatter.headings(fields)
    for r in records:
        # Manage the case of objects and the case of dicts
        rowdata = None

        # Instance of a custom class
        if hasattr(r, '__class__') and r.__class__.__module__ != 'builtins':
            rowdata = [getattr(r, fieldname) for fieldname in fields]
        # Dict
        elif type(r) is dict:
            rowdata = [r[fieldname] for fieldname in fields]
        else:
            raise TypeError(f'Unsupported types of element in the container: {type(r).__name__}')
        formatter.row(rowdata)

class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [ (fmt % item) for fmt, item in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])

def create_formatter(name, column_formats=None, upper_headers=False):

    if name not in TableFormatter._formats:
        __import__(f'{__package__}.formats.{name}')

    formatter_cls = TableFormatter._formats.get(name)

    if not formatter_cls:
        raise RuntimeError('Unknown format %s' % name)

    if column_formats:
        class formatter_cls(ColumnFormatMixin, formatter_cls):
              formats = column_formats

    if upper_headers:
        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()
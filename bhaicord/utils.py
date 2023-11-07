from typing import (
    Type,
    Any,
    Dict,
    List,
    Optional,
    TYPE_CHECKING,
    Callable,
    Iterable,
    Union,
    TypeVar
)
import attr
import datetime

T = Callable[[Any], Any]
DataType = Dict[str, Any]

_T = TypeVar("_T")


def from_obj_to_dict(obj: Type[Any], *, ignore: Optional[List[str]] = None) -> DataType:
    """
    Converts an object to dictionary

    We first make some check, since some classes.
    may use ``__dict__`` or ``__slots__``

    Args:
        obj (typing.Type[Any]): The instance or class
        ignore (typing.Optional[typing.List[str]]):
            List containing fields to ignore

    Return:
        typing.Dict[str, typing.Any]:
            A dictionary key-value pairs
    """
    if ignore is None:
        ignore = []

    if hasattr(obj, "__dict__"):
        data = obj.__dict__
    else:
        data = obj.__slots__

    new = {}
    for key in data:
        if key not in ignore:
            if not key.startswith("_"):
                new[key] = getattr(obj, key)

    return new


def simplify_attrs_from_dict(ignore: Optional[Iterable[str]] = None) -> T:

    """
    Some decorator to initialize
    all values given from a dictionary

    Args:
        ignore (typing.Iterable[str]): attributes to ignore

    Return:
        Callable - The class wrapper
    """

    if ignore is None:
        ignore = []

    def class_wrapper(cls: Type[Any]) -> T:

        def call_class(*args, **kwargs) -> Type[Any]:

            instance = cls(*args, **kwargs)
            data: Dict[str, Any] = kwargs.get("data")

            for key, value in data.items():
                if key not in ignore:
                    setattr(instance, key, value)

            return instance
        return call_class
    return class_wrapper


def add_ext(hash_: str) -> str:

    if hash_.startswith("a_"):
        return f"{hash_}.gif"

    return f"{hash_}.png"


def snowflake_to_date(snowflake: Union[str, int]) -> datetime.datetime:
    """
    Converts a snowflake to a valid `datetime.datetime` object

    Args:
        snowflake (typing.Union[str, int]): A valid snowflake

    Returns: `datetime.datetime`
    """

    # The algorithm applied is the same as documented in
    # https://discord.com/developers/docs/reference

    # (snowflake >> 22) + Discord Epoch
    ms = (int(snowflake) >> 22) + 1420070400000

    # Divided by 1000 and then provided to datetime.datetime
    return datetime.datetime.utcfromtimestamp(ms / 1000)


def make_optional(callable_: Callable[[Any], Any], *args, kwargs: Dict[str, Any] = None) -> Optional[Any]:
    """
    Some values from models may be null,
    if we pass an invalid value, an exception might be raised.

    Args:
        callable_(typing.Callable): The callable object
        args (typing.Tuple): All needed arguments
        kwargs (typing.Dict[str, typing.Any]): The data

    """

    try:
        if kwargs is None:
            return callable_(*args)

        return callable_(*args, **kwargs)
    except (KeyError, Exception):
        return None


def is_object(obj: Any) -> bool:
    """To check if a variable is an object"""
    return hasattr(obj, "__dict__") or hasattr(obj, "__slots__")


class Utilities:

    def generate_repr_(
            self, *,
            all_attributes: bool = True,
            attributes: Optional[List[str]] = None,
            allow_none: bool = True

    ) -> str:
        """A helper function to create our repr content

        Keyword Arguments:
            all_attributes (bool): Whether to add all attributes in repr content or not.
                It's True by default

            attributes (Optional[List[str]]):
                Attributes to display

            allow_none (bool): Whether you allow attribute None value or not.
                It's True by default

        Note:
            if `all_attributes` is True, attributes must be None

        """

        def check(var: Any) -> str:
            if isinstance(var, str):
                return f"'{var}'"
            return var

        if all_attributes and attributes:
            raise Exception('You cannot use both')

        if not all_attributes and not attributes:
            raise Exception('You need to use at least one')

        arguments = []

        args = self.__dict__ or self.__slots__

        for argument in args:
            if not all_attributes:
                if argument in attributes:
                    arguments.append((argument, getattr(self, argument, None)))
            else:
                arguments.append((argument, getattr(self, argument, None)))

        new_args = []

        for arg, value in arguments:
            if value is None:
                if not allow_none:
                    continue

            new_args.append(f"{arg}={check(value)}")

        return f"<{self.__class__.__name__} {' '.join(new_args)}>"
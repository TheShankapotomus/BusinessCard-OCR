from re import compile


class BusinessCardParser(object):
    """A document parser that builds _ContactInfo objects

    Attributes
    ----------
    _email_expr : pattern object
        A regex pattern to validate email addresses
    """

    def __init__(self):
        self._email_expr = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def get_contact_info(self, document):
        """Initial processing of business card document

        Note
        ----
        Processing is redirected to the _filter_fields() method

        Parameters
        ----------
        document : str
            A multiline document compressed into a string object

        Returns
        -------
        :obj:`_ContactInfo`
            A populated _ContactInfo object with the extracted data

        """
        fields = self._filter_fields(document.split('\n'))

        return _ContactInfo(**fields)

    def _filter_fields(self, document):
        """Extracts all _ContactInfo fields from a documents

        Note
        ----
        The field_map is populated with the attributes set in _ContactInfo.__slots__

        Parameters
        ----------
        document : :obj:`list` of :obj:`str`
            A list containing each line of the document passed in

        Returns
        -------
        :obj:`dict`
            A dictionary to be passed as the **kwargs to a _ContactInfo initializer

        """
        field_map = {k[2:]: None for k in _ContactInfo.__slots__}

        for line in document:

            if sum(c.isdigit() for c in line) > 6 and "fax" not in line.lower():
                field_map["phone"] = ''.join((c for c in line if c.isdigit()))

            elif '@' in line:
                addr = [t for t in line.split(' ') if '@' in t and '.' in t][0]
                field_map["email"] = addr if self._email_expr.match(addr) else None

        if field_map["email"]:

            check, name = field_map["email"].split('@')[0], None

            for line in document:
                for token in line.split(' '):

                    if token.lower() in check:
                        name = line
                        break

            field_map["name"] = name

        return field_map


class _ContactInfo(object):
    """Data class to store business card info

    Note
    ----
    No attribute manipulation should take place in this class.
    All attributes should be stored in __slots__ for use in the BusinessCardParser.
    All getters call str() on attributes to handle non-string objects

    Parameters
    ----------
    __name : str
        Name field of a business card document
    __phone : str
        Phone number field of a business card document
    __email : str
        Email address field of a business card document
    """

    __slots__ = ("__name", "__phone", "__email")

    def __init__(self, **kwargs):
        self.__name = kwargs["name"]
        self.__phone = kwargs["phone"]
        self.__email = kwargs["email"]

    def __str__(self):
        """Special format string output with every field populated"""
        return f"Name: {self.get_name()}\n" \
               f"Phone: {self.get_phone_number()}\n" \
               f"Email: {self.get_email_address()}"

    def get_name(self):
        """Return str of __name attribute"""
        return str(self.__name)

    def get_phone_number(self):
        """Return str of __phone attribute"""
        return str(self.__phone)

    def get_email_address(self):
        """Return str of __email attribute"""
        return str(self.__email)

from re import compile


class BusinessCardParser(object):

    def __init__(self):
        self._email_expr = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def get_contact_info(self, document):

        fields = self._filter_fields(document.split('\n'))

        return _ContactInfo(**fields)

    def _filter_fields(self, document):

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

    __slots__ = ("__name", "__phone", "__email")

    def __init__(self, **kwargs):

        self.__name = kwargs["name"]
        self.__phone = kwargs["phone"]
        self.__email = kwargs["email"]

    def __str__(self):
        return f"Name: {self.get_name()}\n" \
               f"Phone: {self.get_phone_number()}\n" \
               f"Email: {self.get_email_address()}"

    def get_name(self):
        return str(self.__name)

    def get_phone_number(self):
        return str(self.__phone)

    def get_email_address(self):
        return str(self.__email)

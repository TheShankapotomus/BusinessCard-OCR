from re import compile
from nltk.tag.stanford import CoreNLPNERTagger


class BusinessCardParser(object):

    def __init__(self):

        self._email_expr = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        self._entity_tagger = CoreNLPNERTagger(url="http://localhost:9000")

    def get_contact_info(self, document):

        fields = self._filter_fields(document.split('\n'))

        return _ContactInfo(fields)

    #Should we prefilter here, this is the parser after all?
    def _filter_fields(self, document):

        field_map = {k[2:]: "N/A" for k in _ContactInfo.__slots__}

        #Use whole document to accurately tag
        for tag in self._entity_tagger.tag(" ".join(document)):

            if tag[1] == "PERSON":
                field_map["name"] += tag[0]

        for line in document:

            #E.164?
            if len([c.isdigit() for c in line]) > 6 and "fax" not in line.lower():
                field_map["phone"] = ''.join((c for c in line if c.isdigit()))

            #RFC5322?
            elif '@' in line:
                addr = [t for t in line.split(' ') if '@' in t and '.' in t][0]
                field_map["email"] = addr if self._email_expr.match(addr) else "N/A"

        return field_map


class _ContactInfo(object):

    __slots__ = ("__name", "__phone", "__email")

    def __init__(self, **kwargs):

        for v in self.__slots__:
            setattr(self, v, kwargs[v[2:]])

    def __str__(self):
        return f"Name: {self.get_name()}\n \
                 Phone: {self.get_phone_number()}\n \
                 Email: {self.get_email_address()}\n"

    def get_name(self):
        return self.__name.title()

    def get_phone_number(self):
        return self.__phone

    def get_email_address(self):
        return self.__email

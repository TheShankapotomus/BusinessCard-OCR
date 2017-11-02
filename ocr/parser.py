

class BusinessCardParser(object):

    def get_contact_info(self, document):

        fields = self._filter_fields(document.split("\n"))

        return _ContactInfo(*fields)

    #Should we prefilter here, this is the parser after all?
    def _filter_fields(self, document):

        field_map = {"name": [], "phone": [], "email": []}

        for line in document:

            if len(line.split(' ')) == 2:
                field_map["name"].append(line)

            #work with E.164
            elif len([c.isdigit() for c in line]) > 7 or "phone" in line.lower():
                field_map["phone"].append(line)

            #work with RFC5322
            elif '@' in line and '.' in line:
                field_map["email"].append(line)

        return field_map


class _ContactInfo(object):

    __slots__ = ("name", "phone", "email")

    def __init__(self, **kwargs):

        self.get_name(kwargs["name"])
        self.get_phone_number(kwargs["phone"])
        self.get_email_address(kwargs["email"])

    #Check if words are in dictionary, if so, leave line alone
    def get_name(self):
        pass

    #grab all digits out of string
    def get_phone_number(self):
        pass

    #if it has an @ and a . its probably formed well
    def get_email_address(self):
        pass
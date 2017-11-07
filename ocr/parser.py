from nltk.tag.stanford import CoreNLPNERTagger


class BusinessCardParser(object):

    def __init__(self):

        self.entity_tagger = CoreNLPNERTagger(url='http://localhost:9000')

    def get_contact_info(self, document):

        fields = self._filter_fields(document.split("\n"))

        return _ContactInfo(*fields)

    #Should we prefilter here, this is the parser after all?
    def _filter_fields(self, document):

        field_map = {k: None for k in _ContactInfo.__slots__}

        for line in document:

            #add human name parsing, dictionary check is too vague
            if len(line.split(' ')) == 2:
                test = st.tag([line])
                field_map["name"] = ""

            #work with E.164?
            elif len([c.isdigit() for c in line]) > 7 and "fax" not in line.lower():
                field_map["phone"] = line

            #work with RFC5322?
            elif '@' in line and '.' in line:
                field_map["email"] = line

        return field_map


class _ContactInfo(object):

    __slots__ = ("name", "phone", "email")

    def __init__(self, **kwargs):

        for v in self.__slots__:
            setattr(self, v, kwargs[v])

    def get_name(self):
        return self.name

    #grab all digits out of string
    def get_phone_number(self):
        return ''.join((c for c in self.phone if c.isdigit()))

    #if it has an '@' and a '.'
    def get_email_address(self):
        return [s for s in self.email.split(' ') if '@' in s and '.' in s][0]
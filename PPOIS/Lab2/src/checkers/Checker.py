import re


class Checker:

    @staticmethod
    def date_is_valid(date):
        return re.fullmatch("(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})", date)

import datetime


class InvalidDateException(Exception):
    def __init__(self, message):
        self.message = message
        self.return_status_code = 400
        self.type = "Invalid Request"

    def __str__(self):
        return self.message


def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%d/%m/%Y').date()
    except ValueError:
        raise InvalidDateException("%s is not a correct date, expect format DD/MM/YYYY !" % date_string)

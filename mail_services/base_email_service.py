from datetime import date, datetime, timedelta
from base64 import urlsafe_b64decode
from banks_mail_readers.base_reader import BaseReader


class EmailService():
    def __init__(self, days_from: int):
        self.name = 'Base Service'
        self.credentials = None
        self.service = None
        # End date must be tomorrow in order to
        # To Ensure all messages (including today) al fetched
        self.date_to = date.today() + timedelta(1)
        self.date_from = self.date_to - timedelta(days_from)

    def get_query(self, bank: BaseReader):
        query = f'before: {self.date_to:%Y/%m/%d}'
        query += f' after: {self.date_from:%Y/%m/%d}'
        query += f' from:{bank.email} '

        for sbj in bank.subjetcs_to_ignore:
            query += f'-"{sbj}" '

        return query

    def get_message_body(self, encoded_data: str) -> str:
        """Decode message body to be able to parse it to HTML.

        Arguments:
            encoded_data {str} -- base64 encode html message

        Returns:
            str -- decoded html message
        """
        return urlsafe_b64decode(encoded_data)

    def authenticate(self):
        raise NotImplementedError

    def build_service(self):
        raise NotImplementedError

    def query_mail(self):
        raise NotImplementedError

    def read_mail(self):
        raise NotImplementedError

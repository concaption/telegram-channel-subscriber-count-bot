"""
- This module is responsible for handling the gsheet related tasks
"""
import json
import logging
from typing import Dict, List, Optional

from googleapiclient.errors import HttpError
from pygsheets import authorize, Worksheet, Spreadsheet
from pygsheets.client import Client
from pygsheets.exceptions import NoValidUrlKeyFound

from core import Constant

logger = logging.getLogger(__name__)


class Gsheet:
    """
    Gsheet class to manage the tasks related to gsheet
    """
    _servie_file = Constant.data_dir.joinpath("service.json")
    client: Optional[Client] = None
    service_email: Optional[str] = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initializes the client
        """
        if cls._servie_file.is_file() and cls._servie_file.exists():
            with open(cls._servie_file, "r") as f:
                try:
                    key_data = json.load(f)

                except json.JSONDecodeError:
                    pass

                else:
                    cls.authorize(key_data=key_data, write_data=False)

    @classmethod
    def authorize(cls, key_data: Dict[str, str], write_data: bool = True) -> bool:
        """
        Authorizes the client to handle the api calls
        :return:
        """
        service_email = key_data.get("client_email")
        if service_email:
            cls.client = authorize(service_account_json=json.dumps(key_data))
            cls.service_email = service_email
            if write_data:
                with open(cls._servie_file, "w") as f:
                    json.dump(key_data, f)

            return True

        return False

    @classmethod
    def has_access(cls, sheet_url: str) -> Optional[str]:
        """
        Check if the bot has access to this sheet
        :param sheet_url:
        :return:
        """
        no_valid_url_key = "Google sheet url is invalid"
        can_not_access = "Bot doesn't have access of this sheet. Please share the sheet to this " \
                         f"service email: {cls.service_email} with editor privilege."
        try:
            cls.client.open_by_url(url=sheet_url)

        except NoValidUrlKeyFound:
            return no_valid_url_key

        except HttpError:
            return can_not_access

    @classmethod
    def add_data(
        cls,
        sheet_url: str,
        values: List[str],
    ) -> None:
        """
        Adds the data to the Google sheet
        :param sheet_url: str
        :param values:
        :return:
        """
        spread_sheet: Spreadsheet = cls.client.open_by_url(url=sheet_url)
        parts = sheet_url.split("#gid=")
        work_sheet_id: Optional[str] = None
        if len(parts) == 2:
            work_sheet_id = parts[-1]

        if work_sheet_id is None:
            work_sheet: Worksheet = spread_sheet.sheet1

        else:
            work_sheet: Worksheet = spread_sheet.worksheet(property="id", value=work_sheet_id)

        rows = work_sheet.get_col(col=1, include_tailing_empty=False)
        last_row = len(rows) + 1
        # work_sheet.update_value(addr=(last_row, column_index), val=data)
        work_sheet.update_row(index=last_row, values=values)

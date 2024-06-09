import requests
import io
from typing import Any
from time import sleep

from katana.unit import NotEnglishAndPrintableUnit, NotApplicable
from katana.units.crypto import CryptoUnit


def decodeSubstitute(cipher: str, time=3) -> str:
    """
    This is based on https://github.com/rallip/substituteBreaker
    All it does is use the ``requests`` module to send the ciphertext to
    quipqiup and returns the results as a string.
    """
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }

    clues = ""
    url = "https://quipqiup.com/solve"
    data = {"ciphertext":cipher,"clues":clues,"mode":"auto","was_auto":True,"was_clue":False}

    response = json.loads( requests.post(url, data=json.dumps(data), headers=headers, verify=False).text )

    sleep( min(response["max_time"], time) )

    url = "https://quipqiup.com/status"
    data = {"id":response["id"]}

    return requests.post(url, data=json.dumps(data), headers=headers, verify=False).text


class Unit(NotEnglishAndPrintableUnit, CryptoUnit):
@@ -84,7 +93,7 @@ def __init__(self, *args, **kwargs):

        try:
            requests.get(
                "https://quipqiup.com/", verify=False
            )
        except requests.exceptions.ConnectionError:
            raise NotApplicable("cannot reach quipqiup solver")

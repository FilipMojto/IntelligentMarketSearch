import algorithm
from typing import List, Dict

class EAN:
    # --- EAN configuration ---

    # -- Constant static variables --
    __EAN_LEN = 13
    __SUBCODE_COUNT = 4
    __COUNTRY_CODE_LEN = 2
    __MANUFACTURER_CODE_LEN = 6
    __PRODUCT_ITEM_CODE_LEN = 6
    __CHECK_DIGIT_LEN = 1

    # -- Configurable static variables --
    __DELIMITER = '.'
    

    def get_code(self):
        return self.__CODE

    def set_delimiter(self, delimiter: str):
        if not isinstance(delimiter, str):
            raise ValueError("Invalid type for delimiter, provide a string!")

        self.__DELIMITER = delimiter

    def __init__(self, code : str):
        if len(code) != self.__EAN_LEN:
            raise ValueError(f"Invalid length for EAN code! Valid length: {self.__EAN_LEN}")

        subcodes = code.split(self.__DELIMITER)

        if len(subcodes) != self.__SUBCODE_COUNT:
            raise ValueError("Invalid EAN structure!")
        
        if len(subcodes[0]) != self.__COUNTRY_CODE_LEN or not subcodes[0].isdigit():
            raise ValueError("Invalid country code structure!")
        elif len(subcodes[1]) != self.__MANUFACTURER_CODE_LEN or not subcodes[1].isdigit():
            raise ValueError("Invalid manufacturer code structure!")
        elif len(subcodes[2]) != self.__PRODUCT_ITEM_CODE_LEN or not subcodes[2].isdigit():
            raise ValueError("Invalid product item structure!")
        elif len(subcodes[3]) != self.__CHECK_DIGIT_LEN or not subcodes[3].isdigit():
            raise ValueError("Invalid check digit structure!")
        
        self.__CODE = code
        

        #if len(code) != self.__

class Product:

    def get_EAN(self) -> EAN:
        return self.__EAN

    def get_name(self) -> str:
        return self.__name

    def __init__(self, EAN : EAN, name: str = "unspecified", price: int = -1) -> None:
        self.__EAN = EAN
        self.__name = name

class Market:

    def register_product(self, product: Product):
        self.__products.append(product)

    def __init__(self, ID: int = 0, name: str = "Unspecified") -> None:
        self.__ID = ID
        self.__products: List[Product] = []
        self.name = name

    

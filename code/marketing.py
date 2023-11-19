from typing import List, Dict

class EAN:
    # --- EAN configuration ---

    # -- Constant static variables --
    __EAN_LEN = 13
    __SUBCODE_COUNT = 4
    __COUNTRY_CODE_LEN = 2
    __MANUFACTURER_CODE_LEN = 5
    __PRODUCT_ITEM_CODE_LEN = 5
    __CHECK_DIGIT_LEN = 1

    # -- Configurable static variables --
    __DELIMITER = '-'
    

    def get_code(self):
        return self.__CODE

    def set_delimiter(self, delimiter: str):
        if not isinstance(delimiter, str):
            raise ValueError("Invalid type for delimiter, provide a string!")

        self.__DELIMITER = delimiter

    def __init__(self, code : str):
        
        if not isinstance(code, str):
            raise TypeError("Invalid parameter type of an EAN object!")

        if len(code) != (self.__EAN_LEN + 3):
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
        
class Product:
    def get_ID(self) -> int:
        return self.__ID

    def get_EAN(self) -> EAN:
        return self.__EAN

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def __init__(self, ean : EAN, ID: int = 0, name: str = "unspecified", price: int = -1) -> None:
        if not isinstance(ean, EAN) or not isinstance(ID, int) or not isinstance(name, str) or not isinstance(price, float):
            raise TypeError("Invalid type of a parameter for a Product object!")
        
        self.__ID : int = ID
        self.__EAN : EAN = ean
        self.__name : str = name
        self.__price : float = price
        
class Market:

    def get_ID(self) -> int:
        return self.__ID

    def can_register(self, product: Product) -> bool:
        
        for prod in self.__products:
            if product.get_ID() == prod.get_ID() or product.get_EAN() == prod.get_EAN():
                return False
        
        return True

    def register_product(self, product: Product):

        if not self.can_register(product=product):
            raise ValueError("Not unique Product ID or EAN!")
        
        self.__products.append(product)

    def __init__(self, ID: int = 0, name: str = "Unspecified") -> None:
        
        if not isinstance(ID, int) or not isinstance(name, str):
            raise TypeError("Invalid type of a parameter for a Market object!")

        self.__ID = ID
        self.__products: List[Product] = []
        self.name = name

    

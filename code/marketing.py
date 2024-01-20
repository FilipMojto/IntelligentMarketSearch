
import csv

class Market:
    
    def ID(self) -> int:
        return self.__ID
    
    def name(self) -> str:
        return self.__name
    
    def store_name(self) -> str:
        return self.__store_name
    
    def product_ID(self) -> ID:
        return self.__product_ID
    
    def register_product(self) -> int:
        original_val = self.__product_ID
        self.__product_ID += 1
        return original_val
        
    def categories(self) -> tuple[str]:
        return self.__categories

    def __init__(self, ID: int, name: str, store_name: str, product_ID: int, categories: tuple[str]) -> None:
        self.__ID = ID
        self.__name = name
        self.__store_name = store_name
        self.__product_ID = product_ID
        self.__categories = categories
        pass



class MarketManager:
    ID_INDEX = 0
    NAME_INDEX = ID_INDEX + 1
    STORE_NAME_INDEX = NAME_INDEX + 1
    PRODUCT_ID_INDEX = STORE_NAME_INDEX + 1
    CATEGORIES_ID_INDEX = PRODUCT_ID_INDEX + 1

    CATEGORIES_DELIMITER=';'

    def __init__(self, src_file: str) -> None:
        self.__src_file = src_file
        pass

    def get_market(self, ID: int) -> Market:
        with open(self.__src_file, 'r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

        for line in lines:
            if line[MarketManager.ID_INDEX] == str(ID):
                return Market(ID=ID,name=line[MarketManager.NAME_INDEX], store_name=line[MarketManager.STORE_NAME_INDEX], product_ID=int(line[MarketManager.PRODUCT_ID_INDEX]),
                              categories=line[MarketManager.CATEGORIES_ID_INDEX].split(MarketManager.CATEGORIES_DELIMITER))
        
        return None
    
    def update_market(self, market: Market):
        with open(self.__src_file, 'r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

        for line in lines:
            if line[self.ID_INDEX] == str(market.ID()):
                line[self.PRODUCT_ID_INDEX] = market.product_ID()
                break
        else:
            raise ValueError("Market is not officially registered!")

        with open(self.__src_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)    


    

if __name__ == "__main__":
    ha = MarketManager("../resources/markets.csv")
    market = ha.get_market(1)
    market.register_product()

    ha.update_market(market)
    print("HAHA")
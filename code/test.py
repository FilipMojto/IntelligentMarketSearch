import multiprocessing as mp
import csv
import time
from typing import List, Dict
from tkinter import *

import config_paths as cfg
import AOSS.components.script as scrip
from AOSS.structure.shopping import MarketHub, ProductCategory, Product
from AOSS.components.processing import ProductCategorizer
from AOSS.components.marrec import MarketExplorer
from AOSS.components.search import ProductMatcher
from AOSS.components.scraping.base import ProductScraper
from AOSS.gui.product_specification import ProductSpecificationMenu
from AOSS.gui.shopping_list import ShoppingListFrame

# ---- BASIC DATA PANEL - ROW 1 ---- #
  
        
# class MainView(Frame):

#     def __init__(self, *args, **kw):
#         super(MainView, self).__init__(*args, **kw)

#         self.columnconfigure(0, weight=1, minsize=250)
#         self.columnconfigure(1, weight=3, minsize=265)
#         self.rowconfigure(0, weight=1)
#         self.shopping_list = None

#         self.specification_menu = ProductSpecificationMenu(self, text="Product Specification", bg='dimgrey', 
#                                                            shopping_list_frame=self.shopping_list, font=('Arial', 18, 'bold'),
#                                                            bd=3)
#         self.specification_menu.grid(row=0, column=0, sticky="NSEW", padx=5)

#         self.shopping_list = ShoppingListFrame(self, text="Shopping List", bg='grey', font=('Arial', 18, 'bold'), labelanchor='n',
#                                                bd=3)
#         self.shopping_list.grid(row=0, column=1, sticky="NSEW", padx=5)






#output_file = "./test.csv"
from datetime import datetime

from AOSS.gui.main_view import MainView


def on_key_press(event, main_view: MainView):

    key_pressed = event.keysym

    if key_pressed == "Delete":
        main_view.market_explorer_frame.delete_product()
    #print(f"Key pressed: {key_pressed}")

def main():

    hub = MarketHub(src_file=cfg.MARKET_HUB_FILE['path'])
    hub.load_markets()
    hub.load_products()
    matcher = ProductMatcher(market_hub=hub)
    ha = matcher.match(text="rozok biely", category=None, limit=5, for_each=True)


    explorer = MarketExplorer(market_hub=hub, limit=5)
    explorer.explore(product_list=[(1, "rozok biely", None, 1)])
    

    # scraper = ProductScraper(market=hub.market(identifier=2))
    # products = scraper.scrape_categories(identifiers=(0, 1), mode='index', console_log=True)


    # start = time.time()
    # hub.load_products()
    # end = time.time()

    matcher = ProductMatcher(market_hub=hub)
    ha = matcher.match(text="hell energeticky napoj 500", markets=(3,))
    

    print("KAKA")

    # with MarketHub(src_file=cfg.MARKET_HUB_FILE['path']) as hub:
    #     scraper = ProductScraper(market=hub.market(identifier=2))
    #     products = scraper.scrape_all(console_log=True)
    #     print("haha")
        
    # #     matcher = ProductMatcher(market_hub=hub)
    # #     match_ = matcher.match(text="Hell energeticky napoj 500", markets=(2,),
    # #                            category=None, limit=5, min_match=0, sort_words=True)
    # #     market = hub.market(identifier=2)
        
    # #     for mat in match_:
    # #        print(f"{market.get_product(identifier=mat.product_ID)}: {mat.ratio}\n")


    #     # explorer = MarketExplorer(market_hub=hub)

    #     # exploration = explorer.explore(product_list=[('Travanlive mlieko polotucne 1.5',
    #     #                                               None,
    #     #                                               1), ('Hell energeticky napoj 500', None, 1)],
    #     #                                               limit=3)
        
    #     # #exploration.sort(key=lambda x : (x.market_ID, -x.products[0][1]) )

    #     # for expl in exploration:
            
    #     #     for product in expl.products:
    #     #         print(f"{product[0].name}: {product[1]}: {expl.total_price}")

        

    # app = Tk()
    # app.geometry("1295x520")
    
    # #app.resizable(width=False, height=False)
    
    # # frame = Frame(app, bg="RED")
    # # frame.grid(row=0, column=0, sticky="NSEW")

    # # frame.rowconfigure(0, weight=0)
    # # frame.columnconfigure(0, weight=0)

    # # icon = PhotoImage(file=cfg.SHOPPING_CART_ICON_2).subsample(17, 17)

    # # button = Button(frame, text="  to Cart", font=("Arial", 13), image=icon, compound='left')
    # # button.grid(row=0, column=0)



    # scroller = MainView(app, root=app)
    # scroller.grid(row=0, column=0, sticky="NSEW")

    # app.bind("<Key>", lambda event, main_view=scroller: on_key_press(event, main_view))

    # # scroller.shopping_list.insert_item("DLD", 0)
    # # scroller.shopping_list.insert_item("NIENCOO KD", 1)

    # #    scroller.insert_item("DLD", 0)
    # #scroller.insert_item("DLD", 1)
    # #scroller.insert_item("DLD", 1)
    # #scroller.insert_item("DLD", 1)
    # #scroller.insert_item("DLD", 1)
    # #scroller.insert_item("DLD", 1)
    # #scroller.insert_item("DLD", 1)


    # #specification_menu = ProductSpecificationMenu(app, text="Product Specification", font=('Arial', 18, 'bold'), bg="dimgrey")
    # #specification_menu.grid(row=0, column=0, sticky="NEW")

    # # wide_panel = Frame(app, bg='dimgrey')
    # # wide_panel.grid(row=0, column=0, sticky="NSEW")
    # # wide_panel.rowconfigure(0, weight=1, minsize=50)
    # # wide_panel.rowconfigure(1, weight=1, minsize=50)
    # # wide_panel.columnconfigure(0, weight=1)
    # # wide_panel.columnconfigure(1, weight=200)

    # # # name configuration

    # # name_frame = Frame(wide_panel, bg='grey')
    # # name_frame.grid(row=0, column=0, sticky="NSEW")
    # # name_frame.rowconfigure(0, weight=1)
    # # name_frame.columnconfigure(0, weight=1)

    # # name_frame_label = Label(name_frame, text="Enter name:", bg='dimgrey', font=("Arial", 12))
    # # name_frame_label.grid(row=0, column=0, sticky="E", padx=5)

    # # name_frame_entry = Entry(wide_panel, font=("Arial", 13))
    # # name_frame_entry.grid(row=0, column=1, sticky="NSEW", pady=3, padx=5)

    # # # amount configuration

    # # amount_frame = Frame(wide_panel, bg='grey')
    # # amount_frame.grid(row=1, column=0, sticky="NSEW")
    # # amount_frame.rowconfigure(0, weight=1)
    # # amount_frame.columnconfigure(0, weight=1)

    # # amount_frame_label = Label(amount_frame, text="Enter amount:", bg='dimgrey', font=("Arial", 12))
    # # amount_frame_label.grid(row=0, column=0, sticky="E", padx=5)

    # # amount_frame_entry = Entry(wide_panel, font=("Arial", 13))
    # # amount_frame_entry.grid(row=1, column=1, sticky="NSEW", pady=3, padx=5)

    # app.rowconfigure(0, weight=1)
    # app.columnconfigure(0, weight=1)
    # app.mainloop()
    


    # First Row Widgets

    # product_name_label = Label(basic_data_panel, text="Name: ",
    #                                 font=("Arial", 12), padx=5, bg='grey')
    # product_name_label.grid(row=0, column=0, sticky="E")

    # product_name_entry = Entry(basic_data_panel, font=('Arial', 13))
    # product_name_entry.grid(row=0, column=1, sticky="WNES", pady=0)

    # to_cart_button = Button(basic_data_panel, text="To Cart", font=("Arial", 12))
    # to_cart_button.grid(row=0, column=2, sticky="EW", padx=3)

    # # Second Row Widgets

    # product_amount_label = Label(basic_data_panel, text="Amount: ", font=("Arial", 12), padx=5, bg='grey')
    # product_amount_label.grid(row=1, column=0, sticky="E")
    
    # product_amount_entry = Entry(basic_data_panel, font=('Arial', 13))
    # product_amount_entry.grid(row=1, column=1, sticky="WNES", pady=0)

    # basic_data_panel.rowconfigure(0, weight=1)
    # basic_data_panel.rowconfigure(1, weight=1)

    # basic_data_panel.columnconfigure(0, weight=1)#, minsize=10)
    # basic_data_panel.columnconfigure(1, weight=5)#, minsize=30)
    # basic_data_panel.columnconfigure(2, weight=2)#, minsize=20)

    # app.rowconfigure(0, weight=1)
    # app.columnconfigure(0, weight=1)


    
    
    # with MarketHub(src_file=cfg.MARKET_HUB_FILE['path']) as hub:
    #     market = hub.market(1, mode='index')


    #     scraper = ProductScraper(market=market)
    #     products = scraper.scrape_categories(identifiers=(19,21, 23))

        
    #     for product, market_ID in products:
    #         print(product.__str__())



    # category_map = {}
    # with open(file=cfg.CATEGORY_MAP_FILE['path'], mode='r', encoding='utf-8') as f3:
    #     mappings = csv.DictReader(f3)
    #     for mapping in mappings:
    #         key = (mapping['name'], mapping['market_ID'])
    #         category_map[key] = mapping['ID']

    # # Read products and update query_string
    # with open(file=cfg.PRODUCT_FILE['path'], mode='r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     products = list(reader)  # Read all rows into a list

    # # Update query_string based on category mappings
    # for row in products:
    #     key = (row['query_string_ID'], row['market_ID'])
    #     if key in category_map:
    #         row['query_string_ID'] = category_map[key]

    # # Write the updated data back to the same file
    # with open(file=cfg.PRODUCT_FILE['path'], mode='w', encoding='utf-8', newline='') as f2:
    #     fieldnames = ['ID', 'name', 'normalized_name', 'price', 'approximation', 'category',
    #                 'query_string_ID', 'market_ID', 'created_at', 'updated_at']
    #     products_writer = csv.DictWriter(f2, fieldnames=fieldnames)

    #     # Write the header
    #     products_writer.writeheader()

    #     # Write the updated rows
    #     products_writer.writerows(products)




    # time_str = "2024-02-10 16:43:12"
    # datetime_object = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    
    # current = datetime.now()
    # difference = current - datetime_object
    # print(difference.total_seconds())

    # print(f"difference: {current - datetime_object}")

    # exit(0)



    # with MarketHub(src_file=cfg.MARKET_HUB_FILE['path']) as hub:
        
    #     matcher = ProductMatcher(market_hub=hub)
    #     matcher.set_subset(market_ID=2)



    #     start = time.time()
    #     mat = matcher.match(text="Clever Čerstvé vajcia M 10ks", markets=(2,), limit=5)
    #     end = time.time()
    #     print(f"Time: {end - start}")


        
    #     for m in mat:
    #         market = hub.market(identifier=m.market_ID)
    #         print(market.get_product(identifier=m.product_ID).__str__())



        
        

    #     explorer = MarketExplorer(market_hub=hub)
    #     explorations = explorer.explore(product_list=[("rozok biely", None), ("pivo zlaty bazant jahoda", None)], metric='price')

    #     market = hub.market(identifier=2)
    #     market.load_products()

    #     market.remove_products(products="Avokádo. ks")
    #     market.save_products()

    #     # market.load_products()
    #     # market.update_product(product=Product(name='Avokádo. ks', price=1.84,approximation=0,
    #     #                                       created_at="SD", updated_at="DS"))
        
    #     # start = time.time()
    #     # market.save_products()
    #     # end = time.time()
    #     # print(f"Time: {end - start}")  

    #     # start = time.time()
    #     # product = market.get_product(identifier=107962)
    #     # end = time.time()
    #     # print(f"Time: {end - start}")        
    #     # print(f"Found: {product.__str__()}")

    #     # start = time.time()
    #     # product = market.get_product_by_name(name="MaxSport Protein Nella 200 g")
    #     # end = time.time()
    #     # print(f"Time: {end - start}")
    #     # print(f"Found: {product.__str__()}")


    #     # print(len(hub.product_df().filter(hub.product_df()['market_ID'] == 2)))

    exit(0)


        # categorizer = ProductCategorizer(market_hub=hub)
        # categorizer.recategorize()

    # Create a multiprocessing Queue for communication
#     main_to_subprocess = mp.Queue()

#     count = 4

#     all_to_main = mp.Queue(maxsize=5)
#     processes: List[tuple[mp.Process, str]] = []

#     hub = MarketHub(src_file=cfg.MARKET_HUB_FILE['path'])
#     hub.load_markets()
#     hub.load_products()


#     product_df = hub.product_df()


#     for row in product_df.iter_rows(named=True):
   
#         if len(processes) < count:
#             categorizer = mp.Process(target=scrip.launch_subprocess, args=(all_to_main, row['normalized_name']))

#             categorizer.start()
#             processes.append((categorizer, row['normalized_name']))
             
#             if len(processes) != count:
#                 time.sleep(2)
#             continue

#         while True:
#             if not all_to_main.empty():
#                 response: tuple[int, ProductCategory] = all_to_main.get(block=False)

#                 if isinstance(response, tuple):
#                     pid, category = response
#                     found = False
#                     # let's find a subprocess which finished
#                     for process, product in processes:
#                         if process.pid == pid:
#                             with open(file=output_file, mode='a', encoding='utf-8', newline='') as output_f:
#                                 output_f.write(product + ': ' + category.name + '\n')

#                             process.join()
#                             processes.remove((process, product))
#                             found = True
#                             break
#                     else:
#                         print("Provided process ID not found!")
                    
#                     if found: break

#                 else:
#                     print("Unknown response type!")
            
#             # else:
#             #     time.sleep(1.5)
                


        





#     # Launch the subprocess
#     #subprocess_process = mp.Process(target=scrip.launch_subprocess, args=(main_to_subprocess,))
    
    
#     #subprocess_process.start()
#     #print(f"subprocess: {subprocess_process.pid}")

#     # Send data to the subprocess through the Queue
#     #main_to_subprocess.put("Hello from the main process!")

    



#     # Wait for the subprocess to finish
#  #   subprocess_process.join()

#     print("Main process finished.")


if __name__ == "__main__":
    main()
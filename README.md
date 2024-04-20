# AutomatedOnlineShoppingSystem
This repository contains design and implementation of automation web application which is currently under development.

Application will offer intelligent decision-making automation process whoose aim is to recommend which market to visit according to a criterium. This is mostly price.


## Repository structure

Here we explain individual subfolders of this directory.

### Design

### Code

### Docs

## Versioning

### Version 1.0.0 

#### Release Date: 20.02.2024

#### Description
The very first version of AOSS application. Contains the core of our business goal.

Note that this version is still under intensive development, therefore bugs and new features will soon appear.

#### Processes

At the start-up application launches serveral __subprocesses__:

a) __Data Scraping&Processing Process__ or __DSPP__

b) __Data Provision&Maintainence Process__ or __DPMP__

c) __Grahical User Interface Process__ or __GUIP__

#### Features

a) Fully implemented and user-friendly __Graphical User Interface__

b) Fully implemented __intelligent product search__ and __market recommendation logic__

c) __Automated updating system__ - data scraping, processing and storage


### Version 1.0.1

#### Release Date: 24.02.2024

#### Description

This version only fixes discovered bugs in the version __1.0.0__. Check features for more details.

#### Features

a) Fixed __loading screen progress reports__

b) Fixed a bug in __DPMP update synchronization__, next_product_ID for market ID wasn't saved properly 

### Version 2.0.0

#### Release Date: 03.03.2024

#### Description

New version with brand new gui and other features!

#### Features

    a) New GUI layout

        a1) MainMenu included!
        a2) New background coloring!
        a3) Settings also included!
        a3) Neater styling for several widgets, like buttons, entries, etc.!

    
    b) Improved IPC
        - GUI process now has to send signals related to Settings tuning. Therefore IPC and the signals got more detailed structure to process all various types of messages more efficiently.
    
    c) Bug fixes
        
        c1) Bugs in GUI window resizing fixed!
        c2) Rounding succession rate in MarketExplorer to 2 decimal places fixed!
        c2) Bugs in IPC, processes DPMP and GUI contained communication errors, these have been fixed!

### Version 2.1.0

#### Release Date: 08.03.2024

#### Description

Improvement of version 2.0.0 including various new functionality in GUI.

#### Features

##### Improved GUI Visualization&Usage
        
    a1) Implemented history of searched products

        - User is intelligently offered to choose from their history of searched products, therefore there is no need to search the same product again and again.
        - The history is stored persistently in a new .csv file called searched_products.

    a2) Quantity specification menu

        - This includes preventing user from entering something else than numerical data. The Entry is highlighted in red if invalid input is entered.
        - The Default quantity value is automatically set to 1.
        - User can also use increment&decrement buttons.
    
    a3) New progress reports during the loading screen

        - This includes additional update process explained further below.

##### Improved DPMP logic

    - If certain amount of data are outdated, all data will be completely scraped and updated again.

##### Bug Fixes

    - Fixed fonting when entering product quantity.

### Version 2.2.0

#### Release Date: 20.04.2024

#### Description

Brand new version which brings some new features enhancing product search.

#### Features

##### Full Refresh - reworked

    - __Full Refresh Update__ now logically updates all local data without removing them first.

##### Full Refresh Prompt Window Included

    - In this version, user is now prompted to accept or reject the Full Refresh when it is required.

##### Categorization Mode included

    - Using categories to improve the search results is now more appealling. User is now able to specify categorization mode via GUI in the form of a Combobox widget. Combobox contains following options:

    a) __Off__
    b) __Manual Mapping__
    c) __TM-based Mapping__

    User can only specify a category if any of 2 last options is selected. Manual Mapping is based on manual categorization of products which was done by author. This method still contains some imperfections. TM-based mapping is based on the __training market__ and its products. Products from training market are categorized manually, others are categorized by their similarities to products in training market. This method has generally worse search results than manual mapping.

##### Bug Fixes

    a) Deleting a product from a product list using button caused errors, as it wasnt really removed from inner list. This is now fixed








        
    


    



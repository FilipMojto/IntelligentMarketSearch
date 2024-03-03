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


    



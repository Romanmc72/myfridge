# MyFridge
The purpose of this repository is to have library that can take input from the outside world in the form of a 12 digit UPC-A and return the calorie content of a particular quantity of food idnetified by that UPC. [universal product code](https://en.wikipedia.org/wiki/Universal_Product_Code)

## Example: 
bar code for milk (Dean Foods Company REDUCED FAT MILK; NONFAT MILK; VITAMIN A PALMITATE; VITAMIN D3.)
UPC = 041900076610

will show you that 1 gallon is:
2227 calories

## How?
This repositry uses python's requests library in conjunction with the [edamam food database API](https://developer.edamam.com/food-database-api-docs).
[Sign up](https://developer.edamam.com/food-database-api) and get your own credentials for free!
They have a few other API's as well.

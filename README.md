## GTA Online Sell Limit Helper

This program will help you stay under the sell limit following 2 basic rules:
  1. You can't sell more than 2 cars in 2 hours.
  2. You can't sell more than 7 cars in 30 hours.

To use the program, simply run it using Python3.8 from the command line.
`python3 gta_sell_limit/main.py`

Additionally, you can pass a command line option to skip the intial main menu.
`python3 main.py 1` will immidiately invoke option 1 of the main menu to log that you just sold a car.
`python3 main.py 2` will immidiately invoke option 2 of the main menu to check the status of your sell limits.

The program will save data about your car sells automatically, so there's no need to run it 24/7. The data is saved
using Python's pickle module. The hidden file `.picklejar` contains your saved data; deleting this file will
cause your program to "forget" about any cars you have sold and so the limit information may be incorrect.

Contributions are unexpected but welcome. There are no contributer guidelines to follow, just write clean working code
and there will be few issues.
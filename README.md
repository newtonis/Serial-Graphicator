# Serial Graphicator
Open Source Free Serial Port Client capable of graph values that are received in **JSON format**
You can do projects with, for example, **arduino** or **microcontrollers** to transform data sent from them to computer into fancy **graphics**.

![alt tag](1456029137.92.png)


### [New] Windows executable for easy install ###

I have just added to project a new **window standalone executable**, graph.exe. In order to run the graphicator you only need to **#download all files in some directory** and then run **graph.exe**. I am not sure if currently the serial port on windows works accurately (altough the program does), but if it does not I will make it compatible with that platform soon.


### Introduction ###

Hi. I'll explain how to use this simple but useful tool. First of all you need a **python** installation complemented with the **pygame** graphics library and the **pyserial** library. You'll find plenty of ways to install them on internet and usually you **won't have problems** when installing them. After that you only need to **execute** the final **graph.py** to make the program run. Here there are some links to make you learn how to install python, pygame and pyserial

+ [How to install python - How to install py-serial](https://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector/installing-python-and-pyserial)
+ [How to install pygame] (https://www.youtube.com/watch?v=0xgn-HKzZes) 

The program should **detect the ports autonomously** and will test to check data of all of them with this **baudrates**
+ 4800
+ 9600
+ 14400
+ 19200
+ 28800
+ 38400
+ 57600
+ 115200

. If something is recived in any port then the selector of that port will be highlighted. 

You can **change the baudrate** when you enter a port, you should only click on the **port title** in the upper part of the screen.


### Which format should you use to send information to the program? ###
You must use **json** format. This means the **two commands** you can use actually are
```
"{'COM':'plot', 'name':'Plot 1','value':4564564}\n"
```
to **plot** a point in the **graph**, where the 4564564 is the value to graph in that instant, and 'Plot 1' the name of the graph associated with it (the program autodetects when there is a new signal so no need of initial signal, just **update signals**). And remeber to set a '\n' (**end of line**) character after each signal sent because otherwise the program won't graph anything as it **will wait until the '\n' arrives** to divide the **signal**. If you want to **set the color** of the signal (rather than a random number) you can add a "color":(r,g,b) parameter altough I haven't tested yet it should work.

And the other **command** is 
```
"{'COM':'line','value':'This is a test of Serial Graphicator'}\n"
```
You should use this command to **send words** to be shown on the console of the program. Remember to use the **end of line** character also.

**Warning**: As the program is beta version it can crash suddenly if you send commands that do not respect the format. Please avoid doing that, only send messages that apply to the rules


**Report any bug** to ariel.nowik@gmail.com. This program is **totally free** for all so feel free to use it, modify it or send feedback. Good Luck guys!


### Screenshots ###
![alt tag](1456028622.43.png)
![alt tag](1456028628.79.png)
![alt tag](1456028631.55.png)
![alt tag](1456028638.35.png)
![alt tag](1456028641.77.png)
![alt tag](1456028649.37.png)
![alt tag](1456028654.02.png)




### Bonus ###

Easy and fast **instalation** and **run** for linux with commands (only *Linux*!). If you type these commands (and there are no **errors** the program will be installed and will be executed

```
sudo apt-get install python-pygame
sudo apt-get install git
git clone https://github.com/newtonis/SerialGraphicator/
cd SerialGraphicator
python graph.py
```

### Advice for linux ###

In **linux** sometimes the serial port is **blocked by admin** by default (what will make the program throw an exception because of permisions). To solve this you can execute
```
sudo chmod -R 777 /dev
```

or more easily you can just **run the program on admin** mode
instead of
```
python graph.py
```
you **type**
```
sudo python graph.py
```

# SerialGraphicator
Open Source Free Serial Port Client capable of graph values that are received in JSON format
You can do projects with arduino or microcontrollers to transform data sent from them to computer into fancy graphics

Hi. I'll explain how to use this simple but useful tool. First of all you need a python installation complemented with the pygame graphics library and the pyserial library. You'll find plenty of ways to install them on internet and usually you won't have problems when installing them. After that you only need to execute the final graph.py to make the program run.


The program should detect the ports autonomously and will test to check data of all of them with this baudrates [4800 ,9600 , 14400 , 19200 , 28800 , 38400, 57600 , 115200]. If something is recived in any port then the selector of that port will be highlighted. 

You can change the baudrate when you enter a port, you should only click on the port title in the upper part of the screen.


<h2>Which format should you use to send information to the program? <\h2>
You must use json format. This means the two commands you can use actually are
```
"{'COM':'plot', 'name':'Plot 1','value':4564564}\n"
```
to plot a point in the graph, where the 4564564 is the value to graph in that instant, and 'Plot 1' the name of the graph associated with it (the program autodetects when there is a new signal so no need of initial signal, just update signals). And remeber to set a '\n' (end of line) character after each signal sent because otherwise the program won't graph anything as it will wait until the '\n' arrives to divide the signal

And the other command is 
```
"{'COM':'line','value':'This is a test of Serial Graphicator'}\n"
```
You should use this command to sent words to be shown on the console of the program. Remember to use the end of line character also. I think there are no other advises.



Report any bug to ariel.nowik@gmail.com. This program is totally free for all so feel free to use it, modify it or send feedback. Good Luck guys!



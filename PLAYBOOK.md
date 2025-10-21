## COS 460/540 - Computer Networks
# Project 2: HTTP Server

# Deiby Wu

This project is written in Python on MacOS.

## How to compile

Since it's Python code, user is not required to compile anything, just make sure to have Python installed.

## How to run

First, make sure you are in the folder containing all the source codes. From the server side, run `python3 web_server.py <port_number> <folder_path>` From the client side, run telnet localhost <port_number>

e.g. From server side: `python3 web_server.py 8888 www`
e.g. From client side: `telnet localhost 8888`

* <port_number> has to be the same for both, the clients and the server side.
* Depending of your python settings, you may have to run `python web_server.py <port_number>`

## My experience with this project

First thing I did was to reuse some of my code from the first project, from there I also rely on this two sources: (https://stackoverflow.com/questions/32623756/how-to-get-input-from-html-using-python-socket) (https://www.youtube.com/watch?v=Hncp0mPfUvk) to have a better idea of how to start this assignment. I will say the most difficult thing about this project was the headers. I initially did not do headers and just did socket.send(html file content), which kind of worked, but it was not what the assignment was looking for. Everything made more sense after figuring out how the headers had to be formatted.

At one point I redo most of my code because of the way I setup the thread system. I used Class to handle request just like in my first project, but it just got overcomplicated, so I instead use functions to handle threads. After finishing most of the requirements, I focused on replicating the behavior of the original http.server that Python already have, like forcing two \r\n\r\n, or making sure user type GET at first. There are still more use cases that has to be handle, but I believe is not part of this assignment.

I learned about mimetypes from here: (https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/). I basically understood how to properly format the different file types, and create my own custom function to handle all the file types in the project (which are only 3).

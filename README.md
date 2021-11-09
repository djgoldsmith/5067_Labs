# Sandbox Based CTF Challenges

 - Cuz the wizemen came across the desert innit :p
 
All of these levels are some form of python based sandbox escape.
We will modify the filtering / Amount of information that is given to the user.
 

## Levels

### Easy

  - Pretty much a full python interpreter.
  - Although everything needs to be a one liner.


### Moderate

 - Try thinking of a way of doing one of the nifty, Pre-Compiled exploits.
 

### Hard

 - Lets do a full blown sandbox...
 - Kill the Globals and filter out some of the "Bad" inputs.






## Notes

Base the code on https://github.com/cs01/pyxtermjs

We can instal node modules locally using npm-install <whatever>

Thus we do ```npm install xterm```


### Xterm notes

Getting input 

the ```onData``` command does things in a character by character basis

https://www.linkedin.com/pulse/xtermjs-local-echo-ioannis-charalampidis

https://flask-socketio.readthedocs.io/en/latest/

We could probably do something nifty with hooks for the various control sequences

https://xtermjs.org/docs/guides/hooks/



https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes#dissecting-functions
https://ctf-wiki.github.io/ctf-wiki/pwn/linux/sandbox/python-sandbox-escape/

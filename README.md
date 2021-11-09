# Comsec 12 Days CTF:  SSTI Style challenges

Three SSTI based challenges to thrill and delight.

NOTE:  I can easily make Boot 2 Root.

## Levels

 - [x] Easy.  Basic Template includes,  we will stick some limited filtering on it just for fun
   - Don't really care about shell execution, so we can leave that there
 - [x] Moderate:  Milk and Cookies
    - As Easy, but we need to set some cookies to get a decent level of code execution
	- [X] Leak the Source and use the Key to modify cookies
    - [X] Blind SSTI for the injection
	- [X] Flag is not called flag, so they need to search for it.
 - Hard:  Add a decent level of Python Jail
    - All of the Above.  Set a cookie using Flask Encrypted cookies
	- Kill Global
    - Bypass Regexp 
    - Win

## TODO

  - [ ] Add proper flags for Each level
  - [ ] Proper Key for the Cookies
  - [ ] Think about changing Intermediate for Hard (And adding a Node one instead)
  - [ ] Check Debug will come up through dirbuster

## Base Image

 - Python with Flask / Jinja and friends.
 
Build this with 

```
docker build -t cueh/flask .
```

Run with 

```
docker run --rm -p 5000:5000 cueh/flask
```


You can checkout the Easy dir on how we expand this out.

Update Dockerfile

```
FROM cueh/flask

WORKDIR /opt
ADD app.py /opt  #Do Whatever we want to do here
```

### Compose Files

Use [Easy for reference](Easy)

Two Versions

 - [Standard docker-compose](Easy/docker-compose.yml)  Standard Compose file
 - [Testing](Easy/compose-devel.yml)  Does everything in a volume for testing



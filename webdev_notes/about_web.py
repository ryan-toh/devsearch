"""

from old python course
# HOW THE WEB WORKS

    There are multiple protocols that PCs use to talk to each other
    # Most Common: HTML, Email Protocols (IMAP, SMTP, POP3)

    Purpose: To retrieve html files, images, documents, etc
    Extended to handle data + documents (RSS, web services)

    Making an HTTP request
    example:
    "GET http://data.pr4e.org/page1.htm HTTP/1.0"
    - connects to the server, requesting the document "page1.html"

    you can include headers: eg system agent, preferred lang, etc

    HTTP response data

    HTTP/1.1 200 OK - "A file was found, no error"
    Date:
    Server:
    Last-Modified:
    Content-Type:

    The browser uses these data to render a template to show the user

    TCP Connections/Sockets

    - A port number is like a phone number, allows PCs to talk to each other
    "An endpoint of a bidirectional inter-process communication flow across an
    internet protocol based compouter network, such as the internet"

    - Allows multiple apps to coexist on the same server (since you have diff port nos)

    # HTML (Hypertext Markup Language)

    - a way of marking up text to indicate that some text is different from other text,
    using tags, eg. <p></p> <body></body>
    current generation: HTML5

# HTML - Structure

    <!DOCTYPE html>
    <html>
        # metadata
        <head>
        </head>
        # displayable content
        <body>
        </body>
    </html>

    whitespace and line wrapping is handled (usually) by the browser,
    you do not ned to add them yourself.

    closing tags are required for each html tag less self closing tags
    eg. <img src=""/>

    printing html special characters
    "<" -- &lt
    ">" -- &gt
    "&" -- &amp
    etc...

    # html comments
    - start with "!" and there are two dashes "--" between the comment
    <!-- insert your comment here -->

    # html links
    <a href="www.yourwebsite.com/page2.htm">Link Name</a
    "a" stands for anchor
    "href" stands for hypertext reference

    the website in question can also be accessed with a relative link
    if the file is in the same directory as the previous file on the server.

    # html lists
    eg.
    <ul>
        <li>
        ItemName
        </li>
    </ul>

    a list with a single element

    # html tables
    eg.
    <table>
    <tr>
            <th>
            Table header here
            </th>
        </tr>
        <tr>
            <td>
            Table data here
            </td>
        </tr>
    </table>

    a table with a single column and two rows for the header and data

# CSS (cascading style sheets)
    the syntax is very different from html,

    example syntax.

    body {
        font-family: arial, sans-serif;
        font-size: 100%;

    }

    selector - body
    property - font-family & font-size
    value - arial, sans-serif; font-size

    # How to apply CSS to a html document
    - inline, using style=attribute in the html tag itself
    - embedded stylesheet in the <head> of the document, using <style></style>
    - An external stylesheet in a seperate file, that is in the header of the html file eg.
    <link type="text/css" rel="stylesheet" href="rules.css">

    css will render the most specific css property (ie if you add a monospaced attribute into a specific tag,
    it will override the earlier tag (eg font-family=arial) set at the header).

    # HTML span and div tags

    span does not have any styling
    div is a block tag that also does not have any styling,
    it is for organising your html file (divs can be nested too)

    <p></p> creates blank spaces around the element

    <div></div> is just a block enclosing the element

    you can assign id's and classes to each div or span tag (so you can target and customise them)

    example syntax

    html file
    <div id="first-paragraph">
        Hello, world
    </div>

    <div class="second-paragraph bye">
        <p>
        Hello, bye!
        </p>
    </div>

    css file
    # first-paragraph {
        font-family: monospace;
    }

    .second-paragraph {
        color: green;
    }

    .bye {
        margin-left: 20px;
        margin-right: 20px;s2a
    }

    "#" represents id's, where ids are unique
    "." represents classes, where a class can be used on multiple tags

    you can do "nested" tags, eg.

    .second-paragraph p {
        background-color: yellow;
    }

    some helpful css attributes

    style="float:right/left" - allows you to shift an element to a corner of a page

    style="margin": 1em - include a 5px border around an element (the width of the letter "m")

    <bonus> <br clear="all"> - a html attribute, but allows you to clear
    the hanging wrap before a new element is added (the empty space at the bottom left or right
    due to the different length of two elements side by side)

    there are 16 default HTML colors (aqua, black, blue, fuchsia, gray, green, lime, maroon, gray...)
    that you can use by name directly
"""
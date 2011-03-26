import sys

wikiURL = "http://code.google.com/p/jee6-cdi/wiki/"
f = file(sys.argv[1])
lines = f.readlines()

#Looks for a signature file in the local dir
sig=file("signature.htm").read()

def processParts(parts):
    lst = []
    parts = parts.split()
    for part in parts:
        lst.append(processPart(part))

    return " ".join(lst)

def processPart(part):
    # This is screaming to be fixed, quick and dirty is not ridiculous. I need to parse things better.
    if part.startswith("*`") and part.endswith("`*"):
        part = part[2:-2]
        return "<b><code>%s</code></b>" % part
    elif part.startswith("*`") and part.endswith("`*,"):
        part = part[2:-3]
        return "<b><code>%s</code></b>," % part
    elif part.startswith("*`") and part.endswith("`*;"):
        part = part[2:-3]
        return "<b><code>%s</code></b>;" % part
    elif part.startswith("*`") and part.endswith("`*:"):
        part = part[2:-3]
        return "<b><code>%s</code></b>:" % part
    elif part.startswith("@*`") and part.endswith("`*"):
        part = part[3:-2]
        return "<b><code>%s</code></b>" % part
    elif part.startswith("\"*`") and part.endswith("`*\""):
        part = part[3:-3]
        return '"<b><code>%s</code></b>"' % part
    elif part.startswith("*`") and part.endswith("`*'s"):
        part = part[2:-4]
        return "<b><code>%s</code></b>'s" % part
    elif part.startswith("*`") and part.endswith("`*."):
        part = part[2:-3]
        return "<b><code>%s</code></b>." % part


    elif part.startswith("*") and part.endswith("*"):
        part = part[1:-1]
        return "<b>%s</b>" % part
    elif part.startswith("*") and part.endswith("*."):
        part = part[1:-2]
        return "<b>%s</b>." % part
    elif part.startswith("*") and part.endswith("*,"):
        part = part[1:-2]
        return "<b>%s</b>," % part
    elif part.startswith("*") and part.endswith("*'s"):
        part = part[1:-3]
        return "<b>%s</b>'s" % part

    elif part.startswith("`") and part.endswith("`"):
        part = part[1:-1]
        return "<code>%s</code>" % part
    elif part.startswith("`") and part.endswith("`."):
        part = part[1:-2]
        return "<code>%s</code>." % part
    elif part.startswith("`") and part.endswith("`,"):
        part = part[1:-2]
        return "<code>%s</code>," % part
    elif part.startswith("`") and part.endswith("`'s"):
        part = part[1:-3]
        return "<code>%s</code>'s" % part

    else:
        return part


def processURL(url) :
    url[-1] = url[-1][:-1]
    theURL = url[0][1:]
    if not theURL.startswith("http://") and not theURL.startswith("https://"):
        theURL = "%s%s" % (wikiURL, theURL)

    body = " ".join( url[1:] )
    sys.stdout.write ( " <a href='%s'>%s</a>" % ( theURL, body ))


inCode=0
inOL=0
inUL=0
cl=0

for line in lines:

    if line[0:3] == "{{{":
        inCode=1
        print "\n<pre class='java'>"
        continue
    if line[0:3] == "}}}":
        inCode=0
        print "</pre>\n"
        cl = cl +1
        if cl % 7 == 0:
            print sig
            print "<!--pagebreak-->"
        continue
    if inCode:
        print line,
        continue

    line = line.strip()
    if line=="":
        if inUL:
            print "</ul>"
            inUL=0
        elif inOL:
            print "</ol>"
            inOL=0
        else:
            #print "<br />"
            pass
        continue

    if line[0:4] == "====":
        print "<br />"
        print "<br />"
        print "<h5>%s</h5>" % processParts(line[4:-4])
        print "<br />"
        continue
    if line[0:3] == "===":
        print "<br />"
        print "<br />"
        print "<h4>%s</h4>" % processParts(line[3:-3])
        print "<br />"
        continue
    if line[0:2] == "==":
        print "<br />"
        print "<br />"
        print "<h3>%s</h3>" % processParts(line[2:-2])
        print "<br />"
        continue
    if line[0:1] == "=":
        print "<br />"
        print "<br />"
        print "<h2>%s</h2>" % processParts(line[1:-1])
        print "<br />"
        continue

    if line.startswith("# ") and not inOL:
        inOL=1
        print "<ol>"

    if line.startswith("* ") and not inUL:
        inUL=1
        print "<ul>"

    if line.startswith("# ") and inOL:
        line = line[1:]
        sys.stdout.write("<li>")

    if line.startswith("* ") and inUL:
        line = line[1:]
        sys.stdout.write("<li>")



    parts = line.split()
    inURL = 0
    url = []
    for part in parts:
        if part[-1]=="]":
            inURL = 0
            url.append(part)
            processURL(url)
#            print "END=%s" % url,
            print "",
            continue
        if part.endswith("],"):
            inURL = 0
            url.append(part[:-1])
            processURL(url)
            print ",",
#            print "END WITH COMMA=%s" % url,
            continue
        if part.endswith("]."):
            inURL = 0
            url.append(part[:-1])
            processURL(url)
            print ".",
            continue
        if inURL == 1:
            url.append(part)
#            print "PART=%s" % part,
            continue
        if part[0:1]=="[":
            url = []
            inURL = 1
            url.append(part)
#            print "START=%s" % part,
            continue            
        if not inURL:
            print processPart(part),
    if inOL:
        sys.stdout.write("</li>")

    if inUL:
        sys.stdout.write("</li>")
    print ""

print "There are %d code listings in this article" % cl

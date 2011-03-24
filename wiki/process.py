import sys

#f = file("DependencyInjectionAnIntroductoryTutorial.wiki")
f = file("test.wiki")
lines = f.readlines()

def processURL(url) :
    url[-1] = url[-1][:-1]
    sys.stdout.write ( " <a href='%s'>%s</a>" % ( url[0][1:], " ".join( url[1:] ) ))



inCode=0
inOL=0
inUL=0

for line in lines:

    if line[0:3] == "{{{":
        inCode=1
        print "\n<pre class='java'>"
        continue
    if line[0:3] == "}}}":
        inCode=0
        print "</pre>\n"
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
        print "<h5>%s</h5>" % line[4:-4]
        print "<br />"
        continue
    if line[0:3] == "===":
        print "<br />"
        print "<h4>%s</h4>" % line[3:-3]
        print "<br />"
        continue
    if line[0:2] == "==":
        print "<br />"
        print "<h3>%s</h3>" % line[2:-2]
        print "<br />"
        continue
    if line[0:1] == "=":
        print "<br />"
        print "<h2>%s</h2>" % line[1:-1]
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
            if part.startswith("*`") and part.endswith("`*"):
                part = part[2:-2]
                print "<b><code>%s</code></b>" % part,
            elif part.startswith("*`") and part.endswith("`*,"):
                part = part[2:-3]
                print "<b><code>%s</code></b>," % part,
            elif part.startswith("*`") and part.endswith("`*'s"):
                part = part[2:-4]
                print "<b><code>%s</code></b>'s" % part,

            else:
                print part,
    if inOL:
        sys.stdout.write("</li>")

    if inUL:
        sys.stdout.write("</li>")
    print ""

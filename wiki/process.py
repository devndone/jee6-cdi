import sys
import re

wikiURL = "http://code.google.com/p/jee6-cdi/wiki/"
f = file(sys.argv[1])
lines = f.readlines()

pagebreak = True
if len (sys.argv) >= 3:
    if sys.argv[2]=="False":pagebreak = False
    else: pagebreak = True

blog = False
if len (sys.argv) >= 4:
    if sys.argv[3]=="False":blog = False
    else: blog  = True

respectLineBreaks = True
if len (sys.argv) >= 5:
    if sys.argv[4]=="False":respectLineBreaks = False
    else: respectLineBreaks  = True
    

#Looks for a signature file in the local dir
sig=file("signature.htm").read()

class MatchReplace:
    def __init__(self, pattern, template):
        self.pattern = re.compile(pattern)
        self.template = template
    def processLine(self, line):
        while True:
            match = self.pattern.search(line)
            if not match:
                break
            line = line.replace(match.group(0), self.template % match.group(2))
        return line

boldMR = MatchReplace(r"""(\*)([\w.,!?;"'\-/{} @]+)(\*)""", "<b>%s</b>")
codeMR = MatchReplace(r"""(`)([\w.,!?;"'\-/{} @]+)(`)""", "<code>%s</code>")
boldCodeMR = MatchReplace(r"""(\*`)([\w.,!?;"'\-/{} @]+)(`\*)""", "<b><code>%s</code></b>")

matcherReplacers = [boldCodeMR, boldMR, codeMR]

def processLine(line):
    for mr in matcherReplacers:
        line = mr.processLine(line)
    return line

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
codeListingsPerPage=10

for line in lines:

    if line[0:3] == "{{{":
        inCode=1
        if not blog:
            print "\n<pre class='java'>"
        else:
            print "\n<pre class='brush: java'>"
        continue
    if line[0:3] == "}}}":
        inCode=0
        print "</pre>\n"
        cl = cl +1
        if pagebreak and cl % codeListingsPerPage  == 0:
            print "<b>Continue reading...</b> Click on the navigation links below the author bio to read the other pages of this article."
            print sig
            print "<!--pagebreak-->"
        continue
    if inCode:
        line = line.replace("<", "&lt;").replace(">","&gt;")
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
        print "<h5>%s</h5>" % processLine(line[4:-4])
        print "<br />"
        continue
    if line[0:3] == "===":
        print "<br />"
        print "<br />"
        print "<h4>%s</h4>" % processLine(line[3:-3])
        print "<br />"
        continue
    if line[0:2] == "==":
        print "<br />"
        print "<br />"
        print "<h3>%s</h3>" % processLine(line[2:-2])
        print "<br />"
        continue
    if line[0:1] == "=":
        print "<br />"
        print "<br />"
        print "<h2>%s</h2>" % processLine(line[1:-1])
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

    line = processLine(line)

    parts = line.split()
    inURL = 0
    url = []
    for part in parts:
        if part[-1]=="]":
            inURL = 0
            url.append(part)
            processURL(url)
            print "",
            continue
        if part.endswith("],"):
            inURL = 0
            url.append(part[:-1])
            processURL(url)
            print ",",
            continue
        if part.endswith("]."):
            inURL = 0
            url.append(part[:-1])
            processURL(url)
            print ".",
            continue
        if inURL == 1:
            url.append(part)
            continue
        if part[0:1]=="[":
            url = []
            inURL = 1
            url.append(part)
            continue            
        if not inURL:
            print processLine(part),
    if inOL:
        sys.stdout.write("</li>")

    if inUL:
        sys.stdout.write("</li>")
    if respectLineBreaks: 
        print ""

print "There are %d code listings in this article" % cl

import re


gSimplifySpaces = re.compile("  +")
def simplifySpaces(line):
    line = gSimplifySpaces.subn(" ", line)[0]
    line = line.strip()
    return line


gKeywordRe=re.compile("-p *([^ =]+)(?:=(\d+))?")
def parseTaskLine(line):
    """Parse line of form:
    project some text -p keyword1 -p keyword2=12 some other text
    returns a tuple of ("project", "some text some other text", {keyword1: None, keyword2:12})"""
    def fixKeywordValue(value):
        if value != '':
            return int(value)
        else:
            return None

    # First extract project name
    line = simplifySpaces(line)
    project, line = line.split(" ", 1)

    # Extract keywords
    matches = gKeywordRe.findall(line)
    matches = [(x, fixKeywordValue(y)) for x,y in matches]
    keywordDict = dict(matches)

    # Erase keywords
    line = gKeywordRe.subn("", line)[0]
    line = simplifySpaces(line)
    return project, line, keywordDict


def createTaskLine(projectName, title, keywordDict):
    tokens = []
    for keywordName, value in keywordDict.items():
        tokens.append("-p")
        if value:
            tokens.append(keywordName + "=" + str(value))
        else:
            tokens.append(keywordName)

    tokens.insert(0, projectName)

    tokens.append(title)
    return " ".join(tokens)


def extractYagtdField(line, field):
    textParts = []
    regExp = re.compile(field + "([^ ]+)")
    lst = regExp.findall(line)
    if len(lst) == 1:
        field = lst[0]
    elif len(lst) == 0:
        field = None
    else:
        raise Exception("Multiple '%s' fields found" % field)

    line = regExp.subn("", line)[0]
    line = simplifySpaces(line)
    return line, field
# vi: ts=4 sw=4 et
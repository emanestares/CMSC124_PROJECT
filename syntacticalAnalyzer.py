import re

grammarRegex = {
  "HAI": "^HAI (\d+.\d)*",
  "I HAS A": "^I HAS A \w+(\w|\d)* (ITZ (-*\d+|-*\d+\.\d+|WIN|FAIL|\".*\"))?",
  "BIGGR OF": "^BIGGR OF (-*\d+|-*\d+\.\d+) AN (-*\d+|-*\d+\.\d+)",
  "SMALLR OF": "^SMALLR OF (-*\d+|-*\d+\.\d+) AN (-*\d+|-*\d+\.\d+)",
  "SUM OF": "^SUM OF (-*\d+|-*\d+\.\d+) AN (-*\d+|-*\d+\.\d+)",
  "BOTH SAEM": "^BOTH SAEM (-*\d+|-*\d+\.\d+) AN (-*\d+|-*\d+\.\d+)",
  "VISIBLE": "^VISIBLE .+",
  "OBTW": "^OBTW .*",
  "TLDR": "^TLDR",
  "BTW": "^BTW .*",
  "HOW IZ I": "^HOW IZ I \w+(\w*|\d*)* (YR \w+)+",
  "FOUND YR": "^FOUND YR .+",
  "IF U SAY SO": "^IF U SAY SO",
  "KTHXBYE": "^KTHXBYE",
  "GIMMEH": "GIMMEH \w+(\w|\d)*",
  "VARIABLE": "\w+(\w|\d)* R (-*\d+|-*\d+\.\d+|WIN|FAIL|\".*\"|\w+(\w|\d)*)"
}

# GRAMMAR

def analyze(lexemesList):
  line = ""
  keyWord = ""
  lineNumber = 1

  # TODO: for testing; should be removed
  # print(lexemesList)
  print("\n[!] Analyze Module Output: ")

  if lexemesList[0][0] != "HAI":
    print("Syntax Error in line " + str(lineNumber) + " : Start of code not found.\n")

    # checks for end of code keyword, prompts user if none found
  if lexemesList[-1][0] != "KTHXBYE":
    print("Syntax Error " + str(lineNumber) + " : End of code not found.\n")
  
  for lexeme in lexemesList:    
    if line == "":
      keyWord = lexeme

    if lexeme != ['\n', 'Line Break']:
      line += lexeme[0]
      line += " "

    else:
      print("["+str(lineNumber) + "]" + line)
      if keyWord[1] == "Variable Identifier":
        keyWord = ["VARIABLE"]

      if line.strip() == "":
        lineNumber+= 1
        continue
      
      if re.search(grammarRegex[keyWord[0]], line) == None:
        print("fail:" + line)
        print("error in line " + str(lineNumber))
      else:
        print("passed:" + line)

      line = ""
      lineNumber+= 1
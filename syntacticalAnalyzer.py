class node:
  def __init__(self, val, child):
    self.val = val
    self.child = child

grammar = {
  "Program": ["Start of Program"],
  "Start of Program": ["Statement"],
  "Statement": [["Statement", "Statement Repeater"], ["Print"], ["Input"], ["Comment"], ["Cond"], ["Cast"], ["vardecportion"], ["concatentaion"]], 
  "End": ["End of Program"]
}

while(True):

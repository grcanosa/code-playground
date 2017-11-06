
Differences between call by name and call by value
---------------------------------------------------

CBN: Evaluates expression only when needed
CBV: Evaluates expression first always.

Scala is CBV by default, however you can force a CBN in a parameter using =>

For example:
def callOnce(x: Int, y: Int) is CBV in its two parameters
def callOnce(x: Int, y: => Int) is CBN in its second parameter. :
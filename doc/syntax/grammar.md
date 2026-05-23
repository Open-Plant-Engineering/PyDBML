# Grammar Specification

This document defines the formal grammar of the PyDBML language.

The grammar is expressed in an EBNF-like notation.

---

## 1. Lexical Elements

### 1.1 Identifier

```

identifier ::= letter { letter | digit | "\_" }

```

---

### 1.2 Variable

```

local\_var  ::= "!" identifier
global\_var ::= "!!" identifier

```

---

### 1.3 Literal

```

number  ::= digit { digit } \[ "." digit { digit } ]
string  ::= "|" { character } "|" | "'" { character } "'"
boolean ::= "true" | "false"

```

---

## 2. Program Structure

```

program ::= { statement }

```

---

## 3. Statements

```

statement ::=
assignment
\| print\_stmt
\| import\_stmt
\| if\_stmt
\| do\_stmt
\| function\_def
\| return\_stmt
\| break\_stmt
\| skip\_stmt
\| handle\_stmt
\| label\_stmt
\| golabel\_stmt
\| expression\_stmt

```

---

## 4. Import Statement

```

import\_stmt ::=
"import" "|" identifier "|"              (\* file/plugin import *)
\| "import" "module" identifier             (* Python module import *)
\| "import" "module" "|" identifier "|"     (* optional module pipe syntax \*)

```

---

## 5. Assignment

```

assignment ::= variable "=" expression
variable   ::= local\_var | global\_var

```

---

## 6. Print Statement

```

print\_stmt ::= "$P" expression

```

---

## 7. If Statement

```

if\_stmt ::=
"if" "(" expression ")" "then"
block
{ "elseif" "(" expression ")" "then"
block
}
\[ "else"
block
]
"endif"

```

---

## 8. Do Loop

```

do\_stmt ::=
"do"
(
range\_clause
\| indices\_clause
\| values\_clause
\| ε
)
block
"enddo"

```

---

### 8.1 Range Clause

```

range\_clause ::= variable "from" expression "to" expression

```

---

### 8.2 Indices Clause

```

indices\_clause ::= variable "indices" expression

```

---

### 8.3 Values Clause

```

values\_clause ::= variable "values" expression

```

---

## 9. Function Definition

```

function\_def ::=
"define" "function" global\_var "(" \[param\_list] ")" "is" type
block
"endfunction"

```

---

### 9.1 Parameter List

```

param\_list ::= param { "," param }
param      ::= identifier \[ "is" type ]

```

---

### 9.2 Function Call

```

function\_call ::= global\_var "(" \[arg\_list] ")"
arg\_list      ::= expression { "," expression }

```

---

## 10. Return Statement

```

return\_stmt ::= "return" expression

```

---

## 11. Skip / Break

```

break\_stmt ::= "break"
skip\_stmt  ::= "skipif" "(" expression ")"

```

---

## 12. Expressions

```

expression ::= logical\_or

```

---

### 12.1 Logical OR

```

logical\_or ::= logical\_and { "OR" logical\_and }

```

---

### 12.2 Logical AND

```

logical\_and ::= equality { "AND" equality }

```

---

### 12.3 Equality

```

equality ::= comparison { ( "==" | "!=" ) comparison }

```

---

### 12.4 Comparison

```

comparison ::= term { ( ">" | "<" | ">=" | "<=" ) term }

```

---

### 12.5 Term

```

term ::= factor { ( "+" | "-" ) factor }

```

---

### 12.6 Factor

```

factor ::= unary { ( "\*" | "/" ) unary }

```

---

### 12.7 Unary

```

unary ::= \[ "NOT" ] postfix

```

---

### 12.8 Postfix (IMPORTANT ADDITION ✅)

Supports method calls, attribute access, and indexing.

```

postfix ::= primary { postfix\_op }

postfix\_op ::=
"." identifier "(" \[arg\_list] ")"   (\* method call *)
\| "." identifier                      (* attribute access *)
\| "\[" expression "]"                  (* index access \*)

```

---

### 12.9 Primary

```

primary ::=
number
\| string
\| boolean
\| variable
\| function\_call
\| object\_creation
\| iftrue\_expr
\| "(" expression ")"

```

---

## 13. Object Creation

```

object\_creation ::= "object" identifier "(" \[arg\_list] ")"

```

---

## 14. Expression Statement

```

expression\_stmt ::= expression

```

---

## 15. Block

```

block ::= { statement }

```

---

## 16. Types

```

type ::= "real" | "string" | "boolean" | "array" | "object"

```

---

## 17. Special Expressions

### IfTrue Expression

```

iftrue\_expr ::= "iftrue" "(" expression "," expression "," expression ")"

```

---

## 18. Error Handling

```

handle\_stmt ::=
"HANDLE" "(" code\_list ")"
block
{ "ELSEHANDLE" condition block }
"ENDHANDLE"

```

---

## 19. Label and Jump

```

label\_stmt   ::= "label" identifier
golabel\_stmt ::= "golabel" identifier

```

---

## 20. Notes

1. Grammar is implemented using recursive-descent parsing.
2. Expressions follow defined operator precedence rules.
3. Function execution introduces a new scope.
4. Variables are resolved dynamically at runtime.
5. Identifiers and method names are **case-insensitive**.
6. Method calls follow runtime resolution order:
   - built-in
   - PyDBML object
   - plugin
   - Python method fallback
7. Object creation supports:
   - PyDBML objects
   - plugin classes
   - Python functions and classes

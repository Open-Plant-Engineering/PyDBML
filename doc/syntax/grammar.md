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
string  ::= '"' { character } '"' | "'" { character } "'"
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
\| print        \_stmt
\| if           \_stmt
\| do           \_stmt
\| function     \_def
\| return       \_stmt
\| break        \_stmt
\| skip         \_stmt
\| expression   \_stmt

```

---

## 4. Assignment

```

assignment ::= variable "=" expression
variable   ::= local\_var | global\_var

```

---

## 5. Print Statement

```

print\_stmt ::= "$P" expression

```

---

## 6. If Statement

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

## 7. Do Loop

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

### 7.1 Range Clause

```

range\_clause ::= variable "from" expression "to" expression

```

---

### 7.2 Indices Clause

```

indices\_clause ::= variable "indices" expression

```

---

### 7.3 Values Clause

```

values\_clause ::= variable "values" expression

```

---

## 8. Function Definition

```

function\_def ::=
"define" "function" global\_var "(" \[param\_list] ")" "is" type
block
"endfunction"

```

---

### 8.1 Parameter List

```

param\_list ::= param { "," param }
param      ::= identifier

```

---

### 8.2 Function Call

```

function\_call ::= global\_var "(" \[arg\_list] ")"
arg\_list      ::= expression { "," expression }

```

---

## 9. Return Statement

```

return\_stmt ::= "return" expression

```

---

## 10. Skip / Break

```

break\_stmt ::= "break"

skip\_stmt  ::= "skipif" "(" expression ")"

```

---

## 11. Expressions

```

expression ::= logical\_or

```

---

### 11.1 Logical OR

```

logical\_or ::= logical\_and { "OR" logical\_and }

```

---

### 11.2 Logical AND

```

logical\_and ::= equality { "AND" equality }

```

---

### 11.3 Equality

```

equality ::= comparison { ( "==" | "!=" ) comparison }

```

---

### 11.4 Comparison

```

comparison ::= term { ( ">" | "<" | ">=" | "<=" ) term }

```

---

### 11.5 Term

```

term ::= factor { ( "+" | "-" ) factor }

```

---

### 11.6 Factor

```

factor ::= unary { ( "\*" | "/" ) unary }

```

---

### 11.7 Unary

```

unary ::= \[ "NOT" ] primary

```

---

### 11.8 Primary

```

primary ::=
number
\| string
\| boolean
\| variable
\| function\_call
\| object\_creation
\| "(" expression ")"

```

---

## 12. Object Creation

```

object\_creation ::= "object" identifier "(" \[arg\_list] ")"

```

---

## 13. Object Access

```

object\_access ::= primary "." identifier

```

---

## 14. Index Access

```

index\_access ::= primary "\[" expression "]"

```

---

## 15. Expression Statement

```

expression\_stmt ::= expression

```

---

## 16. Block

```

block ::= { statement }

```

---

## 17. Types

```

type ::= "real" | "string" | "boolean" | "array" | "object"

```

---

## 18. Special Expressions

### IfTrue Expression

```

iftrue\_expr ::= "iftrue" "(" expression "," expression "," expression ")"

```

---

## 19. Error Handling

```

handle\_stmt ::=
"HANDLE" "(" code\_list ")"
block
{ "ELSEHANDLE" condition block }
"ENDHANDLE"

```

---

## 20. Label and Jump

```

label\_stmt   ::= "label" identifier
golabel\_stmt ::= "golabel" identifier

```

---

## 21. Notes

1. Grammar is evaluated using recursive-descent parsing.
2. Expressions follow operator precedence.
3. Function scope introduces new variable scope.
4. Variables are resolved dynamically at runtime.


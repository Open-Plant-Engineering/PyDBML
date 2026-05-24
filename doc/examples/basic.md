
# Basic Examples

## Example 1

```

!x = 5
!y = 10
!z = !x + !y

$P !z

```

---

## Example 2

```

if (!x > 5) then
    $P "greater"
else
    $P "smaller"
endif

```

---

## Example 3

```

do !i from 1 to 5
    $P !i
enddo

```
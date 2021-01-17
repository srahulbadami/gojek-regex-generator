# Regex Generator

A Regex String generator that takes a regular expression as argument and returns strings that match the given regular expression. 
`generate(/[-+]?[0-9]{1,16}[.][0-9]{1,6}/, 10)`

should return results like
```
"-1752643936.096896"
"9519688.31"
"+1.7036"
"+65048.3876"
"-6547028036936294.111"
"07252345.650"
"-27557.78"
"7385289878518.439775"
"13981103761187.90"
"4100273498885.614"
```
This Generator has the following features:
`.` Match any character except newline  
`[` Start character class definition  
`]` End character class definition  
`?` 0 or 1 quantifier  
`*` 0 or more quantifiers  
`+` 1 or more quantifier  
`{` Start min/max quantifier  
`}` End min/max quantifier  
`|` Start of alternative branch  
`(` Start subpattern  
`)` End subpattern  

## How To Use ?

python regex-gen.py 
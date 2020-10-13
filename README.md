# karmasataka

exclusion regexes for DocFetcher:
excludes:
 - all files without `_` in them
 - all files ending with `_translation.txt`
 - all files ending with `.po`
```
[^_]+\.txt
.*?_translation\.txt
.*\.po
```

TODO: 
 - implement paragraph transfer on the translation file of the reader version.
 - implement `oe` to `œ`
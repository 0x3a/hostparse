# hostparse
`hostparse` - A command-line client for URL and hostname swizzling

## Usage
`hostparse` installs as a commandline utility and takes input from stdin. In essence hostparse has a few simple parseable items it can extract from a URL. This is the full list of items:

* scheme
* username
* password
* subdomain
* domain
* hostname
* tld
* port
* path
* params
* query
* fragment

These items can be used as 'swizzling' operators seperated by a comma (`,`). For example, lets say the input contains a url from which you want to extract just the registered domain with its tld you can do:

```
hostparse domain,tld
```

Now what is neat with these items is that the tool will match the shortest match without duplicates. This means that instead of typing `tld` you can also type `tl` or even `t` as there are no other items that would conflict. The same query as before can also be written as:

```
hostparse d,t
```

The only thing to be careful of is the match, for example you can't use `p` for `port` as it will also match other items (the tool will warn you about this and simply return without processing data). You have to get the right match, `po` will work for `ports` however `pa` won't work woth `path` as it will also match `params` which means you have to use `pat` for path.

Additionally the data the tool outputs uses a delimiter based on the items you choose, so if you choose `domain` and `tld` it will be outputed as: `<domain>.<tld>`. You can change this delimiter value with the `-d` operator after you specify the items to filter out. If you don't want a delimiter you can specify it as `-d''`.

## Bugs & Features

Feel free to open issues for features or bugs you've found or do a pull request and you will be rewarded somewhere later in life for it.

# make_match

make_match is an python script designed to take KBART-style .csv files
and return formatted code for the Ebsco EDS exact match search box

## USAGE

```shell
    python make_match.py [-h] [-e EXISTING_CODE] link_file
```

  link_file         link_file is a csv KBART-inspired file. It requires
                    publication_title and title_url. Optional fields include
                    date_first_issue_online,date_last_issue_online,
                    abbreviation (multiple abbreviations separated by ; )
                    , no_proxy (mark with 1 for open access titles). 
                    The date section and url can be repeated.

optional arguments:
  -h, --help        show this help message and exit
  -e EXISTING_CODE  existing code to incorporate

After the program has run a link_file_code.txt file will be generated which contains the EDS code


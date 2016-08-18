import os, csv
import argparse
import string

if __name__ == "__main__":

    proxy = 'https://clsproxy.library.caltech.edu/login?url='

    parser = argparse.ArgumentParser(description=\
    "Takes journal full text links and produces code for Elsevier FTF \
    Exact match results box")
    parser.add_argument('link_file', type=str, help= \
    "link_file is a csv KBART-inspired file. It \
    requires publication_title and title_url. \
    Optional fields include date_first_issue_online,date_last_issue_online, \
    abbreviation (separated by ; ), \
    no_proxy (mark with 1 for open access titles). \
    The date section, url, and proxy can be repeated \
    A _code file will be generated which contains the EDS code")
    parser.add_argument('-e', dest='existing_code',help="existing code to incorporate")

    args = parser.parse_args()

    if os.path.isfile(args.link_file)==False:
        raise NameError(args.link_file+' Does Not Exist')

    infile = open(args.link_file)
    linkd = csv.DictReader(infile)

    outstring = ''
    first = 0 #Key for using if statement
    if args.existing_code: #we're merging with an existing file
        inmerge = open(args.existing_code)
        inline = inmerge.readline()
        while inline!= '</script>':
            if len(inline)<5 and inline[0] == '}': #remove final }
                inline = inmerge.readline()
            else:
                outstring = outstring + inline
                inline = inmerge.readline()
    else: #We need the script header
        outstring = open('header.txt').read()
        first=1

    for row in linkd:

        #Extract labels for title
        title = row['publication_title']
        if 'no_proxy' in row:
            if row['no_proxy'] == 1:
                link = row['title_url']
            else:
                link = proxy + row['title_url'] 
        else:
            link = proxy + row['title_url']

        date = ''
        if 'date_first_issue_online' in row and 'date_last_issue_online' in row:
            if len(row['date_first_issue_online']) > 0 and\
            len(row['date_last_issue_online']) > 0: 
                date = "Access all issues from "\
                + row['date_first_issue_online'] + " to " +\
                row['date_last_issue_online']

        #format text
        if first==1:
            outstring = outstring + 'if('
            first=0 #reset
        else:
            outstring = outstring + '} else if ('
        
        terms = [string.lower(title)]
        if 'abbreviation' in row:
            if len(row['abbreviation']) > 0:
                split = row['abbreviation'].split(';')
                for s in split:
                    terms.append(s)
        for index,t in enumerate(terms):
            outstring = outstring + "(searchterm == \""\
            +t+"\") || (searchterm == \"ti "+t+"\") || (searchterm == \"so "+t+"\")"  
            if index == len(terms):
                outstring = outstring + ' || '

        outstring = outstring + "){\n"
        outstring = outstring + \
        "    $('.placard-container', window.parent.document).css(\"display\",\"none\");\n"

        outstring = outstring + "   resultdiv1 = \'<div class=\"knownitems\" id=\"Placard_widget\"\
style=\"border-width:2px;border-color:#12408c;background-color:#cde2f8;padding:10px;\"><div \
style=\"float:left; padding:10px;\"><p style=\"font-size:140%;font-weight:bold;color:black;\"> \
Looking for <em>" + title + "</em>?</p></div><div style=\"float:left;padding:10px;\">\
<p style=\"font-size:12px;padding-top:1px\"><ul><li><a href=\"" + link\
+ " style=\"text-decoration:none;\" target=\"_blank\">"+ date +\
"</a></li></ul></div></div></div>\';\n  \
$('.result-list',window.parent.document).before(resultdiv1);\n\n"

    outstring = outstring + "}\n</script>"
    outname = args.link_file.split('.')[0]+'_code.txt'
    outfile=open(outname,'w')
    outfile.write(outstring)

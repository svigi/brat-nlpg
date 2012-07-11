# Contributors #

In order by changed lines of code ([Ballmer][ballmer] says [SLOC][sloc]
    is an IBM religion):

[ballmer]:  http://en.wikipedia.org/wiki/Steve_Ballmer 
[sloc]:     http://en.wikipedia.org/wiki/Source_lines_of_code

* Goran Topić       &lt;REDACTED&gt;
* Sampo Pyysalo     &lt;REDACTED&gt;
* Pontus Stenetorp  &lt;REDACTED&gt;
* Illes Solt        &lt;solt tmit bme hu&gt;
* David McClosky    &lt;david.mcclosky gmail com&gt;

Extracted using the following bash one-liner:

    echo -e "Changed\tAdded\tDeleted\tName"; (OIFS="$IFS"; IFS=$'\n'; for author in `git log --format='%aN <%aE>' | sort -u`; do git log -C --author="$author" --pretty=tformat: --numstat | awk "BEGIN{add=0;del=0}\$1{add+=\$1}\$2{del+=\$2}END{print (add+del) \"\\t\" add \"\\t\" del \"\\t$author\"}"; done | sort -gr)

Some contributors has sometimes forgotten to configure their installation
properly, but seeing who is who on the list and adding up the changed lines is
fairly straightforward.

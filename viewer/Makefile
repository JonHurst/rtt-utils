all: viewer.html

viewer.html: rtt.xsl ../rtt.xml ../text/*
	xsltproc --xinclude rtt.xsl ../rtt.xml > viewer.html

<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns="http://www.w3.org/1999/xhtml">

<xsl:output method="xml"
	    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
	    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
	    version="1.0"/>


<xsl:template match="book">
  <html>
    <head>
      <title><xsl:value-of select="title"/>: <xsl:value-of select="subtitle"/></title>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
      <link rel="stylesheet" type="text/css" href="styles.css"/>
      <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
      <script type="text/javascript" src="script.js"></script>
    </head>
    <body>
      <xsl:apply-templates select="pages"/>
    </body>
  </html>
</xsl:template>


<xsl:template match="page">
  <table class="page">
    <xsl:attribute name="id">
      <xsl:text>pg</xsl:text><xsl:value-of select="@id"/>
    </xsl:attribute>
    <tr><th colspan="3">Page <xsl:value-of select="@id"/></th></tr>
    <tr>
    <xsl:apply-templates select="tags"/>
    </tr>
    <tr>
    <xsl:apply-templates select="image"/>
    <td class="lnum"></td>
    <xsl:apply-templates select="text"/>
    </tr>
    <xsl:if test="notes">
      <tr class="notes">
        <td colspan="3">
          <h2>Transcriber's notes</h2>
          <ul>
          <xsl:for-each select="notes/note">
            <li><xsl:value-of select="."/></li>
          </xsl:for-each>
          </ul>
        </td>
      </tr>
    </xsl:if>
  </table>
</xsl:template>


<xsl:template match="tags">
  <tr class="formatting"><td colspan="3">
    <xsl:choose>
      <xsl:when test="@class='block_formatting'">
        <xsl:text>Block Formatting:</xsl:text>
      </xsl:when>
      <xsl:when test="@class='inline_formatting'">
        <xsl:text>Inline Formatting:</xsl:text>
      </xsl:when>
    </xsl:choose>
    <ul><xsl:apply-templates/></ul>
  </td></tr>
</xsl:template>


<xsl:template match="tag">
  <li><xsl:value-of select="."/></li>
</xsl:template>


<xsl:template match="image">
    <td class="img_ph">
      <span class="ph">Loading…</span>
      <a class='img_link'>
      <xsl:attribute name="href">
        <xsl:text>../</xsl:text><xsl:value-of select="@src"/>
      </xsl:attribute>
      <xsl:text>Show</xsl:text>
      <br/>
      <xsl:text>image</xsl:text>
    </a></td>
</xsl:template>


<xsl:template match="text">
  <td class="text">
    <p><xsl:value-of select="."/></p>
  </td>
</xsl:template>

</xsl:stylesheet>
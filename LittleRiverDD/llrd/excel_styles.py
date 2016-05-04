#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     15/04/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from xlwt import Alignment, XFStyle, Borders, Font

# **************************************************************************************
# styles
#
# year break dashed border
yearBreak = XFStyle()
yearBorders = Borders()
yearBorders.bottom = Borders.DASHED
yearBreak.borders = yearBorders

# center align
alignCenter = Alignment()
alignCenter.horz = Alignment.HORZ_CENTER
alignCenter.vert = Alignment.VERT_CENTER

# Top alignment, should be used for all cells
topAlign = Alignment()
topAlign.vert = Alignment.VERT_TOP

# header centered and wrapped
alignWrap = Alignment()
alignWrap.horz = Alignment.HORZ_CENTER
alignWrap.wrap = Alignment.WRAP_AT_RIGHT

# headers font
fntHeaders = Font()
fntHeaders.height = 220
fntHeaders.name = 'Calibri'

# header styles
styleHeaders = XFStyle()
styleHeaders.font = fntHeaders
styleHeaders.alignment.wrap = True
styleHeaders.alignment = alignCenter

# headers with boarder
styleHeadersWithBorder = XFStyle()
styleHeadersWithBorder.font = fntHeaders
styleHeadersWithBorder.alignment.wrap = True
styleHeadersWithBorder.alignment = alignWrap
styleHeadersWithBorder.borders = yearBorders

# left alignment
leftAlign = Alignment()
leftAlign.horz = Alignment.HORZ_LEFT
leftAlign.vert = Alignment.VERT_TOP
leftAlign.wrap = Alignment.WRAP_AT_RIGHT

# right alignment
rightAlign = Alignment()
rightAlign.horz = Alignment.HORZ_RIGHT
rightAlign.vert = Alignment.VERT_TOP
rightAlign.wrap = Alignment.WRAP_AT_RIGHT

# style for left justified and wrapped
styleHeadersLeft = XFStyle()
styleHeadersLeft.font = fntHeaders
styleHeadersLeft.alignment.wrap = True
styleHeadersLeft.alignment = leftAlign

# style for right justified and wrapped
styleHeadersRight = XFStyle()
styleHeadersRight.font = fntHeaders
styleHeadersRight.alignment.wrap = True
styleHeadersRight.alignment = rightAlign

# style for right justified and underline
styleHeadersRight2 = XFStyle()
styleHeadersRight2.font = fntHeaders
styleHeadersRight2.alignment.wrap = True
styleHeadersRight2.alignment = rightAlign
styleHeadersRight2.borders = yearBorders


# blank line
underline = XFStyle()
uBorders = Borders()
uBorders.bottom = Borders.THIN
underline.borders = uBorders

# date format
styleDate = XFStyle()
styleDate.num_format_str = 'MM/DD/YYYY'
styleDate.font = fntHeaders
styleDate.alignment = leftAlign

# currency format
styleCurrency = XFStyle()
styleCurrency.num_format_str = '#,##0.00'
styleCurrency.font = fntHeaders
styleCurrency.alignment = rightAlign

# style for section-township-range
zfillStyle = XFStyle()
zfillStyle.num_format_str = '00'
zfillStyle.font = fntHeaders
zfillStyle.alignment = leftAlign

# default
defaultStyle = XFStyle()
defaultStyle.font = fntHeaders
defaultStyle.alignment = leftAlign

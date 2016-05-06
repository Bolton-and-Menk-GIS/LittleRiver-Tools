import arcpy
import os
import datetime
from . import utils
from . import AbstractOfReceipts
from . import MaintenanceAssessmentList
from . import proxy
from . import OwnerReceipt
from . import flags
from . import download
from . import contours
reload(utils)
reload(OwnerReceipt)
reload(AbstractOfReceipts)
reload(MaintenanceAssessmentList)
reload(proxy)
reload(flags)
reload(download)
reload(contours)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Little River Drainage District Tools"
        self.alias = "Little River DD Tools"

        # List of tool classes associated with this toolbox
        self.tools = [SetupConfigFile, AbstractOfReceiptsTool, MaintenanceAssessmentListTool, ProxyTool,
                      OwnerReceiptsCodeTool, OwnerReceiptsCountyTool, CreateFlagTable, DownloadParcels,
                      GenerateContoursTool]


class SetupConfigFile(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Setup Configuration File"
        self.description = ""
        self.category = 'Setup'
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        gdb = arcpy.Parameter(displayName="Geodatabase",
            name="Geodatabase",
            datatype="Workspace",
            parameterType="Required",
            direction="Input")

        return [gdb]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[0].filter.list = ['LocalDatabase', 'RemoteDatabase']
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        d = {p.name: p.valueAsText for p in parameters}
        utils.passArgs(utils.writeConfig, d)

class AbstractOfReceiptsTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Abstract of Receipts Report"
        self.description = ""
        self.category = 'Reports'
        self.canRunInBackground = False
        self.gdb = utils.Geodatabase()

    def getParameterInfo(self):
        """Define parameter definitions"""
        output = arcpy.Parameter(displayName="Output Excel File",
            name="out_excel",
            datatype="File",
            parameterType="Required",
            direction="Output")

        county = arcpy.Parameter(displayName="County",
            name="county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        where = arcpy.Parameter(displayName="Where Clause",
            name="where_clause",
            datatype="SQL Expression",
            parameterType="Optional",
            direction="Optional")

        orderBy = arcpy.Parameter(displayName="Order By",
            name="orderBy",
            datatype="Value Table",
            parameterType="Optional",
            direction="Input")

        # dummy parameter, just necessary for where clause
        table = arcpy.Parameter(displayName='Table',
            name='table',
            datatype='Table',
            parameterType='Optional',
            direction='Input')

        # set value for table so where clause can be applied
        table.value = self.gdb.summary_table
        where.parameterDependencies = [table.name]

        # value table for Order By
        orderBy.parameterDependencies = [table.name]
        orderBy.columns = [['Field', 'Fields']]

        return [output, county, where, orderBy, table]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[4].enabled = False
        parameters[4].value = self.gdb.summary_table
        parameters[0].filter.list = ['xls']
        if not parameters[3].altered:
            parameters[3].value = [['OWNER_CODE']]
        parameters[1].filter.list = self.gdb.list_counties()
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText for p in parameters][:-1]
        utils.passArgs(AbstractOfReceipts.generateAOR, args)


class MaintenanceAssessmentListTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Maintenance Assessment List"
        self.description = ""
        self.category = 'Reports'
        self.canRunInBackground = False
        self.gdb = utils.Geodatabase()

    def getParameterInfo(self):
        """Define parameter definitions"""
        output = arcpy.Parameter(displayName="Output Excel File",
            name="out_excel",
            datatype="File",
            parameterType="Required",
            direction="Output")

        county = arcpy.Parameter(displayName="County",
            name="county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        rate = arcpy.Parameter(displayName="Rate",
            name="rate",
            datatype="Double",
            parameterType="Required",
            direction="Input")

        year = arcpy.Parameter(displayName="Year",
            name="year",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        where = arcpy.Parameter(displayName="Where Clause",
            name="where_clause",
            datatype="SQL Expression",
            parameterType="Optional",
            direction="Optional")

        orderBy = arcpy.Parameter(displayName="Order By",
            name="orderBy",
            datatype="Value Table",
            parameterType="Optional",
            direction="Input")

        # dummy parameter, just necessary for where clause
        table = arcpy.Parameter(displayName='Table',
            name='table',
            datatype='Table',
            parameterType='Optional',
            direction='Input')

        # set value for table so where clause can be applied
        table.value = self.gdb.summary_table
        where.parameterDependencies = [table.name]

        # value table for Order By
        orderBy.parameterDependencies = [table.name]
        orderBy.columns = [['Field', 'Fields']]

        return [output, county, rate, year, where, orderBy, table]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[6].enabled = False
        parameters[6].value = self.gdb.breakdown_table
        parameters[0].filter.list = ['xls']
        if not parameters[5].altered:
            parameters[5].value = [['CODE'], ['DESCRIPTION']]
        parameters[1].filter.list = self.gdb.list_counties()

        parameters[2].filter.type = 'Range'
        parameters[2].filter.list = [1.0, 100.0]
        if not parameters[2].value:
            parameters[2].value = 9.0

        cur_year = datetime.datetime.now().year
        parameters[3].filter.list = range(cur_year-5, cur_year + 5)
        if not parameters[3].value:
            parameters[3].value = cur_year - 1

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText for p in parameters][:-1]
        utils.passArgs(MaintenanceAssessmentList.generateMAL, args)

class ProxyTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Proxies"
        self.description = ""
        self.category = 'Reports'
        self.canRunInBackground = False
        self.gdb = utils.Geodatabase()

    def getParameterInfo(self):
        """Define parameter definitions"""
        output = arcpy.Parameter(displayName="Output Folder",
            name="out_folder",
            datatype="Folder",
            parameterType="Required",
            direction="Input")

        county = arcpy.Parameter(displayName="County",
            name="county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        city = arcpy.Parameter(displayName="Meeting City",
            name="city",
            datatype="String",
            parameterType="Required",
            direction="Input")

        mCounty = arcpy.Parameter(displayName="Meeting County",
            name="meeting_county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        date = arcpy.Parameter(displayName="Meeting Date",
            name="date",
            datatype="Date",
            parameterType="Required",
            direction="Input")

        return [output, county, city, mCounty, date]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[1].filter.list = self.gdb.list_counties()
        if not parameters[2].altered:
            parameters[2].value = proxy.DEFAULT_CITY

        if not parameters[3].altered:
            parameters[3].value = proxy.DEFAULT_COUNTY

        if not parameters[4].altered:
            parameters[4].value = proxy.DEFAULT_DATE

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText if i != 4 else p.value for i,p in enumerate(parameters)]
        utils.passArgs(proxy.generateProxyBallots, args)

class OwnerReceiptsCountyTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Owner Receipts by County"
        self.description = ""
        self.category = 'Reports'
        self.canRunInBackground = False
        self.gdb = utils.Geodatabase()

    def getParameterInfo(self):
        """Define parameter definitions"""
        output = arcpy.Parameter(displayName="Output Folder",
            name="out_folder",
            datatype="Folder",
            parameterType="Required",
            direction="Input")

        county = arcpy.Parameter(displayName="County",
            name="county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        year = arcpy.Parameter(displayName="Year",
            name="year",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        where = arcpy.Parameter(displayName="Where Clause",
            name="where_clause",
            datatype="SQL Expression",
            parameterType="Optional",
            direction="Optional")

        name = arcpy.Parameter(displayName="Mail To Name",
            name="name",
            datatype="String",
            parameterType="Required",
            direction="Input")

        addr = arcpy.Parameter(displayName="Mail To Address",
            name="address",
            datatype="String",
            parameterType="Required",
            direction="Input")

        csz = arcpy.Parameter(displayName="Mail To City, State Zip",
            name="csz",
            datatype="String",
            parameterType="Required",
            direction="Input")

        add_maps = arcpy.Parameter(displayName="Create Map Reports",
            name="add_maps",
            datatype="Boolean",
            parameterType="Optional",
            direction="Input")



        return [output, county, year, where, name, addr, csz, add_maps]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[1].filter.list = self.gdb.list_counties()
        if not parameters[2].altered:
            parameters[2].value = utils.LAST_YEAR

        if not parameters[4].altered:
            parameters[4].value = OwnerReceipt.DEFAULT_MAIL_NAME

        if not parameters[5].altered:
            parameters[5].value = OwnerReceipt.DEFAULT_MAIL_ADDR

        if not parameters[6].altered:
            parameters[6].value = OwnerReceipt.DEFAULT_MAIL_CSZ

        if not parameters[7].altered:
            parameters[7].value = False

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText for p in parameters]
        utils.passArgs(OwnerReceipt.generateOwnerReceiptsForCounty, args)
        #OwnerReceipt.generateOwnerReceiptsForCounty(*args)

class OwnerReceiptsCodeTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Owner Receipt by Code"
        self.description = ""
        self.category = 'Reports'
        self.canRunInBackground = False
        self.gdb = utils.Geodatabase()

    def getParameterInfo(self):
        """Define parameter definitions"""
        output = arcpy.Parameter(displayName="Output Folder",
            name="out_folder",
            datatype="Folder",
            parameterType="Required",
            direction="Input")

        code = arcpy.Parameter(displayName="Owner Code",
            name="county",
            datatype="String",
            parameterType="Required",
            direction="Input")

        year = arcpy.Parameter(displayName="Year",
            name="year",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        where = arcpy.Parameter(displayName="Where Clause",
            name="where_clause",
            datatype="SQL Expression",
            parameterType="Optional",
            direction="Input")

        name = arcpy.Parameter(displayName="Mail To Name",
            name="name",
            datatype="String",
            parameterType="Required",
            direction="Input")

        addr = arcpy.Parameter(displayName="Mail To Address",
            name="address",
            datatype="String",
            parameterType="Required",
            direction="Input")

        csz = arcpy.Parameter(displayName="Mail To City, State Zip",
            name="csz",
            datatype="String",
            parameterType="Optional",
            direction="Input")

        add_maps = arcpy.Parameter(displayName="Create Map Reports",
            name="add_maps",
            datatype="Boolean",
            parameterType="Optional",
            direction="Input")



        return [output, code, year, where, name, addr, csz, add_maps]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if not parameters[1].hasBeenValidated and not parameters[1].altered:
            parameters[1].filter.list = self.gdb.getOwnerCodes()
        if not parameters[2].altered:
            parameters[2].value = utils.LAST_YEAR

        if not parameters[4].altered:
            parameters[4].value = OwnerReceipt.DEFAULT_MAIL_NAME

        if not parameters[5].altered:
            parameters[5].value = OwnerReceipt.DEFAULT_MAIL_ADDR

        if not parameters[6].altered:
            parameters[6].value = OwnerReceipt.DEFAULT_MAIL_CSZ

        if not parameters[7].altered:
            parameters[7].value = False

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText for p in parameters]
        utils.passArgs(OwnerReceipt.generateOwnerReceiptByCode, args)
        #OwnerReceipt.generateOwnerReceiptByCode(*args)

class CreateFlagTable(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Flag Table"
        self.description = ""
        self.category = 'Data Validation'
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        acre_threshold = arcpy.Parameter(displayName="Acre Percent Threshold",
            name="acre_threshold",
            datatype="LONG",
            parameterType="Optional",
            direction="Input")

        min_acre_diff = arcpy.Parameter(displayName="Minimum Acre Difference",
            name="min_acre_diff",
            datatype="DOUBLE",
            parameterType="Optional",
            direction="Input")

        return [acre_threshold, min_acre_diff]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if not parameters[0].value:
            parameters[0].value = 10
        if not parameters[1].value:
            parameters[1].value = 40

        parameters[0].filter.type = 'Range'
        parameters[0].filter.list = [1, 100]

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        args = [p.valueAsText for p in parameters]
        utils.passArgs(flags.getFlags, args)
##        flags.getFlags(*args)

class DownloadParcels(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Download Parcels"
        self.description = ""
        self.category = 'Parcels'
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        return []

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        utils.passArgs(download.parcelDownload, [])

class GenerateContoursTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate Contours"
        self.description = "Generates clean contours, especially in areas with low relief"
        self.category = 'Elevation'
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        dem = arcpy.Parameter(displayName="DEM",
            name="dem",
            datatype="Raster Layer",
            parameterType="Required",
            direction="Input")

        out_contours = arcpy.Parameter(displayName="Output Contours",
            name="out_contours",
            datatype="Feature Class",
            parameterType="Required",
            direction="Output")

        interval = arcpy.Parameter(displayName="Contour Interval",
            name="interval",
            datatype="Long",
            parameterType="Optional",
            direction="Input")

        z_factor = arcpy.Parameter(displayName="Z-Factor",
            name="z_factor",
            datatype="Double",
            parameterType="Optional",
            direction="Input")

        index_interval = arcpy.Parameter(displayName="Contour Index Interval",
            name="index_interval",
            datatype="Long",
            parameterType="Optional",
            direction="Input")

        contour_length_threshold = arcpy.Parameter(displayName="Contour Length Threshold",
            name="contour_length_threshold",
            datatype="Long",
            parameterType="Optional",
            direction="Input")

        return [dem, out_contours, interval, z_factor, index_interval, contour_length_threshold]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[2].filter.type = 'Range'
        parameters[2].filter.list = [1, 10]

        if not parameters[2].value and not parameters[2].altered:
            parameters[2].value = 2

        if not parameters[3].value and not parameters[3].altered:
            parameters[3].value = 3.28084

        parameters[4].filter.list = range(5, 105, 5)
        if not parameters[4].value and not parameters[4].altered:
            parameters[4].value = 10

        if not parameters[5].value and not parameters[5].altered:
            parameters[5].value = 200

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.addOutputsToMap = True
        args = [p.valueAsText for p in parameters]
        utils.passArgs(contours.getContours, args)

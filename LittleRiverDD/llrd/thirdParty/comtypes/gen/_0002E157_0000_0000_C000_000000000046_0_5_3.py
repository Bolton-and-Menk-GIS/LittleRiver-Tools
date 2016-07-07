# -*- coding: mbcs -*-
typelib_path = u'C:\\Program Files (x86)\\Common Files\\Microsoft Shared\\VBA\\VBA6\\VBE6EXT.OLB'
_lcid = 0 # change this if required
from ctypes import *
from comtypes import GUID
from comtypes import CoClass
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from ctypes.wintypes import VARIANT_BOOL
from ctypes import HRESULT
from comtypes import BSTR
from comtypes.automation import IDispatch
from comtypes.automation import VARIANT
from comtypes import IUnknown
from comtypes import DISPMETHOD, DISPPROPERTY, helpstring
import comtypes.gen._2DF8D04C_5BFA_101B_BDE5_00AA0044DE52_0_2_7


class Addins(CoClass):
    _reg_clsid_ = GUID('{DA936B63-AC8B-11D1-B6E5-00A0C90F2744}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _AddIns(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{DA936B62-AC8B-11D1-B6E5-00A0C90F2744}')
    _idlflags_ = ['dual', 'oleautomation']
Addins._com_interfaces_ = [_AddIns]

class _VBComponentsEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E115-0000-0000-C000-000000000046}')
    _idlflags_ = ['oleautomation']
_VBComponentsEvents._methods_ = [
]
################################################################
## code template for _VBComponentsEvents implementation
##class _VBComponentsEvents_Impl(object):

class VBComponents(CoClass):
    _reg_clsid_ = GUID('{BE39F3D7-1B13-11D0-887F-00A0C90F2744}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _VBComponents_Old(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E162-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class _VBComponents(_VBComponents_Old):
    _case_insensitive_ = True
    _iid_ = GUID('{EEE0091C-E393-11D1-BB03-00C04FB6C4A6}')
    _idlflags_ = ['dual', 'oleautomation']
VBComponents._com_interfaces_ = [_VBComponents]

class CodePane(CoClass):
    _reg_clsid_ = GUID('{0002E178-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _CodePane(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E176-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation']
CodePane._com_interfaces_ = [_CodePane]

class _VBComponent_Old(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E164-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class CodeModule(CoClass):
    _reg_clsid_ = GUID('{0002E170-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _CodeModule(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E16E-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation', 'hidden']
CodeModule._com_interfaces_ = [_CodeModule]


# values for enumeration 'vbext_ComponentType'
vbext_ct_StdModule = 1
vbext_ct_ClassModule = 2
vbext_ct_MSForm = 3
vbext_ct_ActiveXDesigner = 11
vbext_ct_Document = 100
vbext_ComponentType = c_int # enum
class Application(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E158-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class VBE(Application):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E166-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
class Properties(CoClass):
    _reg_clsid_ = GUID('{0002E18B-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _Properties(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E188-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
Properties._com_interfaces_ = [_Properties]

class Window(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E16B-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
_VBComponent_Old._methods_ = [
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'Saved',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'lpfReturn' )),
    COMMETHOD([dispid(48), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrReturn' )),
    COMMETHOD([dispid(48), 'propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'pbstrReturn' )),
    COMMETHOD([dispid(49), 'propget'], HRESULT, 'Designer',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'ppDispatch' )),
    COMMETHOD([dispid(50), 'propget'], HRESULT, 'CodeModule',
              ( ['retval', 'out'], POINTER(POINTER(CodeModule)), 'ppVbaModule' )),
    COMMETHOD([dispid(51), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(vbext_ComponentType), 'pKind' )),
    COMMETHOD([dispid(52)], HRESULT, 'Export',
              ( ['in'], BSTR, 'FileName' )),
    COMMETHOD([dispid(53), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(54), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(VBComponents)), 'lppcReturn' )),
    COMMETHOD([dispid(55), 'propget'], HRESULT, 'HasOpenDesigner',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'lpfReturn' )),
    COMMETHOD([dispid(56), 'propget'], HRESULT, 'Properties',
              ( ['retval', 'out'], POINTER(POINTER(Properties)), 'lpppReturn' )),
    COMMETHOD([dispid(57)], HRESULT, 'DesignerWindow',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'lppcReturn' )),
    COMMETHOD([dispid(60)], HRESULT, 'Activate'),
]
################################################################
## code template for _VBComponent_Old implementation
##class _VBComponent_Old_Impl(object):
##    @property
##    def Designer(self):
##        '-no docstring-'
##        #return ppDispatch
##
##    def _get(self):
##        '-no docstring-'
##        #return pbstrReturn
##    def _set(self, pbstrReturn):
##        '-no docstring-'
##    Name = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Saved(self):
##        '-no docstring-'
##        #return lpfReturn
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return lppcReturn
##
##    def Activate(self):
##        '-no docstring-'
##        #return 
##
##    def Export(self, FileName):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CodeModule(self):
##        '-no docstring-'
##        #return ppVbaModule
##
##    @property
##    def HasOpenDesigner(self):
##        '-no docstring-'
##        #return lpfReturn
##
##    @property
##    def Type(self):
##        '-no docstring-'
##        #return pKind
##
##    @property
##    def Properties(self):
##        '-no docstring-'
##        #return lpppReturn
##
##    def DesignerWindow(self):
##        '-no docstring-'
##        #return lppcReturn
##

class _VBProjects_Old(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E165-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class VBProject(CoClass):
    _reg_clsid_ = GUID('{0002E169-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _ProjectTemplate(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E159-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class _VBProject_Old(_ProjectTemplate):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E160-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
class _VBProject(_VBProject_Old):
    _case_insensitive_ = True
    _iid_ = GUID('{EEE00915-E393-11D1-BB03-00C04FB6C4A6}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
VBProject._com_interfaces_ = [_VBProject]

_VBProjects_Old._methods_ = [
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppcReturn' )),
    COMMETHOD([dispid(20), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
]
################################################################
## code template for _VBProjects_Old implementation
##class _VBProjects_Old_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##

class Reference(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E17E-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation']
class References(CoClass):
    _reg_clsid_ = GUID('{0002E17C-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _References(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E17A-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation', 'hidden']
class _dispReferences_Events(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{CDDE3804-2064-11CF-867F-00AA005FF34A}')
    _idlflags_ = ['nonextensible', 'hidden']
    _methods_ = []
References._com_interfaces_ = [_References]
References._outgoing_interfaces_ = [_dispReferences_Events]


# values for enumeration 'vbext_RefKind'
vbext_rk_TypeLib = 0
vbext_rk_Project = 1
vbext_RefKind = c_int # enum
Reference._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(References)), 'retval' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrName' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'Guid',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrGuid' )),
    COMMETHOD([dispid(1610743812), 'propget'], HRESULT, 'Major',
              ( ['retval', 'out'], POINTER(c_int), 'pMajor' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'Minor',
              ( ['retval', 'out'], POINTER(c_int), 'pMinor' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'FullPath',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrLocation' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'BuiltIn',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pfIsDefault' )),
    COMMETHOD([dispid(1610743816), 'propget'], HRESULT, 'IsBroken',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pfIsBroken' )),
    COMMETHOD([dispid(1610743817), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(vbext_RefKind), 'pKind' )),
    COMMETHOD([dispid(1610743818), 'propget'], HRESULT, 'Description',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrName' )),
]
################################################################
## code template for Reference implementation
##class Reference_Impl(object):
##    @property
##    def Major(self):
##        '-no docstring-'
##        #return pMajor
##
##    @property
##    def Name(self):
##        '-no docstring-'
##        #return pbstrName
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def IsBroken(self):
##        '-no docstring-'
##        #return pfIsBroken
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def BuiltIn(self):
##        '-no docstring-'
##        #return pfIsDefault
##
##    @property
##    def FullPath(self):
##        '-no docstring-'
##        #return pbstrLocation
##
##    @property
##    def Guid(self):
##        '-no docstring-'
##        #return pbstrGuid
##
##    @property
##    def Type(self):
##        '-no docstring-'
##        #return pKind
##
##    @property
##    def Minor(self):
##        '-no docstring-'
##        #return pMinor
##
##    @property
##    def Description(self):
##        '-no docstring-'
##        #return pbstrName
##

class _Windows_old(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E16A-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
_Windows_old._methods_ = [
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppptReturn' )),
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'lppcReturn' )),
    COMMETHOD([dispid(201), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
]
################################################################
## code template for _Windows_old implementation
##class _Windows_old_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppptReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##

_ProjectTemplate._methods_ = [
    COMMETHOD([dispid(1), 'hidden', 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'hidden', 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
]
################################################################
## code template for _ProjectTemplate implementation
##class _ProjectTemplate_Impl(object):
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppaReturn
##


# values for enumeration 'vbext_VBAMode'
vbext_vm_Run = 0
vbext_vm_Break = 1
vbext_vm_Design = 2
vbext_VBAMode = c_int # enum
class VBProjects(CoClass):
    _reg_clsid_ = GUID('{0002E101-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _VBProjects(_VBProjects_Old):
    _case_insensitive_ = True
    _iid_ = GUID('{EEE00919-E393-11D1-BB03-00C04FB6C4A6}')
    _idlflags_ = ['dual', 'oleautomation']
VBProjects._com_interfaces_ = [_VBProjects]


# values for enumeration 'vbext_ProjectProtection'
vbext_pp_none = 0
vbext_pp_locked = 1
vbext_ProjectProtection = c_int # enum
_VBProject_Old._methods_ = [
    COMMETHOD([dispid(116), 'propget'], HRESULT, 'HelpFile',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrHelpFile' )),
    COMMETHOD([dispid(116), 'propput'], HRESULT, 'HelpFile',
              ( ['in'], BSTR, 'lpbstrHelpFile' )),
    COMMETHOD([dispid(117), 'propget'], HRESULT, 'HelpContextID',
              ( ['retval', 'out'], POINTER(c_int), 'lpdwContextID' )),
    COMMETHOD([dispid(117), 'propput'], HRESULT, 'HelpContextID',
              ( ['in'], c_int, 'lpdwContextID' )),
    COMMETHOD([dispid(118), 'propget'], HRESULT, 'Description',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrDescription' )),
    COMMETHOD([dispid(118), 'propput'], HRESULT, 'Description',
              ( ['in'], BSTR, 'lpbstrDescription' )),
    COMMETHOD([dispid(119), 'propget'], HRESULT, 'Mode',
              ( ['retval', 'out'], POINTER(vbext_VBAMode), 'lpVbaMode' )),
    COMMETHOD([dispid(120), 'propget'], HRESULT, 'References',
              ( ['retval', 'out'], POINTER(POINTER(References)), 'lppReferences' )),
    COMMETHOD([dispid(121), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrName' )),
    COMMETHOD([dispid(121), 'propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'lpbstrName' )),
    COMMETHOD([dispid(122), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(123), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(VBProjects)), 'lppaReturn' )),
    COMMETHOD([dispid(131), 'propget'], HRESULT, 'Protection',
              ( ['retval', 'out'], POINTER(vbext_ProjectProtection), 'lpProtection' )),
    COMMETHOD([dispid(133), 'propget'], HRESULT, 'Saved',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'lpfReturn' )),
    COMMETHOD([dispid(135), 'propget'], HRESULT, 'VBComponents',
              ( ['retval', 'out'], POINTER(POINTER(VBComponents)), 'lppcReturn' )),
]
################################################################
## code template for _VBProject_Old implementation
##class _VBProject_Old_Impl(object):
##    @property
##    def VBComponents(self):
##        '-no docstring-'
##        #return lppcReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return lpbstrDescription
##    def _set(self, lpbstrDescription):
##        '-no docstring-'
##    Description = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return lpdwContextID
##    def _set(self, lpdwContextID):
##        '-no docstring-'
##    HelpContextID = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Protection(self):
##        '-no docstring-'
##        #return lpProtection
##
##    @property
##    def References(self):
##        '-no docstring-'
##        #return lppReferences
##
##    @property
##    def Mode(self):
##        '-no docstring-'
##        #return lpVbaMode
##
##    def _get(self):
##        '-no docstring-'
##        #return lpbstrHelpFile
##    def _set(self, lpbstrHelpFile):
##        '-no docstring-'
##    HelpFile = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Saved(self):
##        '-no docstring-'
##        #return lpfReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return lpbstrName
##    def _set(self, lpbstrName):
##        '-no docstring-'
##    Name = property(_get, _set, doc = _set.__doc__)
##


# values for enumeration 'vbext_ProjectType'
vbext_pt_HostProject = 100
vbext_pt_StandAlone = 101
vbext_ProjectType = c_int # enum
_VBProject._methods_ = [
    COMMETHOD([dispid(138)], HRESULT, 'SaveAs',
              ( ['in'], BSTR, 'FileName' )),
    COMMETHOD([dispid(139)], HRESULT, 'MakeCompiledFile'),
    COMMETHOD([dispid(140), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(vbext_ProjectType), 'lpkind' )),
    COMMETHOD([dispid(141), 'propget'], HRESULT, 'FileName',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrReturn' )),
    COMMETHOD([dispid(142), 'propget'], HRESULT, 'BuildFileName',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrBldFName' )),
    COMMETHOD([dispid(142), 'propput'], HRESULT, 'BuildFileName',
              ( ['in'], BSTR, 'lpbstrBldFName' )),
]
################################################################
## code template for _VBProject implementation
##class _VBProject_Impl(object):
##    def SaveAs(self, FileName):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return lpbstrBldFName
##    def _set(self, lpbstrBldFName):
##        '-no docstring-'
##    BuildFileName = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def FileName(self):
##        '-no docstring-'
##        #return lpbstrReturn
##
##    @property
##    def Type(self):
##        '-no docstring-'
##        #return lpkind
##
##    def MakeCompiledFile(self):
##        '-no docstring-'
##        #return 
##

class AddIn(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{DA936B64-AC8B-11D1-B6E5-00A0C90F2744}')
    _idlflags_ = ['dual', 'oleautomation']
AddIn._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Description',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstr' )),
    COMMETHOD([dispid(0), 'propput'], HRESULT, 'Description',
              ( ['in'], BSTR, 'lpbstr' )),
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppVBE' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(Addins)), 'lppaddins' )),
    COMMETHOD([dispid(3), 'propget'], HRESULT, 'ProgId',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstr' )),
    COMMETHOD([dispid(4), 'propget'], HRESULT, 'Guid',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstr' )),
    COMMETHOD([dispid(6), 'propget'], HRESULT, 'Connect',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'lpfConnect' )),
    COMMETHOD([dispid(6), 'propput'], HRESULT, 'Connect',
              ( ['in'], VARIANT_BOOL, 'lpfConnect' )),
    COMMETHOD([dispid(7), 'propget'], HRESULT, 'Object',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'lppdisp' )),
    COMMETHOD([dispid(7), 'propput'], HRESULT, 'Object',
              ( ['in'], POINTER(IDispatch), 'lppdisp' )),
]
################################################################
## code template for AddIn implementation
##class AddIn_Impl(object):
##    def _get(self):
##        '-no docstring-'
##        #return lpbstr
##    def _set(self, lpbstr):
##        '-no docstring-'
##    Description = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppVBE
##
##    def _get(self):
##        '-no docstring-'
##        #return lppdisp
##    def _set(self, lppdisp):
##        '-no docstring-'
##    Object = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return lppaddins
##
##    def _get(self):
##        '-no docstring-'
##        #return lpfConnect
##    def _set(self, lpfConnect):
##        '-no docstring-'
##    Connect = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Guid(self):
##        '-no docstring-'
##        #return lpbstr
##
##    @property
##    def ProgId(self):
##        '-no docstring-'
##        #return lpbstr
##

class _dispVBProjectsEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E103-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = []
_dispVBProjectsEvents._disp_methods_ = [
    DISPMETHOD([dispid(1)], None, 'ItemAdded',
               ( ['in'], POINTER(VBProject), 'VBProject' )),
    DISPMETHOD([dispid(2)], None, 'ItemRemoved',
               ( ['in'], POINTER(VBProject), 'VBProject' )),
    DISPMETHOD([dispid(3)], None, 'ItemRenamed',
               ( ['in'], POINTER(VBProject), 'VBProject' ),
               ( ['in'], BSTR, 'OldName' )),
    DISPMETHOD([dispid(4)], None, 'ItemActivated',
               ( ['in'], POINTER(VBProject), 'VBProject' )),
]

# values for enumeration 'vbext_WindowState'
vbext_ws_Normal = 0
vbext_ws_Minimize = 1
vbext_ws_Maximize = 2
vbext_WindowState = c_int # enum
class Property(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E18C-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
_Properties._methods_ = [
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Property)), 'lplppReturn' )),
    COMMETHOD([dispid(1), 'hidden', 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'lppidReturn' )),
    COMMETHOD([dispid(40), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
]
################################################################
## code template for _Properties implementation
##class _Properties_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppidReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lplppReturn
##

class CodePanes(CoClass):
    _reg_clsid_ = GUID('{0002E174-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _CodePanes(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E172-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation']
CodePanes._com_interfaces_ = [_CodePanes]


# values for enumeration 'vbext_CodePaneview'
vbext_cv_ProcedureView = 0
vbext_cv_FullModuleView = 1
vbext_CodePaneview = c_int # enum
_CodePane._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(CodePanes)), 'retval' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'retval' )),
    COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'Window',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'retval' )),
    COMMETHOD([dispid(1610743811)], HRESULT, 'GetSelection',
              ( ['out'], POINTER(c_int), 'StartLine' ),
              ( ['out'], POINTER(c_int), 'StartColumn' ),
              ( ['out'], POINTER(c_int), 'EndLine' ),
              ( ['out'], POINTER(c_int), 'EndColumn' )),
    COMMETHOD([dispid(1610743812)], HRESULT, 'SetSelection',
              ( ['in'], c_int, 'StartLine' ),
              ( ['in'], c_int, 'StartColumn' ),
              ( ['in'], c_int, 'EndLine' ),
              ( ['in'], c_int, 'EndColumn' )),
    COMMETHOD([dispid(1610743813), 'propget'], HRESULT, 'TopLine',
              ( ['retval', 'out'], POINTER(c_int), 'TopLine' )),
    COMMETHOD([dispid(1610743813), 'propput'], HRESULT, 'TopLine',
              ( ['in'], c_int, 'TopLine' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'CountOfVisibleLines',
              ( ['retval', 'out'], POINTER(c_int), 'CountOfVisibleLines' )),
    COMMETHOD([dispid(1610743816), 'propget'], HRESULT, 'CodeModule',
              ( ['retval', 'out'], POINTER(POINTER(CodeModule)), 'CodeModule' )),
    COMMETHOD([dispid(1610743817)], HRESULT, 'Show'),
    COMMETHOD([dispid(1610743818), 'propget'], HRESULT, 'CodePaneView',
              ( ['retval', 'out'], POINTER(vbext_CodePaneview), 'pCodePaneview' )),
]
################################################################
## code template for _CodePane implementation
##class _CodePane_Impl(object):
##    def SetSelection(self, StartLine, StartColumn, EndLine, EndColumn):
##        '-no docstring-'
##        #return 
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return retval
##
##    def Show(self):
##        '-no docstring-'
##        #return 
##
##    def GetSelection(self):
##        '-no docstring-'
##        #return StartLine, StartColumn, EndLine, EndColumn
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def Window(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def CountOfVisibleLines(self):
##        '-no docstring-'
##        #return CountOfVisibleLines
##
##    @property
##    def CodeModule(self):
##        '-no docstring-'
##        #return CodeModule
##
##    @property
##    def CodePaneView(self):
##        '-no docstring-'
##        #return pCodePaneview
##
##    def _get(self):
##        '-no docstring-'
##        #return TopLine
##    def _set(self, TopLine):
##        '-no docstring-'
##    TopLine = property(_get, _set, doc = _set.__doc__)
##

class ReferencesEvents(CoClass):
    _reg_clsid_ = GUID('{0002E119-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _ReferencesEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E11A-0000-0000-C000-000000000046}')
    _idlflags_ = ['oleautomation']
class _dispReferencesEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E118-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = []
ReferencesEvents._com_interfaces_ = [_ReferencesEvents]
ReferencesEvents._outgoing_interfaces_ = [_dispReferencesEvents]

class LinkedWindows(CoClass):
    _reg_clsid_ = GUID('{0002E187-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _LinkedWindows(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E16C-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
LinkedWindows._com_interfaces_ = [_LinkedWindows]

class Events(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E167-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation']
class CommandBarEvents(CoClass):
    _reg_clsid_ = GUID('{0002E132-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _CommandBarControlEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E130-0000-0000-C000-000000000046}')
    _idlflags_ = ['oleautomation']
class _dispCommandBarControlEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E131-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = []
CommandBarEvents._com_interfaces_ = [_CommandBarControlEvents]
CommandBarEvents._outgoing_interfaces_ = [_dispCommandBarControlEvents]

Events._methods_ = [
    COMMETHOD([dispid(202), 'propget'], HRESULT, 'ReferencesEvents',
              ( ['in'], POINTER(VBProject), 'VBProject' ),
              ( ['retval', 'out'], POINTER(POINTER(ReferencesEvents)), 'prceNew' )),
    COMMETHOD([dispid(205), 'propget'], HRESULT, 'CommandBarEvents',
              ( ['in'], POINTER(IDispatch), 'CommandBarControl' ),
              ( ['retval', 'out'], POINTER(POINTER(CommandBarEvents)), 'prceNew' )),
]
################################################################
## code template for Events implementation
##class Events_Impl(object):
##    @property
##    def CommandBarEvents(self, CommandBarControl):
##        '-no docstring-'
##        #return prceNew
##
##    @property
##    def ReferencesEvents(self, VBProject):
##        '-no docstring-'
##        #return prceNew
##

class VBComponent(CoClass):
    _reg_clsid_ = GUID('{BE39F3DA-1B13-11D0-887F-00A0C90F2744}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _VBComponent(_VBComponent_Old):
    _case_insensitive_ = True
    _iid_ = GUID('{EEE00921-E393-11D1-BB03-00C04FB6C4A6}')
    _idlflags_ = ['dual', 'oleautomation']
VBComponent._com_interfaces_ = [_VBComponent]

_VBComponents_Old._methods_ = [
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppcReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppptReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
    COMMETHOD([dispid(11)], HRESULT, 'Remove',
              ( ['in'], POINTER(VBComponent), 'VBComponent' )),
    COMMETHOD([dispid(12)], HRESULT, 'Add',
              ( ['in'], vbext_ComponentType, 'ComponentType' ),
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppComponent' )),
    COMMETHOD([dispid(13)], HRESULT, 'Import',
              ( ['in'], BSTR, 'FileName' ),
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppComponent' )),
    COMMETHOD([dispid(20), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
]
################################################################
## code template for _VBComponents_Old implementation
##class _VBComponents_Old_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppptReturn
##
##    def Remove(self, VBComponent):
##        '-no docstring-'
##        #return 
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def Add(self, ComponentType):
##        '-no docstring-'
##        #return lppComponent
##
##    def Import(self, FileName):
##        '-no docstring-'
##        #return lppComponent
##

_VBComponents._methods_ = [
    COMMETHOD([dispid(25)], HRESULT, 'AddCustom',
              ( ['in'], BSTR, 'ProgId' ),
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppComponent' )),
    COMMETHOD([dispid(26), 'hidden'], HRESULT, 'AddMTDesigner',
              ( ['in', 'optional'], c_int, 'index', 0 ),
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppComponent' )),
]
################################################################
## code template for _VBComponents implementation
##class _VBComponents_Impl(object):
##    def AddCustom(self, ProgId):
##        '-no docstring-'
##        #return lppComponent
##
##    def AddMTDesigner(self, index):
##        '-no docstring-'
##        #return lppComponent
##

_dispReferencesEvents._disp_methods_ = [
    DISPMETHOD([dispid(1)], None, 'ItemAdded',
               ( ['in'], POINTER(Reference), 'Reference' )),
    DISPMETHOD([dispid(2)], None, 'ItemRemoved',
               ( ['in'], POINTER(Reference), 'Reference' )),
]
Application._methods_ = [
    COMMETHOD([dispid(100), 'propget'], HRESULT, 'Version',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrReturn' )),
]
################################################################
## code template for Application implementation
##class Application_Impl(object):
##    @property
##    def Version(self):
##        '-no docstring-'
##        #return lpbstrReturn
##

_ReferencesEvents._methods_ = [
]
################################################################
## code template for _ReferencesEvents implementation
##class _ReferencesEvents_Impl(object):

class _dispVBComponentsEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E116-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _methods_ = []
_dispVBComponentsEvents._disp_methods_ = [
    DISPMETHOD([dispid(1)], None, 'ItemAdded',
               ( ['in'], POINTER(VBComponent), 'VBComponent' )),
    DISPMETHOD([dispid(2)], None, 'ItemRemoved',
               ( ['in'], POINTER(VBComponent), 'VBComponent' )),
    DISPMETHOD([dispid(3)], None, 'ItemRenamed',
               ( ['in'], POINTER(VBComponent), 'VBComponent' ),
               ( ['in'], BSTR, 'OldName' )),
    DISPMETHOD([dispid(4)], None, 'ItemSelected',
               ( ['in'], POINTER(VBComponent), 'VBComponent' )),
    DISPMETHOD([dispid(5)], None, 'ItemActivated',
               ( ['in'], POINTER(VBComponent), 'VBComponent' )),
    DISPMETHOD([dispid(6)], None, 'ItemReloaded',
               ( ['in'], POINTER(VBComponent), 'VBComponent' )),
]

# values for enumeration 'vbextFileTypes'
vbextFileTypeForm = 0
vbextFileTypeModule = 1
vbextFileTypeClass = 2
vbextFileTypeProject = 3
vbextFileTypeExe = 4
vbextFileTypeFrx = 5
vbextFileTypeRes = 6
vbextFileTypeUserControl = 7
vbextFileTypePropertyPage = 8
vbextFileTypeDocObject = 9
vbextFileTypeBinary = 10
vbextFileTypeGroupProject = 11
vbextFileTypeDesigners = 12
vbextFileTypes = c_int # enum
class Windows(CoClass):
    _reg_clsid_ = GUID('{0002E185-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _Windows(_Windows_old):
    _case_insensitive_ = True
    _iid_ = GUID('{F57B7ED0-D8AB-11D1-85DF-00C04F98F42C}')
    _idlflags_ = ['dual', 'oleautomation']
Windows._com_interfaces_ = [_Windows]

VBE._methods_ = [
    COMMETHOD([dispid(107), 'propget'], HRESULT, 'VBProjects',
              ( ['retval', 'out'], POINTER(POINTER(VBProjects)), 'lppptReturn' )),
    COMMETHOD([dispid(108), 'propget'], HRESULT, 'CommandBars',
              ( ['retval', 'out'], POINTER(POINTER(comtypes.gen._2DF8D04C_5BFA_101B_BDE5_00AA0044DE52_0_2_7.CommandBars)), 'ppcbs' )),
    COMMETHOD([dispid(109), 'propget'], HRESULT, 'CodePanes',
              ( ['retval', 'out'], POINTER(POINTER(CodePanes)), 'ppCodePanes' )),
    COMMETHOD([dispid(110), 'propget'], HRESULT, 'Windows',
              ( ['retval', 'out'], POINTER(POINTER(Windows)), 'ppwnsVBWindows' )),
    COMMETHOD([dispid(111), 'propget'], HRESULT, 'Events',
              ( ['retval', 'out'], POINTER(POINTER(Events)), 'ppevtEvents' )),
    COMMETHOD([dispid(201), 'propget'], HRESULT, 'ActiveVBProject',
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppptReturn' )),
    COMMETHOD([dispid(201), 'propputref'], HRESULT, 'ActiveVBProject',
              ( ['in'], POINTER(VBProject), 'lppptReturn' )),
    COMMETHOD([dispid(202), 'propget'], HRESULT, 'SelectedVBComponent',
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'lppscReturn' )),
    COMMETHOD([dispid(204), 'propget'], HRESULT, 'MainWindow',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'ppwin' )),
    COMMETHOD([dispid(205), 'propget'], HRESULT, 'ActiveWindow',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'ppwinActive' )),
    COMMETHOD([dispid(206), 'propget'], HRESULT, 'ActiveCodePane',
              ( ['retval', 'out'], POINTER(POINTER(CodePane)), 'ppCodePane' )),
    COMMETHOD([dispid(206), 'propputref'], HRESULT, 'ActiveCodePane',
              ( ['in'], POINTER(CodePane), 'ppCodePane' )),
    COMMETHOD([dispid(209), 'propget'], HRESULT, 'Addins',
              ( ['retval', 'out'], POINTER(POINTER(Addins)), 'lpppAddIns' )),
]
################################################################
## code template for VBE implementation
##class VBE_Impl(object):
##    @property
##    def CodePanes(self):
##        '-no docstring-'
##        #return ppCodePanes
##
##    @property
##    def Windows(self):
##        '-no docstring-'
##        #return ppwnsVBWindows
##
##    @property
##    def SelectedVBComponent(self):
##        '-no docstring-'
##        #return lppscReturn
##
##    @property
##    def MainWindow(self):
##        '-no docstring-'
##        #return ppwin
##
##    @property
##    def ActiveWindow(self):
##        '-no docstring-'
##        #return ppwinActive
##
##    def ActiveVBProject(self, lppptReturn):
##        '-no docstring-'
##        #return 
##
##    def ActiveCodePane(self, ppCodePane):
##        '-no docstring-'
##        #return 
##
##    @property
##    def VBProjects(self):
##        '-no docstring-'
##        #return lppptReturn
##
##    @property
##    def Events(self):
##        '-no docstring-'
##        #return ppevtEvents
##
##    @property
##    def CommandBars(self):
##        '-no docstring-'
##        #return ppcbs
##
##    @property
##    def Addins(self):
##        '-no docstring-'
##        #return lpppAddIns
##


# values for enumeration 'vbext_WindowType'
vbext_wt_CodeWindow = 0
vbext_wt_Designer = 1
vbext_wt_Browser = 2
vbext_wt_Watch = 3
vbext_wt_Locals = 4
vbext_wt_Immediate = 5
vbext_wt_ProjectWindow = 6
vbext_wt_PropertyWindow = 7
vbext_wt_Find = 8
vbext_wt_FindReplace = 9
vbext_wt_Toolbox = 10
vbext_wt_LinkedWindowFrame = 11
vbext_wt_MainWindow = 12
vbext_wt_ToolWindow = 15
vbext_WindowType = c_int # enum
_AddIns._methods_ = [
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(AddIn)), 'lppaddin' )),
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppVBA' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'lppVBA' )),
    COMMETHOD([dispid(40), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
    COMMETHOD([dispid(41)], HRESULT, 'Update'),
]
################################################################
## code template for _AddIns implementation
##class _AddIns_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppVBA
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppVBA
##
##    def Update(self):
##        '-no docstring-'
##        #return 
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppaddin
##

_Windows._methods_ = [
    COMMETHOD([dispid(300)], HRESULT, 'CreateToolWindow',
              ( ['in'], POINTER(AddIn), 'AddInInst' ),
              ( ['in'], BSTR, 'ProgId' ),
              ( ['in'], BSTR, 'Caption' ),
              ( ['in'], BSTR, 'GuidPosition' ),
              ( ['in', 'out'], POINTER(POINTER(IDispatch)), 'DocObj' ),
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'lppcReturn' )),
]
################################################################
## code template for _Windows implementation
##class _Windows_Impl(object):
##    def CreateToolWindow(self, AddInInst, ProgId, Caption, GuidPosition):
##        '-no docstring-'
##        #return DocObj, lppcReturn
##

class Components(CoClass):
    _reg_clsid_ = GUID('{BE39F3D6-1B13-11D0-887F-00A0C90F2744}')
    _idlflags_ = ['hidden']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _Components(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E161-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
Components._com_interfaces_ = [_Components]

_dispReferences_Events._disp_methods_ = [
    DISPMETHOD([dispid(0)], None, 'ItemAdded',
               ( [], POINTER(Reference), 'Reference' )),
    DISPMETHOD([dispid(1)], None, 'ItemRemoved',
               ( [], POINTER(Reference), 'Reference' )),
]
class Component(CoClass):
    _reg_clsid_ = GUID('{BE39F3D8-1B13-11D0-887F-00A0C90F2744}')
    _idlflags_ = ['hidden']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
class _Component(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E163-0000-0000-C000-000000000046}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
Component._com_interfaces_ = [_Component]


# values for enumeration 'vbext_ProcKind'
vbext_pk_Proc = 0
vbext_pk_Let = 1
vbext_pk_Set = 2
vbext_pk_Get = 3
vbext_ProcKind = c_int # enum
_Components._methods_ = [
    COMMETHOD([dispid(0), 'hidden'], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Component)), 'lppcReturn' )),
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppptReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
    COMMETHOD([dispid(11)], HRESULT, 'Remove',
              ( ['in'], POINTER(Component), 'Component' )),
    COMMETHOD([dispid(12)], HRESULT, 'Add',
              ( ['in'], vbext_ComponentType, 'ComponentType' ),
              ( ['retval', 'out'], POINTER(POINTER(Component)), 'lppComponent' )),
    COMMETHOD([dispid(13)], HRESULT, 'Import',
              ( ['in'], BSTR, 'FileName' ),
              ( ['retval', 'out'], POINTER(POINTER(Component)), 'lppComponent' )),
    COMMETHOD([dispid(20), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
]
################################################################
## code template for _Components implementation
##class _Components_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppptReturn
##
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    def Remove(self, Component):
##        '-no docstring-'
##        #return 
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def Add(self, ComponentType):
##        '-no docstring-'
##        #return lppComponent
##
##    def Import(self, FileName):
##        '-no docstring-'
##        #return lppComponent
##

_VBProjects._methods_ = [
    COMMETHOD([dispid(137)], HRESULT, 'Add',
              ( ['in'], vbext_ProjectType, 'Type' ),
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppcReturn' )),
    COMMETHOD([dispid(138)], HRESULT, 'Remove',
              ( ['in'], POINTER(VBProject), 'lpc' )),
    COMMETHOD([dispid(139)], HRESULT, 'Open',
              ( ['in'], BSTR, 'bstrPath' ),
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lpc' )),
]
################################################################
## code template for _VBProjects implementation
##class _VBProjects_Impl(object):
##    def Add(self, Type):
##        '-no docstring-'
##        #return lppcReturn
##
##    def Open(self, bstrPath):
##        '-no docstring-'
##        #return lpc
##
##    def Remove(self, lpc):
##        '-no docstring-'
##        #return 
##

_References._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'retval' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'retval' )),
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Reference)), 'Reference' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(-4)], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppenum' )),
    COMMETHOD([dispid(1610743813)], HRESULT, 'AddFromGuid',
              ( ['in'], BSTR, 'Guid' ),
              ( ['in'], c_int, 'Major' ),
              ( ['in'], c_int, 'Minor' ),
              ( ['retval', 'out'], POINTER(POINTER(Reference)), 'Reference' )),
    COMMETHOD([dispid(1610743814)], HRESULT, 'AddFromFile',
              ( ['in'], BSTR, 'FileName' ),
              ( ['retval', 'out'], POINTER(POINTER(Reference)), 'Reference' )),
    COMMETHOD([dispid(1610743815)], HRESULT, 'Remove',
              ( ['in'], POINTER(Reference), 'Reference' )),
]
################################################################
## code template for _References implementation
##class _References_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return Count
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return ppenum
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return retval
##
##    def Remove(self, Reference):
##        '-no docstring-'
##        #return 
##
##    def AddFromFile(self, FileName):
##        '-no docstring-'
##        #return Reference
##
##    def Item(self, index):
##        '-no docstring-'
##        #return Reference
##
##    def AddFromGuid(self, Guid, Major, Minor):
##        '-no docstring-'
##        #return Reference
##

_VBComponent._methods_ = [
    COMMETHOD([dispid(64), 'propget'], HRESULT, 'DesignerID',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrReturn' )),
]
################################################################
## code template for _VBComponent implementation
##class _VBComponent_Impl(object):
##    @property
##    def DesignerID(self):
##        '-no docstring-'
##        #return pbstrReturn
##

_CodePanes._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'retval' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'retval' )),
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(CodePane)), 'CodePane' )),
    COMMETHOD([dispid(1610743811), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(-4)], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppenum' )),
    COMMETHOD([dispid(1610743813), 'hidden', 'propget'], HRESULT, 'Current',
              ( ['retval', 'out'], POINTER(POINTER(CodePane)), 'CodePane' )),
    COMMETHOD([dispid(1610743813), 'hidden', 'propput'], HRESULT, 'Current',
              ( ['in'], POINTER(CodePane), 'CodePane' )),
]
################################################################
## code template for _CodePanes implementation
##class _CodePanes_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return Count
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return ppenum
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return retval
##
##    def _get(self):
##        '-no docstring-'
##        #return CodePane
##    def _set(self, CodePane):
##        '-no docstring-'
##    Current = property(_get, _set, doc = _set.__doc__)
##
##    def Item(self, index):
##        '-no docstring-'
##        #return CodePane
##

class _VBProjectsEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0002E113-0000-0000-C000-000000000046}')
    _idlflags_ = ['oleautomation']
_VBProjectsEvents._methods_ = [
]
################################################################
## code template for _VBProjectsEvents implementation
##class _VBProjectsEvents_Impl(object):

_CommandBarControlEvents._methods_ = [
]
################################################################
## code template for _CommandBarControlEvents implementation
##class _CommandBarControlEvents_Impl(object):

_LinkedWindows._methods_ = [
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'hidden', 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'ppptReturn' )),
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], VARIANT, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'lppcReturn' )),
    COMMETHOD([dispid(201), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
    COMMETHOD([dispid(202)], HRESULT, 'Remove',
              ( ['in'], POINTER(Window), 'Window' )),
    COMMETHOD([dispid(203)], HRESULT, 'Add',
              ( ['in'], POINTER(Window), 'Window' )),
]
################################################################
## code template for _LinkedWindows implementation
##class _LinkedWindows_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return ppptReturn
##
##    def Remove(self, Window):
##        '-no docstring-'
##        #return 
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def Add(self, Window):
##        '-no docstring-'
##        #return 
##

_dispCommandBarControlEvents._disp_methods_ = [
    DISPMETHOD([dispid(1)], None, 'Click',
               ( ['in'], POINTER(IDispatch), 'CommandBarControl' ),
               ( ['in'], POINTER(VARIANT_BOOL), 'handled' ),
               ( ['in'], POINTER(VARIANT_BOOL), 'CancelDefault' )),
]
class Library(object):
    u'Microsoft Visual Basic for Applications Extensibility 5.3'
    name = u'VBIDE'
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)

_CodeModule._methods_ = [
    COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBComponent)), 'retval' )),
    COMMETHOD([dispid(1610743809), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'retval' )),
    COMMETHOD([dispid(0), 'hidden', 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrName' )),
    COMMETHOD([dispid(0), 'hidden', 'propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'pbstrName' )),
    COMMETHOD([dispid(1610743812)], HRESULT, 'AddFromString',
              ( ['in'], BSTR, 'String' )),
    COMMETHOD([dispid(1610743813)], HRESULT, 'AddFromFile',
              ( ['in'], BSTR, 'FileName' )),
    COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'Lines',
              ( ['in'], c_int, 'StartLine' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(BSTR), 'String' )),
    COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'CountOfLines',
              ( ['retval', 'out'], POINTER(c_int), 'CountOfLines' )),
    COMMETHOD([dispid(1610743816)], HRESULT, 'InsertLines',
              ( ['in'], c_int, 'Line' ),
              ( ['in'], BSTR, 'String' )),
    COMMETHOD([dispid(1610743817)], HRESULT, 'DeleteLines',
              ( ['in'], c_int, 'StartLine' ),
              ( ['in', 'optional'], c_int, 'Count', 1 )),
    COMMETHOD([dispid(1610743818)], HRESULT, 'ReplaceLine',
              ( ['in'], c_int, 'Line' ),
              ( ['in'], BSTR, 'String' )),
    COMMETHOD([dispid(1610743819), 'propget'], HRESULT, 'ProcStartLine',
              ( ['in'], BSTR, 'ProcName' ),
              ( ['in'], vbext_ProcKind, 'ProcKind' ),
              ( ['retval', 'out'], POINTER(c_int), 'ProcStartLine' )),
    COMMETHOD([dispid(1610743820), 'propget'], HRESULT, 'ProcCountLines',
              ( ['in'], BSTR, 'ProcName' ),
              ( ['in'], vbext_ProcKind, 'ProcKind' ),
              ( ['retval', 'out'], POINTER(c_int), 'ProcCountLines' )),
    COMMETHOD([dispid(1610743821), 'propget'], HRESULT, 'ProcBodyLine',
              ( ['in'], BSTR, 'ProcName' ),
              ( ['in'], vbext_ProcKind, 'ProcKind' ),
              ( ['retval', 'out'], POINTER(c_int), 'ProcBodyLine' )),
    COMMETHOD([dispid(1610743822), 'propget'], HRESULT, 'ProcOfLine',
              ( ['in'], c_int, 'Line' ),
              ( ['out'], POINTER(vbext_ProcKind), 'ProcKind' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrName' )),
    COMMETHOD([dispid(1610743823), 'propget'], HRESULT, 'CountOfDeclarationLines',
              ( ['retval', 'out'], POINTER(c_int), 'pDeclCountOfLines' )),
    COMMETHOD([dispid(1610743824)], HRESULT, 'CreateEventProc',
              ( ['in'], BSTR, 'EventName' ),
              ( ['in'], BSTR, 'ObjectName' ),
              ( ['retval', 'out'], POINTER(c_int), 'Line' )),
    COMMETHOD([dispid(1610743825)], HRESULT, 'Find',
              ( ['in'], BSTR, 'Target' ),
              ( ['in', 'out'], POINTER(c_int), 'StartLine' ),
              ( ['in', 'out'], POINTER(c_int), 'StartColumn' ),
              ( ['in', 'out'], POINTER(c_int), 'EndLine' ),
              ( ['in', 'out'], POINTER(c_int), 'EndColumn' ),
              ( ['in', 'optional'], VARIANT_BOOL, 'WholeWord', False ),
              ( ['in', 'optional'], VARIANT_BOOL, 'MatchCase', False ),
              ( ['in', 'optional'], VARIANT_BOOL, 'PatternSearch', False ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pfFound' )),
    COMMETHOD([dispid(1610743826), 'propget'], HRESULT, 'CodePane',
              ( ['retval', 'out'], POINTER(POINTER(CodePane)), 'CodePane' )),
]
################################################################
## code template for _CodeModule implementation
##class _CodeModule_Impl(object):
##    @property
##    def CodePane(self):
##        '-no docstring-'
##        #return CodePane
##
##    def AddFromString(self, String):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CountOfDeclarationLines(self):
##        '-no docstring-'
##        #return pDeclCountOfLines
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return retval
##
##    @property
##    def ProcCountLines(self, ProcName, ProcKind):
##        '-no docstring-'
##        #return ProcCountLines
##
##    def Find(self, Target, WholeWord, MatchCase, PatternSearch):
##        '-no docstring-'
##        #return StartLine, StartColumn, EndLine, EndColumn, pfFound
##
##    def CreateEventProc(self, EventName, ObjectName):
##        '-no docstring-'
##        #return Line
##
##    @property
##    def ProcOfLine(self, Line):
##        '-no docstring-'
##        #return ProcKind, pbstrName
##
##    @property
##    def Lines(self, StartLine, Count):
##        '-no docstring-'
##        #return String
##
##    @property
##    def ProcBodyLine(self, ProcName, ProcKind):
##        '-no docstring-'
##        #return ProcBodyLine
##
##    def InsertLines(self, Line, String):
##        '-no docstring-'
##        #return 
##
##    def AddFromFile(self, FileName):
##        '-no docstring-'
##        #return 
##
##    @property
##    def ProcStartLine(self, ProcName, ProcKind):
##        '-no docstring-'
##        #return ProcStartLine
##
##    def DeleteLines(self, StartLine, Count):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CountOfLines(self):
##        '-no docstring-'
##        #return CountOfLines
##
##    def ReplaceLine(self, Line, String):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return pbstrName
##    def _set(self, pbstrName):
##        '-no docstring-'
##    Name = property(_get, _set, doc = _set.__doc__)
##

class ProjectTemplate(CoClass):
    _reg_clsid_ = GUID('{32CDF9E0-1602-11CE-BFDC-08002B2B8CDA}')
    _idlflags_ = ['hidden']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{0002E157-0000-0000-C000-000000000046}', 5, 3)
ProjectTemplate._com_interfaces_ = [_ProjectTemplate]

Window._methods_ = [
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(Windows)), 'lppaReturn' )),
    COMMETHOD([dispid(99)], HRESULT, 'Close'),
    COMMETHOD([dispid(100), 'propget'], HRESULT, 'Caption',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrTitle' )),
    COMMETHOD([dispid(106), 'propget'], HRESULT, 'Visible',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pfVisible' )),
    COMMETHOD([dispid(106), 'propput'], HRESULT, 'Visible',
              ( ['in'], VARIANT_BOOL, 'pfVisible' )),
    COMMETHOD([dispid(101), 'propget'], HRESULT, 'Left',
              ( ['retval', 'out'], POINTER(c_int), 'plLeft' )),
    COMMETHOD([dispid(101), 'propput'], HRESULT, 'Left',
              ( ['in'], c_int, 'plLeft' )),
    COMMETHOD([dispid(103), 'propget'], HRESULT, 'Top',
              ( ['retval', 'out'], POINTER(c_int), 'plTop' )),
    COMMETHOD([dispid(103), 'propput'], HRESULT, 'Top',
              ( ['in'], c_int, 'plTop' )),
    COMMETHOD([dispid(105), 'propget'], HRESULT, 'Width',
              ( ['retval', 'out'], POINTER(c_int), 'plWidth' )),
    COMMETHOD([dispid(105), 'propput'], HRESULT, 'Width',
              ( ['in'], c_int, 'plWidth' )),
    COMMETHOD([dispid(107), 'propget'], HRESULT, 'Height',
              ( ['retval', 'out'], POINTER(c_int), 'plHeight' )),
    COMMETHOD([dispid(107), 'propput'], HRESULT, 'Height',
              ( ['in'], c_int, 'plHeight' )),
    COMMETHOD([dispid(109), 'propget'], HRESULT, 'WindowState',
              ( ['retval', 'out'], POINTER(vbext_WindowState), 'plWindowState' )),
    COMMETHOD([dispid(109), 'propput'], HRESULT, 'WindowState',
              ( ['in'], vbext_WindowState, 'plWindowState' )),
    COMMETHOD([dispid(111)], HRESULT, 'SetFocus'),
    COMMETHOD([dispid(112), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(vbext_WindowType), 'pKind' )),
    COMMETHOD([dispid(113), 'restricted', 'hidden'], HRESULT, 'SetKind',
              ( ['in'], vbext_WindowType, 'eKind' )),
    COMMETHOD([dispid(116), 'propget'], HRESULT, 'LinkedWindows',
              ( ['retval', 'out'], POINTER(POINTER(LinkedWindows)), 'ppwnsCollection' )),
    COMMETHOD([dispid(117), 'propget'], HRESULT, 'LinkedWindowFrame',
              ( ['retval', 'out'], POINTER(POINTER(Window)), 'ppwinFrame' )),
    COMMETHOD([dispid(118), 'restricted', 'hidden'], HRESULT, 'Detach'),
    COMMETHOD([dispid(119), 'restricted', 'hidden'], HRESULT, 'Attach',
              ( ['in'], c_int, 'lWindowHandle' )),
    COMMETHOD([dispid(120), 'hidden', 'propget'], HRESULT, 'HWnd',
              ( ['retval', 'out'], POINTER(c_int), 'plWindowHandle' )),
]
################################################################
## code template for Window implementation
##class Window_Impl(object):
##    def SetFocus(self):
##        '-no docstring-'
##        #return 
##
##    def SetKind(self, eKind):
##        '-no docstring-'
##        #return 
##
##    def Detach(self):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return plWidth
##    def _set(self, plWidth):
##        '-no docstring-'
##    Width = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    @property
##    def Caption(self):
##        '-no docstring-'
##        #return pbstrTitle
##
##    @property
##    def HWnd(self):
##        '-no docstring-'
##        #return plWindowHandle
##
##    def _get(self):
##        '-no docstring-'
##        #return plTop
##    def _set(self, plTop):
##        '-no docstring-'
##    Top = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return plHeight
##    def _set(self, plHeight):
##        '-no docstring-'
##    Height = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return plWindowState
##    def _set(self, plWindowState):
##        '-no docstring-'
##    WindowState = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return pfVisible
##    def _set(self, pfVisible):
##        '-no docstring-'
##    Visible = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def LinkedWindowFrame(self):
##        '-no docstring-'
##        #return ppwinFrame
##
##    def Close(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def LinkedWindows(self):
##        '-no docstring-'
##        #return ppwnsCollection
##
##    @property
##    def Type(self):
##        '-no docstring-'
##        #return pKind
##
##    def Attach(self, lWindowHandle):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return plLeft
##    def _set(self, plLeft):
##        '-no docstring-'
##    Left = property(_get, _set, doc = _set.__doc__)
##

Property._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Value',
              ( ['retval', 'out'], POINTER(VARIANT), 'lppvReturn' )),
    COMMETHOD([dispid(0), 'propput'], HRESULT, 'Value',
              ( ['in'], VARIANT, 'lppvReturn' )),
    COMMETHOD([dispid(3), 'propget'], HRESULT, 'IndexedValue',
              ( ['in'], VARIANT, 'Index1' ),
              ( ['in', 'optional'], VARIANT, 'Index2' ),
              ( ['in', 'optional'], VARIANT, 'Index3' ),
              ( ['in', 'optional'], VARIANT, 'Index4' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'lppvReturn' )),
    COMMETHOD([dispid(3), 'propput'], HRESULT, 'IndexedValue',
              ( ['in'], VARIANT, 'Index1' ),
              ( ['in', 'optional'], VARIANT, 'Index2' ),
              ( ['in', 'optional'], VARIANT, 'Index3' ),
              ( ['in', 'optional'], VARIANT, 'Index4' ),
              ( ['in'], VARIANT, 'lppvReturn' )),
    COMMETHOD([dispid(4), 'propget'], HRESULT, 'NumIndices',
              ( ['retval', 'out'], POINTER(c_short), 'lpiRetVal' )),
    COMMETHOD([dispid(1), 'hidden', 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lpaReturn' )),
    COMMETHOD([dispid(2), 'hidden', 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(Properties)), 'lpppReturn' )),
    COMMETHOD([dispid(40), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'lpbstrReturn' )),
    COMMETHOD([dispid(41), 'propget'], HRESULT, 'VBE',
              ( ['retval', 'out'], POINTER(POINTER(VBE)), 'lpaReturn' )),
    COMMETHOD([dispid(42), 'propget'], HRESULT, 'Collection',
              ( ['retval', 'out'], POINTER(POINTER(Properties)), 'lpppReturn' )),
    COMMETHOD([dispid(45), 'propget'], HRESULT, 'Object',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppunk' )),
    COMMETHOD([dispid(45), 'propputref'], HRESULT, 'Object',
              ( ['in'], POINTER(IUnknown), 'lppunk' )),
]
################################################################
## code template for Property implementation
##class Property_Impl(object):
##    @property
##    def VBE(self):
##        '-no docstring-'
##        #return lpaReturn
##
##    @property
##    def NumIndices(self):
##        '-no docstring-'
##        #return lpiRetVal
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lpppReturn
##
##    def Object(self, lppunk):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return lppvReturn
##    def _set(self, lppvReturn):
##        '-no docstring-'
##    Value = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lpaReturn
##
##    @property
##    def Collection(self):
##        '-no docstring-'
##        #return lpppReturn
##
##    def _get(self, Index1, Index2, Index3, Index4):
##        '-no docstring-'
##        #return lppvReturn
##    def _set(self, Index1, Index2, Index3, Index4, lppvReturn):
##        '-no docstring-'
##    IndexedValue = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Name(self):
##        '-no docstring-'
##        #return lpbstrReturn
##

_Component._methods_ = [
    COMMETHOD([dispid(1), 'hidden', 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'hidden', 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(Components)), 'lppcReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'IsDirty',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'lpfReturn' )),
    COMMETHOD([dispid(10), 'propput'], HRESULT, 'IsDirty',
              ( ['in'], VARIANT_BOOL, 'lpfReturn' )),
    COMMETHOD([dispid(48), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstrReturn' )),
    COMMETHOD([dispid(48), 'propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'pbstrReturn' )),
]
################################################################
## code template for _Component implementation
##class _Component_Impl(object):
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lppaReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return pbstrReturn
##    def _set(self, pbstrReturn):
##        '-no docstring-'
##    Name = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppcReturn
##
##    def _get(self):
##        '-no docstring-'
##        #return lpfReturn
##    def _set(self, lpfReturn):
##        '-no docstring-'
##    IsDirty = property(_get, _set, doc = _set.__doc__)
##

class SelectedComponents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{BE39F3D4-1B13-11D0-887F-00A0C90F2744}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
SelectedComponents._methods_ = [
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], c_int, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(Component)), 'lppcReturn' )),
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'Application',
              ( ['retval', 'out'], POINTER(POINTER(Application)), 'lppaReturn' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(VBProject)), 'lppptReturn' )),
    COMMETHOD([dispid(10), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'lplReturn' )),
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'lppiuReturn' )),
]
################################################################
## code template for SelectedComponents implementation
##class SelectedComponents_Impl(object):
##    @property
##    def Count(self):
##        '-no docstring-'
##        #return lplReturn
##
##    def Item(self, index):
##        '-no docstring-'
##        #return lppcReturn
##
##    def _NewEnum(self):
##        '-no docstring-'
##        #return lppiuReturn
##
##    @property
##    def Parent(self):
##        '-no docstring-'
##        #return lppptReturn
##
##    @property
##    def Application(self):
##        '-no docstring-'
##        #return lppaReturn
##

__all__ = ['CodePanes', 'vbextFileTypeRes', 'Component',
           '_VBProjects', '_dispVBComponentsEvents', '_VBComponent',
           'LinkedWindows', 'vbextFileTypeModule', 'vbext_VBAMode',
           'vbext_WindowState', 'CommandBarEvents', '_Component',
           'vbext_CodePaneview', 'vbext_wt_Browser', '_Windows_old',
           'AddIn', '_VBComponent_Old', '_VBComponents_Old',
           '_CommandBarControlEvents', '_AddIns',
           'SelectedComponents', 'Components',
           '_dispCommandBarControlEvents', 'vbext_WindowType',
           '_VBProjectsEvents', 'Reference', 'vbext_ProcKind',
           'vbext_RefKind', 'CodeModule', 'vbext_ct_Document',
           'vbext_wt_FindReplace', 'vbextFileTypeProject',
           'Application', 'Addins', 'vbextFileTypeBinary',
           'vbext_ComponentType', 'vbext_ProjectProtection',
           'vbext_rk_TypeLib', 'vbext_wt_PropertyWindow',
           'vbext_pk_Set', 'vbext_wt_Locals', 'vbext_ct_MSForm',
           'vbext_ProjectType', '_Windows', 'vbext_pk_Get',
           '_Components', '_dispVBProjectsEvents', 'vbext_pp_locked',
           'Property', '_VBProjects_Old', 'vbext_wt_Immediate',
           'vbext_ct_StdModule', 'VBComponent', 'vbext_wt_Designer',
           'vbext_wt_LinkedWindowFrame', 'vbext_vm_Run',
           'vbextFileTypes', '_VBComponentsEvents', 'vbext_wt_Find',
           '_ReferencesEvents', 'vbext_wt_Toolbox', 'VBE',
           '_CodeModule', 'vbext_pp_none', 'vbext_cv_ProcedureView',
           'Events', 'VBProject', 'vbext_pt_HostProject',
           'vbextFileTypeGroupProject', '_VBComponents',
           'vbext_ws_Normal', 'vbext_wt_MainWindow',
           'vbextFileTypeExe', 'vbext_ct_ActiveXDesigner',
           '_dispReferences_Events', 'vbextFileTypeForm',
           'Properties', 'vbext_ws_Minimize', 'vbext_wt_ToolWindow',
           '_CodePanes', 'vbext_vm_Break', '_Properties',
           'vbextFileTypeFrx', 'CodePane', 'vbext_pk_Let',
           'vbext_ct_ClassModule', '_References', 'vbext_pk_Proc',
           'Window', 'vbext_wt_Watch', 'References',
           'vbextFileTypePropertyPage', '_LinkedWindows',
           'vbext_rk_Project', 'VBProjects', 'ReferencesEvents',
           'vbext_pt_StandAlone', 'ProjectTemplate',
           'vbextFileTypeClass', 'VBComponents',
           'vbext_cv_FullModuleView', 'vbext_ws_Maximize',
           'vbext_wt_ProjectWindow', '_VBProject',
           'vbextFileTypeDocObject', 'vbext_wt_CodeWindow',
           '_VBProject_Old', 'Windows', '_ProjectTemplate',
           'vbextFileTypeUserControl', 'vbextFileTypeDesigners',
           '_CodePane', '_dispReferencesEvents', 'vbext_vm_Design']
from comtypes import _check_version; _check_version('501')

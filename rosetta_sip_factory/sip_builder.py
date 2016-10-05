import os
import shutil

from lxml import etree as ET

from pydc import factory as dc_factory
from pydnx import factory as dnx_factory
from pymets import mets_factory
from mets_dnx.factory import build_mets


# declare namespaces
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

dc_nsmap = {
    "dc": DC_NS,
    "dcterms": DCTERMS_NS,
    "xsi": XSI_NS,
}

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def build_sip(ie_dmd_dict=None,
        pres_master_dir=None, 
        modified_master_dir=None,
        access_derivative_dir=None,
        cms=None,
        webHarvesting=None,
        generalIECharacteristics=None,
        objectIdentifier=None,
        accessRightsPolicy=None,
        eventList=None,
        input_dir=None,
        digital_original=False,
        sip_title=None,
        output_folder=None):

    # build METS
    mets = build_mets(ie_dmd_dict=ie_dmd_dict,
        pres_master_dir=pres_master_dir, 
        modified_master_dir=modified_master_dir,
        access_derivative_dir=access_derivative_dir,
        cms=cms,
        webHarvesting=webHarvesting,
        generalIECharacteristics=generalIECharacteristics,
        objectIdentifier=objectIdentifier,
        accessRightsPolicy=accessRightsPolicy,
        eventList=eventList,
        input_dir=input_dir,
        digital_original=digital_original)

    # build output SIP folder structure
    streams_dir = os.path.join(output_folder, 'content', 'streams')
    os.makedirs(streams_dir)
    if pres_master_dir != None:
        destination = os.path.join(
            streams_dir, 
            os.path.basename(pres_master_dir))
        os.makedirs(destination)
        copytree(pres_master_dir, destination)
    if modified_master_dir != None:
        destination = os.path.join(
            streams_dir, 
            os.path.basename(modified_master_dir))
        os.makedirs(destination)
        copytree(pres_master_dir, destination)
    if access_derivative_dir != None:
        destination = os.path.join(
            streams_dir, 
            os.path.basename(access_derivative_dir))
        os.makedirs(destination)
        copytree(pres_master_dir, destination)


    with open(os.path.join(
                output_folder, 
                'content', 
                'mets.xml'), 
            'w') as metsfile:
        metsfile.write(ET.tounicode(mets, pretty_print=True))
    
    # write SIP DC file if SIP title is supplied
    if sip_title != None:
        dc_xml = ET.Element('{%s}record' % DC_NS, nsmap=dc_nsmap)
        title = ET.SubElement(dc_xml, '{%s}title' % DC_NS, nsmap=dc_nsmap)
        title.text = sip_title
        with open(os.path.join(
                    output_folder,
                   'content', 
                   'dc.xml'), 
                    'wb') as dc_file:
            dc_file.write(ET.tostring(dc_xml, xml_declaration=True,
                encoding="UTF-8"))
import json
import os
import shutil

from lxml import etree as ET

from pydc import factory as dc_factory
from pydnx import factory as dnx_factory
from pymets import mets_factory
from mets_dnx.factory import build_mets, build_single_file_mets, build_mets_from_json


# declare namespaces
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

dc_nsmap = {
    "dc": DC_NS,
    "dcterms": DCTERMS_NS,
    "xsi": XSI_NS,
}

mets_dnx_nsmap = {
    'mets': 'http://www.loc.gov/METS/',
    'dnx': 'http://www.exlibrisgroup.com/dps/dnx'
}

def _build_dc_sip(output_dir, sip_title):
    dc_xml = ET.Element('{%s}record' % DC_NS, nsmap=dc_nsmap)
    title = ET.SubElement(dc_xml, '{%s}title' % DC_NS, nsmap=dc_nsmap)
    title.text = sip_title
    with open(os.path.join(
                output_dir,
               'content', 
               'dc.xml'), 
                'wb') as dc_file:
        dc_file.write(ET.tostring(dc_xml, xml_declaration=True,
            encoding="UTF-8"))

def _copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def build_sip(
        ie_dmd_dict=None,
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
        output_dir=None):
    """
    Builds Submission Information Package.

    Moves the nominated files and folders into a Rosetta-friendly SIP
    structure and creates a METS XML files describing the SIP.

    Args:
        ie_dmd_dict: A dictionary inside a list, with each of the keys
            being the dc or dcterms element (with a dc or dcterms 
            prefix), and the dictionary. values being the dc/dcterms
            values e.g: 
            [{'dc:title': 'Sample Title', 'dc:identifier': '0001'}].
            The list must be a maximum length of 1.
        pres_master_dir: A string representing the location of the
            preservation master directory. Can, of course, receive an
            os.path.join() constrcution. All SIPs must have a 
            pres_master_dir.
        modified_master_dir: A string representing the location of the 
            modified master directory. Can take an os.path.join()
            construction.
        access_derivative_dir: A string representing the location of
            the access derivative directory. Can take an os.path.join()
            construction.
        cms = A dictionary inside a list. Allowed keys are 'system' and
            'recordId'. Values must be strings. e.g.
            [{'system': 'ilsdb', 'recordId': '7718a'}]
            The list must be a maximum length of 1.
        webHarvesting: A dictionary inside a list. For describing a 
            deposit from the Web Curator Tool. Allowed keys are
            'primarySeedURL', 'WCTIdentifier', 'targetName', 'group',
            'harvestDate' and 'harvestTime'. Values must be strings.
            e.g.
            [{'primarySeedUrl': 'http://www.sample.com', 
              'targetName': 'Sample Website'}]
            The list must be a maximum length of 1.
        generalIECharacteristics: A dictionary inside a list. Allowed
            keys are 'submissionReason', 'status', 'statusDate',
            'IEEntityType', 'UserDefinedA', 'UserDefinedB' and
            'UserDefinedC'. Values must be strings. e.g.
            [{'submissionReason': 'Web Harvesting',
              'IEEntityType': 'webHarvestIE'}]
            The list must be a maximum length of 1.
        objectIdentifier: A dictionary inside a list. Allowed keys are
            'objectIdentifierType' and 'objectIdentifierValue'. Values
            must be strings. e.g.
            [{'objectIdentifierType': 'ALMAMMS',
              'objectIdentifierValue': '99935273554528'}]
            The list must be a maximum length of 1.
        accessRightsPolicy: A dictionary inside a list. Allowed keys
            are 'policyId' and 'policyDescription'. Values must be
            strings. e.g.
            [{'policyId': '100', 'policyDescription': 'Open Access'}]
            The list must be a maximum length of 1.
        eventList: A list of dictionaries. Allowed keys are 
            'eventIdentifierType', 'eventIdentifierValue', 'eventType',
            'eventDescription', 'eventDateTime', 'eventOutcome1',
            'eventOutcomeDetail1', 'eventOutcomeDetailExtension1',
            'eventOutcome2', 'eventOutcomeDetail2',
            'eventOutcomeDetailExtension2', 'eventOutcome2',
            'eventOutcomeDetail2', 'eventOutcomeDetailExtension2',
            'linkingAgentIdentifierXMLID1',
            'linkingAgentIdentifierType1',
            'linkingAgentIdentifierValue1', 'linkingAgentRole1',
            'linkingAgentIdentifierXMLID2',
            'linkingAgentIdentifierType2',
            'linkingAgentIdentifierValue2', 'linkingAgentRole2',
            'linkingAgentIdentifierXMLID3',
            'linkingAgentIdentifierType3',
            'linkingAgentIdentifierValue3' and 'linkingAgentRole3'.
            Values must be strings. e.g.
            [{'eventType': 'PRE-DEPOSIT', 
              'eventDescription': 'changed foo to bar',
              'eventDateTime': '2016-03-14 14:22:01',
              'eventOutcome1': 'SUCCESS'}]
            The list may contain any number of dictionaries. Each 
            dictionary represents a separate event.
        input_dir: The root directory of the group of files or folders
            that will be turned into a SIP. Can take an os.path.join() 
            construction. If the SIP consists only of a single
            representation, this value will most probably be the same
            as pres_master_dir.
        digital_original: Boolen value. Describes whether the
            Intellectual Entity is a born-digital resource or not.
            Default is False.
        sip_title: A string. If this is supplied, then a dc.xml file
            will be added to the SIP, where a dc:title element will be
            populated with the string as its value.
        output_dir: A string representing where on the file system the
            SIP should be written to. Will accept an os.path.join()
            construction.
    """

    # build METS
    mets = build_mets(
        ie_dmd_dict=ie_dmd_dict,
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
    streams_dir = os.path.join(output_dir, 'content', 'streams')
    os.makedirs(streams_dir)
    if pres_master_dir != None:
        # 2016-10-26: casing for where PM is the same as
        # input_dir, in which case, omit the parent dir
        # for the stream and throw the file straight into
        # the streams dir
        if (modified_master_dir == None and 
            access_derivative_dir == None and
            input_dir == pres_master_dir):
            destination = os.path.join(streams_dir)
        else:
            destination = os.path.join(
                streams_dir, 
                os.path.basename(pres_master_dir))
            os.makedirs(destination)
        _copytree(pres_master_dir, destination)
    if modified_master_dir != None:
        destination = os.path.join(
            streams_dir, 
            os.path.basename(modified_master_dir))
        os.makedirs(destination)
        _copytree(pres_master_dir, destination)
    if access_derivative_dir != None:
        destination = os.path.join(
            streams_dir, 
            os.path.basename(access_derivative_dir))
        os.makedirs(destination)
        _copytree(pres_master_dir, destination)


    mets.write(os.path.join(output_dir, 'content', 'mets.xml'), pretty_print=True)
    
    # write SIP DC file if SIP title is supplied
    if sip_title != None:
        _build_dc_sip(output_dir, sip_title)


def build_single_file_sip(ie_dmd_dict=None,
        filepath=None,
        cms=None,
        webHarvesting=None,
        generalIECharacteristics=None,
        objectIdentifier=None,
        accessRightsPolicy=None,
        eventList=None,
        digital_original=False,
        sip_title=None,
        output_dir=None):
    # build mets
    mets = build_single_file_mets(ie_dmd_dict=ie_dmd_dict,
                filepath=filepath,
                cms=cms,
                webHarvesting=webHarvesting,
                generalIECharacteristics=generalIECharacteristics,
                objectIdentifier=objectIdentifier,
                accessRightsPolicy=accessRightsPolicy,
                eventList=eventList,
                digital_original=digital_original)
    

    # build output SIP folder structure
    streams_dir = os.path.join(output_dir, 'content', 'streams')
    os.makedirs(streams_dir)
    shutil.copy2(filepath, os.path.join(streams_dir,
                    os.path.basename(filepath)))
    mets.write(os.path.join(output_dir, 'content', 'mets.xml'), pretty_print=True)
    if sip_title != None:
        _build_dc_sip(output_dir, sip_title)

def _move_files_from_json(json_doc, streams_dir):
    if type(json_doc) == str:
        rep_dict = json.loads(json_doc)
    else:
        rep_dict = json_doc
    for item in rep_dict:
        origin = item['physical_path']
        destination = item['fileOriginalPath']
        if not os.path.exists(os.path.join(streams_dir, os.path.dirname(destination))):
            try:
                os.makedirs(os.path.join(streams_dir, os.path.dirname(destination)))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        shutil.copy2(origin, os.path.join(streams_dir, destination))



def build_sip_from_json(ie_dmd_dict=None,
        pres_master_json=None, 
        modified_master_json=None,
        access_derivative_json=None,
        cms=None,
        webHarvesting=None,
        generalIECharacteristics=None,
        objectIdentifier=None,
        accessRightsPolicy=None,
        eventList=None,
        input_dir=None,
        digital_original=False,
        sip_title=None,
        output_dir=None):
    # build METS
    mets = build_mets_from_json(
        ie_dmd_dict=ie_dmd_dict,
        pres_master_json=pres_master_json, 
        modified_master_json=modified_master_json,
        access_derivative_json=access_derivative_json,
        cms=cms,
        webHarvesting=webHarvesting,
        generalIECharacteristics=generalIECharacteristics,
        objectIdentifier=objectIdentifier,
        accessRightsPolicy=accessRightsPolicy,
        eventList=eventList,
        input_dir=input_dir,
        digital_original=digital_original)

    # build output SIP folder structure
    streams_dir = os.path.join(output_dir, 'content', 'streams')
    os.makedirs(streams_dir)

    # print(ET.tounicode(mets, pretty_print=True))
    # files_list = mets.findall(".//{http://www.loc.gov/METS/}fileSec/{http://www.loc.gov/METS/}fileGrp/{http://www.loc.gov/METS/}file")
    # for file in files_list:
    #     print("finding {}!".format(file.attrib["ADMID"]))
    #     origin = mets.find('.//mets:amdSec[@ID="%s"]/mets:techMD/mets:mdWrap/mets:xmlData/dnx/section[@id="generalFileCharacteristics"]/record/key[@id="fileOriginalPath"]' % (file.attrib["ADMID"]), namespaces=mets_dnx_nsmap ).text
    #     destination = os.path.join(file.find(".//{http://www.loc.gov/METS/}FLocat").attrib["{http://www.w3.org/1999/xlink}href"])
    #     if not os.path.exists(os.path.join(streams_dir, os.path.dirname(destination))):
    #         try:
    #             os.makedirs(os.path.join(streams_dir, os.path.dirname(destination)))
    #         except OSError as exc:  # Guard against race condition
    #             if exc.errno != errno.EEXIST:
    #                 raise
    #     # _copytree(origin, destination)
    #     shutil.copy2(origin, destination)

    mets.write(os.path.join(output_dir, 'content', 'mets.xml'), pretty_print=True)
    for entry in (pres_master_json, modified_master_json, access_derivative_json):
        if entry != None:
            _move_files_from_json(entry, streams_dir)

    
    # write SIP DC file if SIP title is supplied
    if sip_title != None:
        _build_dc_sip(output_dir, sip_title)
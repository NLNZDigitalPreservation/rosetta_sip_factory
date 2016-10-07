import os
import shutil

from lxml import etree as ET
from nose.tools import *

from rosetta_sip_factory import sip_builder as sb


def test_mets_dnx():
    """Test basic construction of METS DNX"""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 
                'data', 
                'output_1')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data', 
                'test_batch_1', 
                'pm'),
        modified_master_dir=
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent', 
                 'IEEntityType': 'periodicIE'}
                ],
        output_dir=output_dir
        )

    # print(ET.tounicode(mets, pretty_print=True))

def test_sip_single_rep_multi_folder_hierarchy():
    """Build SIP with single representation in a complex folder structure"""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_2')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_2',
                'root_folder'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_2'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent', 
                 'IEEntityType': 'periodicIE'}
                 ],
        output_dir=output_dir
        )
    
def test_sip_build_correct_digital_original_value():
    """Test to confirm bug fix - digital original value was being populated with
    output folder value"""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_1')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'pm'),
        modified_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                ],
        digital_original=True,
        output_dir=output_dir
        )
    metsxml = ET.parse(os.path.join(output_dir, 'content', 'mets.xml'))
    mets = metsxml.getroot()
    # grab first example of the element
    digital_original_el = mets.xpath('.//dnx:key[@id="DigitalOriginal"]',
        namespaces={'dnx': 'http://www.exlibrisgroup.com/dps/dnx'})[0]
    assert(digital_original_el.text == "true")


def test_mets_dnx_with_dc_xml():
    """Test basic construction of METS DNX with a dc.xml file for the 
    SIP title
    """
    output_dir = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), 
                'data',
                'output_1')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}    
    sip_title = 'Test Deposit'
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'pm'),
        modified_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1',
                'mm'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_1'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                'IEEntityType': 'periodicIE'}],
        sip_title=sip_title,
        output_dir=output_dir
        )
    files_list = os.listdir(os.path.join(output_dir, 'content'))
    if 'dc.xml' in files_list:
        dc_xml = ET.parse(os.path.join(output_dir, 'content', 'dc.xml'))
        dc = dc_xml.getroot()
        title = dc.xpath(".//dc:title", namespaces=dc.nsmap)[0].text
    else:
        title = None
    assert(title == sip_title)
from rosetta_sip_factory import sip_builder as sb

from lxml import etree as ET
from nose.tools import *

import os
import shutil


def test_mets_dnx():
    """Test basic construction of METS DNX"""
    output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'output_1')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'pm'),
        modified_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'mm'),
        input_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test_batch_1'),
        generalIECharacteristics=[{'submissionReason': 'bornDigitalContent', 'IEEntityType': 'periodicIE'}],
        output_folder=output_folder
        )

    # print(ET.tounicode(mets, pretty_print=True))

def test_sip_single_rep_multi_folder_hierarchy():
    """Build SIP with single representation in a complex folder structure"""
    output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'output_2')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_2', 'root_folder'),
        input_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test_batch_2'),
        generalIECharacteristics=[{'submissionReason': 'bornDigitalContent', 'IEEntityType': 'periodicIE'}],
        output_folder=output_folder
        )
    
def test_sip_build_correct_digital_original_value():
    """Test to confirm bug fix - digital original value was being populated with
    output folder value"""
    output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'output_1')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    ie_dc_dict = {"dc:title": "test title"}
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'pm'),
        modified_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'mm'),
        input_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test_batch_1'),
        generalIECharacteristics=[{'submissionReason': 'bornDigitalContent', 'IEEntityType': 'periodicIE'}],
        digital_original=True,
        output_folder=output_folder
        )
    metsxml = ET.parse(os.path.join(output_folder, 'content', 'mets.xml'))
    mets = metsxml.getroot()
    # grab first example of the element
    digital_original_el = mets.xpath('.//dnx:key[@id="DigitalOriginal"]',
        namespaces={'dnx': 'http://www.exlibrisgroup.com/dps/dnx'})[0]
    # digital_original_el = mets.xpath('.//*[@id="DigitalOriginal"]')
    print(digital_original_el.text)
    assert(digital_original_el.text == "true")
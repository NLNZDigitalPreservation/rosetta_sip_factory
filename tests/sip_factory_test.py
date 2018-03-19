import os
import shutil

from lxml import etree as ET
from nose.tools import *

from rosetta_sip_factory import sip_builder as sb


CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


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
    input_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_2')
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                input_dir,
                'root_folder'),
        input_dir=os.path.join(
                input_dir),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                 ],
        output_dir=output_dir
        )
    input_content = os.listdir(input_dir)
    streams_content = os.listdir(
                        os.path.join(
                            output_dir,
                            'content',
                            'streams'))
    for thing in input_content:
        assert(thing in streams_content)


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


def test_single_file_mets_dnx_with_dc_xml():
    """Test basic construction of a single-file METS DNX with a dc.xml
    file for the SIP title
    """
    output_dir = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                'data',
                'output_3')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    sip_title = 'Test Deposit'
    sb.build_single_file_sip(
        ie_dmd_dict=ie_dc_dict,
        filepath=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_3',
                'presmaster.jpg'),
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


def test_sip_single_rep_flat_files():
    """Build SIP with single representation in a flat filestructure"""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_4')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    input_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4')
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                input_dir),
        input_dir=os.path.join(
                input_dir),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                 ],
        output_dir=output_dir
        )
    input_content = os.listdir(input_dir)
    streams_content = os.listdir(
                        os.path.join(
                            output_dir,
                            'content',
                            'streams'))
    for thing in input_content:
        assert(thing in streams_content)


def test_sip_single_rep_json():
    """Build SIP with single representation with JSON input"""

    pm_json = """[
        {"fileOriginalName": "img_1.jpg",
         "fileOriginalPath": "img_1.jpg",
         "physical_path" : "%s/img_1.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1"},
         {"fileOriginalName": "img_2.jpg",
         "fileOriginalPath": "img_2.jpg",
         "physical_path" : "%s/img_2.jpg",
         "MD5": "11c2563db299225b38d5df6287ccda7d",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2"}
    ]""" % (os.path.join(CURRENT_DIR, "data", "test_batch_4"),
            os.path.join(CURRENT_DIR, "data", "test_batch_4"))
    # pm_json = """[
    #     {"name": "img_1.jpg",
    #      "path": "%s/img1.jpg",
    #      "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
    #      "fileCreationDate": "1st of January, 1601",
    #      "fileModificationDate": "1st of January, 1601",
    #      "label": "Image One",
    #      "note": "This is a note for image 1"},
    #      {"name": "img_2.jpg",
    #      "path": "%s/img2.jpg",
    #      "MD5": "11c2563db299225b38d5df6287ccda7d",
    #      "fileCreationDate": "1st of January, 1601",
    #      "fileModificationDate": "1st of January, 1601",
    #      "label": "Image Two",
    #      "note": "This is a note for image 2"}
    # ]""" % (os.path.join(CURRENT_DIR, "data", "test_batch_4"),
    #         os.path.join(CURRENT_DIR, "data", "test_batch_4"))

    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_4')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "test title"}
    input_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4')
    sb.build_sip_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json=pm_json,
        input_dir=os.path.join(
                input_dir),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                 ],
        output_dir=output_dir
        )


def test_sip_build_pm_and_ad():
    """Test to confirm bug fix - make sure that the output AD directory gets the
    AD files, not PM files."""
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
        access_derivative_dir=os.path.join(
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
    ad_input_files = os.listdir(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        'data',
                        'test_batch_1',
                        'mm'))
    ad_output_files = os.listdir(os.path.join(
                            output_dir,
                            'content',
                            'streams',
                            'mm'))
    for f in ad_input_files:
        assert(f in ad_output_files)

def test_sip_build_pm_and_mm():
    """Test to confirm bug fix - make sure that the output AD directory gets the
    AD files, not PM files."""
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
    ad_input_files = os.listdir(os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        'data',
                        'test_batch_1',
                        'mm'))
    mm_output_files = os.listdir(os.path.join(
                            output_dir,
                            'content',
                            'streams',
                            'mm'))
    for f in ad_input_files:
        assert(f in mm_output_files)

def test_sip_build_multiple_ies():
    """Test to build a SIP with two IEs in it. Only PMs."""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_4')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    ie_dc_dict = {"dc:title": "test title"}
    other_ie_dc_dict = {"dc:title": "Other test title"}
    
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_3'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_3'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                ],
        digital_original=True,
        mets_filename='test1',
        output_dir=output_dir
        )

    sb.build_sip(
        ie_dmd_dict=other_ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                ],
        digital_original=True,
        mets_filename='test2',
        output_dir=output_dir
        )
    output_files = os.listdir(os.path.join(output_dir, 'content', 'streams'))
    for f in ['img_1.jpg', 'img_2.jpg', 'presmaster.jpg']:
        assert(f in output_files)
    output_metses = os.listdir(os.path.join(output_dir, 'content'))
    for f in ['test1.xml', 'test2.xml']:
        assert(f in output_metses)

@raises(Exception)
def test_sip_build_multiple_ies_with_same_named_files():
    """Test to see how this process handles two IEs that both have the same named
    files."""
    output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'output_4')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    ie_dc_dict = {"dc:title": "test title"}
    other_ie_dc_dict = {"dc:title": "Other test title"}
    
    sb.build_sip(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                ],
        digital_original=True,
        mets_filename='test1',
        output_dir=output_dir
        )

    sb.build_sip(
        ie_dmd_dict=other_ie_dc_dict,
        pres_master_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        input_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_4'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                 'IEEntityType': 'periodicIE'}
                ],
        digital_original=True,
        mets_filename='test2',
        output_dir=output_dir
        )
    output_files = os.listdir(os.path.join(output_dir, 'content', 'streams'))
    for f in ['img_1.jpg', 'img_2.jpg']:
        assert(f in output_files)
    output_metses = os.listdir(os.path.join(output_dir, 'content'))
    for f in ['test1.xml', 'test2.xml']:
        assert(f in output_metses)


def test_single_file_mets_dnx_with_macron():
    """Test single-file METS DNX with a macron title 
    """
    output_dir = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                'data',
                'output_3')
    # first off, delete anything that's in the output folder
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ie_dc_dict = {"dc:title": "māori"}
    sip_title = 'Test Deposit'
    sb.build_single_file_sip(
        ie_dmd_dict=ie_dc_dict,
        filepath=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data',
                'test_batch_3',
                'presmaster.jpg'),
        generalIECharacteristics=[
                {'submissionReason': 'bornDigitalContent',
                'IEEntityType': 'periodicIE'}],
        sip_title=sip_title,
        output_dir=output_dir
        )
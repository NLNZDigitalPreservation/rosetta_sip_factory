import os
from os.path import join

from lxml import etree as ET

from rosetta_sip_factory import sip_builder as sb
from tests import INPUTS_PATH
from tests.utils import read_mets_files


class TestBatchOne:
    pres_master_dir = join(INPUTS_PATH, "test_batch_1", "pm")
    modified_master_dir = join(INPUTS_PATH, "test_batch_1", "mm")
    input_dir = join(INPUTS_PATH, "test_batch_1")
    general_ie_characteristics = [
        {"submissionReason": "bornDigitalContent", "IEEntityType": "periodicIE"}
    ]
    ie_dc_dict = {"dc:title": "test title"}
    titles = ["Test_IE_0", "Another_test", "test with spaces", "camelCaseTest"]

    def test_mets_dnx(self, outputs_path):
        """
        Test basic construction of METS DNX
        """
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.pres_master_dir,
            modified_master_dir=self.modified_master_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
        )
        assert True

    def test_sip_build_correct_digital_original_value(self, outputs_path):
        """
        Test to confirm bug fix - digital original value was being populated with
        output folder value
        """
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.pres_master_dir,
            modified_master_dir=self.modified_master_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            digital_original=True,
            output_dir=outputs_path,
        )
        metsxml = ET.parse(join(outputs_path, "content", "mets.xml"))
        mets = metsxml.getroot()

        # grab first example of the element
        digital_original_el = mets.xpath(
            './/dnx:key[@id="DigitalOriginal"]',
            namespaces={"dnx": "http://www.exlibrisgroup.com/dps/dnx"},
        )[0]
        assert digital_original_el.text == "true"

    def test_mets_dnx_with_dc_xml(self, outputs_path):
        """
        Test basic construction of METS DNX with a dc.xml file for the
        SIP title
        """
        sip_title = "Test Deposit"

        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.pres_master_dir,
            modified_master_dir=self.modified_master_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            sip_title=sip_title,
            output_dir=outputs_path,
        )

        files_list = os.listdir(join(outputs_path, "content"))
        if "dc.xml" in files_list:
            dc_xml = ET.parse(join(outputs_path, "content", "dc.xml"))
            dc = dc_xml.getroot()
            title = dc.xpath(".//dc:title", namespaces=dc.nsmap)[0].text
        else:
            title = None
        assert title == sip_title

    def test_sip_build_pm_and_ad(self, outputs_path):
        """
        Test to confirm bug fix - make sure that the output AD directory gets the
        AD files, not PM files.
        """
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.pres_master_dir,
            modified_master_dir=self.modified_master_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            digital_original=True,
            output_dir=outputs_path,
        )

        modified_master_outputs_path = join(outputs_path, "content", "streams", "mm")
        ad_input_files = os.listdir(self.modified_master_dir)
        ad_output_files = os.listdir(modified_master_outputs_path)
        for f in ad_input_files:
            assert f in ad_output_files

    def test_multiple_full_IEs_in_one_SIP_folder(self, outputs_path):
        for title in self.titles:
            ie_dmd_dict = [{"dc:title": title}]
            sb.build_sip(
                ie_dmd_dict=ie_dmd_dict,
                pres_master_dir=self.pres_master_dir,
                modified_master_dir=self.modified_master_dir,
                input_dir=self.input_dir,
                output_dir=outputs_path,
                mets_filename=title,
            )

        content_path = join(outputs_path, "content")
        expected_xmls = [f"{t}.xml" for t in self.titles] + ["streams"]
        for file in os.listdir(content_path):
            assert file in expected_xmls

    def test_build_sip_with_exclude_file_characteristics(self, outputs_path):
        """
        Test exclude_file_characteristics
        """
        sip_title = "Test Deposit"
        exclude_file_characteristics = [
            "fileOriginalPath",
            "fileSizeBytes",
            "fileModificationDate",
            "fileCreationDate",
        ]
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.pres_master_dir,
            modified_master_dir=self.modified_master_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            sip_title=sip_title,
            output_dir=outputs_path,
            exclude_file_characteristics=exclude_file_characteristics,
        )
        mets_data = read_mets_files(outputs_path)
        for data in mets_data:
            assert "fileOriginalPath" not in data
            assert "fileSizeBytes'" not in data
            assert "fileModificationDate" not in data
            assert "fileCreationDate" not in data

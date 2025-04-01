import glob
from os.path import join

import pytest
from lxml import etree as ET

from rosetta_sip_factory import sip_builder as sb
from tests import INPUTS_PATH
from tests.utils import read_mets_files


class TestBatch3:
    ie_dc_dict = {"dc:title": "test title"}
    inputs_path = join(INPUTS_PATH, "test_batch_3")
    general_ie_characteristics = [
        {"submissionReason": "bornDigitalContent", "IEEntityType": "periodicIE"}
    ]

    @pytest.mark.parametrize(
        "sip_title",
        [
            pytest.param("Test Deposit"),
            pytest.param("Another title"),
            pytest.param("      "),
            pytest.param("123456789"),
        ],
    )
    def test_single_file_mets_dnx_with_dc_xml(self, sip_title, outputs_path):
        """
        Test basic construction of a single-file METS DNX with a dc.xml
        file for the SIP title
        """
        sb.build_single_file_sip(
            ie_dmd_dict=self.ie_dc_dict,
            filepath=join(self.inputs_path, "presmaster.jpg"),
            generalIECharacteristics=self.general_ie_characteristics,
            sip_title=sip_title,
            output_dir=outputs_path,
        )
        dc_xml_path = glob.glob(join(outputs_path, "**", "dc.xml"), recursive=True)[0]
        dc_xml = ET.parse(dc_xml_path)
        dc = dc_xml.getroot()
        title = dc.xpath("//dc:title", namespaces=dc.nsmap)[0].text
        assert title == sip_title

    @pytest.mark.parametrize(
        "sip_title, expected_exception",
        [
            pytest.param(123456789, TypeError),
        ],
    )
    def test_single_file_mets_dnx_with_dc_xml_null(
        self, sip_title, expected_exception: Exception, outputs_path
    ):
        """
        Null test - test basic construction of a single-file METS DNX with a dc.xml
        file for the SIP title
        """
        with pytest.raises(expected_exception):
            sb.build_single_file_sip(
                ie_dmd_dict=self.ie_dc_dict,
                filepath=join(self.inputs_path, "presmaster.jpg"),
                generalIECharacteristics=self.general_ie_characteristics,
                sip_title=sip_title,
                output_dir=outputs_path,
            )

    @pytest.mark.parametrize(
        "dc_title, sip_title", [pytest.param("māori", "Māori Test Deposit")]
    )
    def test_single_file_mets_dnx_with_macron(self, outputs_path, dc_title, sip_title):
        """
        Test single-file METS DNX with a macron title
        """
        ie_dc_dict = {"dc:title": dc_title}
        sb.build_single_file_sip(
            ie_dmd_dict=ie_dc_dict,
            filepath=join(
                self.inputs_path,
                "presmaster.jpg",
            ),
            generalIECharacteristics=self.general_ie_characteristics,
            sip_title=sip_title,
            output_dir=outputs_path,
        )

    @pytest.mark.parametrize(
        "exclude_file_characteristics",
        [
            pytest.param(
                [
                    "fileOriginalPath",
                    "fileSizeBytes",
                    "fileModificationDate",
                    "fileCreationDate",
                ]
            ),
            pytest.param(
                [
                    "fileOriginalPath",
                    "fileCreationDate",
                ]
            ),
            pytest.param(
                [
                    "fileSizeBytes",
                    "fileModificationDate",
                ]
            ),
            pytest.param(
                [
                    "fileCreationDate",
                ]
            ),
        ],
    )
    def test_build_single_file_sip_with_exclude_file_characteristics(
        self, outputs_path, exclude_file_characteristics
    ):
        general_ie_characteristics = [{"IEEntityType": "periodicIE"}]

        sb.build_single_file_sip(
            ie_dmd_dict=self.ie_dc_dict,
            filepath=join(
                self.inputs_path,
                "presmaster.jpg",
            ),
            generalIECharacteristics=general_ie_characteristics,
            sip_title="Test Deposit",
            output_dir=outputs_path,
            exclude_file_characteristics=exclude_file_characteristics,
        )
        data = read_mets_files(outputs_path)[0]
        for attr in exclude_file_characteristics:
            assert attr not in data

import copy
import json
import os
from os.path import join

from rosetta_sip_factory import sip_builder as sb
from tests import INPUTS_PATH
from tests.utils import read_json


class TestBatchFour:
    input_dir = join(INPUTS_PATH, "test_batch_4")
    ie_dc_dict = {"dc:title": "test title"}
    general_ie_characteristics = [
        {"submissionReason": "bornDigitalContent", "IEEntityType": "periodicIE"}
    ]
    pres_master_json = read_json(join(INPUTS_PATH, "pres_masters", "batch_4.json"))

    def test_sip_single_rep_flat_files(self, outputs_path):
        """
        Build SIP with single representation in a flat filestructure
        """
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=self.input_dir,
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
        )
        input_content = os.listdir(self.input_dir)
        streams_content = os.listdir(join(outputs_path, "content", "streams"))
        for file_name in input_content:
            assert file_name in streams_content

    def test_sip_single_rep_json(self, outputs_path):
        """Build SIP with single representation with JSON input"""
        pres_master_json = copy.deepcopy(self.pres_master_json)
        for file_dict in pres_master_json:
            physical_path = join(self.input_dir, file_dict["fileOriginalName"])
            file_dict["physical_path"] = physical_path

        sb.build_sip_from_json(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_json=json.dumps(pres_master_json),
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
        )
        assert True

    def test_sip_build_multiple_ies_with_same_named_files(self, outputs_path):
        """
        Test to see how this process handles two IEs that both have the same named
        files.
        """
        titles = ["test title", "Another test title"]
        ie_dc_dicts = [{"dc:title": t} for t in titles]
        mets_filenames = ["test1", "test2"]

        for ie_dc_dict, mets_filename in zip(ie_dc_dicts, mets_filenames):
            sb.build_sip(
                ie_dmd_dict=ie_dc_dict,
                pres_master_dir=self.input_dir,
                input_dir=self.input_dir,
                generalIECharacteristics=self.general_ie_characteristics,
                digital_original=True,
                mets_filename=mets_filename,
                output_dir=outputs_path,
            )

        expected_images = ["img_1.jpg", "img_2.jpg"]
        for mets_filename in mets_filenames:
            path = join(outputs_path, "content", "streams", mets_filename)
            output_files = sorted(os.listdir(path))
            assert output_files == expected_images

        output_mets_files = os.listdir(join(outputs_path, "content"))
        expected_xmls = [f"{f}.xml" for f in mets_filenames] + ["streams"]
        for file in output_mets_files:
            assert file in expected_xmls

    import pytest

    @pytest.mark.parametrize(
        "title, file",
        [
            pytest.param("Test_IE_1", "img_1.jpg"),
            pytest.param("Test_IE_2", "img_2.jpg"),
        ],
    )
    def test_multiple__single_file_IEs_in_one_SIP_folder(
        self, outputs_path, title, file
    ):
        ie_dmd_dict = [{"dc:title": title}]
        sb.build_single_file_sip(
            ie_dmd_dict=ie_dmd_dict,
            filepath=join(self.input_dir, file),
            output_dir=outputs_path,
            mets_filename=title,
        )

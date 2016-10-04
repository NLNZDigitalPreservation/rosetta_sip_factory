from pydc import factory as dc_factory
from pydnx import factory as dnx_factory
from pymets import mets_factory
from mets_dnx.factory import build_mets

from lxml import etree as ET

import os
import shutil


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
        # print("line 43! DEBUG")
        # print(os.path.basename(pres_master_dir))
        destination = os.path.join(streams_dir, os.path.basename(pres_master_dir))
        os.makedirs(destination)
        # shutil.copytree(pres_master_dir, destination)
        copytree(pres_master_dir, destination)
    if modified_master_dir != None:
        destination = os.path.join(streams_dir, os.path.basename(modified_master_dir))
        os.makedirs(destination)
        # shutil.copytree(pres_master_dir, destination)
        copytree(pres_master_dir, destination)
    if access_derivative_dir != None:
        destination = os.path.join(streams_dir, os.path.basename(access_derivative_dir))
        os.makedirs(destination)
        # shutil.copytree(pres_master_dir, destination)
        copytree(pres_master_dir, destination)


    with open(os.path.join(output_folder, 'content', 'mets.xml'), 'w') as metsfile:
        metsfile.write(ET.tounicode(mets, pretty_print=True))
    # return mets
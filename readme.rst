Rosetta SIP Factory
===================
Generate Rosetta-compliant Submission Information Packages

Background
----------
The Rosetta digital preservation application provides multiple different avenues for depositing digital content, including a web interface deposit, csv and METS XML. The METS XML process lends itself well to processing large numbers of records, and Ex Libris (the developers of Rosetta) provide a Java-based SDK for constructing deposit mechanisms (available at https://github.com/ExLibrisGroup/Rosetta.dps-sdk-projects).  
The Rosetta SIP Factory provides functionality for creating METS XML deposits for the Rosetta application, but it is built with Python rather than Java. While it does not offer the full range of options that are available with the Java-based deposit SDK, it aims to provide a quick and easy mechanism for common use cases. It also aims to appeal to people who prefer working with Python rather than Java.


Usage
-----
::

    from rosetta_sip_factory import sip_builder
    sip_builder.build_sip(
        ie_dmd_dict=None,
        pres_master_dir=None,
        modified_master_dir=None,
        access_derivative_dir=None,
        cms=None,
        generalIECharacteristics=None,
        objectIdentifier=None,
        accessRightsPolicy=None,
        eventList=None,
        input_dir=None,
        digital_original=False,
        sip_title=None,
        output_dir=None
    )

**NOTE**: If you are wondering why the above arguments are a mixture of snake_case and camelCase, it is beacuse the camelCase terms are the terms as used within Ex Libris's DNX metadata schema. While the author is coming to regret this stylistic decision, it does have the benefit of being able to directly map the arguments to their DNX metadata elements.

The above arguments (if required) should be submitted in the following format:

**ie_dmd_dict** = dictionary, such as follows::

    {"dc:title": "Title of record", "dcterms:isPartOf": "19926",
     "dc:identifier xsi:type=InstitionalIdentifier": "A1234",
     "dcterms:provenance": "Transferred from Agency ABCD"}

(See below in the "dc, dcterms and xsi mapping in ie_dmd" description for more
details about building an ie_dmd section)  
**pres_master_dir** = string (can supply os.path.join() construct if preferred)  

**modified_master_dir** = string (can supply os.path.join() construct if preferred)  

**access_derivative_dir** = string (can supply os.path.join() construct if preferred)  

**cms** = dictionary inside list, such as follows::

    [{'system': <system name>, 'recordId': <CMS ID> },]
 
**generalIECharacteristics** = dictionary inside list, such as follows::

    [{'IEEntityType': <entity type>, 'submissionReason': <submission reason>},]
 
**objectIdentifier** = dictionary inside list, such as follows::  

    [{'objectIdentifierType': <object identifier type>, 'objectIdentifierValue': <object identifier value>}]

**accessRightsPolicy** = dictionary inside list, such as follows::

    [{'policyId': <policy ID>, 'policyDescription': <policy description>},]

**eventList** = dictionary inside list, such as follows::  

    [{'eventDateTime': <event datetime>, 
      'eventType': <event type>,
      'eventIdentifierType': <event identifier type>, 
      'eventIdentifierValue': <event identifier value>,
      'eventOutcome1': <event outcome 1>,
      'eventOutcomeDetail1': <event outcome detail 1>,
      'eventDescription': <event description>,
      'linkingAgentIdentifierType1': <linking agent identifier type 1>,
      'linkingAgentIdentifierValue1': <linking agent identifier value 1>
      },]

(**Note**: Not all key/value pairs are required for events.)  

**input_dir** = string (can supply os.path.join() construct if preferred)  

**digital_original** = Boolean (default is False)  

**sip_title** = String  

**output_dir** = string (can supply os.path.join() construct if preferred)  

In addition to the "build_sip" function, there is also a convenience function called "build_single_file_sip", which takes a "filepath" parameter, and does not accept "pres_master_dir", "modified_master_dir", "access_derivative_dir" or "input_dir". An example of its usage is shown in the "Common Use Case Examples" subsection below.  

Typical SIP folder structure
----------------------------
The build_sip function creates a SIP struture that is compliant with what the Rosetta application expects to see. Below is an example of how a single-representation SIP would look:
(Note: in all of these examples, the sip_title parameter has been supplied, which results in the dc.xml file being generated)::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |  
             |_streams
             |   |
             |   |_file1.txt
             |   |
             |   |_file2.txt
             |
             |_mets.xml
             |
             |_dc.xml

Below is an example of a multi-representation SIP::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |
             |_streams
             |   |
             |   |_pres_master
             |   |    |
             |   |    |_file1.tif
             |   |    |
             |   |    |_file2.tif
             |   |
             |   |_modified_master
             |   |    |
             |   |    |_file1.jpg
             |   |    |
             |   |    |_file2.jpg
             |   |
             |   |_access_derivative
             |        |
             |        |_file1.pdf
             |    
             |_mets.xml
             |
             |_dc.xml


You can have as many "sip_folder" folders in the "Base_location_on_server" as you like.  
Depending on your mode of deposit, you may want to add a settings folder and settings.properties file. If that is the case, you should add them so the SIP structure looks like this::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |_settings
             |   |
             |   |_settings.properties
             |
             |_streams
             |   |
             |   |_file1.txt
             |   |
             |   |_file2.txt
             |
             |_mets.xml
             |
             |_dc.xml

The "settings.properties" file should look like this::

    material_flow_id=12345
    deposit_set_id=1
    user_name=username
    user_password=password
    user_institution=INS00
    user_producer_id=99999

with your appropriate values instead of the placeholder values.

Common Use Case Examples
------------------------
**SIP for an Intellectual Entity that consists of one file**  
  
Directory Structure:
::

  /path/to/base_dir
            |
            |__file1.tif
  
Code:
::

    import os
    from rosetta_sip_factory import sip_builder

    # set the filepath and the output directory for convenience's sake
    filepath = os.path.join('/', 'path', 'to', 'base_dir', 'file1.jpg',)
    output_dir = os.path.join('/', 'path', 'to', 'destination_dir')

    sip_builder.build_single_file_sip(
        ie_dmd_dict=[{'dc:title': 'title of IE',
                      'dcterms:isPartOf': 'Series 001'
                    }],
        filepath=filepath,
        generalIECharacteristics=[{'IEEntityType': 'unpublishedImages',
                                   'status': 'ACTIVE'
                                 }],
        objectIdentifier=[{'objectIdentifierType': 'ALMAMMS',
                           'objectIdentifierValue': '9901234578901234'}],
        accessRightsPolicy=[{'policyId': '1000'}],
        digital_original=True,
        sip_title='Title of SIP',
        output_dir=output_dir
    )

**SIP for an Intellectual Entity with one representation, consisting of files in one directory**  
  
Directory Structure:
::

    /path/to/base_dir
            |
            |__rep_folder
                   |
                   |__file1.tif
                   |__file2.tif
  
Code:
::

    import os
    from rosetta_sip_factory import sip_builder

    # set the base directory and the output directory for convenience's sake
    base_dir = os.path.join('/', 'path', 'to', 'base_dir')
    output_dir = os.path.join('/', 'path', 'to', 'destination_dir')

    sip_builder.build_sip(
        ie_dmd_dict=[{'dc:title': 'title of IE',
                      'dcterms:isPartOf': 'Series 001'
                    }],
        pres_master_dir=os.path.join(base_dir, 'rep_folder'),
        generalIECharacteristics=[{'IEEntityType': 'unpublishedImages',
                                   'status': 'ACTIVE'
                                 }],
        objectIdentifier=[{'objectIdentifierType': 'ALMAMMS',
                           'objectIdentifierValue': '9901234578901234'}],
        accessRightsPolicy=[{'policyID': '1000'}],
        input_dir=base_dir,
        digital_original=True,
        sip_title='Title of SIP'
        output_dir=output_dir
    )
(**NOTE** : in the above excerpt, it would also be possible to set the input dir as the same directory as the rep. In that case,
the files would be placed directly in the "content" directory in the SIP, rather than being placed inside another directory.
The primary reason for ordering representations in their own directories is to avoid the possibility of multiple representations
containing files with the same name.)

**SIP for an Intellectual Entity with two representations, consisting of files in one directory per rep**  
  
Directory Structure:
::

    /path/to/base_dir
            |
            |__rep_folder_1
            |      |
            |      |__file1.tif
            |      |__file2.tif
            |
            |__rep_folder_2   
                   |
                   |__file1.jpg
                   |__file2.jpg
  
Code:
::

    import os
    from rosetta_sip_factory import sip_builder

    # set the base directory and the output directory for convenience's sake
    base_dir = os.path.join('/', 'path', 'to', 'base_dir')
    output_dir = os.path.join('/', 'path', 'to', 'destination_dir')

    sip_builder.build_sip(
        ie_dmd_dict=[{'dc:title': 'title of IE',
                      'dcterms:isPartOf': 'Series 001'
                    }],
        pres_master_dir=os.path.join(base_dir, 'rep_folder_1'),
        modified_master_dir=os.path,join(base_dir, 'rep_folder_2'),
        generalIECharacteristics=[{'IEEntityType': 'unpublishedImages',
                                   'status': 'ACTIVE'
                                 }],
        objectIdentifier=[{'objectIdentifierType': 'ALMAMMS',
                           'objectIdentifierValue': '9901234578901234'}],
        accessRightsPolicy=[{'policyID': '1000'}],
        input_dir=base_dir,
        digital_original=True,
        sip_title='Title of SIP'
        output_dir=output_dir
    )

**SIP for an Intellectual Entity where rep and file level details are described as JSON documents**  

Directory Structure:
::

    /full/path/to/base_dir
                 |
                 |__rep_folder_1
                        |
                        |__file1.tif
                        |__file2.tif
                        |__file3.tif

  
Code:
::

    import os
    from rosetta_sip_factory import sip_builder

    # set the base directory and the output directory for convenience's sake
    base_dir = os.path.join('/', 'path', 'to', 'base_dir')
    output_dir = os.path.join('/', 'path', 'to', 'destination_dir')

    pm_json = [{'fileOriginalName': 'file1.tif',
                'fileOriginalPath': os.path.join('rep_folder_1', 'file1.tif'), 
                'physical_path': os.path.dir(base_dir, 'rep_folder_1', 'file1.tif')),
                'MD5': '11c2563db299225b38d5df6287ccda7d',
                'fileSizeBytes': '25678'
                'fileCreationDate': 'Wed Aug 09 14:10:22 NZDT 2017',
                'fileModificationDate': 'Mon Nov 13 15:19:34 NZDT 2017',
                'label': 'Image One',
                'note': 'This is a note for Image One'},
                {'fileOriginalName': 'file2.tif',
                'fileOriginalPath': os.path.join('rep_folder_1', 'file2.tif'), 
                'physical_path': os.path.dir(base_dir, 'rep_folder_1', 'file2.tif')),
                'MD5': '9d09f20ab8e37e5d32cdd1508b49f0a9',
                'fileSizeBytes': '113715'
                'fileCreationDate': 'Fri Sep 22 09:01:21 NZDT 2017',
                'fileModificationDate': 'Wed Nov 15 16:54:02 NZDT 2017',
                'label': 'Image Two',
                'note': 'This is a note for Image two'},
                {'fileOriginalName': 'file3.tif',
                'fileOriginalPath': os.path.join('rep_folder_1', 'file3.tif'), 
                'physical_path': os.path.dir(base_dir, 'rep_folder_1', 'file3.tif')),
                'MD5': '861f762a651b0feaa64cd6bf346e6d46',
                'fileSizeBytes': '189552'
                'fileCreationDate': 'Tue Aug 29 11:45:29 NZDT 2017',
                'fileModificationDate': 'Mon Dec 11 08:32:06 NZDT 2017',
                'label': 'Image Three',
                'note': 'This is a note for Image Three'}]

    sip_builder.build_sip_from_json(
        ie_dmd_dict=[{'dc:title': 'title of IE',
                      'dcterms:isPartOf': 'Series 001'
                    }],
        pres_master_json=pm_json,
        generalIECharacteristics=[{'IEEntityType': 'unpublishedImages',
                                   'status': 'ACTIVE'
                                 }],
        objectIdentifier=[{'objectIdentifierType': 'ALMAMMS',
                           'objectIdentifierValue': '9901234578901234'}],
        accessRightsPolicy=[{'policyID': '1000'}],
        input_dir=base_dir,
        digital_original=True,
        sip_title='Title of SIP'
        output_dir=output_dir
    )


dc, dcterms and xsi mapping in ie_dmd
-------------------------------------
The ie_dmd component does some behind-the scenes parsing of namespace prefixes 
and attributes. Specifically, the following three namespaces are supported:   
dc - is mapped to "http://purl.org/dc/elements/1.1/"   
dcterms - is mapped to "http://purl.org/dc/terms/"   
xsi - is mapped to "http://www.w3.org/2001/XMLSchema-instance", and is
intended only for use with attributes, not the element names.

Note that multi-word dc/dcterms elements should be camelCased (i.e. the dcterms element "Bibliographic Citation" should be rendered as "dcterms:bibligraphicCitation").

Installing Rosetta SIP Factory
------------------------------
If you have downloaded the package, unzip it and execute the following command::  
    python setup.py install  
This package will also install the most recent lxml library via pip if it is
not already installed.

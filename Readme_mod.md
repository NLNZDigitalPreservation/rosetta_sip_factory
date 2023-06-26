## Problem description:

The changes have been made to address ambiguities in some of the XML tags and to handle long paths within the METS file. These changes allow for customized exclusion of one or more tags from the METS output.
```

            general_file_characteristics = [{
                'fileOriginalPath': file_original_location,
                'fileSizeBytes': str(file_size_bytes),
                'fileModificationDate': last_modified,
                'fileCreationDate': created_time,
                'fileOriginalName': file_original_name,
                'label': file_label}]
```
Use case:
```
build_sip(
	...
        output_dir=self.output_folder, 
	exclude_file_char = ['fileOriginalPath','fileSizeBytes', 'fileModificationDate','fileCreationDate'])
```
In this case 'fileOriginalPath','fileSizeBytes', 'fileModificationDate','fileCreationDate' will not be displayed in the mets.

## Changes description:

The changes applied to both rosetta_sip_factory and mets_dnx libraries 


1. For **rosetta_sip_factory** (sip_builder.py) new parameter "exclude_file_char" was added to build_single_file_sip  and build_sip functions.
test_build_sip_with_exclude_file_char() test was added.


```

def build_single_file_sip(...
                          exclude_file_char = []):


    # build mets
    mets = build_single_file_mets(...
        
        			exclude_file_char = exclude_file_char)

```

2. For mets_dnx (factory.py) new parameter "exclude_file_char" was added to build_single_file_mets  and build_mets functions 
and also this logic for removing tags.

```
            for file_char in exclude_file_char:
                general_file_characteristics[0].pop(file_char)
```

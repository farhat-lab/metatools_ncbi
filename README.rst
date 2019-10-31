Purpose
=======
The main purpose of metatools_ncbi is to help you to download NCBI biosample and RunInfo metadata from a list of biosamples or a taxonomic id (txid).


Installation
============
You can install metatools_ncbi through pip::

    pip install metatools_ncbi


Usage
=====

Downloading metadata
--------------------

We want to download all the metadata associated to the biosamples of the microorganism *Mycobaterium tuberculosis*. First of all we determine the taxonomic id of this microorganism through NCBI (`NCBI taxonomy`_). The id for *M. tuberculosis* is txid1773.

.. _NCBI taxonomy: https://www.ncbi.nlm.nih.gov/taxonomy

We download the metadata of all the biosamples with the following command::

    metatools_download biosamples -t txid1773 json_biosamples

In order to download the RunInfo metadata we need to have a file with the list of the biosamples. We can generate it like this::

    ls  json_biosamples/ | sed -e 's/.json//' > list_biosamples.txt

Our list of biosamples is very long (54,179 elements). We can split this list in smaller lists (If your list is not that long, you might want to skip this step)::

    split -l 1000 -d list_biosamples.txt to_download

Now we can use metatools_ncbi to download the RunInfo metadata::

    for current_file in `ls to_download*`;
    do
    echo " - Downloading RunInfos -- biosamples present in ${current_file}";
    metatools_download runs ${current_file} json_runs/;
    done

Converting NCBI IDs
-------------------

In order to convert a NCBI IDs (e.g. bioprojects, run ids) to biosamples, you can type the following command::

    metatools_convert list_ids.txt ids_converted.txt

You can also use use this functionality in your own code::

    from metatools_ncbi import convert_to_biosample
    list_of_ncbi_ids=["SRS2577112", "SRR6152911", "SRP047263", "PRJNA413593", "PRJNA211721"]
    list_biosamples=convert_to_biosample.convert_to_biosample(list_of_ncbi_ids)

    print(list_biosamples)
    ['SAMN07766347', 'SAMN07765863', 'SAMN02673324', '', 'SAMN02231188']

NOTE: the NCBI ID PRJNA413593 has not been converted to a biosample because it contains 1378 biosamples (`check it yourself`_), so it is impossible to establish the biosample you are interested in using this ID.

.. _check it yourself: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA413593

Roadmap (Changelog)
===================
Todo

* module available on Conda ✕
* the code that converts sequencing runs and bioprojects to biosamples is too slow

Version 0.2.1

* bin/metatools_convert was not included in setup.py (bugfix)

Version 0.2.0

* added functionality ("metatools_convert") to convert a list of NCBI IDs (e.g. sequencing runs, bioprojects) to biosamples, when possible (feature)

Version 0.1.5

* fixed: "metatools_download runs" cannot handle empty lines in the list of biosamples (bug fix)

Version 0.1.4

* fixed: "?" character at the end of the name of each json file when I download the metadata about the runs (bug fix)
* fixed: the dictionary "d" inside the function get_json_runinfo_from_biosamples is storing all the sequencing runs information for all biosamples instead of the one/those of a single biosample (bug fix)

Version 0.1.3

* metatools_download should not have a .py extension (documentation)

Version 0.1.2

* I improved the documentation (README.rst).

Version 0.1.1

* updated dependencies (progress), added information on how to install the module (README.rst)

Version 0.1.0

* download all biosample metadata of a given species using the NCBI txid (feature)
* download biosample metadata providing a list of biosamples (feature)
* download RunInfo metadata providing a list of biosamples (feature)
* module available on Pypi

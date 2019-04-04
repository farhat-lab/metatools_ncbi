Purpose
=======
The main purpose of metatools_ncbi is to help you to download NCBI biosample and RunInfo metadata from a list of biosamples or a taxonomic id (txid).

Usage
=====
We want to download all the metadata associated to the biosamples of the microorganism *Mycobaterium tuberculosis*. First of all we determine the taxonomic id of this microorganism through NCBI (`NCBI taxonomy`_). The id for *M. tuberculosis* is txid1773.

.. _NCBI taxonomy: https://www.ncbi.nlm.nih.gov/taxonomy

We download the metadata of all the biosamples with the following command::

    ./bin/metatools_download.py biosamples -t txid1773 json_biosamples

In order to download the RunInfo metadata we need to have a file with the list of the biosamples. We can generate it like this::

    ls  json_biosamples/ | sed -e 's/.json//' > list_biosamples.txt

Our list of biosamples is very long (54,179 elements). We can split this list in smaller lists (If your list is not that long, you might want to skip this step)::

    split -l 1000 -d list_biosamples.txt to_download

Now we can use metatools_ncbi to download the RunInfo metadata::

    for current_file in `ls to_download*`;
    do
    echo " - Downloading RunInfos -- biosamples present in ${current_file}";
    ./bin/metatools_download.py runs ${current_file} json_runs/;
    done


Roadmap (Changelog)
===================
- Version 0.1
  - download all biosamples of a given species using the NCBI txid (feature)
  - download biosamples metadata providing a list of biosamples_parser (feature)
  - download RunInfo metadata providing a list of biosamples (feature)
  - ? at the end of the name of each json file when I download the metadata about the runs (bug)
  - module available on Pypi ✕
  - module available on Conda ✕

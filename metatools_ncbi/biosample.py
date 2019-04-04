import os
import re
import json
import requests
import csv
from progress.bar import IncrementalBar

def get_biosample_numerical_ids_from_taxid(taxid):
	"""
	Takes a taxid and returns the biosample ids (numerical ids)
	"""
	# I should manage better the retmax
	request = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=biosample&term={}&retmax=100000&retmode=json".format(taxid)
	response = requests.get(url=request,stream=True)
	response.encoding = 'utf-8'
	d_response = json.loads(response.text)
	list_biosample_ids = d_response["esearchresult"]["idlist"]
	return(list_biosample_ids)

def generate_lists_k_elments_from_list(original_list: list, k: int) -> list:
	"""
	Splits a long list in smaller lists of k elements
	"""
	for i in range(0, len(original_list), k):
		yield original_list[i:i + k]
		#returns a generator object

def get_json_metadata_from_biosamples(list_biosamples: list, num_records_per_request: int, dir_json: str):
	list_of_dicts_metadata = []
	all_attributes = {}
	list_of_lists = list(generate_lists_k_elments_from_list(list_biosamples, num_records_per_request))
	with IncrementalBar('Downloading...', max=len(list_of_lists), suffix='%(percent).1f%%') as bar:
		for chunk, current_list in enumerate(list_of_lists):
			#print("* analyzing chunk {} of {}".format(chunk,len(list_of_lists)))
			request = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id={}&retmode=text".format(",".join(current_list))
			response = requests.get(url = request, stream = True)
			response.encoding = 'utf-8'
			#print(response.text)
			data_response = re.split("\n\n",response.text)
			#print(data_response)
			# I create the json files in the output directory
			if not os.path.exists(dir_json):
				os.makedirs(dir_json)
			for entry in [x for x in data_response if x != "\n"]:
				d_metadata, list_of_attributes = parse_text_response_get_metadata(entry)
				list_of_dicts_metadata.append(d_metadata.copy())
				for a in list_of_attributes:
					all_attributes[a] = True
				try:
					biosample = d_metadata["accession"]
					with open(os.path.join(dir_json, biosample + ".json"),"w") as outf:
						json.dump(d_metadata, outf, indent = 4)
				except:
					print(d_metadata)
					print(" * I cannot determine the accession for this entry")
			bar.next()
	#print(list_of_dicts_metadata)
	with open(os.path.join(dir_json, "list_of_attributes.json"),"w") as outf:
		json.dump(all_attributes, outf, indent = 4)

def parse_text_response_get_metadata(text_response: str) -> tuple:
	"""
	Parses one single record of the NCBI response
	"""
	# d_response is a dictionary created from the text response
	d_response = {}
	re_title = re.compile("^[0-9]+:")
	re_identifiers = re.compile("^Identifiers:")
	re_attribute = re.compile("^    /")
	re_accession = re.compile("^Accession:")
	re_keywords = re.compile("^Keywords:")
	re_description = re.compile("^Description:")
	re_empty_line = re.compile("^$")
	description = ""
	flag_description = 0
	for row in text_response.splitlines():
		if bool(re_empty_line.match(row)):
			break
		elif bool(re_title.match(row)):
			data_title = row.split(": ",1)
			d_response["title"] = data_title[1]
		elif bool(re_identifiers.match(row)):
			string_identifiers = row.replace("Identifiers: ","")
			identifiers = string_identifiers.split("; ")
			for identifier in identifiers:
				try:
					(identifier_name, identifier_data) = identifier.split(": ",1)
				except:
					print("* [ERROR] I cannot split this line as expected:")
					print(identifier)
				identifier_name = identifier_name.replace(" ","_").lower()
				d_response[identifier_name] = identifier_data
		elif bool(re_attribute.match(row)):
			string_attribute = row.replace("    /","")
			data_attribute = string_attribute.split("=")
			attribute_name = data_attribute[0].replace(" ","_").lower()
			d_response[attribute_name] = data_attribute[1].strip('""')
		elif bool(re_accession.match(row)):
			flag_description = 0
			string_accession = row.replace("Accession: ", "")
			data_accession = string_accession.split("\tID: ")
			#print(data_accession)
			d_response["accession"] = data_accession[0]
			d_response["id"] = data_accession[1]
		elif bool(re_keywords.match(row)):
			flag_description = 0
			data_title = row.split(": ")
			d_response["keywords"] = data_title[1]
		elif bool(re_description.match(row)):
			flag_description = 1
		elif flag_description == 1:
			description = description + row
	d_response["description"] = description
	list_of_attributes = d_response.keys()
	return(d_response, list_of_attributes)

def get_runinfo_from_ncbi_id(term: str) -> str:
	request = "http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term={}".format(term)
	response = requests.get(url=request, stream=True)
	response.encoding = 'utf-8'
	return(response.text)

def get_csv_runinfo_from_biosamples(list_of_biosamples: list, csv_outfile: str):
	flag_header = 0
	with open(csv_outfile, "w") as outf:
		for biosample in list_of_biosamples:
			response = get_runinfo_from_ncbi_id(biosample)
			data = response.splitlines()
			header = data.pop(0)
			if (header.startswith("Run")) and (flag_header == 0):
				outf.write("{}\n".format(header))
				flag_header = 1
			outf.write("\n".join(data))

def get_json_runinfo_from_biosamples(list_of_biosamples: list, dir_json: str):
	d = {}
	# I create the json files in the output directory
	if not os.path.exists(dir_json):
		os.makedirs(dir_json)
	with IncrementalBar('Downloading...', max=len(list_of_biosamples), suffix='%(percent).1f%%') as bar:
		for biosample in list_of_biosamples:
			response = get_runinfo_from_ncbi_id(biosample)
			data = csv.DictReader(response.splitlines())
			for entry in data:
				d[entry["Run"]] = {}
				d[entry["Run"]] = entry
			with open(os.path.join(dir_json, biosample + ".json"),"w") as outf:
				json.dump(d, outf, indent = 4)
			bar.next()

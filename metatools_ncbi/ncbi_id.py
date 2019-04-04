import os
import re
import json
import requests
import csv


def get_ncbi_id_type(my_id):
	#bioproject
	re_bp=re.compile("^PRJ")
	if(len(re_bp.findall(my_id))!=0):
		return "bioproject"
	#biosample
	re_bs=re.compile("^SAM")
	if(len(re_bs.findall(my_id))!=0):
		return "biosample"
	#run
	re_r=re.compile("^ERR")
	re_r2=re.compile("^SRR")
	if((len(re_r.findall(my_id))!=0) or (len(re_r2.findall(my_id))!=0)):
		return "sra"
	return "unknown"

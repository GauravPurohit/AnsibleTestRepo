#!/usr/bin/python

import requests,os,zipfile,shutil
import requests.packages.urllib3
from shutil import copyfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# suppressing certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   

ANSIBLE_METADATA = {
	'metadata_version':'1.0',
	'status':['preview'],
	'supported_by':'curated'
}

DOCUMENTATION = '''
---
module: Ansible DownloadZip,Extract and Copy module
description: This module downloads archive.zip file from specified URL, unzips contents and copies over to desired location
options:
	name: 
		description: Name of the module being tested
		required: True
	url:
		description: Specified URL should point to the online service/repository location that holds the ansible.zip file
		required: True
	message:
		description: Optional message to include with the tests
		required: False
	success:
		description: Indicates the status of the test run at various points viz. during download, extract, copy. 
		required: False
'''

EXAMPLES = '''
---
# Pass in the name,url,message 
"name": "Ansible DownloadZip,Extract and Copy module",
"url":"https://raw.githubusercontent.com/GauravPurohit/AnsibleTestRepo/master/ansible.zip"
"message":"Test 1: Downloads zip, extracts content and copies it over to desired location"
"success":""

$ Pass in name, incorrect url, message
"name": "Ansible DownloadZip,Extract and Copy module",
"url":"https://raw.githubusercontent.com/GauravPurohit/AnsibleTestRepo/master/ansible.zip"
"message":"Test 2: Incorrect Url will fail downloading archive from the online service"
"success":""

'''

RETURN = '''
	name: 
		description: Name of the module being tested
		required: True
	url:
		description: Specified URL should point to the online service/repository location that holds the ansible.zip file
		required: True
	message:
		description: Optional message to include with the tests
		required: False
	success:
		description: Indicates the status of the test run at various points viz. during download, extract, copy. 
		required: False
'''

from ansible.module_utils.basic import AnsibleModule


# 'ExtractZipandCopyToDir' function extracts contents from the downloaded archive and copies it over to another directory.
# zipfilepath: C:\\cygwin1\\usr\\local\\lib\\library\\ansible.zip indicates the download location for the arhive
# zipfileextractdir: C:\\cygwin1\\usr\\local\\lib\\library\\ansible\\ indicates the directory where archive contents are to be extracted
# result: This dictionary stores the modified values of module_args to indicate the user at the output
# module: This is used by AnsibleModule to take in arguments from the 'arguments.json' file

def ExtractZipandCopyToDir(zipfilepath,zipfileextractdir,result,module):
	UnZipFileNewLocation = "C:\\cygwin1\\usr\\local\\lib\\library\\exports\\"    				# CopyTo directory location
	UnZipFileName = "ansible.config"
	try: 
		# extract contents
		tozip = zipfile.ZipFile(zipfilepath,'r')
		tozip.extractall(zipfileextractdir)
		tozip.close()
	except:
		result['success'] = "File Extract failed!"
		module.fail_json(msg='Error extracting the specified zip file', **result)
	try:
		if not os.path.exists(UnZipFileNewLocation):
			os.makedirs(UnZipFileNewLocation)
	except:
		result['success'] = "File Extract failed!"
		module.fail_json(msg='Error locating and/or creating the directory at the specified location!', **result)
	try: 
		# copy extracted contents to 'exports' directory
		copyfile(zipfileextractdir+UnZipFileName,UnZipFileNewLocation+UnZipFileName)
	except:
		result['success'] = "File Copy failed!"
		module.fail_json(msg='Error locating and/or copying the file at the specified location!', **result)
	try:
		# removes archive file and previous extracted directory
		if os.path.exists(zipfilepath):
			os.remove(zipfilepath)
		shutil.rmtree(zipfileextractdir)
	except:
		result['success'] = "File Copy failed!"
		module.fail_json(msg='Error locating and/or removing the file and/or directory at the specified path!', **result)
		
		
# 'DownloadZip' function downloads archive file from the specified online service/repository. 
# result: This dictionary stores the modified values of module_args to indicate the user at the output
# module: This is used by AnsibleModule to take in arguments from the 'arguments.json' file

def DownloadZip(result,module):
	ZipFileDwnLocation = "C:\\cygwin1\\usr\\local\\lib\\library\\"      									#File download location
	ZipFileName = "ansible.zip"																				#Downloaded archive file name
	ZipFileExtractDir = "C:\\cygwin1\\usr\\local\\lib\\library\\ansible\\"									#Directory to be extracted to
	DefaultUrlLink = "https://raw.githubusercontent.com/GauravPurohit/AnsibleTestRepo/master/ansible.zip" 			#Default Link to download archive file 
	
	if not result['url'] or result['url'] == '':
		url = UrlLink
	try: 
		# make webrequest using specified URL
		responsecontent = requests.get(result['url'], verify=False)
		if not responsecontent.status_code == 200:
			result['success'] = "File Download failed!"
			module.fail_json(msg='Error message:'+responsecontent.content)
	except:
		result['success'] = "File Download failed!"
		module.fail_json(msg='Error making a webrequest to the specified URL!', **result)
	try:
		# write response to generate archive file
		with open((ZipFileDwnLocation+ZipFileName),'wb') as f:
			f.write(responsecontent.content)
	except:
		result['success'] = "File Download failed!"
		module.fail_json(msg='Error writing the specified file from URL to the disk!', **result)
		
	ExtractZipandCopyToDir((ZipFileDwnLocation+ZipFileName),ZipFileExtractDir,result,module)
	
	result['success'] = "Download,Extract,Copy completed."
	module.exit_json(msg='Exports complete!', **result)
	
# 'main' function gets all the arguments required by the AnsibleModule from external 'arguments.json' file 
# and defines the result dictionary required to hold the modified values of module_args for the output. 

def main():
	module_args = dict(
	name = dict(type='str',required=True),   									#AnsibleModule name
	url = dict(type='str',required=True),    									#Download URL 
	message = dict(type='str',required=False),  								#Optional message
	success = dict(type='str',required=False, default="Initiating tests!")  	#Success indicator
	)
	module = AnsibleModule(
		argument_spec=module_args,
	)
	result = dict(
		name=module.params['name'],
		url=module.params['url'],
		message=module.params['message'],
		success=module.params['success']
	)
	DownloadZip(result,module)
	
	
if __name__ == '__main__':
	main()
		
		
		

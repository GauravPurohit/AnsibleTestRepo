#!/usr/bin/python

import requests
import os
import zipfile
import shutil
import requests.packages.urllib3
from shutil import copyfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
"message":"<Optional message goes here>"
"success":""
'''

RETURN = '''

'''

from ansible.module_utils.basic import AnsibleModule


def ExtractZipandCopyToDir(zipfilepath,zipfileextractdir,result,module):
	UnZipFileNewLocation = "C:\\cygwin1\\usr\\local\\lib\\library\\exports\\"
	UnZipFileName = "ansible.config"
	try: 
		tozip = zipfile.ZipFile(zipfilepath,'r')
		tozip.extractall(zipfileextractdir)
		tozip.close()
	except:
		module.fail_json(msg='Error extracting the specified zip file', **result)
	try:
		if not os.path.exists(UnZipFileNewLocation):
			os.makedirs(UnZipFileNewLocation)
	except:
		module.fail_json(msg='Error locating and/or creating the directory at the specified location!', **result)
	try: 
		copyfile(zipfileextractdir+UnZipFileName,UnZipFileNewLocation+UnZipFileName)
	except:
		module.fail_json(msg='Error locating and/or copying the file at the specified location!', **result)
	try:
		if os.path.exists(zipfilepath):
			os.remove(zipfilepath)
		shutil.rmtree(zipfileextractdir)
	except:
		module.fail_json(msg='Error locating and/or removing the file and/or directory at the specified path!', **result)
		

def DownloadZip(result,module):
	ZipFileDwnLocation = "C:\\cygwin1\\usr\\local\\lib\\library\\"
	ZipFileName = "ansible.zip"
	ZipFileExtractDir = "C:\\cygwin1\\usr\\local\\lib\\library\\ansible\\"
	
	if not result['url'] or result['url'] == '':
		url = "https://raw.githubusercontent.com/GauravPurohit/AnsibleTestRepo/master/ansible.zip"
	try: 
		responsecontent = requests.get(result['url'], verify=False)
		if not responsecontent.status_code == 200:
			module.fail_json(msg='Error making a webrequest to the specified URL!', **result)
	except: 
		module.fail_json(msg='Error making a webrequest to the specified URL!', **result)
	try:
		with open((ZipFileDwnLocation+ZipFileName),'wb') as f:
			f.write(responsecontent.content)
	except:
		module.fail_json(msg='Error writing the specified file from URL to the disk!', **result)
		
	ExtractZipandCopyToDir((ZipFileDwnLocation+ZipFileName),ZipFileExtractDir,result,module)
	
	result['success'] = "True"
	module.exit_json(msg='Exports complete!', **result)
	

def main():
	module_args = dict(
	name = dict(type='str',required=True),
	url = dict(type='str',required=True),
	message = dict(type='str',required=False),
	success = dict(type='str',required=False, default="Initiating tests!")
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
		
		
		

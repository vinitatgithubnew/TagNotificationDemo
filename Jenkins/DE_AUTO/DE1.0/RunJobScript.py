# Script to trigger the Installer creation on creation of Github Tag
# Created Date: 04-May-2023
# Created By: Vinit Kulkarni (vinkulka@bmc.com)
# Updated Date: 04-May-2023
# Updated By: 
# Referred Files (Make sure these files have accurate values before running this script):
# job.properties
# config.properties
# Usage : py .\RunJobScript.py

#-----------Libraries and Parameters Section Starts -----------------------------------
#Python Modules/Libraries
import sys
import subprocess
import  re

#Script Parameters
JENKINS_URL = 'java -jar jenkins-cli.jar -s http://vl-aus-domqa134:8080/ -auth admin:admin -webSocket'
#-----------Libraries and Parameters Section Ends -----------------------------------

#-----------Functions Section Starts -----------------------------------
#function to validate configuration files
def validateConfigFiles():
	errors = ""
	configDictionary = loadConfigProperties()
	jobDictionary = loadJobProperties()
	if not configDictionary["PLATFORM_HELM_VERSION"]:
		errors = errors + " PLATFORM_HELM_VERSION is blank.\n"
	if not configDictionary["SMARTAPPS_HELM_VERSION"]:
		errors = errors + " SMARTAPPS_HELM_VERSION is blank.\n"
	if not configDictionary["HELM_VERSION"]:
		errors = errors + " HELM_VERSION is blank.\n"
	if not configDictionary["TARGET_VERSION"]:
		errors = errors + " TARGET_VERSION is blank.\n"
	if not configDictionary["TEMPLATE_SMARTAPPS_HELM_VERSION"]:
		errors = errors + " TEMPLATE_SMARTAPPS_HELM_VERSION is blank.\n"
	if not configDictionary["JENKINS_JOB_NAME"]:
		errors = errors + " JENKINS_JOB_NAME is blank.\n"
	return errors
 
#Function to load the job.properties file to dictionary
def loadJobProperties():
	with open('job.properties') as file:
		jobDictionary = dict(line.strip().split('=') for line in file)
	return jobDictionary

#Function to load the job.properties file to dictionary
def loadConfigProperties():
	with open('config.properties') as file:
		configDictionary = dict(line.strip().split('=') for line in file)
	return configDictionary

#Function to Replace the content in the HELIX_ONPREM_DEPLOYMENT file by refering to job.properties 
def updateUberPipeline():
	configDictionary = loadConfigProperties()
	file = open("..\..\..\pipeline\jenkinsfile\HELIX_ONPREM_DEPLOYMENT.jenkinsfile", "r")
	replaced_content = ""
	#Replace the PLATFORM and SMARTAPPS HELM VERSION + Update SOURCE_VERSION
	for line in file:
		new_line= line
		if "name: 'PLATFORM_HELM_VERSION')" in line:
			new_line = line.replace(line.split("['", 1)[1].split("']")[0], configDictionary["PLATFORM_HELM_VERSION"])
		elif "name: 'SMARTAPPS_HELM_VERSION')" in line:
			new_line = line.replace(line.split("['", 1)[1].split("']")[0], configDictionary["SMARTAPPS_HELM_VERSION"])
		elif "name: 'SOURCE_VERSION')" in line:
			if configDictionary["APPEND_SOURCE_VERSION"] != '':
				versions = line.split("[", 1)[1].split("]")[0].split(",")
				lastVersion = versions.pop()
				replace_str = lastVersion + ",'" + configDictionary["APPEND_SOURCE_VERSION"] + "'"
				new_line = line.replace(lastVersion, replace_str)
		replaced_content = replaced_content + new_line
	file.close()

	#Replace the content in the HELIX_ONPREM_DEPLOYMENT file
	write_file = open("..\..\..\pipeline\jenkinsfile\HELIX_ONPREM_DEPLOYMENT.jenkinsfile", "w")
	write_file.write(replaced_content)
	write_file.close()

#Function to update ITSM Template file with correct TARGET and HELM version from job.properties
def updateITSMTemplateFile(fileName):
	configDictionary = loadConfigProperties()
	filePath = "..\\..\\..\\pipeline\\tasks\\inputTemplates\\" + fileName
	file = open(filePath, "r")
	replaced_content = ""
	#Replace the PLATFORM and SMARTAPPS HELM VERSION + Update SOURCE_VERSION
	for line in file:
		new_line= line
		type(line)
		if line.startswith("HELM_VERSION"):
			print(line)
			new_line = 'HELM_VERSION="'+ configDictionary["HELM_VERSION"] + '"\n'
		elif line.startswith("TARGET_VERSION"):
			print(line)
			new_line = 'TARGET_VERSION="'+ configDictionary["TARGET_VERSION"] + '"\n'
		elif line.startswith("SMARTAPPS_HELM_VERSION"):
			print(line)
			new_line = 'SMARTAPPS_HELM_VERSION="'+ configDictionary["TEMPLATE_SMARTAPPS_HELM_VERSION"] + '"\n'
		replaced_content = replaced_content + new_line
	file.close()

	#Replace the content in the HELIX_ONPREM_DEPLOYMENT file
	write_file = open(filePath, "w")
	write_file.write(replaced_content)
	write_file.close()

#Function to prepare the Batch file with git and Jenkins commands
def addGitAndJenkinCommandsToBatch():
	jobDictionary = loadJobProperties()
	configDictionary = loadConfigProperties()
	JOB_NAME = configDictionary["JENKINS_JOB_NAME"]
	jobParameters = ''
	for key in jobDictionary:
		jobParameters = jobParameters + ' -p ' + key + '=' + jobDictionary[key]

	with open(r'TriggerInstallerJob.bat', 'w+') as file:
		file.writelines('cd ..\..\..\ \n') #itsm-git-installer path where git commands can be executed
		file.writelines('git add .\n')
		commitMessage = 'Updated with version ' + configDictionary["PLATFORM_HELM_VERSION"]
		file.writelines('git commit -m "' + commitMessage + '"\n')
		file.writelines('git push\n')
		file.writelines('cd Jenkins/DE_AUTO/DE1.0\n')
		
		#check in the changes and push to repo
		file.writelines(JENKINS_URL + ' build ' + JOB_NAME + jobParameters + ' \n')
		file.writelines(JENKINS_URL + ' console '+ JOB_NAME + ' -f')
#-----------Functions Section Ends -----------------------------------
    
#-----------Execution Section Starts -----------------------------------
#Step 1: Replace/update Uber Pipeline and ITSM Template files with correct version number
errors = validateConfigFiles()
if not errors:
    updateUberPipeline()
    updateITSMTemplateFile("itsmtemplate_compact.sh")
    updateITSMTemplateFile("itsmtemplate_large.sh")
    updateITSMTemplateFile("itsmtemplate_small.sh")
    updateITSMTemplateFile("itsmtemplate_medium.sh")
    #Step 2: Create the Batch file with Jenkin command with correct parameters
    addGitAndJenkinCommandsToBatch()
    #Step 3: Trigger the job
    print("Jenkins parameters read from config files and commands ready. Running the job now.")
    subprocess.call([r'TriggerInstallerJob.bat'])
else:
	print("Parameters in the configuration files is/are not valid. Errors:")
	print(errors)
#-----------Execution Section Ends -----------------------------------
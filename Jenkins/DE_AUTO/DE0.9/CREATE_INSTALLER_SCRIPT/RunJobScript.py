# Script to trigger the Installer creation on creation of Github Tag
# Created Date: 04-May-2023
# Created By: Vinit Kulkarni (vinkulka@bmc.com)
# Updated Date: 04-May-2023
# Updated By: 
# Referred Files (Make sure these files have accurate values before running this script):
# config.properties
# job.properties
# Usage : py .\RunJobScript.py

#-----------Libraries and Parameters Section Starts -----------------------------------
#Python Modules/Libraries
import sys
import subprocess
import  re

#-----------Libraries and Parameters Section Ends -----------------------------------

#-----------Functions Section Starts -----------------------------------
#function to validate configuration files
def validateConfigFiles():
	print("Validating config files...")
	errors = ""
	configDictionary = loadConfigProperties()
	if not configDictionary["PLATFORM_HELM_VERSION"]:
		errors = errors + " PLATFORM_HELM_VERSION is blank.\n"
	if not configDictionary["SMARTAPPS_HELM_VERSION"]:
		errors = errors + " SMARTAPPS_HELM_VERSION is blank.\n"
	if not configDictionary["JENKINS_JOB_NAME"]:
		errors = errors + " JENKINS_JOB_NAME is blank.\n"

	if not errors:
		print("Validation of config files successful...")

	return errors
 
#Function to load the job.properties file to dictionary
def loadJobProperties():
	with open('job.properties') as file:
		comment_less = filter(None, (line.split('#')[0].strip() for line in file))
		jobDictionary = dict(line.strip().split('=') for line in comment_less)
	return jobDictionary

#Function to load the job.properties file to dictionary
def loadConfigProperties():
	with open('config.properties') as file:
		comment_less = filter(None, (line.split('#')[0].strip() for line in file))
		configDictionary = dict(line.strip().split('=') for line in comment_less)
	return configDictionary

#Function to Replace the content in the HELIX_ONPREM_DEPLOYMENT file by refering to job.properties 
def updateUberPipeline():
	configDictionary = loadConfigProperties()
	print("Updating uber pipeline jenkinsfile...")
	file = open("../../../../pipeline/jenkinsfile/HELIX_ONPREM_DEPLOYMENT.jenkinsfile", "r")
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
	write_file = open("../../../../pipeline/jenkinsfile/HELIX_ONPREM_DEPLOYMENT.jenkinsfile", "w")
	write_file.write(replaced_content)
	write_file.close()
	print("Update uber pipeline jenkinsfile successful...")
 
#Function to update ITSM Template file with correct TARGET and HELM version from job.properties
def updateITSMTemplateFile(fileName):
	print("Updating itsm Template file " + fileName + "...")    
	configDictionary = loadConfigProperties()
	filePath = "../../../../pipeline/tasks/inputTemplates/" + fileName
	file = open(filePath, "r")
	replaced_content = ""
	#Replace the PLATFORM and SMARTAPPS HELM VERSION + Update SOURCE_VERSION
	for line in file:
		new_line= line
		type(line)
		if line.startswith("HELM_VERSION"):
			new_line = 'HELM_VERSION="'+ configDictionary["PLATFORM_HELM_VERSION"] + '"\n'
		elif line.startswith("TARGET_VERSION"):
			new_line = 'TARGET_VERSION="'+ configDictionary["PLATFORM_HELM_VERSION"] + '"\n'
		elif line.startswith("SMARTAPPS_HELM_VERSION"):
			new_line = 'SMARTAPPS_HELM_VERSION="'+ configDictionary["SMARTAPPS_HELM_VERSION"] + '"\n'
		replaced_content = replaced_content + new_line
	file.close()

	#Replace the content in the HELIX_ONPREM_DEPLOYMENT file
	write_file = open(filePath, "w")
	write_file.write(replaced_content)
	write_file.close()
	print("Update itsm Template file " + fileName + " successful...")

#Function to prepare the Batch file with git and Jenkins commands
def addGitAndJenkinCommandsToBatch():
	print("Preparing Batch file with git and jenkins commands...")
	jobDictionary = loadJobProperties()
	configDictionary = loadConfigProperties()
	JENKINS_URL = 'java -jar jenkins-cli.jar -s http://' + configDictionary["JENKINS_SERVER"] + ':' + configDictionary["JENKINS_PORT"]+ '/ -auth ' + configDictionary["JENKINS_USERNAME"]+':'+configDictionary["JENKINS_PASSWORD"] + ' -webSocket'
	JOB_NAME = configDictionary["JENKINS_JOB_NAME"]
	#Set Job Parameters before creating jenkins command
	jobDictionary["PLATFORM_HELM_VERSION"] = configDictionary["PLATFORM_HELM_VERSION"]
	jobDictionary["SMARTAPPS_HELM_VERSION"] = configDictionary["SMARTAPPS_HELM_VERSION"]
	jobDictionary["ZIP_VERSION"] = configDictionary["ZIP_VERSION"]
	jobDictionary["PLAYBOOKS_REPO_BRANCH"] = configDictionary["PLAYBOOKS_REPO_BRANCH"]
	
	jobParameters = ''
	for key in jobDictionary:
		jobParameters = jobParameters + ' -p ' + key + '=' + jobDictionary[key].replace('GIT_TOKEN', configDictionary['GIT_TOKEN'])

	with open(r'TriggerInstallerJob.sh', 'w+') as file:
		file.writelines('cd ../../../../ \n') #itsm-git-installer path where git commands can be executed
		file.writelines('git add .\n')
		commitMessage = 'HELM_VERSION: ' + configDictionary["PLATFORM_HELM_VERSION"] + ' and SMARTAPPS_VERSION: ' + configDictionary["SMARTAPPS_HELM_VERSION"]
		file.writelines('git commit -m "' + commitMessage + '"\n')
		file.writelines('git push\n')
		file.writelines('cd Jenkins/DE_AUTO/DE0.9\n')
		
		#check in the changes and push to repo
		file.writelines(JENKINS_URL + ' build ' + JOB_NAME + jobParameters + ' \n')
		file.writelines(JENKINS_URL + ' console '+ JOB_NAME + ' -f')
		print("Prepare Batch file with git and jenkins commands successful...")
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
    print("Running the batch file for installer creation now....")
    #subprocess.call([r'sh TriggerInstallerJob.sh'], shell=True)
else:
	print("Parameters in the configuration files is/are not valid. Errors:")
	print(errors)
#-----------Execution Section Ends -----------------------------------
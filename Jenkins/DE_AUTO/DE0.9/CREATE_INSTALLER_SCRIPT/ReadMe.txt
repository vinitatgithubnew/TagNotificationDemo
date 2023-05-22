# Steps to configure environment and run the installer screation job
# Created Date: 04-May-2023
# Created By: Vinit Kulkarni (vinkulka@bmc.com)
# Updated Date: 
# Updated By: 

Steps to Create the Installer Creation Job on your Jenkins Instance (Need to be done once per Jenkins Server):
- Navigate to DE1.0 folder in itsm-on-premise-installer repository. For e.g. /var/git/AUTO/itsm-on-premise-installer/Jenkins/DE_AUTO/DE1.0
- Execute command from your dedicated VM machine: curl http://admin:admin@vl-aus-domqa134:8080/job/CREATE_ONPREM_INSTALLER/config.xml | java -jar jenkins-cli.jar -s http://<JENKIN_USERNAME>:<JENKIN_PASSWORD>@<JENKIN_INSTANCE>:<PORT>/ create-job CREATE_ONPREM_INSTALLER
For e.g http://admin:admin@vl-aus-domqa134:8080/job/CREATE_ONPREM_INSTALLER/config.xml | java -jar jenkins-cli.jar -s http://Admin:Admin@clm-aus-uqe1fr:8080/ create-job CREATE_ONPREM_INSTALLER
- This will create the installer creation job with required parameters on your Jenkins instance.

Steps to Run the Installer Creation Script:
- Navigate to CREATE_INSTALLER_SCRIPT folder in itsm-on-premise-installer repository. For e.g. /var/git/AUTO/itsm-on-premise-installer/Jenkins/DE_AUTO/DE1.0/CREATE_INSTALLER_SCRIPT
- Edit config.properties file: vi config.properties
- Modify following parameters as per your requirements:
APPEND_SOURCE_VERSION=2021308.1.08.00 //Keept this blank if no SOURCE_VERSION to append
PLATFORM_HELM_VERSION=2022106.0.04.00 //New HELM_VERSION - tag received from the product team. Keep it unchanged if want to continue with same version.
SMARTAPPS_HELM_VERSION=2022106.0.04.06 //New SMARTAPPS_HELM_VERSION - tag received from the product team. Keep it unchanged if want to continue with same version.
ZIP_VERSION=22106_DROP4 //Update the ZIP version as per requirement
PLAYBOOKS_REPO_BRANCH=213000-maint//Update the branch if needed
JENKINS_JOB_NAME=CREATE_ONPREM_INSTALLER
JENKINS_SERVER=vl-aus-domqa134 //Your Jenkins Server Name
JENKINS_PORT=8080 //Your Jenkins Port
JENKINS_USERNAME=admin //Your Jenkins Username
JENKINS_PASSWORD= //Your Jenkins Password
GIT_TOKEN=//Git Token
- Review job.properties file and modify parameters if needed. Please note, python script uses following job parameters from config.properties that you need not modify in job.properties.
PLAYBOOKS_REPO_BRANCH
PLATFORM_HELM_VERSION
SMARTAPPS_HELM_VERSION
ZIP_VERSION
- Run the script using following command:
python RunJobScript.py
- After completion, build (zip) will be available at: /tmp/<ZIP_VERSION>
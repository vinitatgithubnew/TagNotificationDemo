cd ..\..\..\ 
git add .
git commit -m "Updated with version 2022106.0.02.00"
git push
cd Jenkins/DE_AUTO/DE1.0
java -jar jenkins-cli.jar -s http://vl-aus-domqa134:8080/ -auth admin:admin -webSocket build HELIX_IS_ZIP_RETAG -p CUSTOMER_CONFIG_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/DSOM-ADE/onprem-remedyserver-config.git -p ITSM_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/helix-data-migration/itsm-on-premise-installer.git -p PLAYBOOKS_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/core-remedy/helix-deploy-playbooks.git -p PLAYBOOKS_REPO_BRANCH=213000-maint -p HELM_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/core-remedy/containerization-certified.git -p SMARTAPPS_HELM_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/core-remedy/containerization-smartapps-certified.git -p SMARTREPORTING_PLAYBOOKS_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/core-remedy/smartreporting-deploy-playbooks.git -p SMARTREPORTING_HELM_REPO=https://9bbd889ebd2f1d15d1430c183b850d3be54301cb@github.bmc.com/core-remedy/smartreporting-containerization-certified.git -p ADD_DTR_YAML=false -p PLATFORM_HELM_VERSION=2022106.0.03.00 -p SMARTAPPS_HELM_VERSION=2022106.0.03.04 -p SMARTREPORTING_HELM_VERSION=210503.1.09.00 -p SMARTREPORTING2_HELM_VERSION=2021303.1.06.00 -p AGENT=vl-aus-domqa134 -p CHECKOUT_USING_USER=github -p ZIP_VERSION=22106_DROP3 -p RETAG_PLATFORM=false -p PLATFORM_HELM_NEW_TAG=2021308.1.00.00 -p RETAG_SMARTAPPS=false -p SMARTAPPS_HELM_NEW_TAG=2021308.1.00.00
java -jar jenkins-cli.jar -s http://vl-aus-domqa134:8080/ -auth admin:admin -webSocket console HELIX_IS_ZIP_RETAG -f
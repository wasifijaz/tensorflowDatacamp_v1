from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os
import argparse

def DataByXPath(driver,xpath):
    try:    
        data = driver.find_elements_by_xpath(xpath)[0]
        return data.text
    except Exception: 
        return None
    
def PressButton(driver,xpath):
    elem = driver.find_element_by_xpath(xpath)
    action = ActionChains(driver)
    action.click(on_element = elem)
    action.perform()
    time.sleep(5)

def SendElement(driver, xpath, data):
    element = driver.find_elements_by_xpath(xpath)[0]
    element.send_keys(data)

def Package_Mapping(driver,trackingIds):
    packageMapping = pd.DataFrame(columns = ['Tracking_ID','Latest_Status','Delivery_Status','Destination','Shipped_From','Shipped_On','Delivered_To','Delivered_On','Service','Shipment_Weight','Signed_By'])

    for x in trackingIds:
        print('Tracking ID: ',x)
        
        SendElement(driver,'//*[@id="frmTrackSearch"]/div/div/input',x)
        PressButton(driver,"//*[@id='frmTrackSearch']/div/div/span/button")
        
        latestStatus = DataByXPath(driver,"//*[@id='us-0']/div[5]/div[2]/div/section/div[1]/div[1]/div[1]/div")
        deliveryStatus = DataByXPath(driver,"//*[@id='us-0']/div[5]/div[2]/div/section/div[1]/div[2]/div[1]/div")
        destination = DataByXPath(driver,"//*[@id='us-0']/div[5]/div[2]/div/section/div[1]/div[2]/div[2]/div")
        shippedFrom = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[1]/div[1]/div[2]")
        shippedOn  = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[1]/div[2]/div[2]")
        deliveredTo = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[2]/div[1]/div[2]")
        deliveredOn = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[2]/div[2]/div[2]")
        service = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[3]/div[1]/div[2]")
        shipmentWeight = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[3]/div[2]/div[2]")
        signedBy = DataByXPath(driver,"//*[@id='us-0']/div[6]/div/div[2]/section/div/div[3]/div[9]/div[2]")

        packageMapping.loc[trackingIds[trackingIds == x].index[0]] = [x,latestStatus,deliveryStatus,destination,shippedFrom,shippedOn,deliveredTo,deliveredOn,service,shipmentWeight,signedBy]
        packageMapping = packageMapping.dropna(thresh = 2, axis = 0)
    
    packageMapping.to_csv("D:/packageMapping_Website_Data.csv", index=True)
    print(packageMapping)

def Package_Trackr(driver,trackingIds):
    packageTrackr = pd.DataFrame(columns = ['Tracking_ID','Shipped_From','Shipped_On','Delivered_To','Delivered_On','Service','Shipment_Weight'])

    for x in trackingIds:
        print('Tracking ID: ',x)
        
        SendElement(driver,'//*[@id="track-box-form"]/div/input',x)
        PressButton(driver,"//*[@id='track-box-form']/div/span[2]/button")

        shippedFrom = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[1]/div[1]/div/div[2]")
        shippedOn  = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[1]/div[2]/div/div[2]")
        deliveredTo = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[2]/div[1]/div/div[2]")
        deliveredOn = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[2]/div[2]/div/div[2]")
        service = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[3]/div[1]/div/div[2]")
        shipmentWeight = DataByXPath(driver,"//*[@id='track-info-panel-region']/div/div[8]/div[4]/div[1]/div/div[2]")
        
        packageTrackr.loc[trackingIds[trackingIds == x].index[0]] = [x,shippedFrom,shippedOn,deliveredTo,deliveredOn,service,shipmentWeight]
        packageTrackr = packageTrackr.dropna(thresh = 2, axis = 0)

        PressButton("//*[@id='body']/div[1]/div/ul/li[1]/a")
        if 'google_vignette' in driver.current_url:
            driver.get('https://www.packagetrackr.com/track')
    
    packageTrackr.to_csv("D:/packageTrackr_Website_Data.csv", index=True)
    print(packageTrackr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--Package_Mapping',action='store_true')
    parser.add_argument('--Package_Trackr',action='store_true')
    args = parser.parse_args()
        
    options = webdriver.ChromeOptions()
    options.binary_location = os.path.normpath("C:/Program Files/Google/Chrome/Application/chrome.exe")
    chrome_driver_binary = os.path.normpath("C:/Users/wasif.ijaz/Downloads/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    data = pd.read_csv(os.path.normpath("C:/Users/wasif.ijaz/Downloads/Mailroom_OCR_Regex_tracking_Test_Set_Courier_from_DB.csv"))
    mailroomData = pd.DataFrame(data)

    trackingIds = mailroomData['tracking_no']
    trackingIds = trackingIds.dropna(axis=0)

    if args.Package_Mapping:
        driver.get('https://packagemapping.com/') 
        time.sleep(10)     
        Package_Mapping(driver,trackingIds)
        driver.close()

    elif args.Package_Trackr:
        driver.get('https://www.packagetrackr.com/')
        time.sleep(10)
        Package_Trackr(driver,trackingIds)
        driver.close()

if __name__ == '__main__':
    main()
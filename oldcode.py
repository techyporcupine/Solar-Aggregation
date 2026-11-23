def commons():
    global totalDCPower
    commonsPreURL = 'https://solrenview.com/cgi-bin/cgihandler.cgi?&view=4,0,0,1&cond=site_ID=6740'
    commonsURL = f'https://solrenview.com/downloads/tmp/Site6740_Eastern(Inverter-Direct,Day%20of%20{todayDate}).csv'

    #try:
    #    requests.get(commonsPreURL, timeout=15, headers=headers)
    #    commonsDF = pandas.read_csv(commonsURL,skiprows=2,storage_options=headers) # make dataframe for UC

    #except requests.exceptions.RequestException as e:
    #    print(f"Error grabbing University Commons: {e}")
    #    return


    with requests.Session() as session:
        session.headers.update(headers)
        
        try:
            session.get(commonsPreURL, timeout=15)
            
            csv_response = session.get(commonsURL, timeout=15)
            csv_response.raise_for_status() # Ensure the download actually worked
            
        except requests.exceptions.RequestException as e:
            print(f"Error grabbing University Commons: {e}")
            return

    commonsDF = pandas.read_csv(io.StringIO(csv_response.text), skiprows=2)

    commonsDF = commonsDF.drop(0) # drop row 0 (one with units)
    commonsDF = commonsDF.dropna(subset=['AC Voltage']) # drop any rows without data in their "AC Voltage" column
    commonsDF['DC Voltage'] = commonsDF['DC Voltage'].str.strip("\t") # strip the trailing "\t" that was in the DC Voltage column
    commonsDF['DC Current'] = commonsDF['DC Current'].str.strip() # strip the trailing space that was in the DC current column
    commonsDF[['VDC1','VDC2']] = commonsDF['DC Voltage'].str.split("/",expand=True) # Create VDC1 and VDC2 from DC Voltage
    commonsDF[['DC1 Cur','DC2 Cur']] = commonsDF['DC Current'].str.split("/",expand=True) # Create DC1 Cur and DC2 Cur from DC Voltage
    commonsDF[['VAC1','VAC2','VAC3']] = commonsDF['AC Voltage'].str.split("/",expand=True) # Create VAC columns for each phase
    commonsDF['DC1 Pow'] = (commonsDF['VDC1'].astype(float)*commonsDF['DC1 Cur'].astype(float))*0.001
    commonsDF['DC2 Pow'] = (commonsDF['VDC2'].astype(float)*commonsDF['DC2 Cur'].astype(float))*0.001
    commonsDF['DC Pow'] = commonsDF['DC1 Pow'] + commonsDF['DC2 Pow']
    commonsDF = commonsDF.drop(columns=['AC Power','Ambient','Irradiance','Wind Direction','Wind Speed','DC Voltage','DC Current','AC Voltage']) # drop columns with these in the name

    #print(commonsDF.tail(20))

    #print(commonsDF['DC1 Pow'].tail(20))

    print("\n----University Commons Solar----")
    print("Producing since September 2018")
    print("Latest Data:")
    print("- Module Temperature: " + str(commonsDF['Module'].iloc[-1]))
    print("- AC Voltages (per phase): " + str(commonsDF['VAC1'].iloc[-1]) + " VAC1, " + str(commonsDF['VAC2'].iloc[-1]) + " VAC2, " + str(commonsDF['VAC3'].iloc[-1]) + " VAC3")
    print("- DC Voltages (per string): " + str(commonsDF['VDC1'].iloc[-1]) + " VDC1, " + str(commonsDF['VDC2'].iloc[-1]) + " VDC2")
    print("- DC Current (per string): " + str(commonsDF['DC1 Cur'].iloc[-1]) + "A, " + str(commonsDF['DC2 Cur'].iloc[-1]) + "A")
    print("- DC Wattage (per string): " + str(commonsDF['DC1 Pow'].iloc[-1]) + "kW, " + str(commonsDF['DC2 Pow'].iloc[-1]) + "kW")
    print("- DC Wattage (total): " + str(commonsDF['DC Pow'].iloc[-1]) + "kW")
    totalDCPower += commonsDF['DC Pow'].iloc[-1]


def roselawn():
    global totalDCPower
    roselawnPreURL = 'https://solrenview.com/cgi-bin/cgihandler.cgi?&view=4,0,0,1&cond=site_ID=6738'
    roselawnURL = f'https://solrenview.com/downloads/tmp/Site6738_Eastern(Inverter-Direct,Day%20of%20{todayDate}).csv'

    #try:
    #    requests.get(roselawnPreURL, timeout=15, headers=headers)
    #    roselawnDF = pandas.read_csv(roselawnURL,skiprows=2,storage_options=headers) # make dataframe for roselawn
    #except requests.exceptions.RequestException as e:
    #    print(f"Error grabbing Roselawn: {e}")
    #    return

    with requests.Session() as session:
        session.headers.update(headers)
        
        try:
            session.get(roselawnPreURL, timeout=15)
            
            csv_response = session.get(roselawnURL, timeout=15)
            csv_response.raise_for_status() # Ensure the download actually worked
            
        except requests.exceptions.RequestException as e:
            print(f"Error grabbing Roselawn: {e}")
            return

    roselawnDF = pandas.read_csv(io.StringIO(csv_response.text), skiprows=2)


    roselawnDF = roselawnDF.drop(0) # drop row 0 (one with units)
    roselawnDF = roselawnDF.dropna(subset=['AC Voltage','AC Voltage.1']) # drop any rows without data in their "AC Voltage" column
    roselawnDF['DC Voltage'] = roselawnDF['DC Voltage'].str.strip("\t") # strip the trailing "\t" that was in the DC Voltage column
    roselawnDF['DC Voltage.1'] = roselawnDF['DC Voltage.1'].str.strip("\t") # strip the trailing "\t" that was in the DC Voltage column
    roselawnDF['DC Current'] = roselawnDF['DC Current'].str.strip() # strip the trailing space that was in the DC current column
    roselawnDF['DC Current.1'] = roselawnDF['DC Current.1'].str.strip() # strip the trailing space that was in the DC current column
    roselawnDF[['VDC1','VDC2']] = roselawnDF['DC Voltage'].str.split("/",expand=True) # Create VDC1 and VDC2 from DC Voltage
    roselawnDF[['VDC1.1','VDC2.1']] = roselawnDF['DC Voltage.1'].str.split("/",expand=True) # Create VDC1 and VDC2 from DC Voltage
    roselawnDF[['DC1 Cur','DC2 Cur']] = roselawnDF['DC Current'].str.split("/",expand=True) # Create DC1 Cur and DC2 Cur from DC Voltage
    roselawnDF[['DC1.1 Cur','DC2.1 Cur']] = roselawnDF['DC Current.1'].str.split("/",expand=True) # Create DC1 Cur and DC2 Cur from DC Voltage
    roselawnDF[['VAC1','VAC2','VAC3']] = roselawnDF['AC Voltage'].str.split("/",expand=True) # Create VAC columns for each phase
    roselawnDF[['VAC1.1','VAC2.1','VAC3.1']] = roselawnDF['AC Voltage.1'].str.split("/",expand=True) # Create VAC columns for each phase
    roselawnDF['DC1 Pow'] = (roselawnDF['VDC1'].astype(float)*roselawnDF['DC1 Cur'].astype(float))*0.001
    roselawnDF['DC1.1 Pow'] = (roselawnDF['VDC1.1'].astype(float)*roselawnDF['DC1.1 Cur'].astype(float))*0.001
    roselawnDF['DC2 Pow'] = (roselawnDF['VDC2'].astype(float)*roselawnDF['DC2 Cur'].astype(float))*0.001
    roselawnDF['DC2.1 Pow'] = (roselawnDF['VDC2.1'].astype(float)*roselawnDF['DC2.1 Cur'].astype(float))*0.001
    roselawnDF['DC.0 Pow'] = roselawnDF['DC1 Pow'] + roselawnDF['DC2 Pow']
    roselawnDF['DC.1 Pow'] = roselawnDF['DC1.1 Pow'] + roselawnDF['DC2.1 Pow']
    roselawnDF['DC Pow'] = roselawnDF['DC.0 Pow'] + roselawnDF['DC.1 Pow']

    roselawnDF = roselawnDF.drop(columns=['AC Power','Ambient','Irradiance','Wind Direction','Wind Speed','DC Voltage','DC Current','AC Voltage']) # drop columns with these in the name

    #print(roselawnDF.tail(20))

    #print(roselawnDF['DC1 Pow'].tail(20))

    print("\n----Roselawn Solar----")
    print("Producing since September 2018")
    print("Latest Data:")
    print("- Module Temperature: " + str(roselawnDF['Module'].iloc[-1]))
    print("- Inv. 0 AC Voltages (per phase): " + str(roselawnDF['VAC1'].iloc[-1]) + " VAC1, " + str(roselawnDF['VAC2'].iloc[-1]) + " VAC2, " + str(roselawnDF['VAC3'].iloc[-1]) + " VAC3")
    print("- Inv. 0 DC Voltages (per string): " + str(roselawnDF['VDC1'].iloc[-1]) + " VDC1, " + str(roselawnDF['VDC2'].iloc[-1]) + " VDC2")
    print("- Inv. 0 DC Current (per string): " + str(roselawnDF['DC1 Cur'].iloc[-1]) + "A, " + str(roselawnDF['DC2 Cur'].iloc[-1]) + "A")
    print("- Inv. 0 DC Wattage (per string): " + str(roselawnDF['DC1 Pow'].iloc[-1]) + "kW, " + str(roselawnDF['DC2 Pow'].iloc[-1]) + "kW")
    print("- Inv. 0 DC Wattage (total): " + str(roselawnDF['DC.0 Pow'].iloc[-1]) + "kW")

    print("- Inv. 1 AC Voltages (per phase): " + str(roselawnDF['VAC1.1'].iloc[-1]) + " VAC1, " + str(roselawnDF['VAC2.1'].iloc[-1]) + " VAC2, " + str(roselawnDF['VAC3'].iloc[-1]) + " VAC3")
    print("- Inv. 1 DC Voltages (per string): " + str(roselawnDF['VDC1.1'].iloc[-1]) + " VDC1, " + str(roselawnDF['VDC2.1'].iloc[-1]) + " VDC2")
    print("- Inv. 1 DC Current (per string): " + str(roselawnDF['DC1.1 Cur'].iloc[-1]) + "A, " + str(roselawnDF['DC2.1 Cur'].iloc[-1]) + "A")
    print("- Inv. 1 DC Wattage (per string): " + str(roselawnDF['DC1.1 Pow'].iloc[-1]) + "kW, " + str(roselawnDF['DC2.1 Pow'].iloc[-1]) + "kW")
    print("- Inv. 1 DC Wattage (total): " + str(roselawnDF['DC.1 Pow'].iloc[-1]) + "kW")

    print("- DC Wattage (total): " + str(roselawnDF['DC Pow'].iloc[-1]) + "kW")
    totalDCPower += roselawnDF['DC Pow'].iloc[-1]

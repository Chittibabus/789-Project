
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import csv
import datetime
import pickle as pkl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# In[ ]:


month_number = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


# In[ ]:


def Structure_for_data_sortdate():
    print('hi')
    Crimefileread = csv.reader(open(r'crime file',
        'r'))
    fld = next(Crimefileread)
    print(fld)
    crimes_datewise = {'fld': fld, 'data':{}}
    i = 0
    for row in Crimefileread:
        dateSplit = row[2].split(' ')[0]
        datemapper = dateSplit.split('/')
        date = datetime.date(int(datemapper[2]), int(datemapper[0]), int(datemapper[1]))
        if date in crimes_datewise['data'].keys():
            crimes_datewise['data'][date].append(row)
        else:
            crimes_datewise['data'][date] = [row]
        if i%10000 == 0:
            print (i)
        i += 1
    return crimes_datewise
    pkl.dump(crimes_datewise, open('crimes_datewise.pkl', 'wb'))
    print('Hi')


# In[ ]:


def count_alleylightsand_crimes(crmbsdt=None):
    print('hi')
    Outagefile_read = csv.reader(open(r'alley lights file','r'))
    fld = next(Outagefile_read)
    print (fld)
    if crmbsdt == None:
        crmbsdt = Structure_for_data_sortdate()
    output_file = open('crimes_alley' + '.csv', 'w')
    crime_types = ['THEFT', 'NARCOTICS', 'BATTERY', 'CRIMINAL DAMAGE'] +        ['MOTOR VEHICLE THEFT', 'ROBBERY', 'ASSAULT', 'BURGLARY', 'HOMICIDE']
    header = ','.join(map(str, fld))
    header += ',DateCreated,DateCompleted,OutageDuration,After.Period.Duration,'
    header_offset = len(header)
    for t in crime_types:
        tabel_list = [v.capitalize() for v in t.split(' ')]
        tabel_srt = str(tabel_list).strip('[]')            .replace(' ','').replace(',','').replace('\'','')
        header += tabel_srt + '.During,'
        header += tabel_srt + '.Before,'
        header += tabel_srt + '.After,'
    header += 'Crimes.Alley.During,Crimes.Alley.Before,Crimes.Alley.After,'
    header += 'Crimes.All.During,Crimes.All.Before,Crimes.All.After,'
    header += 'DeceptivePractice.During,DeceptivePractice.Before,DeceptivePractice.After\n'
    output_file.write(header)
    print (header)
    Type_of_crime = dict((t, crime_types.index(t)*3) for t in crime_types)
    indexing_alley = 3 * len(crime_types)
    Index_all = indexing_alley + 3
    dec_index = Index_all + 3
    print (Type_of_crime)
    
    j = 0
    next(Outagefile_read)
    for row in Outagefile_read:
        print(row[2])
        s = str(row).strip('[]')
        dmy = row[2].split('-')
        crime_date  = datetime.date(2000+int(dmy[2]), int(dmy[1]),int(dmy[0]))
        dmy = row[3].split('-')
        crm_date  = datetime.date(2000+int(dmy[2]), int(dmy[1]),int(dmy[0]))
        if crm_date > datetime.date(2019, 12, 31):
            continue
            
        s += ',' + str(crime_date) + ',' + str(crm_date) + ','
        
        
        counts = [0] * (3*len(crime_types) + 9)
        during_outage = (crime_date, crm_date)
        before_outage = (max(datetime.date(2001, 1, 1), crime_date-datetime.timedelta(37)),
            crime_date-datetime.timedelta(7))
        after_outage = (crm_date + datetime.timedelta(7),
            min(datetime.date(2019, 12, 31), crm_date + datetime.timedelta(37)))
        
        s += str((during_outage[1]-during_outage[0]).days+1) + ','
        s += str((after_outage[1]-after_outage[0]).days) + ','
        out_location1 = str(row[4]).split()[0].zfill(5)[0:3]  
        out_location2 = " ".join(str(row[4]).split()[1:])     
        
        
        # DURING_OUTAGE
        d = during_outage[0]
        while d <= during_outage[1]:
            for c in crmbsdt['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loc_crime1 = str(c[3]).split()[0][0:3]
                    loc_crime2 = " ".join(str(c[3]).split()[1:])
                    if loc_crime1 == out_location1 and loc_crime2 == out_location2:
                        if c[7] == 'ALLEY':
                            if t == 'DECEPTIVE PRACTICE':
                                counts[dec_index] += 1
                            else:
                                counts[Index_all] += 1
                                counts[Type_of_crime[t]] += 1
                                counts[indexing_alley] += 1
            d += datetime.timedelta(1)
        
        # BEFORE_OUTAGE
        d = before_outage[0]
        while d < before_outage[1]:
            for c in crmbsdt['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loc_crime1 = str(c[3]).split()[0][0:3]
                    loc_crime2 = " ".join(str(c[3]).split()[1:])
                    if loc_crime1 == out_location1 and loc_crime2 == out_location2:
                        if c[7] == 'ALLEY':
                            if t == 'DECEPTIVE PRACTICE':
                                counts[dec_index+1] += 1
                            else:
                                counts[Index_all+1] += 1
                                counts[Type_of_crime[t]+1] += 1
                                counts[indexing_alley+1] += 1
            d += datetime.timedelta(1)
        
        # AFTER_OUTAGE
        d = after_outage[0] + datetime.timedelta(1)
        while d <= after_outage[1]:
            for c in crmbsdt['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loc_crime1 = str(c[3]).split()[0][0:3]
                    loc_crime2 = " ".join(str(c[3]).split()[1:])
                    if loc_crime1 == out_location1 and loc_crime2 == out_location2:
                        if c[7] == 'ALLEY':
                            if t == 'DECEPTIVE PRACTICE':
                                counts[dec_index+2] += 1
                            else:
                                counts[Index_all+2] += 1
                                counts[Type_of_crime[t]+2] += 1
                                counts[indexing_alley+2] += 1
            d += datetime.timedelta(1)
        s += str(counts).strip('[]') + '\n'
        output_file.write(s)
        j += 1
        if j%10 == 0:
            print (j)
        
    output_file.close()


# In[ ]:


def Count_lightsandCrimes(outage_type='street-one', crmbydate=None):
    
    if outage_type == 'street-one':
        outage_file = r'srteet one out file'
    elif outage_type == 'street-all':
        outage_file = r'street all out'
    outage_r = csv.reader(open(outage_file, 'r'))
    fields_data = next(outage_r)
    print (fields_data)
    if crmbydate == None:
        crmbydate = Structure_for_data_sortdate()
    
    
    out_file_crime = open(outage_type + '.csv', 'w')
    
    
    crime_types = ['THEFT', 'NARCOTICS', 'BATTERY', 'CRIMINAL DAMAGE'] +        ['MOTOR VEHICLE THEFT', 'ROBBERY', 'ASSAULT', 'BURGLARY', 'HOMICIDE']
    
    
    header = ','.join(map(str, fields_data))
    header += ',DateCreated,DateCompleted,OutageDuration,After.Period.Duration,'
    header_offset = len(header)
    for t in crime_types:
        
        tebel_list = [v.capitalize() for v in t.split(' ')]
        tebel_str = str(tebel_list).strip('[]')            .replace(' ','').replace(',','').replace('\'','')
        header += tebel_str + '.During,'
        header += tebel_str + '.Before,'
        header += tebel_str + '.After,'
    header += 'Crimes.Alley.During,Crimes.Alley.Before,Crimes.Alley.After,'
    header += 'Crimes.All.During,Crimes.All.Before,Crimes.All.After,'
    header += 'DeceptivePractice.During,DeceptivePractice.Before,DeceptivePractice.After\n'
    out_file_crime.write(header)
    
    print (header)
    type_crime_byid = dict((t, crime_types.index(t)*3) for t in crime_types)
    index_alley = 3 * len(crime_types)
    index_all = index_alley + 3
    dec_index = index_all + 3
    print (type_crime_byid)

    j = 0
    next(outage_r)
    for row in outage_r:
        
        s = str(row).strip('[]')
        dmy = row[2].split('-')
        cr_date  = datetime.date(2000+int(dmy[2]), int(month_number[dmy[1]]),
            int(dmy[0]))
        dmy = row[3].split('-')
        co_date  = datetime.date(2000+int(dmy[2]), int(month_number[dmy[1]]),
            int(dmy[0]))
        if co_date > datetime.date(2019, 12, 31):
            continue

        s += ',' + str(cr_date) + ',' + str(co_date) + ','
        
        
        counts = [0] * (3*len(crime_types) + 9)
        during_outage_wind = (cr_date, co_date)
        before_outage_wind = (max(datetime.date(2001, 1, 1), cr_date-datetime.timedelta(37)),
            cr_date-datetime.timedelta(7))
        after_outage_wind = (co_date + datetime.timedelta(7),
            min(datetime.date(2019, 12, 31), co_date + datetime.timedelta(37)))
        
        s += str((during_outage_wind[1]-during_outage_wind[0]).days+1) + ','
        s += str((after_outage_wind[1]-after_outage_wind[0]).days) + ','
        out_location1 = str(row[4]).split()[0].zfill(5)[0:3]  
        out_location2 = " ".join(str(row[4]).split()[1:])     
         
        
        # DURING_OUTAGE
        d = during_outage_wind[0]
        while d <= during_outage_wind[1]:
            for c in crmbydate['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loctn_crime1 = str(c[3]).split()[0][0:3]
                    loctn_crime2 = " ".join(str(c[3]).split()[1:])
                    if loctn_crime1 == out_location1 and loctn_crime2 == out_location2:
                        if t == 'DECEPTIVE PRACTICE':
                            counts[dec_index] += 1
                        else:
                            counts[index_all] += 1
                            counts[type_crime_byid[t]] += 1
                            if c[7] == 'ALLEY':
                                counts[index_alley] += 1
            d += datetime.timedelta(1)
        
        # BEFORE_OUTAGE
        d = before_outage_wind[0]
        while d < before_outage_wind[1]:
            for c in crmbydate['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loctn_crime1 = str(c[3]).split()[0][0:3]
                    loctn_crime2 = " ".join(str(c[3]).split()[1:])
                    if loctn_crime1 == out_location1 and loctn_crime2 == out_location2:
                        if t == 'DECEPTIVE PRACTICE':
                            counts[dec_index+1] += 1
                        else:
                            counts[index_all+1] += 1
                            counts[type_crime_byid[t]+1] += 1
                            if c[7] == 'ALLEY':
                                counts[index_alley+1] += 1
            d += datetime.timedelta(1)
        
        # AFTER_OUTAGE
        d = after_outage_wind[0] + datetime.timedelta(1)
        while d <= after_outage_wind[1]:
            for c in crmbydate['data'][d]:
                t = c[5]
                if (t in crime_types or t == 'DECEPTIVE PRACTICE')                    and c[15] != '' and c[16] != '':
                    loctn_crime1 = str(c[3]).split()[0][0:3]
                    loctn_crime2 = " ".join(str(c[3]).split()[1:])
                    if loctn_crime1 == out_location1 and loctn_crime2 == out_location2:
                        if t == 'DECEPTIVE PRACTICE':
                            counts[dec_index+2] += 1
                        else:
                            counts[index_all+2] += 1
                            counts[type_crime_byid[t]+2] += 1
                            if c[7] == 'ALLEY':
                                counts[index_alley+2] += 1
            d += datetime.timedelta(1)
        s += str(counts).strip('[]') + '\n'
        out_file_crime.write(s)
        j += 1
        if j%10 == 0:
            print (j)
   
    out_file_crime.close()


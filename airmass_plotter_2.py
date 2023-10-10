
'''
version 2.0 - updated star airmass plotting routine.
Queries JPL Horizons for Jupiter, Saturn, Uranus, and Neptune and plots airmasses over time. Will also plot and any manually-entered cal stars, but have to save those airmasses manually.
Uses https://astroquery.readthedocs.io/en/latest/jplhorizons/jplhorizons.html to query Horizons. See github page for info on requirements and installation.
Astroplan, for plotting airmasses of stars: https://github.com/astropy/astroplan/tree/main
IRTF star catalog: http://irtfweb.ifa.hawaii.edu/IRrefdata/Catalogs/bsc_a0.dat


To do: could make x-axis more intuitive with better time labels.

Emma Dahl, 2/22/2023
'''

from astroquery.jplhorizons import Horizons
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import astroplan
from astroplan import Observer
from astropy.coordinates import SkyCoord
from astroplan import FixedTarget
from astropy.time import Time



fig, ax = plt.subplots(dpi=100)
fig.set_size_inches(7, 5) # set size

# UTC = HST + 10 hrs
observing_start_time_UTC = '2023-10-14 10:00:00'
observing_end_time_UTC = '2023-10-14 16:00:00' # day after
save_location = './airmass_plot.png' # name and where the figure will be saved



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Outer Planets

# Define Jupiter object; 568 = Mauna Kea
id_number = '599' # Jupiter
obj = Horizons(id=id_number, location='568', epochs={'start':observing_start_time_UTC,                                                      'stop':observing_end_time_UTC,                                                       'step':'10m'}) 
# put ephimerides into a table
table = obj.ephemerides() 
# convert day/time to usable units:
dates = []
for i in table['datetime_str']:
    dates.append(datetime.strptime(i, '%Y-%b-%d %H:%M')) # define the format of the datetime_str column
# Plot curve, converting time to HST:
plt.plot(np.array(dates)-timedelta(hours=10), table['airmass'],label='Jupiter', linewidth=2)
# save RA/dec
jup_coord = np.array((table['RA'],table['DEC']))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Define Saturn object; 568 = Mauna Kea
id_number = '699' # Saturn
obj = Horizons(id=id_number, location='568', epochs={'start':observing_start_time_UTC,                                                      'stop':observing_end_time_UTC,                                                       'step':'10m'}) 
# put ephimerides into a table
table = obj.ephemerides() 
# convert day/time to usable units:
dates = []
for i in table['datetime_str']:
    dates.append(datetime.strptime(i, '%Y-%b-%d %H:%M')) # define the format of the datetime_str column
# Plot curve, converting time to HST:
plt.plot(np.array(dates)-timedelta(hours=10), table['airmass'],label='Saturn')
# save RA/dec
sat_coord = np.array((table['RA'],table['DEC']))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Define Uranus object; 568 = Mauna Kea
id_number = '799' # Uranus
obj = Horizons(id=id_number, location='568', epochs={'start':observing_start_time_UTC,                                                      'stop':observing_end_time_UTC,                                                       'step':'10m'}) 
# put ephimerides into a table
table = obj.ephemerides() 
# convert day/time to usable units:
dates = []
for i in table['datetime_str']:
    dates.append(datetime.strptime(i, '%Y-%b-%d %H:%M')) # define the format of the datetime_str column
# Plot curve, converting time to HST:
plt.plot(np.array(dates)-timedelta(hours=10), table['airmass'],label='Uranus')
# save RA/dec
ur_coord = np.array((table['RA'],table['DEC']))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Define Neptune object; 568 = Mauna Kea
id_number = '899' # Neptune
obj = Horizons(id=id_number, location='568', epochs={'start':observing_start_time_UTC,                                                      'stop':observing_end_time_UTC,                                                       'step':'10m'}) 
# put ephimerides into a table
table = obj.ephemerides() 
# convert day/time to usable units:
dates = []
for i in table['datetime_str']:
    dates.append(datetime.strptime(i, '%Y-%b-%d %H:%M')) # define the format of the datetime_str column
# Plot curve, converting time to HST:
plt.plot(np.array(dates)-timedelta(hours=10), table['airmass'],label='Neptune')
# save RA/dec
nep_coord = np.array((table['RA'],table['DEC']))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Stars

star1_label = 'HD 219477 (G2V)'
# RA and dec: 23:15:46      +28:14:52 

star2_label = 'HD 13936 (A0V)'
#  02h15m28.3s -09d27m56s

star3_label = 'HD 12846 (G2V)'
# 2  6 30.24  +24 20  2.4

irtf = Observer.at_site('irtf')

# replace coordinates
coordinates_star1 = SkyCoord('23h15m46s', '+28d14m52s', frame='icrs')
coordinates_star2 = SkyCoord('02h15m28.3s', '-09d27m56s', frame='icrs')
coordinates_star3 = SkyCoord('02h06m30.2s', '+24d20m02.4s', frame='icrs')

# replace name with Star name
star1 = FixedTarget(name=star1_label, coord=coordinates_star1)
star2 = FixedTarget(name=star2_label, coord=coordinates_star2)
star3 = FixedTarget(name=star3_label, coord=coordinates_star3)

# use dates from above planet object to make stars
HST_date_array = np.array(dates)#-timedelta(hours=10)

airmass_star1 = []
airmass_star2 = []
airmass_star3 = []

for d in HST_date_array:
    airmass_star1.append(float(irtf.altaz(d, star1).secz))
    airmass_star2.append(float(irtf.altaz(d, star2).secz))
    airmass_star3.append(float(irtf.altaz(d, star3).secz))
    
#plt.plot(np.array(dates)-timedelta(hours=10), airmass_star1, label=star1_label, linestyle='dashed')
plt.plot(np.array(dates)-timedelta(hours=10), airmass_star2, label=star2_label,linestyle='dashed')
plt.plot(np.array(dates)-timedelta(hours=10), airmass_star3, label=star3_label,linestyle='dashed')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# line at 1.5 airmasses; limit for this observing run
#plt.plot([datetime.strptime(observing_start_time_UTC, '%Y-%m-%d %H:%M:%S')-timedelta(hours=10), datetime.strptime(observing_end_time_UTC, '%Y-%m-%d %H:%M:%S')-timedelta(hours=10)], [1.5,1.5], '--')

plt.gca().invert_yaxis()
plt.title(str(datetime.strptime(observing_start_time_UTC, '%Y-%m-%d %H:%M:%S').date()))
plt.ylabel('Airmass')
plt.xlabel('Date, hour (HST)')
plt.legend()
plt.ylim(3.0,0.9)
plt.savefig(save_location, bbox_inches='tight')
#plt.show()


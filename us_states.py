# coding=utf-8
#
# Provides a list of selected US states along with their average coordinates. 
# Allows to match a location described by its latitude and longitude with the listed states.
#
# Resources:
#   * Python Dictionary of US States, http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories
#   * Average Latitude and Longitude for US States, http://dev.maxmind.com/geoip/legacy/codes/state_latlon
#   * Distance between latitude and longitude pairs using the Haversine formula, http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python
#   * Searching a Python dictionary by value, http://rtoodtoo.net/2012/03/20/searching-dictionary-by-value-in-python
#
# Coordinates convention:
#   * signed decimal degrees without compass direction, negative numbers represent south or west
#   * examples: 
#	latitudes:
#       30° 45´ 50´´N -> 30.4550
#       28° 61´ 39´´S -> -28.6139
#
#	longitudes:
#       77° 20´ 89´´E -> 30.4550
#       30° 45´ 50´´W -> 30.4550

import json
import math

class USStates(object):
  
  def __init__(self):

    # Tolerated accuracy in kilometers expressed as a maximum number of kilometers
    # the searched location can be distant from the given state's average coordinates
    # for the location to be considered as part of that state  
    self.max_distance = 500

    # Earth's mean radius in kilometers 
    self.R = 6371

    # A list of selected US states along with their average coordinates
    self.states = {
        'AK': {'name':'Alaska','coords':[61.3850,-152.2683]},
        'AL': {'name':'Alabama','coords':[32.7990,-86.8073]},
        'AR': {'name':'Arkansas','coords':[34.9513,-92.3809]},
        'AS': {'name':'American Samoa','coords':[14.2417,-170.7197]},
        'AZ': {'name':'Arizona','coords':[33.7712,-111.3877]},
        'CA': {'name':'California','coords':[36.1700,-119.7462]},
        'CO': {'name':'Colorado','coords':[39.0646,-105.3272]},
        'CT': {'name':'Connecticut','coords':[41.5834,-72.7622]},
        'DC': {'name':'District of Columbia','coords':[38.8964,-77.0262]},
        'DE': {'name':'Delaware','coords':[39.3498,-75.5148]},
        'FL': {'name':'Florida','coords':[27.8333,-81.7170]},
        'GA': {'name':'Georgia','coords':[32.9866,-83.6487]},
        'HI': {'name':'Hawaii','coords':[21.1098,-157.5311]},
        'IA': {'name':'Iowa','coords':[42.0046,-93.2140]},
        'ID': {'name':'Idaho','coords':[44.2394,-114.5103]},
        'IL': {'name':'Illinois','coords':[40.3363,-89.0022]},
        'IN': {'name':'Indiana','coords':[39.8647,-86.2604]},
        'KS': {'name':'Kansas','coords':[38.5111,-96.8005]},
        'KY': {'name':'Kentucky','coords':[37.6690,-84.6514]},
        'LA': {'name':'Louisiana','coords':[31.1801,-91.8749]},
        'MA': {'name':'Massachusetts','coords':[42.2373,-71.5314]},
        'MD': {'name':'Maryland','coords':[39.0724,-76.7902]},
        'ME': {'name':'Maine','coords':[44.6074,-69.3977]},
        'MI': {'name':'Michigan','coords':[43.3504,-84.5603]},
        'MN': {'name':'Minnesota','coords':[45.7326,-93.9196]},
        'MO': {'name':'Missouri','coords':[38.4623,-92.3020]},
        'MP': {'name':'Northern Mariana Islands','coords':[14.8058,145.5505]},
        'MS': {'name':'Mississippi','coords':[32.7673,-89.6812]},
        'MT': {'name':'Montana','coords':[46.9048,-110.3261]},
        'NC': {'name':'North Carolina','coords':[35.6411,-79.8431]},
        'ND': {'name':'North Dakota','coords':[47.5362,-99.7930]},
        'NE': {'name':'Nebraska','coords':[41.1289,-98.2883]},
        'NH': {'name':'New Hampshire','coords':[43.4108,-71.5653]},
        'NJ': {'name':'New Jersey','coords':[40.3140,-74.5089]},
        'NM': {'name':'New Mexico','coords':[34.8375,-106.2371]},
        'NV': {'name':'Nevada','coords':[38.4199,-117.1219]},
        'NY': {'name':'New York','coords':[42.1497,-74.9384]},
        'OH': {'name':'Ohio','coords':[40.3736,-82.7755]},
        'OK': {'name':'Oklahoma','coords':[35.5376,-96.9247]},
        'OR': {'name':'Oregon','coords':[44.5672,-122.1269]},
        'PA': {'name':'Pennsylvania','coords':[40.5773,-77.2640]},
        'PR': {'name':'Puerto Rico','coords':[18.2766,-66.3350]},
        'RI': {'name':'Rhode Island','coords':[41.6772,-71.5101]},
        'SC': {'name':'South Carolina','coords':[33.8191,-80.9066]},
        'SD': {'name':'South Dakota','coords':[44.2853,-99.4632]},
        'TN': {'name':'Tennessee','coords':[35.7449,-86.7489]},
        'TX': {'name':'Texas','coords':[31.1060,-97.6475]},
        'UT': {'name':'Utah','coords':[40.1135,-111.8535]},
        'VA': {'name':'Virginia','coords':[37.7680,-78.2057]},
        'VI': {'name':'Virgin Islands','coords':[18.0001,-64.8199]},
        'VT': {'name':'Vermont','coords':[44.0407,-72.7093]},
        'WA': {'name':'Washington','coords':[47.3917,-121.5708]},
        'WI': {'name':'Wisconsin','coords':[44.2563,-89.6385]},
        'WV': {'name':'West Virginia','coords':[38.4680,-80.9696]},
        'WY': {'name':'Wyoming','coords':[42.7475,-107.2085]}
    }

  def is_valid_code(self, code):
    return code in self.states

  def by_name(self, name):
    names = [ k for k, v in self.states.items() if v['name'] == name ]
    return names[0] if len(names) > 0 else None

  def haversine(self, origin, destination):
    # two pairs of latitude and longitude, i.e. origin vs destination
    lat1, lon1 = origin
    lat2, lon2 = destination

    # deltas between origin and destination coordinates
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)

    # a central angle between the two points
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)

    # the determinative angle of the triangle on the surface of the sphere (Earth) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # a spherical distance between the two points, i.e. hills etc are not considered 
    return self.R * c 

  def by_coords(self, latitude, longitude):
    distances = {}
    for k, v in self.states.iteritems():
      coords = v['coords']  
      distance = self.haversine(coords, [latitude, longitude])
      distances[k] = distance

    shortest_distance = min(distances.values())

    if shortest_distance > self.max_distance:
      return None
    else:
      return [ k for k, v in distances.items() if v == shortest_distance ][0]
 
def main():
  us_states = USStates()
  print us_states.by_name('California')
  print us_states.by_coords(38.3454, -121.2935) # Sacramento, California
  print us_states.by_coords(30.25, -97.75) # Austin, Texas

if __name__ == '__main__':
    main()
 

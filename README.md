I have recently enrolled to [Introduction to Data Science](https://class.coursera.org/datasci-002). One of the very first assignments was Twitter sentinent analysis performed in Python. Leaving a whole lot aside, what captured my attention was a requirement to resolve tweets' geocoded locations WITHOUT relying on 3rd party services.

The assignment paper suggested to use a [Python Dictionary of State Abbreviations](http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories). That proved helpful indeed. I have decided to combine this resource with [Average Latitude and Longitude for US States](http://dev.maxmind.com/geoip/legacy/codes/state_latlon) and ended up with a single dictionary containing all essential information, i.e. state codes, names and coordinates:

```python
{
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
  ..
```

A complete dictionary is to be found in [us_states.py](./us_states.py).

Having all the relevant information in place, I was looking for a feasible way of associating the tweets with the list of US states. Turns out that [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula) is one of the most popular methods for calculating distance between two pairs of coordinates.

My implementation of the Haversine formula merely mirrors the unbeatable [Python example at platoscave.net](http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python), here is the result (see [us_states.py](./us_states.py) for full details):

```python
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
```
The algorithm above is the core of my custom search method, which simply picks up the state which closely matches the provided coordinates (a minimum distance). To eliminate non-US countries, I have set a hard limit of 500 km as a maximum distance between the provided coordinates and the average coordinates of any of the states. This leaves me with a nice and handy feature:

```python
def main():
  us_states = USStates()
  
  # Sacramento, California - prints CA
  print us_states.by_coords(38.3454, -121.2935)
  
  # Austin, Texas - prints TX
  print us_states.by_coords(30.25, -97.75)
  
  # New Delhi, India - yields no results 
  # as the minimum calculated distance is well over 13.000 km
  print us_states.by_coords(28.6139, 77.2089)
```

One last note, the coordinates comprise latitude and longitude using the convention of a signed decimal degrees without compass direction. Negative numbers represent south or west, examples:

```python
#   latitudes:
#   30° 45´ 50´´N -> 30.4550
#   28° 61´ 39´´S -> -28.6139
#
#   longitudes:
#   77° 20´ 89´´E -> 77.2089
#   30° 45´ 50´´W -> -30.4550
```

[us_states.py](./us_states.py) contains the full implementation, whereas [us_states_test.py](./us_states_test.py) are unit tests covering the main scenarios as well as some edge cases.


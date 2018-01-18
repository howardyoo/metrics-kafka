# example of converting dropwizard metrics json into wavefront data for proxy.
# supporting point tags in the message payload
# howard yoo 2017.12.4
# updated in 2018.1.17 - to add support for metric name point tags
import json

# example json string to parse.
json_string = """
{
   "hostName":"localhost",
   "timers":{
      "test.test-timer{}":{
         "count":1,
         "max":503.627465,
         "mean":503.627465,
         "min":503.627465,
         "p50":503.627465,
         "p75":503.627465,
         "p95":503.627465,
         "p98":503.627465,
         "p99":503.627465,
         "p999":503.627465,
         "stddev":0.0,
         "m15_rate":0.0,
         "m1_rate":0.0,
         "m5_rate":0.0,
         "mean_rate":0.6491825224591039,
         "duration_units":"milliseconds",
         "rate_units":"calls/second"
      }
   },
   "histograms":{
      "test.response-sizes{}":{
         "count":1,
         "max":100,
         "mean":100.0,
         "min":100,
         "p50":100.0,
         "p75":100.0,
         "p95":100.0,
         "p98":100.0,
         "p99":100.0,
         "p999":100.0,
         "stddev":0.0
      }
   },
   "counters":{
      "test.requests{mode=test, type=counter2}":{
         "count":1
      },
      "test.requests{mode=test, type=counter}":{
         "count":1
      }
   },
   "ip":"192.168.2.110",
   "rateUnit":"second",
   "pointTags":{
      "cluster":"c-1",
      "appName":"myapp"
   },
   "gauges":{
      "test.jvm.mem.non-heap.used{}":{
         "value":19992776
      },
      "test.jvm.mem.pools.Metaspace.usage{}":{
         "value":0.9669634285619704
      },
      "test.jvm.mem.total.init{}":{
         "value":270991360
      },
      "test.jvm.mem.pools.PS-Survivor-Space.max{}":{
         "value":11010048
      },
      "test.jvm.mem.pools.PS-Old-Gen.used-after-gc{}":{
         "value":0
      },
      "test.jvm.mem.pools.Metaspace.init{}":{
         "value":0
      },
      "test.jvm.mem.heap.usage{}":{
         "value":0.004368015908500841
      },
      "test.jvm.mem.pools.Compressed-Class-Space.max{}":{
         "value":1073741824
      },
      "test.jvm.mem.total.max{}":{
         "value":3817865215
      },
      "test.jvm.mem.heap.committed{}":{
         "value":257425408
      },
      "test.jvm.mem.pools.PS-Eden-Space.committed{}":{
         "value":67108864
      },
      "test.jvm.mem.pools.PS-Eden-Space.init{}":{
         "value":67108864
      },
      "test.jvm.mem.heap.init{}":{
         "value":268435456
      },
      "test.jvm.mem.pools.PS-Old-Gen.used{}":{
         "value":16384
      },
      "test.jvm.mem.pools.PS-Old-Gen.max{}":{
         "value":2863661056
      },
      "test.jvm.mem.pools.Code-Cache.used{}":{
         "value":3282240
      },
      "test.jvm.mem.pools.PS-Old-Gen.committed{}":{
         "value":179306496
      },
      "test.jvm.mem.pools.Compressed-Class-Space.init{}":{
         "value":0
      },
      "test.jvm.mem.pools.Compressed-Class-Space.usage{}":{
         "value":0.0018396005034446716
      },
      "test.jvm.gc.PS-MarkSweep.time{}":{
         "value":0
      },
      "test.jvm.mem.pools.PS-Eden-Space.used-after-gc{}":{
         "value":0
      },
      "test.jvm.mem.pools.Code-Cache.committed{}":{
         "value":3342336
      },
      "test.jvm.mem.non-heap.max{}":{
         "value":-1
      },
      "test.jvm.mem.heap.max{}":{
         "value":3817865216
      },
      "test.jvm.mem.pools.PS-Eden-Space.max{}":{
         "value":1409286144
      },
      "test.jvm.mem.pools.PS-Survivor-Space.usage{}":{
         "value":0.7815043131510416
      },
      "test.jvm.mem.pools.PS-Old-Gen.usage{}":{
         "value":5.721347491761259E-6
      },
      "test.jvm.mem.heap.used{}":{
         "value":16676496
      },
      "test.jvm.mem.pools.Metaspace.committed{}":{
         "value":15466496
      },
      "test.jvm.mem.pools.PS-Old-Gen.init{}":{
         "value":179306496
      },
      "test.jvm.mem.non-heap.committed{}":{
         "value":20905984
      },
      "test.jvm.mem.total.used{}":{
         "value":36918568
      },
      "test.jvm.mem.pools.Compressed-Class-Space.committed{}":{
         "value":2097152
      },
      "test.jvm.mem.pools.Metaspace.used{}":{
         "value":14975872
      },
      "test.jvm.mem.total.committed{}":{
         "value":278331392
      },
      "test.jvm.mem.pools.Metaspace.max{}":{
         "value":-1
      },
      "test.jvm.mem.pools.PS-Survivor-Space.used-after-gc{}":{
         "value":8604400
      },
      "test.jvm.mem.pools.Code-Cache.init{}":{
         "value":2555904
      },
      "test.jvm.mem.pools.PS-Survivor-Space.used{}":{
         "value":8604400
      },
      "test.jvm.mem.pools.Compressed-Class-Space.used{}":{
         "value":1975256
      },
      "test.jvm.mem.pools.PS-Survivor-Space.committed{}":{
         "value":11010048
      },
      "test.jvm.gc.PS-MarkSweep.count{}":{
         "value":0
      },
      "test.jvm.gc.PS-Scavenge.count{}":{
         "value":1
      },
      "test.jvm.mem.pools.Code-Cache.usage{}":{
         "value":0.013081614176432292
      },
      "test.jvm.mem.pools.Code-Cache.max{}":{
         "value":251658240
      },
      "test.jvm.mem.non-heap.init{}":{
         "value":2555904
      },
      "test.jvm.mem.pools.PS-Eden-Space.used{}":{
         "value":8055712
      },
      "test.jvm.gc.PS-Scavenge.time{}":{
         "value":10
      },
      "test.jvm.mem.non-heap.usage{}":{
         "value":-2.0245744E7
      },
      "test.jvm.mem.pools.PS-Survivor-Space.init{}":{
         "value":11010048
      },
      "test.jvm.mem.pools.PS-Eden-Space.usage{}":{
         "value":0.005716164906819661
      }
   },
   "durationUnit":"milliseconds",
   "clock":1516244746764,
   "meters":{

   }
}
"""

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def convertTimer(a_timer):
	if a_timer is None:
		return ""
	
	m_map = {}
	l_pointTag = {}
	s = ""

	for key in a_timer:
		values = a_timer[key]
		for value in values:
			v = values[value];
			if type(v).__name__ == "str" or type(v).__name__ == "unicode":
				l_pointTag[value] = v
			else:
				m_map[key + "." + value] = values[value];

	m_pointTag = merge_two_dicts(g_pointTag, l_pointTag)

	# now, print out all the metrics along with merged local and global pointtags
	for mname in m_map:
		s += toWavefrontData(mname, str(m_map[mname]), source, str(clock), m_pointTag) + "\n"

	return s

def convertGauge(a_gauge):
	if a_gauge is None:
		return ""

	s = ""
	for key in a_gauge:
		s += toWavefrontData(key, str(a_gauge[key]["value"]), source, str(clock), g_pointTag) + "\n"
	return s

def convertCounter(a_counter):
	if a_counter is None:
		return ""

	s = ""
	for key in a_counter:
		s += toWavefrontData(key, str(a_counter[key]["count"]), source, str(clock), g_pointTag) + "\n"
	return s

def convertHistogram(a_histogram):
	if a_histogram is None:
		return ""

	s = ""
	for key in a_histogram:
		values = a_histogram[key]
		for value in values:
			s += toWavefrontData(key + "." + value, str(values[value]), source, str(clock), g_pointTag) + "\n"
	return s


def pointTagsToStr(pointTags):
	s = ""
	for key in pointTags:
		s += " "
		s += key
		s += "="
		s += "\"" + pointTags[key] + "\""
	return s

def strToDict(string):
	if string.find('{}') > -1:
		metric = string.split('{}')
		metric[1] = {}
		return metric
	if string.find('{') > -1:
		metric = string.split('{')
		ptstring = metric[1].split('}')[0]
		ptdict = dict(x.strip().split('=') for x in ptstring.split(','))
		metric[1] = ptdict
		return metric
	else:
		v = [string, {}]
		return v

def toWavefrontData(metricName, value, source, timestamp, pointTags):
	s = ""
	if metricName != "":
		mtrArray = strToDict(metricName)

		if value != "":
			if source != "":
				s += mtrArray[0] + " " + value
				if timestamp != "":
					s += " " + timestamp
				s += " source=\"" + source + "\""
				if pointTags is not None:
					s += pointTagsToStr(pointTags)
					s += pointTagsToStr(mtrArray[1])
	return s

def convertMetricsToWavefront(jsondata):
	s = ""
	s += convertTimer(jsondata['timers'])
	s += convertHistogram(jsondata['histograms'])
	s += convertCounter(jsondata['counters'])
	s += convertGauge(jsondata['gauges'])
	return s

# --------------- MAIN CODE ------------------

# parse the json into json object
jsondata = json.loads(json_string)

# collect the following global parameters
ip = jsondata['ip']
hostname = jsondata['hostName']
clock = jsondata['clock']
rateUnit = jsondata['rateUnit']
durationUnit = jsondata['durationUnit']

# define source. if localhost is the hostname, use ip instead
source = hostname
if source == "localhost":
	source = ip

# global point tag
g_pointTag = {}

# if point tags exist, use it.
if 'pointTags' in jsondata:
    g_pointTag = jsondata['pointTags']

# append additional point tags
g_pointTag["rateUnit"] = str(rateUnit)
g_pointTag["durationUnit"] = str(durationUnit)

# main convert function
print(convertMetricsToWavefront(jsondata))

print "--- end ---"

# end


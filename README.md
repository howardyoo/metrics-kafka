# metrics-kafka
Dropwizard Metrics reporter for kafka.

https://github.com/dropwizard/metrics

Report json metrics data to kafka. Kafka comsumer can process metrics data.

NOTE: this library requires 5.0-development branch.

## Example

### Environment Setup

http://kafka.apache.org/082/documentation.html#quickstart

### Reporter

```java
package io.github.hengyunabc.metrics.test;

import java.io.IOException;
import java.util.Properties;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;
import java.util.Map;
import java.util.HashMap;

import io.dropwizard.metrics5.ConsoleReporter;
import io.dropwizard.metrics5.Histogram;
import io.dropwizard.metrics5.MetricRegistry;
import io.dropwizard.metrics5.MetricName;
import io.dropwizard.metrics5.Counter;
import io.dropwizard.metrics5.Timer.Context;
import io.dropwizard.metrics5.jvm.GarbageCollectorMetricSet;
import io.dropwizard.metrics5.jvm.MemoryUsageGaugeSet;

import io.github.hengyunabc.metrics.WavefrontKafkaReporter;
import kafka.producer.ProducerConfig;

public class WavefrontKafkaReporterSample
{
	static final MetricRegistry metrics = new MetricRegistry();
	static public Timer timer = new Timer();

	public static void main(String args[]) throws IOException,
			InterruptedException {
		ConsoleReporter reporter = ConsoleReporter.forRegistry(metrics)
				.convertRatesTo(TimeUnit.SECONDS)
				.convertDurationsTo(TimeUnit.MILLISECONDS).build();
		metrics.register("jvm.mem", new MemoryUsageGaugeSet());
		metrics.register("jvm.gc", new GarbageCollectorMetricSet());

		// the new point tags for metric name feature
		Map<String, String> tags = new HashMap<String, String>();
		tags.put("type", "counter");
		tags.put("mode", "test");

		MetricName name = new MetricName("requests", tags);
		Counter counter = metrics.counter(name);

		// counter increment test
		counter.inc();

		// second counter, with same name, but different tags
		Map<String, String> tags2 = new HashMap<String, String>();
		tags2.put("type", "counter2");
		tags2.put("mode", "test");

		MetricName name2 = new MetricName("requests", tags2);
		Counter counter2 = metrics.counter(name2);
		counter2.inc();

		final Histogram responseSizes = metrics.histogram("response-sizes");
		final io.dropwizard.metrics5.Timer metricsTimer = metrics
				.timer("test-timer");

		timer.schedule(new TimerTask() {
			int i = 100;

			@Override
			public void run() {
				Context context = metricsTimer.time();
				try {
					TimeUnit.MILLISECONDS.sleep(500);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				responseSizes.update(i++);
				context.stop();
			}

		}, 1000, 1000);

		reporter.start(5, TimeUnit.SECONDS);

		String hostName = "localhost";
		String topic = "test-wf-kafka-reporter";
		Properties props = new Properties();
		props.put("metadata.broker.list", "127.0.0.1:9092");
		props.put("serializer.class", "kafka.serializer.StringEncoder");
		props.put("partitioner.class", "kafka.producer.DefaultPartitioner");
		props.put("request.required.acks", "1");

		String prefix = "test.";
		ProducerConfig config = new ProducerConfig(props);
		
		// configure using two point tags
		WavefrontKafkaReporter wavefrontKafkaReporter = WavefrontKafkaReporter.forRegistry(metrics)
				.config(config).topic(topic).hostName(hostName).prefix(prefix).withPointTag("cluster", "c-1").withPointTag("appName", "myapp").build();

		wavefrontKafkaReporter.start(1, TimeUnit.SECONDS);

		TimeUnit.SECONDS.sleep(500);
	}
}
```

The json send to kafka will like this:
```json
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
```

### KafkaConsumer

```java
import java.io.IOException;

import io.github.hengyunabc.metrics.MessageListener;
import io.github.hengyunabc.metrics.MetricsKafkaConsumer;

public class MetricsKafkaConsumerSample {

	String zookeeper;
	String topic;
	String group;

	MetricsKafkaConsumer consumer;

	public static void main(String[] args) throws IOException {

		String zookeeper = "localhost:2181";
		String topic = "test-kafka-reporter";
		String group = "consumer-test";

		MetricsKafkaConsumer consumer = new MetricsKafkaConsumer();

		consumer = new MetricsKafkaConsumer();
		consumer.setZookeeper(zookeeper);
		consumer.setTopic(topic);
		consumer.setGroup(group);
		consumer.setMessageListener(new MessageListener() {

			@Override
			public void onMessage(String message) {
				System.err.println(message);
			}
		});
		consumer.init();

		System.in.read();

		consumer.desotry();
	}
}
```
## Reporter with pointTag support
You can also use WavefrontKafkaReporter which you can append 'pointTags' to the reporting metrics. PointTag specifies additional information using key value pair. See below example where withPointTag() method is used to specify two pontTags, cluster and appName to further specify which cluster and which app this metric is being originated.

```
WavefrontKafkaReporter wavefrontKafkaReporter = WavefrontKafkaReporter.forRegistry(metrics).config(config).topic(topic).hostName(hostName).prefix(prefix).withPointTag("cluster", "c-1").withPointTag("appName", "myapp").build();
```
You can additionally provide Map<String, String> to provide multiple point tags in single method.
```
Map<String, String> pointTags = new HashMap<String, String>();
pointTags.put("cluster","c-1");
pointTags.put("appName","myapp");

WavefrontKafkaReporter wavefrontKafkaReporter = WavefrontKafkaReporter.forRegistry(metrics).config(config).topic(topic).hostName(hostName).prefix(prefix).withPointTag(pointTags).build();

```

The resulting JSON output will contain the following additional object map in its message as shown below:
```
{
  ...
  "pointTags":{  
      "appName":"myapp",
      "cluster":"c-1"
   }
}
```

## metric name point tags
This library uses the new feature in dropwizard 5.0 (not fully released and in development currently) that allows users to
add point tags per metric name. Notice that the output metric name now has {} at the end which may contain
point tag values if they have any.

```
Map<String, String> tags = new HashMap<String, String>();
tags.put("type", "counter");
tags.put("mode", "test");
MetricName name = new MetricName("requests", tags);
Counter counter = metrics.counter(name);
```

The output result will look something like this:
``` json
{
"counters":{  
      "test.requests{mode=test, type=counter2}":{  
         "count":1
      }
}
```

## Maven dependency

```xml
<dependency>
    <groupId>io.github.hengyunabc</groupId>
    <artifactId>metrics-kafka</artifactId>
    <version>0.0.3</version>
</dependency>
```

This library has dependency to non-public maven repository
```xml
<dependency>
	<groupId>io.dropwizard.metrics5</groupId>
	<artifactId>metrics-core</artifactId>
	<version>5.0.0-SNAPSHOT</version>
</dependency>

<dependency>
	<groupId>io.dropwizard.metrics5</groupId>
	<artifactId>metrics-json</artifactId>
	<version>5.0.0-SNAPSHOT</version>
</dependency>

<dependency>
	<groupId>io.dropwizard.metrics5</groupId>
	<artifactId>metrics-jvm</artifactId>
	<version>5.0.0-SNAPSHOT</version>
	<scope>test</scope>
</dependency>
```

Therefore, in order to properly build this, you would need to clone the 5.0-development branch of dropwizard metrics to your local file system. 

```
git clone -b 5.0-development https://github.com/dropwizard/metrics.git
```

Then, install the whole projects to your local maven repository.

```
mvn install
```

## Others

https://github.com/hengyunabc/zabbix-api

https://github.com/hengyunabc/zabbix-sender

https://github.com/hengyunabc/metrics-zabbix

https://github.com/hengyunabc/kafka-zabbix

## License

Apache License V2

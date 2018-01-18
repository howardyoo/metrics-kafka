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
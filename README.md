### Overview
- This codebase forks from the source code of GeoMesa 2.3.2, and we add some code to support the functionality of Cymo
- The directories related to Cymo show as follows:
  - The source code of Cymo is located at `geomesa-index-api/src/main/java/com/rogerguo/cymo`
  - The configuration file is located at `geomesa-index-api/src/main/resources/cymo/conf`
  - The server side filter is located at `geomesa-hbase/geomesa-hbase-datastore/src/main/scala/org/locationtech/geomesa/hbase/filters`
    
### Prerequisites
- Java JDK 1.8
- Apache Maven 3.5.2 or later 
- a GitHub client 
- an HBase 1.3.x or 1.4.x instance 
- the GeoMesa HBase distributed runtime installed for your HBase instance (see below)

https://www.geomesa.org/documentation/2.3.2/tutorials/geomesa-quickstart-hbase.html

### Build

GeoMesa uses custom HBase filters and coprocessors to speed up queries. In order to use them, you must deploy the distributed runtime jar to the HBase to the directory specified by the HBase

#### Generate GeoMesa HBase distributed runtime (for Cymo)
- Compile the GeoMesa Distributed Runtime JAR
```
cd geomesa-index-api
mvn clean install -Dlicense.skip=true -Dmaven.test.skip=true

cd geomesa-hbase/geomesa-hbase-datastore
mvn clean install -Dlicense.skip=true -Dmaven.test.skip=true

cd geomesa-hbase/geomesa-hbase-distributed-runtime
mvn clean package -Dlicense.skip=true -Dmaven.test.skip=true
```
The runtime JAR can be found in `geomesa-hbase/geomesa-hbase-distributed-runtime/target`

- Copy the runtime JAR to the HBase lib directory such as `hbase-1.4.11/lib`

- Register the Coprocessors
  It is possible to register the coprocessors in the main hbase-site.xml. To do this simply add the coprocessor classnames to the hbase.coprocessor.user.region.classes key. Note that this requires HBase to be taken offline.
```
<configuration>
  <property>
    <name>hbase.coprocessor.user.region.classes</name>
    <value>org.locationtech.geomesa.hbase.coprocessor.GeoMesaCoprocessor</value>
  </property>
</configuration>
```

### Run

#### Run demo example
```
mvn exec:java -Dexec.mainClass="com.rogerguo.client.cymo.experiment.test.HBaseClient" -Dexec.args="--hbase.zookeepers 127.0.0.1 --hbase.catalog evaluation-demo"
```

### Predication component
The predication component is implemented by Python (located at `geomesa-test/src/main/python`)

The predication result is write to a HBase table. To write to HBase from Python, we need to start thrift server
```
./hbase-daemon.sh start thrift
```
### Query Dataset
The query workload can be found in the directory `geomesa-test/src/main/resources/demo`.

The query workload used for training can be found from the link `https://drive.google.com/file/d/13Jf6xtZSnZx-U0uyLhVGZvZaQolQpWJQ/view?usp=sharing`



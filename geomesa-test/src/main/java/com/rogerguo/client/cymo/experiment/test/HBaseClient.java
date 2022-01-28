/*
 * Copyright (c) 2013-2018 Commonwealth Computer Research, Inc.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Apache License, Version 2.0 which
 * accompanies this distribution and is available at
 * http://www.opensource.org/licenses/apache2.0.php.
 */

package com.rogerguo.client.cymo.experiment.test;

import com.rogerguo.client.cymo.experiment.data.CommonData;
import org.apache.commons.cli.ParseException;
import org.locationtech.geomesa.hbase.data.HBaseDataStoreFactory;

public class HBaseClient extends GeoMesaClient {



    public HBaseClient(String[] args, CommonData data, boolean readOnly, String logFilename) throws ParseException {
        super(args, new HBaseDataStoreFactory().getParametersInfo(), data, readOnly, logFilename);
    }

    public static void main(String[] args) {
        try {

            String logFilename = "/home/yangguo/Data/logs/response-time-log/query.spatial.005.24.3.csv";
            String queryFilename = "/home/yangguo/Codes/cymo-learning/util/test-query.csv";

            String dataFilename = "/home/yangguo/Data/DataSet/Trajectory/Taxi_Trips_Sorted_1m_Samples.csv";
            //String dataFilename = "/home/yangguo/Codes/geomesa-cymo/geomesa-test/src/main/resources/demo/extracted.csv";
            //CommonData data = new ChicagoTaxiDataTestGeoMesaZ3(queryFilename, dataFilename);
            //CommonData data = new NYCTaxiFormattedDataTestSynthetic(queryFilename, dataFilename);
            CommonData data = new ChicagoTaxiDataTest(queryFilename, dataFilename);

            HBaseClient client = new HBaseClient(args, data, true, logFilename);
            client.myExecute();
            //client.myExecute();
        } catch (ParseException e) {
            System.exit(1);
        } catch (Throwable e) {
            e.printStackTrace();
            System.exit(2);
        }
        System.exit(0);
    }
}

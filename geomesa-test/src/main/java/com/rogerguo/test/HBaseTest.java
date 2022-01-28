package com.rogerguo.test;

import com.rogerguo.cymo.config.VirtualLayerConfiguration;
import com.rogerguo.cymo.curve.CurveMeta;
import com.rogerguo.cymo.curve.ZCurve;
import com.rogerguo.cymo.hbase.HBaseDriver;
import com.rogerguo.cymo.hbase.RowKeyHelper;
import com.rogerguo.cymo.virtual.VirtualLayerGeoMesa;
import com.rogerguo.cymo.virtual.entity.CellLocation;
import com.rogerguo.cymo.virtual.entity.NormalizedLocation;
import com.rogerguo.cymo.virtual.helper.CurveTransformationHelper;
import com.rogerguo.cymo.virtual.helper.NormalizedDimensionHelper;
import com.rogerguo.cymo.virtual.helper.VirtualSpaceTransformationHelper;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

/**
 * @Description
 * @Date 2020/6/18 16:02
 * @Created by X1 Carbon
 */
public class HBaseTest {

    static ZCurve zCurve = new ZCurve();

    public static void main(String[] args) throws IOException {
        /*HBaseDriver hBaseDriver = new HBaseDriver("127.0.0.1");
        hBaseDriver.scan(VirtualLayerGeoMesa.VIRTUAL_LAYER_INFO_TABLE, Bytes.toBytes("test"), Bytes.toBytes("test"));*/
        long start = System.currentTimeMillis();
        for (int i = 0; i < 1000; i++) {
            for (int j = 0; j < 10000; j++) {
                testKey(i, j, i);
            }
        }

        long stop = System.currentTimeMillis();
        System.out.println("time: " + (stop - start));
    }

    public static void testZCurve() {
        for (int i = 0; i < 1000; i++) {
            for (int j = 0; j < 10000; j++) {
                zCurve.getCurveValue(i, j);
            }
        }
    }

    public static void testConcatByteKey() {
        for (int i = 0; i < 1000; i++) {
            for (int j = 0; j < 10000; j++) {
                RowKeyHelper.concatDataTableByteRowKey(i, j, i);
            }
        }
    }

    public static void testKey(int longitude, int latitude, int time) {
        NormalizedLocation normalizedLocation = new NormalizedLocation((int)longitude, (int)latitude, (int)time);


        // 2. transform to virtual space
        CellLocation cell = VirtualSpaceTransformationHelper.toCellLocation(normalizedLocation);

        //CellLocation firstCellLocationOfThisSubspace = VirtualSpaceTransformationHelper.getFirstCellLocationOfThisSubspace(cell);

        NormalizedLocation firstCellNormalizedLocation = VirtualSpaceTransformationHelper.fromSubspaceLocation(cell.getPartitionID(), cell.getSubspaceLongitude(), cell.getSubspaceLatitude());
        int firstCellLocationOfThisSubspaceLongitude = firstCellNormalizedLocation.getX() / VirtualLayerConfiguration.SPATIAL_VIRTUAL_LONGITUDE_GRANULARITY;
        int firstCellLocationOfThisSubspaceLatitude = firstCellNormalizedLocation.getY() / VirtualLayerConfiguration.SPATIAL_VIRTUAL_LATITUDE_GRANULARITY;
        int firstCellLocationOfThisSubspaceTime = firstCellNormalizedLocation.getT();


        // 3. curve encoding
        long virtualCellID = CurveTransformationHelper.generate3D(cell.getCurveMeta(), cell.getCellLongitude() - firstCellLocationOfThisSubspaceLongitude, cell.getCellLatitude() - firstCellLocationOfThisSubspaceLatitude, cell.getCellTime() - firstCellLocationOfThisSubspaceTime);

        long virtualSpaceID = CurveTransformationHelper.generate2D(new CurveMeta(VirtualLayerConfiguration.DEFAULT_STRATEGY), cell.getSubspaceLongitude(), cell.getSubspaceLatitude());
        int partitionID = cell.getPartitionID();

        //RowKeyHelper.concatIndexTableStringRowKey(partitionID, virtualSpaceID);
    }
}

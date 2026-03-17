public class SingleLongMethodJava {
    public String buildReport(int[] values, boolean includeAverage) {
        int total = 0;
        int count = 0;
        for (int value : values) {
            total += value;
            count++;
        }

        int max = Integer.MIN_VALUE;
        for (int value : values) {
            if (value > max) {
                max = value;
            }
        }

        int min = Integer.MAX_VALUE;
        for (int value : values) {
            if (value < min) {
                min = value;
            }
        }

        String report = "total=" + total + ", count=" + count + ", min=" + min + ", max=" + max;
        if (includeAverage && count > 0) {
            double average = (double) total / count;
            report = report + ", average=" + average;
        }
        return report;
    }
}

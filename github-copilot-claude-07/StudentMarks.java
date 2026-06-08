public class StudentMarks {

    public static double calculateAverage(int[] marks) {
        int total = 0;
        for (int m : marks) {
            total += m;
        }
        return (double) total / marks.length;
    }

    public static String calculateGrade(double avg) {
        if (avg >= 90) {
            return "A";
        } else if (avg >= 75) {
            return "B";
        } else if (avg >= 50) {
            return "C";
        } else {
            return "F";
        }
    }

    public static void main(String[] args) {
        String[] names = {"Rahul Sharma", "Priya Verma"};
        int[][] marks = {
            {85, 78, 92, 74},
            {91, 88, 95, 89}
        };

        for (int i = 0; i < names.length; i++) {
            double avg = calculateAverage(marks[i]);
            String grade = calculateGrade(avg);

            System.out.println("Name: " + names[i]);
            System.out.println("Average: " + avg);
            System.out.println("Grade: " + grade);
            System.out.println();
        }
    }
}

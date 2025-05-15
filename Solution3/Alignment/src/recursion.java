public class recursion {

    public static void main(String[] args) {
        String seq1 = "TTACGTAAGC";
        String seq2 = "TATAAT";
        System.out.println(score("", seq1));
    }

    static public int score(String seq1, String seq2){
        int score = 0;
        int gap = -4;
        int match = 3;
        int missMatch = -2;

        if (seq1.equals("") && seq2.equals("")) {
            return 0;
        }else if(seq1.equals("")){
            return score(seq1, seq2.substring(0, seq2.length()-1)) - gap;
        }else if(seq2.equals("")) {
            return score(seq2, seq1.substring(0, seq1.length()-1)) - gap;
        }




        return score;
    }

}

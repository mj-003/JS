import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) 
    {
        if(args.length == 0)
        {
            System.out.println("Please provide the file name as an argument");
            return;
        }

        String fileName = args[0];
        int charCount = 0;
        int wordCount = 0;
        int lineCount = 0;
        Map<String, Integer> wordFrequency = new HashMap<String, Integer>();
        Map<String, Integer> charFrequency = new HashMap<String, Integer>();

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) 
        {
            String line;
            while ((line = reader.readLine()) != null) 
            {
                lineCount++;
                charCount += line.length();
                String[] words = line.split(" ");
                wordCount += words.length;
                for (String word : words) 
                {
                    wordFrequency.put(word, wordFrequency.getOrDefault(word, 0) + 1);
                    for (char c : word.toCharArray()) 
                    {
                        charFrequency.put(String.valueOf(c), charFrequency.getOrDefault(String.valueOf(c), 0) + 1);
                    }
                }
            }
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        }

        char mostFrequentChar = ' ';
        int maxCharFrequency = 0;
        for (Map.Entry<String, Integer> entry : charFrequency.entrySet()) 
        {
            if (entry.getValue() > maxCharFrequency) 
            {
                maxCharFrequency = entry.getValue();
                mostFrequentChar = entry.getKey().charAt(0);
            }
        }

        String mostFrequentWord = "";
        int maxWordFrequency = 0;
        for (Map.Entry<String, Integer> entry : wordFrequency.entrySet()) 
        {
            if (entry.getValue() > maxWordFrequency) 
            {
                maxWordFrequency = entry.getValue();
                mostFrequentWord = entry.getKey();
            }
        }

        System.out.println("path,number_of_characters,number_of_words,number_of_lines,most_common_character,most_common_word");
        System.out.printf("%s,%d,%d,%d,%c,%s\n", fileName, charCount, wordCount, lineCount, mostFrequentChar, mostFrequentWord);
    }
}

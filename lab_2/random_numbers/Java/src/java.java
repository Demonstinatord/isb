
import java.io.*;
public class java {
	public static void main(String[] args) {
		String str="";
		for (int i=0; i<128; i++) {
			double symbol = Math.random();

			if (symbol<0.5) {

				str=str.concat("0");

			}
			else {
				str=str.concat("1");
			}

		}
		System.out.print (str);
		System.out.println();
        try(FileWriter writer = new FileWriter("sequence_java.txt", false))
        {
           // запись всей строки
            
            writer.write(str);
            // запись по символам
            writer.flush();
            writer.close();
        }
        catch(IOException ex){
             
            System.out.println(ex.getMessage());
        } 

	}

}
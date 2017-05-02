import java.util.Random;

public class AnelMultithread extends Thread {
	private static char[] message = new char[80];
	private int id;

	static {
		Random generator = new Random();

		for (int i = 0; i < message.length; i++) {
			if (generator.nextInt() % 2 == 1)
				message[i] = (char) ('A' + generator.nextInt(26));

			else
				message[i] = (char) ('a' + generator.nextInt(26));
		}
	}

	public AnelMultithread(int id) {
		this.id = id;
	}

	public void run() {}

	public static void main(String[] args) {
		System.out.println("Final mesage:\t" + new String(message));
	}
}

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

	public void run() {
		System.out.println("Thread " + this.id);
	}

	public static void main(String[] args) {
		AnelMultithread[] threads = new AnelMultithread[30];

		for (int i = 0; i < 30; i++) {
			threads[i] = new AnelMultithread(i);
			threads[i].start();
		}

		for (int i = 0; i < 30; i++) {
			try {
				threads[i].join();
			}

			catch (InterruptedException e) {}
		}

		System.out.println("Final mesage:\t" + new String(message));
	}
}

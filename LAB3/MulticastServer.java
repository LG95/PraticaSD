import java.io.*;
import java.net.*;
import java.util.Scanner;

public class MulticastServer {
	public static void main(String[] args) {
		final Scanner STDIN = new Scanner(System.in);
		final int PORT = 8888;

		DatagramSocket outSocket = null;
		MulticastSocket inSocket = null;
		byte[] inBuf = new byte[256];
		DatagramPacket inPacket;
		InetAddress address;
		byte[] outBuf;

		try {
			outSocket = new DatagramSocket();
			inSocket = new MulticastSocket(PORT);
			address = InetAddress.getByName("224.2.2.3");
			inSocket.joinGroup(address);

			while ( STDIN.hasNextLine() ) {
				System.out.print("Server> ");
				outBuf = STDIN.nextLine().getBytes();
				outSocket.send(new DatagramPacket(outBuf, outBuf.length, address, PORT));


				inPacket = new DatagramPacket(inBuf, inBuf.length);
				inSocket.receive(inPacket);
				System.out.println("Client@" + inPacket.getAddress() + "> " +
									new String(inBuf, 0, inPacket.getLength()));
			}
		}

		catch (IOException ioe) {
			System.out.println(ioe);
		}

		finally {
			inSocket.close();
			outSocket.close();
		}
	}
}

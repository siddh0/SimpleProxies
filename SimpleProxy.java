import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.URL;

public class SimpleProxy {

    public static void main(String[] args) {
        String[] proxies = {
            //Enter Proxies "HOST:PORT"
        };

        String url = ""; //Enter Target URL

        for (int i = 0; i < proxies.length; i++) {
            try {
                String[] proxyParts = proxies[i].split(":");
                String proxyHost = proxyParts[0];
                int proxyPort = Integer.parseInt(proxyParts[1]);

                Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(proxyHost, proxyPort));
                URL targetUrl = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) targetUrl.openConnection(proxy);

                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder content = new StringBuilder();
                while ((inputLine = in.readLine()) != null) {
                    content.append(inputLine);
                }

                in.close();
                connection.disconnect();

                System.out.println("Proxy " + (i + 1) + " Response Code: " + connection.getResponseCode());
                System.out.println(content.toString()); // Print the first 100 characters of the response
            } catch (Exception e) {
                System.out.println("Proxy " + (i + 1) + " failed: " + e.getMessage());
            }
        }
    }
}

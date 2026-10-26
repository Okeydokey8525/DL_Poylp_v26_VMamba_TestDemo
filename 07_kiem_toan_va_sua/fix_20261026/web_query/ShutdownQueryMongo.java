import com.mongodb.client.MongoClients;
import org.bson.Document;
public class ShutdownQueryMongo {
    public static void main(String[] args) {
        try (var client = MongoClients.create("mongodb://127.0.0.1:27019/?serverSelectionTimeoutMS=3000")) {
            try {
                client.getDatabase("admin").runCommand(new Document("shutdown", 1));
            } catch (Exception exception) {
                // A successful shutdown closes the command connection before a reply.
                System.out.println(exception.getClass().getSimpleName() + ": " + exception.getMessage());
            }
        }
    }
}

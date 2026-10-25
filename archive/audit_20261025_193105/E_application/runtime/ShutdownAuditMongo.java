import com.mongodb.client.MongoClients;
import org.bson.Document;
public class ShutdownAuditMongo {
 public static void main(String[] args) {
  try(var c=MongoClients.create("mongodb://127.0.0.1:27018/?serverSelectionTimeoutMS=3000")) {
   try { c.getDatabase("admin").runCommand(new Document("shutdown",1)); }
   catch(Exception e) { System.out.println(e.getClass().getName()+": "+e.getMessage()); }
  }
 }
}

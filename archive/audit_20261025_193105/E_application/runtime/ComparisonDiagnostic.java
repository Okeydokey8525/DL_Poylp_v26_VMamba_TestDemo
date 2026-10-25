import com.mongodb.client.MongoClients;
import org.springframework.data.mongodb.core.MongoTemplate;
import com.polyp.polypweb.repository.ComparisonHistorySearchRepository;
import com.polyp.polypweb.view.filter.ComparisonHistoryFilter;
public class ComparisonDiagnostic {
 public static void main(String[] args) {
  try(var client=MongoClients.create("mongodb://127.0.0.1:27018")) {
   var repository=new ComparisonHistorySearchRepository(new MongoTemplate(client,"polypweb_audit_20261025"));
   var filter=new ComparisonHistoryFilter().normalize();
   try { System.out.println(repository.search(args[0],filter)); }
   catch(Exception ex) { ex.printStackTrace(); System.exit(2); }
  }
 }
}
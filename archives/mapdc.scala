import scala.io.Source
import java.io.File
import java.nio.charset.CodingErrorAction
import scala.io.Codec
import scala.collection.mutable.Map
import scala.collection.immutable.ListMap
object docId2Count {
    def main(args: Array[String]) {
          //Handling codec errors during reading phase
          implicit val codec = Codec("UTF-8");
          codec.onMalformedInput(CodingErrorAction.REPLACE);

          //create map of docId to content
          var docIdToContentMap = Map[String, String]();

          //Storing only i entries as we are running out of memory
          var i :Int = 0;

          val myDirectory :String = "Project1_data";
          val d = new File(myDirectory);

          //Iterate over all the files in the directory and create content map
          for(file <- d.listFiles if file.getName endsWith ".txt"){
              if (i < 200){
                val fileName = file.getName;
                val docId  = fileName.split("\\.")(0);
                val content = Source.fromFile("./Project1_data/"+docId+".txt").mkString; //returns the file data as String
                docIdToContentMap += (docId -> content);
              }
              i = i+1;
          }

          //Creating word count map from the content for each docId
          val docIdToWordToCountMap = docIdToContentMap.map({
              case (k,v) => k -> v.split("\\s+").groupBy(x=>x).mapValues(x=>x.length) 
          })

        //   println(docIdToWordToCountMap);

          //create map of inverted index
          var wordToDocIdMap = Map[String, Map[String, Int]]();

          for ((docId, wordsNCount) <- docIdToWordToCountMap) {
              for((word, count) <- wordsNCount){
                  if (wordToDocIdMap.contains(word)){
                      if(wordToDocIdMap(word).contains(docId)){
                          wordToDocIdMap(word)(docId) = wordToDocIdMap(word)(docId) + count;
                      }
                      else{
                          wordToDocIdMap(word) += (docId-> count);
                      }
                  }
                  else{
                      var map = Map[String, Int](docId-> count);
                      wordToDocIdMap += (word-> map);
                  }
              }
          }

          //Sort results in inverted index according to word frequency
          val invertedIndex = wordToDocIdMap.map({
              case (k,v) => k -> ListMap(v.toSeq.sortWith(_._2 > _._2):_*)
          })        

          println(invertedIndex);
    }
}
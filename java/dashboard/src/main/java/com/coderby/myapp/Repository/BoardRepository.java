package com.coderby.myapp.Repository;

import static com.mongodb.client.model.Filters.gte;
import static com.mongodb.client.model.Sorts.ascending;
import static com.mongodb.client.model.Sorts.descending;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.bson.Document;
import org.bson.conversions.Bson;
import org.json.simple.JSONObject;
import org.springframework.stereotype.Repository;

import com.mongodb.client.AggregateIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Accumulators;
import com.mongodb.client.model.Aggregates;
import com.mongodb.client.model.Projections;

@Repository
public class BoardRepository implements IBoardRepository {

	String conn = "mongodb://localhost:27017";

	MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");
	MongoDatabase db = mongoClient.getDatabase("news");
	MongoCollection<org.bson.Document> news = db.getCollection("news"); // 전체 기사
	MongoCollection<org.bson.Document> pp_news = db.getCollection("pp_news"); // 전처리 후 기사
	MongoCollection<org.bson.Document> c_wordlist = db.getCollection("c_wordlist"); // 신조어 후보군
	MongoCollection<org.bson.Document> new_word_list = db.getCollection("new_word_list"); // 최종 신조어 

	@Override
	public long totalData() {
		System.out.println("repository ==================");
		long totalData = news.estimatedDocumentCount();

		System.out.println(totalData);
		
		return totalData;
	}

	@Override
	public Document dateRange() {

		AggregateIterable<Document> date = news.aggregate(Arrays
				.asList(Aggregates.group("", Accumulators.min("min", "$date"), Accumulators.max("max", "$date"))));

		MongoCursor<Document> cursor = date.cursor();

		Document doc = new Document();
		
		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				System.out.println(doc.getString("min"));
				System.out.println(doc.getString("max"));
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}
		
		return doc;
	}

	@Override
	public Map<String, Object> category() {

		AggregateIterable<Document> cate = news.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)), Aggregates.sort(descending("count"))));

		MongoCursor<Document> cursor = cate.cursor();

		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();

		List<String> label = new ArrayList<String>();
		List<Integer> count = new ArrayList<Integer>();

		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				label.add(doc.getString("_id"));
				count.add(doc.getInteger("count"));
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}
		
		map.put("label", label);
		map.put("count", count);
		System.out.println(map);

		return map;
	}

	@Override
	public List<String> weekCount() {
		AggregateIterable<Document> weekCount = news.aggregate(Arrays
				.asList(Aggregates.group("$week", Accumulators.sum("count", 1)), Aggregates.sort(ascending("_id"))));

		MongoCursor<Document> cursor = weekCount.cursor();

		Document doc = new Document();

		List<String> week = new ArrayList<String>();

		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				week.add(doc.toJson());
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}

		System.out.println(week);
		
		return week;
	}

	public Map<String, Object> freq() {
		AggregateIterable<Document> cate = news.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)), Aggregates.sort(descending("count"))));

		AggregateIterable<Document> source = news.aggregate(Arrays.asList(
				Aggregates.group("$source", Accumulators.sum("count", 1)), Aggregates.sort(descending("count"))));

		MongoCursor<Document> cursor = cate.cursor();
		MongoCursor<Document> cursor2 = source.cursor();

		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();

		List<String> cateTop = new ArrayList<String>();
		List<String> sourceTop = new ArrayList<String>();

		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				cateTop.add(doc.getString("_id"));
				break;
			}
			
			while (cursor2.hasNext()) {
				doc = cursor2.next();
				sourceTop.add(doc.getString("_id"));
				break;
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}
		
		map.put("cate", cateTop);
		map.put("source", sourceTop);
		
		return map;
	}

	@Override
	public long preData() {
		long preData = pp_news.estimatedDocumentCount();
		
		return preData;
	}

	@Override
	public double preRatio() {
		double preRatio = (double) pp_news.estimatedDocumentCount() / (double) news.estimatedDocumentCount() * 100;
		preRatio = Math.round(preRatio * 10) / 10.0;
		
		return preRatio;
	}

	@Override
	public long candidate() {
		long candidate = c_wordlist.estimatedDocumentCount();
		
		return candidate;
	}

	@Override
	public List<String> wordCloud() {

		Bson projectionFields = Projections.fields(Projections.include("new_word", "freq"), Projections.excludeId());
		MongoCursor<Document> cursor = c_wordlist.find(gte("freq", 50)).projection(projectionFields).iterator();

		List<String> word = new ArrayList<String>();
		Document doc = new Document();

		try {
			while (cursor.hasNext()) {				
				doc = cursor.next();
				word.add(doc.toJson());
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}

		System.out.println(word);
		
		return word;
	}

	@Override
	public Map<String, Object> category2() {
		AggregateIterable<Document> cate = c_wordlist.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)), Aggregates.sort(descending("count"))));
		
		MongoCursor<Document> cursor = cate.cursor();
		
		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();
		
		List<String> label = new ArrayList<String>();
		List<Integer> count = new ArrayList<Integer>();
		
		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				label.add(doc.getString("_id"));
				count.add(doc.getInteger("count"));
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}
		
		map.put("label", label);
		map.put("count", count);
		System.out.println(map);
		
		return map;
	}

	@Override
	public long newWordListCount() {
		long newWordListCount = new_word_list.estimatedDocumentCount();
		
		return newWordListCount;
	}

	@Override
	public List<String> newWordListWeekCount() {
		AggregateIterable<Document> newWord = new_word_list.aggregate(Arrays
				.asList(Aggregates.group("$week", Accumulators.sum("count", 1)), Aggregates.sort(ascending("_id"))));

		MongoCursor<Document> cursor = newWord.cursor();

		Document doc = new Document();

		List<String> newWordListWeekCount = new ArrayList<String>();
		
		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				newWordListWeekCount.add(doc.toJson());
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}

		System.out.println(newWordListWeekCount);

		return newWordListWeekCount;
	}

	@Override
	public Map<String, Object> category3() {
		AggregateIterable<Document> cate = new_word_list.aggregate(Arrays.asList(
				Aggregates.group("$category", Accumulators.sum("count", 1)), Aggregates.sort(descending("count"))));
		
		MongoCursor<Document> cursor = cate.cursor();
		
		Document doc = new Document();
		Map<String, Object> map = new HashMap<String, Object>();
		
		List<String> label = new ArrayList<String>();
		List<Integer> count = new ArrayList<Integer>();
		
		try {
			while (cursor.hasNext()) {
				doc = cursor.next();
				label.add(doc.getString("_id"));
				count.add(doc.getInteger("count"));
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}
		
		map.put("label", label);
		map.put("count", count);
		System.out.println(map);
		
		return map;
	}

	@Override
	public Map<String, Object> table() {
		Bson projectionFields = Projections.fields(Projections.include("new_word", "freq", "category", "week", "date1", "date2"), Projections.excludeId());
		MongoCursor<Document> cursor = c_wordlist.find(gte("freq", 50)).projection(projectionFields).iterator();
		
		Map<String, Object> map = new HashMap<String, Object>();
		
		List<String> new_word = new ArrayList<String>();
		List<Integer> freq = new ArrayList<Integer>();
		List<String> category = new ArrayList<String>();
		List<String> week = new ArrayList<String>();
		List<String> date1 = new ArrayList<String>();
		List<String> date2 = new ArrayList<String>();
		
		Document doc = new Document();
		
		try {
		    while (cursor.hasNext()) {
		    	doc = cursor.next();
				new_word.add(doc.getString("new_word"));
				freq.add(doc.getInteger("freq"));
				category.add(doc.getString("category"));
				week.add(doc.getString("week"));
				date1.add(doc.getString("date1"));
				date2.add(doc.getString("date2"));
		    }
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
		    cursor.close();
		}

		map.put("new_word", new_word);
		map.put("freq", freq);
		map.put("category", category);
		map.put("week", week);
		map.put("date1", date1);
		map.put("date2", date2);
		
		System.out.println(map);
		
		return map;
	}

}

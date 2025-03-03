package com.coderby.myapp.Service;

import java.util.List;
import java.util.Map;

import org.bson.Document;

public interface IBoardService {
	long totalData();
	Document dateRange();
	Map<String, Object> category();
	Map<String, Object> freq();
	List<String> weekCount();
	long preData();
	double preRatio();
	long candidate();
	List<String> wordCloud();
	Map<String, Object> category2();
	long newWordListCount();
	List<String> newWordListWeekCount();
	Map<String, Object> category3();
	Object table();
	List<String> wordCloud2();
}

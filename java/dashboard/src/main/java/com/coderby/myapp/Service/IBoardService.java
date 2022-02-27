package com.coderby.myapp.Service;

import java.util.Map;

import org.bson.Document;

public interface IBoardService {
	long totalData();
	Document dateRange();
	Map<String, Object> category();
}

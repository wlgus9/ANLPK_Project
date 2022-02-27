package com.coderby.myapp.Repository;

import java.util.Map;

import org.bson.Document;

public interface IBoardRepository {
	long totalData();
	Document dateRange();
	Map<String, Object> category();
}

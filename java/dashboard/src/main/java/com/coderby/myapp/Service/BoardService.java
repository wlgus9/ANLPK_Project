package com.coderby.myapp.Service;

import java.util.Map;

import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.coderby.myapp.Repository.IBoardRepository;

@Service
public class BoardService implements IBoardService {

	@Autowired
	IBoardRepository boardRepository;
	
	@Override
	public long totalData() {
		
		System.out.println("Service =============");
		
		long totalData = boardRepository.totalData();
		
		return totalData;
	}
	
	public Document dateRange() {
		
		Document dateRange = boardRepository.dateRange();
		
		return dateRange;
	}

	@Override
	public Map<String, Object> category() {
		
		Map<String, Object> category = boardRepository.category();
		
		return category;
	}

}

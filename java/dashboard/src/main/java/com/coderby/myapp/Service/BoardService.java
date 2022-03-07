package com.coderby.myapp.Service;

import java.util.List;
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

	@Override
	public List<String> weekCount() {
		
		List<String> weekCount = boardRepository.weekCount();
		
		return weekCount;
	}

	@Override
	public Map<String, Object> freq() {
		
		Map<String, Object> freq = boardRepository.freq();
		
		return freq;
	}

	@Override
	public long preData() {
		
		long preData = boardRepository.preData();
		
		return preData;
	}

	@Override
	public double preRatio() {
		
		double preRatio = boardRepository.preRatio();
		
		return preRatio;
	}

	@Override
	public long candidate() {
		
		long candidate = boardRepository.candidate();
		
		return candidate;
	}

	@Override
	public List<String> wordCloud() {
		
		List<String> wordCloud = boardRepository.wordCloud();
		
		return wordCloud;
	}
	
	@Override
	public Map<String, Object> category2() {
		
		Map<String, Object> category2 = boardRepository.category2();
		
		return category2;
	}

	@Override
	public long newWordListCount() {
		
		long newWordListCount = boardRepository.newWordListCount();
		
		return newWordListCount;
	}

	@Override
	public List<String> newWordListWeekCount() {
		
		List<String> newWordListWeekCount = boardRepository.newWordListWeekCount();
		
		return newWordListWeekCount;
	}

	@Override
	public Map<String, Object> category3() {
		
		Map<String, Object> category3 = boardRepository.category3(); 
		
		return category3;
	}

	@Override
	public Map<String, Object> table() {
		
		Map<String, Object> table = boardRepository.table(); 
		
		return table;
	}

}

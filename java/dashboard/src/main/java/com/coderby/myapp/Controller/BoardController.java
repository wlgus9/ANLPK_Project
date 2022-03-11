package com.coderby.myapp.Controller;

import java.util.List;
import java.util.Map;

import org.bson.Document;
import org.json.simple.JSONArray;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.coderby.myapp.Service.IBoardService;

@Controller
public class BoardController {

	@Autowired
	IBoardService boardService;

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Model model) {

		System.out.println("controller ===========");

		// ========================== 데이터 수집 현황 ==========================
		// 총 기사 개수
		long totalData = boardService.totalData();
		model.addAttribute("totalData", totalData);

		// 데이터 수집 기간
		Document dateRange = boardService.dateRange();
		model.addAttribute("min", dateRange.get("min"));
		model.addAttribute("max", dateRange.get("max"));

		// 카테고리, 언론사 빈도수 TOP1
		Map<String, Object> freq = boardService.freq();
		model.addAttribute("freq", freq);

		// 카테고리별 분포
		Map<String, Object> map = boardService.category();
		model.addAttribute("map", map);

		// 기사 수집 추이
		List<String> week = boardService.weekCount();
		model.addAttribute("weekCount", week);

		// ========================== 전처리 현황 ==========================
		// 전처리 진행된 기사 수
		long preData = boardService.preData();
		model.addAttribute("preData", preData);

		// 전처리 진행된 기사 비율
		double preRatio = boardService.preRatio();
		model.addAttribute("preRatio", preRatio);

		// 신조어 후보군 개수
		long candidate = boardService.candidate();
		model.addAttribute("candidate", candidate);

		// 신조어 후보군 워드 클라우드
		List<String> wordCloud = boardService.wordCloud();
		model.addAttribute("wordCloud", wordCloud);

		// 신조어 후보군 카테고리별 분포
		Map<String, Object> map2 = boardService.category2();
		model.addAttribute("map2", map2);

		// ========================== 신조어 추출 현황 ==========================
		// 최종적으로 추출된 신조어 수
		long newWordListCount = boardService.newWordListCount();
		model.addAttribute("newWordListCount", newWordListCount);

		// 신조어 추출 추이
		List<String> newWordListWeekCount = boardService.newWordListWeekCount();
		model.addAttribute("newWordListWeekCount", newWordListWeekCount);

		// 신조어 카테고리 분포
		Map<String, Object> map3 = boardService.category3();
		model.addAttribute("map3", map3);

		return "index";
	}

	@RequestMapping(value = "/table", method = RequestMethod.GET)
	public String table(Model model) {
		
		// ========================== 신조어 테이블 ==========================
		
		Object table = boardService.table();
		
		model.addAttribute("table", table);
		
		return "table";
	}

	@RequestMapping(value = "/prepro", method = RequestMethod.GET)
	public String prepro(Model model) {
		return "prepro";
	}

}
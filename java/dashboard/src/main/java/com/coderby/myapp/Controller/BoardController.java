package com.coderby.myapp.Controller;

import java.util.Map;

import org.bson.Document;
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
		
		long totalData = boardService.totalData();		
		model.addAttribute("totalData", totalData);
		
		Document dateRange = boardService.dateRange();
		model.addAttribute("min", dateRange.get("min"));
		model.addAttribute("max", dateRange.get("max"));
		
		Map<String, Object> map = boardService.category();
		model.addAttribute("map", map);
		return "index";
	}
	
}

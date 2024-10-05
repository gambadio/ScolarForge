# internet_search.py

import json
import os
from datetime import datetime
from typing import List, Dict
import requests
import re
import tempfile

class InternetSearch:
    def __init__(self, claude_api_key: str, perplexity_api_key: str):
        self.claude_api_key = claude_api_key
        self.perplexity_api_key = perplexity_api_key
        self.json_file = 'internetsearch_results.json'

    def generate_search_terms(self, instructions: List[str], scripts: List[str]) -> List[Dict]:
        claude_prompt = self._create_claude_prompt(instructions, scripts)
        search_terms_raw = self._call_claude_api(claude_prompt)
        
        # Save the raw response to a JSON file
        with open('searchterms.json', 'w', encoding='utf-8') as f:
            json.dump({"raw_response": search_terms_raw}, f, ensure_ascii=False, indent=2)
        
        # Try to extract JSON from the response
        json_match = re.search(r'\[.*\]', search_terms_raw, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = search_terms_raw  # If no JSON-like structure found, use the whole response
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Raw content: {search_terms_raw}")
            return []  # Return an empty list if parsing fails

    def perform_internet_search(self, search_terms: List[Dict]) -> List[Dict]:
        perplexity_results = []
        for term in search_terms:
            sonar_prompt = self._create_sonar_prompt(term)
            result = self._call_sonar_api(sonar_prompt)
            perplexity_results.append(result)

        # Process Perplexity results using Claude
        final_results = self._process_perplexity_results(perplexity_results)

        # Save the final results
        self._save_data(final_results)

        return final_results

    def _process_perplexity_results(self, perplexity_results: List[str]) -> List[Dict]:
        # Create temporary files for Perplexity results
        temp_files = []
        for i, result in enumerate(perplexity_results):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
                json.dump(result, temp)
                temp_files.append(temp.name)

        # Create Claude prompt to process Perplexity results
        claude_prompt = self._create_claude_processing_prompt(temp_files)
        
        # Call Claude API to process results
        processed_results = self._call_claude_api(claude_prompt)

        # Clean up temporary files
        for temp_file in temp_files:
            os.unlink(temp_file)

        # Parse the processed results
        try:
            return json.loads(processed_results)
        except json.JSONDecodeError as e:
            print(f"Failed to parse processed results: {e}")
            print(f"Raw content: {processed_results}")
            return []

    def _create_claude_processing_prompt(self, temp_files: List[str]) -> str:
        prompt = "You will write one clean JSON based on the following text files:\n\n"
        for i, temp_file in enumerate(temp_files):
            with open(temp_file, 'r') as f:
                content = f.read()
            prompt += f"File {i+1}:\n{content}\n\n"
        
        prompt += """
        Combine the information from these files into a single JSON array. Each item in the array should have the following structure:
        {
            "title": "Name of finding",
            "author": "Name of the author or website",
            "date_retrieved": "YYYY-MM-DD",
            "url": "URL of the source",
            "content": "Everything found in this source",
            "search_term": "The search term used to find this information"
        }
        
        Ensure that the output is a valid JSON array. Do not include any explanatory text before or after the JSON.
        If the URL is not available, use "unknown" as the value.
        """
        return prompt

    def _create_claude_prompt(self, instructions: List[str], scripts: List[str]) -> str:
        return f"""
        Based on the following instructions and scripts, create a list of 2 possible search terms for internet research.
        Format the output as a JSON list of dictionaries, each containing 'search_term' and 'goal' keys. Do not include any explanatory text before or after the JSON. I REPEAT DO NOT WRITE ANYTHING ELSE THAN THE OUTPUT. 

        Instructions:
        {' '.join(instructions)}

        Scripts:
        {' '.join(scripts)}

        Output format example:
        [
            {{"search_term": "example term 1", "goal": "purpose of this search"}},
            {{"search_term": "example term 2", "goal": "purpose of this search"}},
            ...
        ]
        """

    def _create_sonar_prompt(self, term: Dict) -> str:
        return f"""
        You are an AI assistant helping to find sources for a scientific paper.
        Search the internet for information on the following topic:
        Search term: {term['search_term']}
        Goal: {term['goal']}

        Format your findings as JSON with the following structure:
        {{
            "title": "Name of finding",
            "author": "Name of the author or website",
            "date_retrieved": "{datetime.now().strftime('%Y-%m-%d')}",
            "url": "URL of the source",
            "content": "Everything you find in this source",
            "search_term": "{term['search_term']}"
        }}
        You don't write anything else than the JSON, no explanation or introduction text.
        Ensure to include a valid URL for each source. If you don't know the url, just write "unkown". 
        """

    def _call_claude_api(self, prompt: str) -> str:
        api_url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
        }
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 8192,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            raise Exception(f"Claude API Error: {response.status_code} - {response.text}")

    def _call_sonar_api(self, prompt: str) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.perplexity_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-sonar-huge-128k-online",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": True,
            "stream": False
        }
        response = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"Sonar API Error: {response.status_code} - {response.text}")

    def _save_data(self, data):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
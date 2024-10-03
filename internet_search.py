# internet_search.py

import json
import requests
from typing import List, Dict
from datetime import datetime

class InternetSearch:
    def __init__(self, claude_api_key: str, perplexity_api_key: str):
        self.claude_api_key = claude_api_key
        self.perplexity_api_key = perplexity_api_key

    def generate_search_terms(self, instructions: List[str], scripts: List[str]) -> List[Dict]:
        claude_prompt = self._create_claude_prompt(instructions, scripts)
        search_terms = self._call_claude_api(claude_prompt)
        return json.loads(search_terms)

    def perform_internet_search(self, search_terms: List[Dict]) -> List[Dict]:
        results = []
        for term in search_terms:
            sonar_prompt = self._create_sonar_prompt(term)
            result = self._call_sonar_api(sonar_prompt)
            results.append(result)
        return results

    def _create_claude_prompt(self, instructions: List[str], scripts: List[str]) -> str:
        return f"""
        Based on the following instructions and scripts, create a list of 5 possible search terms for internet research.
        Format the output as a JSON list of dictionaries, each containing 'search_term' and 'goal' keys.

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
            "author": "Name of the author or website",
            "date_retrieved": "{datetime.now().strftime('%Y-%m-%d')}",
            "content": "A summary of the relevant information found"
        }}
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
            try:
                content = result['choices'][0]['message']['content']
                return json.loads(content)
            except json.JSONDecodeError:
                # If the content is not valid JSON, return it as is
                return {
                    "author": "Unknown",
                    "date_retrieved": datetime.now().strftime("%Y-%m-%d"),
                    "content": content
                }
        else:
            raise Exception(f"Sonar API Error: {response.status_code} - {response.text}")

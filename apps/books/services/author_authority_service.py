"""Service for collecting author credentials and calculating authority score using LLM."""

import json
from typing import Any

import httpx
from django.conf import settings

from logger.books.log import get_logger

logger = get_logger(__name__)


class AuthorAuthorityService:
    """Service for collecting author credentials via LLM and external APIs."""

    def __init__(self):
        self.llm_provider = getattr(settings, "LLM_PROVIDER", "deepseek").lower()
        self.deepseek_api_key = getattr(settings, "DEEPSEEK_API_KEY", None)
        self.openai_api_key = getattr(settings, "OPENAI_API_KEY", None)
        self.serpapi_key = getattr(settings, "SERPAPI_KEY", None)

    async def collect_author_info(self, author) -> dict[str, Any]:
        """
        Collect author information from open sources.

        Args:
            author: Author model instance

        Returns:
            Dictionary with credentials data
        """
        # Check API key based on provider
        if self.llm_provider == "deepseek" and not self.deepseek_api_key:
            logger.warning("DEEPSEEK_API_KEY not set, skipping author info collection")
            return {}
        elif self.llm_provider == "openai" and not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set, skipping author info collection")
            return {}

        query = f'{author.first_name} {author.last_name} Python programming author'

        # Search via SerpAPI if available
        search_results = []
        if self.serpapi_key:
            try:
                search_results = await self._search_google(query)
            except Exception as e:
                logger.error(f"Google search failed: {e}")

        # Analyze results via LLM
        try:
            credentials = await self._analyze_with_llm(
                author_name=f"{author.first_name} {author.last_name}",
                search_results=search_results,
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            credentials = {}

        return credentials

    async def _search_google(self, query: str) -> list[dict]:
        """Search via SerpAPI (Google)."""
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "num": 10,
            "hl": "en",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        return data.get("organic_results", [])

    async def _analyze_with_llm(
        self, author_name: str, search_results: list[dict]
    ) -> dict[str, Any]:
        """Analyze search results via LLM (DeepSeek or OpenAI)."""
        # Prepare context for LLM
        context = "\n".join([
            f"Title: {r.get('title', '')}\nSnippet: {r.get('snippet', '')}"
            for r in search_results[:5]
        ])

        if not context:
            context = "No search results available."

        prompt = f"""Analyze information about author {author_name} based on search results.

Search results:
{context}

Extract the following information in JSON format:
{{
    "publications": ["book/article title", ...],
    "citations": approximate citation count (number),
    "awards": ["award/prize name", ...],
    "positions": ["job title", "PhD", "Professor", ...],
    "companies": ["company/university name", ...],
    "expertise": ["area of expertise", ...],
    "authority_indicators": ["signs of authority"],
    "github_stats": {{
        "stars": approximate total stars on repositories (number),
        "followers": approximate GitHub followers (number),
        "contributions": approximate annual contributions (number)
    }},
    "pypi_stats": {{
        "packages": ["popular package names", ...],
        "total_downloads": approximate total downloads (number)
    }},
    "stackoverflow": {{
        "reputation": approximate reputation score (number),
        "python_answers": approximate Python answers count (number)
    }},
    "conferences": ["conference names with years", ...],
    "certifications": ["certification names", ...]
}}

If information not found, return empty arrays and 0 for numbers.
Respond ONLY with valid JSON, no markdown formatting."""

        # Route to appropriate LLM provider
        if self.llm_provider == "deepseek":
            return await self._call_deepseek(prompt)
        else:
            return await self._call_openai(prompt)

    async def _call_deepseek(self, prompt: str) -> dict[str, Any]:
        """Call DeepSeek API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                },
            )
            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"]
        return self._parse_json_response(content)

    async def _call_openai(self, prompt: str) -> dict[str, Any]:
        """Call OpenAI API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                },
            )
            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"]
        return self._parse_json_response(content)

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        """Parse JSON from LLM response, cleaning up markdown if needed."""
        # Clean up markdown formatting if present
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}\nContent: {content}")
            return {}

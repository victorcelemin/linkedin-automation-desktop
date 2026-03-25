"""
Trending Topics Module
Fetches current trending topics in tech/software development from various sources
"""

import requests
import json
import os
from datetime import datetime, timedelta
import random
import re
from urllib.parse import quote

class TrendingTopics:
    """Fetch and manage trending topics in technology/software development"""
    
    def __init__(self):
        self.cache_file = 'data/trending_cache.json'
        self.cache_duration = timedelta(hours=6)  # Refresh every 6 hours
        self.trending = []
        self.load_cache()
    
    def load_cache(self):
        """Load cached trending topics"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    
                cached_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
                if datetime.now() - cached_time < self.cache_duration:
                    self.trending = cache.get('topics', [])
                    return
        except Exception:
            pass
        
        # Cache expired or doesn't exist, fetch new
        self.fetch_trending()
    
    def save_cache(self):
        """Save trending topics to cache"""
        try:
            os.makedirs('data', exist_ok=True)
            cache = {
                'timestamp': datetime.now().isoformat(),
                'topics': self.trending
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_trending(self):
        """Fetch trending topics from multiple sources"""
        topics = []
        
        # Try multiple sources
        topics.extend(self.fetch_devto_trending())
        topics.extend(self.fetch_github_trending())
        topics.extend(self.fetch_hackernews())
        topics.extend(self.fetch_reddit_tech())
        
        # If no topics fetched, use curated list
        if not topics:
            topics = self.get_curated_trending()
        
        # Remove duplicates and keep unique topics
        seen = set()
        unique_topics = []
        for topic in topics:
            key = topic['title'].lower()[:50]
            if key not in seen:
                seen.add(key)
                unique_topics.append(topic)
        
        self.trending = unique_topics[:30]  # Keep top 30
        self.save_cache()
        
        return self.trending
    
    def fetch_devto_trending(self):
        """Fetch trending articles from Dev.to"""
        topics = []
        try:
            url = "https://dev.to/api/articles?top=7&per_page=10"
            headers = {'User-Agent': 'LinkedInAutomation/2.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                articles = response.json()
                for article in articles:
                    topics.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'tags': article.get('tag_list', []),
                        'source': 'dev.to',
                        'url': article.get('url', ''),
                        'category': self.categorize_topic(article.get('title', ''), article.get('tag_list', []))
                    })
        except Exception as e:
            print(f"Error fetching Dev.to: {e}")
        
        return topics
    
    def fetch_github_trending(self):
        """Fetch trending repositories from GitHub"""
        topics = []
        try:
            url = "https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc&per_page=10"
            date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            url = url.format(date=date)
            
            headers = {
                'User-Agent': 'LinkedInAutomation/2.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for repo in data.get('items', [])[:10]:
                    topics.append({
                        'title': f"{repo.get('name', '')}: {repo.get('description', '')[:100]}",
                        'description': repo.get('description', ''),
                        'tags': repo.get('topics', []),
                        'source': 'github',
                        'url': repo.get('html_url', ''),
                        'category': self.categorize_topic(repo.get('name', ''), repo.get('topics', []))
                    })
        except Exception as e:
            print(f"Error fetching GitHub: {e}")
        
        return topics
    
    def fetch_hackernews(self):
        """Fetch top stories from Hacker News"""
        topics = []
        try:
            # Get top story IDs
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                story_ids = response.json()[:20]
                
                # Fetch details for each story
                for story_id in story_ids:
                    try:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        story_response = requests.get(story_url, timeout=5)
                        
                        if story_response.status_code == 200:
                            story = story_response.json()
                            if story and story.get('type') == 'story':
                                title = story.get('title', '')
                                if any(keyword in title.lower() for keyword in 
                                       ['programming', 'software', 'ai', 'api', 'code', 'developer',
                                        'javascript', 'python', 'rust', 'web', 'cloud', 'devops']):
                                    topics.append({
                                        'title': title,
                                        'description': f"Discuss on Hacker News: {story.get('url', '')}",
                                        'tags': ['tech', 'trending'],
                                        'source': 'hackernews',
                                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                                        'category': self.categorize_topic(title, [])
                                    })
                    except Exception:
                        continue
        except Exception as e:
            print(f"Error fetching Hacker News: {e}")
        
        return topics[:10]  # Limit to 10
    
    def fetch_reddit_tech(self):
        """Fetch trending posts from tech subreddits"""
        topics = []
        try:
            subreddits = ['programming', 'technology', 'webdev', 'MachineLearning', 'devops']
            
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                headers = {'User-Agent': 'LinkedInAutomation/2.0'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts[:3]:
                        post_data = post.get('data', {})
                        topics.append({
                            'title': post_data.get('title', ''),
                            'description': f"Discussion: {post_data.get('selftext', '')[:200]}",
                            'tags': [subreddit, 'reddit'],
                            'source': f'reddit/{subreddit}',
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'category': self.categorize_topic(post_data.get('title', ''), [subreddit])
                        })
        except Exception as e:
            print(f"Error fetching Reddit: {e}")
        
        return topics[:10]  # Limit to 10
    
    def get_curated_trending(self):
        """Curated list of trending tech topics (fallback)"""
        current_month = datetime.now().strftime('%B %Y')
        
        curated = [
            {
                'title': 'La revolución de la IA Generativa en el desarrollo de software',
                'description': 'Cómo las herramientas de IA están transformando la forma en que escribimos código',
                'tags': ['ai', 'generative-ai', 'coding', 'productivity'],
                'source': 'curated',
                'category': 'ai',
                'relevance': 'high'
            },
            {
                'title': 'Rust: El lenguaje que está ganando terreno en sistemas críticos',
                'description': 'Microsoft, Google y AWS están adoptando Rust para infraestructura',
                'tags': ['rust', 'systems-programming', 'performance'],
                'source': 'curated',
                'category': 'programming',
                'relevance': 'high'
            },
            {
                'title': 'Edge Computing vs Cloud: ¿Dónde procesar tus datos?',
                'description': 'El debate sobre descentralizar el procesamiento de datos',
                'tags': ['edge-computing', 'cloud', 'infrastructure'],
                'source': 'curated',
                'category': 'infrastructure',
                'relevance': 'medium'
            },
            {
                'title': 'WebAssembly: El futuro de las aplicaciones web de alto rendimiento',
                'description': 'Cómo WASM está permitiendo apps complejas en el navegador',
                'tags': ['webassembly', 'webdev', 'performance'],
                'source': 'curated',
                'category': 'webdev',
                'relevance': 'high'
            },
            {
                'title': 'Platform Engineering: La evolución del DevOps',
                'description': 'Los Internal Developer Platforms están redefiniendo el workflow',
                'tags': ['platform-engineering', 'devops', 'developer-experience'],
                'source': 'curated',
                'category': 'devops',
                'relevance': 'high'
            },
            {
                'title': 'La importancia de la ciberseguridad en la era de la IA',
                'description': 'Nuevos desafíos y oportunidades en seguridad informática',
                'tags': ['cybersecurity', 'ai', 'security'],
                'source': 'curated',
                'category': 'security',
                'relevance': 'high'
            },
            {
                'title': 'Micro-frontends: Escalando aplicaciones frontend',
                'description': 'Arquitecturas modulares para equipos grandes',
                'tags': ['frontend', 'architecture', 'micro-frontends'],
                'source': 'curated',
                'category': 'frontend',
                'relevance': 'medium'
            },
            {
                'title': 'Green Tech: Programación sostenible y eficiente',
                'description': 'Cómo optimizar el código para reducir el impacto ambiental',
                'tags': ['sustainability', 'green-tech', 'optimization'],
                'source': 'curated',
                'category': 'trends',
                'relevance': 'medium'
            },
            {
                'title': 'El auge de los LLMs locales y la privacidad de datos',
                'description': 'Ejecutar modelos de lenguaje en tu propia máquina',
                'tags': ['llm', 'privacy', 'local-ai', 'ollama'],
                'source': 'curated',
                'category': 'ai',
                'relevance': 'high'
            },
            {
                'title': 'TDD en 2026: ¿Sigue siendo relevante?',
                'description': 'Reflexiones sobre el Test-Driven Development en la era de la IA',
                'tags': ['tdd', 'testing', 'best-practices'],
                'source': 'curated',
                'category': 'testing',
                'relevance': 'high'
            },
            {
                'title': 'API Design: Más allá del REST tradicional',
                'description': 'GraphQL, gRPC y las nuevas tendencias en diseño de APIs',
                'tags': ['api', 'graphql', 'grpc', 'architecture'],
                'source': 'curated',
                'category': 'backend',
                'relevance': 'high'
            },
            {
                'title': 'El futuro del trabajo remoto en tech',
                'description': 'Cómo las empresas están adaptándose al trabajo distribuido',
                'tags': ['remote-work', 'culture', 'productivity'],
                'source': 'curated',
                'category': 'culture',
                'relevance': 'high'
            },
            {
                'title': 'TypeScript 6.0: Nuevas características que debes conocer',
                'description': 'Las últimas mejoras en el ecosistema de TypeScript',
                'tags': ['typescript', 'javascript', 'programming'],
                'source': 'curated',
                'category': 'frontend',
                'relevance': 'high'
            },
            {
                'title': 'Kubernetes para mortales: Guía práctica',
                'description': 'Simplificando la orquestación de contenedores',
                'tags': ['kubernetes', 'containers', 'devops'],
                'source': 'curated',
                'category': 'devops',
                'relevance': 'medium'
            },
            {
                'title': 'Los 12 factores de las aplicaciones cloud-nativas',
                'description': 'Principios fundamentales para construir apps modernas',
                'tags': ['cloud-native', 'architecture', 'best-practices'],
                'source': 'curated',
                'category': 'architecture',
                'relevance': 'high'
            }
        ]
        
        return curated
    
    def categorize_topic(self, title, tags):
        """Categorize a topic based on title and tags"""
        text = (title + ' ' + ' '.join(tags)).lower()
        
        categories = {
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 
                   'llm', 'gpt', 'claude', 'generative', 'neural', 'openai'],
            'frontend': ['react', 'vue', 'angular', 'javascript', 'typescript', 'css', 'html', 
                        'frontend', 'ui', 'ux', 'webdev', 'nextjs', 'nuxt'],
            'backend': ['api', 'rest', 'graphql', 'grpc', 'server', 'backend', 'node', 'django', 
                       'flask', 'express', 'spring'],
            'devops': ['devops', 'docker', 'kubernetes', 'k8s', 'ci/cd', 'pipeline', 'deploy', 
                      'infrastructure', 'terraform', 'aws', 'azure', 'gcp'],
            'programming': ['programming', 'coding', 'code', 'language', 'rust', 'go', 'python', 
                           'java', 'c++', 'developer'],
            'security': ['security', 'cybersecurity', 'vulnerability', 'hack', 'encryption', 
                        'authentication', 'oauth'],
            'career': ['career', 'hiring', 'interview', 'resume', 'job', 'salary', 'growth', 
                      'learning', 'mentor'],
            'architecture': ['architecture', 'design pattern', 'microservices', 'monolith', 
                            'scalability', 'system design'],
            'trends': ['trend', 'future', 'emerging', 'new', 'innovation', '2024', '2025', '2026']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    def get_random_topic(self, category=None):
        """Get a random trending topic, optionally filtered by category"""
        if not self.trending:
            self.fetch_trending()
        
        if category:
            filtered = [t for t in self.trending if t.get('category') == category]
            if filtered:
                return random.choice(filtered)
        
        return random.choice(self.trending) if self.trending else None
    
    def get_topics_by_category(self, category):
        """Get all topics for a specific category"""
        if not self.trending:
            self.fetch_trending()
        
        return [t for t in self.trending if t.get('category') == category]
    
    def get_all_categories(self):
        """Get list of available categories"""
        if not self.trending:
            self.fetch_trending()
        
        return list(set(t.get('category', 'general') for t in self.trending))
    
    def force_refresh(self):
        """Force refresh trending topics"""
        self.fetch_trending()
        return self.trending

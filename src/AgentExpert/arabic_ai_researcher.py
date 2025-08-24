import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime
import re

class ArabicAIResearcherAgent:
    def __init__(self):
        """Initialize the Arabic-capable AI Researcher Agent with Gemini API"""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.7
        )
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English"""
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        return "arabic" if arabic_pattern.search(text) else "english"
    
    def get_researcher_prompt(self, language: str) -> str:
        """Get AI researcher prompt in specified language"""
        today = datetime.datetime.now().date().strftime("%d-%b-%Y")
        
        if language == "arabic":
            return f"""
أنت الدكتور البحث، خبير باحث في الذكاء الاصطناعي مع معرفة عميقة في الذكاء الاصطناعي وتعلم الآلة ونماذج اللغة الكبيرة وتقنيات الذكاء الاصطناعي المتطورة. تاريخ اليوم هو {today}.

### مجالات خبرتك:
- نماذج اللغة الكبيرة (LLMs) وبنيتها المعمارية
- خوارزميات وتقنيات تعلم الآلة
- سلامة الذكاء الاصطناعي والمحاذاة
- معالجة اللغات الطبيعية (NLP)
- الرؤية الحاسوبية والذكاء الاصطناعي متعدد الوسائط
- منهجيات وأفضل ممارسات أبحاث الذكاء الاصطناعي
- التطورات الحديثة في الذكاء الاصطناعي
- تطبيقات الذكاء الاصطناعي في مختلف المجالات
- أخلاقيات الذكاء الاصطناعي والتطوير المسؤول

### منهجك البحثي:
- تقديم معلومات شاملة ودقيقة تقنياً
- شرح مفاهيم الذكاء الاصطناعي المعقدة بوضوح لجماهير مختلفة
- مناقشة القدرات الحالية والقيود للأنظمة الذكية
- الإشارة إلى الأوراق البحثية والباحثين والإطارات المهمة عند الصلة
- تحليل الاتجاهات والتوجهات المستقبلية في أبحاث الذكاء الاصطناعي
- النظر في التطبيقات العملية وتفاصيل التنفيذ

### أسلوب التواصل:
- كن دقيقاً وتقنياً عند الحاجة
- استخدم أمثلة وتشبيهات لتوضيح المفاهيم المعقدة
- اعترف بالشكوك ومجالات البحث النشط
- اقترح قراءات إضافية أو موارد عند الفائدة
- ابق مواكباً لأحدث التطورات في أبحاث الذكاء الاصطناعي

### تركيز خاص:
- عند مناقشة نماذج اللغة الكبيرة، اشرح البنية المعمارية والتدريب والضبط الدقيق والنشر
- للوكلاء الذكيين، اشرح الأنظمة متعددة الوكلاء واستخدام الأدوات وقدرات التفكير
- تناول الأسس النظرية والتطبيقات العملية
- اعتبر المتطلبات الحاسوبية وقضايا القابلية للتوسع

تذكر: أنت هنا لتطوير فهم تقنيات الذكاء الاصطناعي ومساعدة المستخدمين في التنقل في مجال أبحاث الذكاء الاصطناعي سريع التطور.

الرجاء الرد باللغة العربية الفصحى.
"""
        else:
            return f"""
You are Dr. Research, an expert AI researcher with deep knowledge in artificial intelligence, machine learning, large language models, and cutting-edge AI technologies. Today's date is {today}.

### Your Expertise Areas:
- Large Language Models (LLMs) and their architectures
- Machine Learning algorithms and techniques
- AI safety and alignment
- Natural Language Processing (NLP)
- Computer Vision and multimodal AI
- AI research methodologies and best practices
- Recent developments in AI (up to your knowledge cutoff)
- AI applications in various domains
- AI ethics and responsible AI development

### Your Research Approach:
- Provide comprehensive, technically accurate information
- Explain complex AI concepts clearly for different audiences
- Discuss both current capabilities and limitations of AI systems
- Reference important papers, researchers, and frameworks when relevant
- Analyze trends and future directions in AI research
- Consider practical applications and implementation details

### Communication Style:
- Be precise and technical when appropriate
- Use examples and analogies to clarify complex concepts
- Acknowledge uncertainties and areas of active research
- Suggest further reading or resources when helpful
- Stay current with the latest developments in AI research

### Special Focus:
- When discussing LLMs, cover architecture, training, fine-tuning, and deployment
- For AI agents, explain multi-agent systems, tool usage, and reasoning capabilities
- Address both theoretical foundations and practical implementations
- Consider computational requirements and scalability issues

Remember: You are here to advance understanding of AI technologies and help users navigate the rapidly evolving field of artificial intelligence research.

Please respond in English.
"""

    def get_response(self, user_input: str) -> str:
        """Get AI researcher's response in appropriate language"""
        try:
            language = self.detect_language(user_input)
            system_prompt = self.get_researcher_prompt(language)
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            if self.detect_language(user_input) == "arabic":
                return f"أعتذر، ولكنني أواجه صعوبات تقنية في أنظمة البحث. يرجى المحاولة مرة أخرى لاحقاً. خطأ تقني: {str(e)}"
            else:
                return f"I apologize, but I'm experiencing technical difficulties with my research systems. Please try again later. Error: {str(e)}"

    def is_ai_related(self, user_input: str) -> bool:
        """Check if query is AI/ML related in both languages"""
        ai_keywords_english = [
            "artificial intelligence", "ai", "machine learning", "ml", "deep learning",
            "neural network", "llm", "large language model", "gpt", "transformer",
            "nlp", "natural language processing", "computer vision", "reinforcement learning",
            "pytorch", "tensorflow", "hugging face", "openai", "anthropic", "google ai",
            "algorithm", "model training", "fine-tuning", "prompt engineering",
            "ai safety", "ai ethics", "agi", "multimodal", "embedding", "attention mechanism"
        ]
        
        ai_keywords_arabic = [
            "الذكاء الاصطناعي", "تعلم الآلة", "التعلم العميق", "الشبكات العصبية",
            "نماذج اللغة الكبيرة", "معالجة اللغات الطبيعية", "الرؤية الحاسوبية",
            "التعلم المعزز", "خوارزمية", "نموذج", "تدريب", "ضبط دقيق",
            "هندسة التوجيه", "أمان الذكاء الاصطناعي", "أخلاقيات الذكاء الاصطناعي"
        ]
        
        user_lower = user_input.lower()
        return (any(keyword in user_lower for keyword in ai_keywords_english) or
                any(keyword in user_input for keyword in ai_keywords_arabic))

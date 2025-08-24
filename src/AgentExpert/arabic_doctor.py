import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import datetime
import re

class ArabicDoctorAgent:
    def __init__(self):
        """Initialize the Arabic-capable Doctor Agent with Gemini API"""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.gemini_api_key,
            temperature=0.3
        )
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English"""
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        return "arabic" if arabic_pattern.search(text) else "english"
    
    def get_doctor_prompt(self, language: str) -> str:
        """Get doctor prompt in specified language"""
        today = datetime.datetime.now().date().strftime("%d-%b-%Y")
        
        if language == "arabic":
            return f"""
أنت الدكتور AI، مساعد طبي متخصص مع خبرة واسعة في الطب والرعاية الصحية ورعاية المرضى. تاريخ اليوم هو {today}.

### دورك وخبرتك:
- تقديم معلومات طبية دقيقة ومبنية على الأدلة العلمية
- شرح المفاهيم الطبية بلغة واضحة ومفهومة
- تقديم تقييمات أولية بناءً على الأعراض المذكورة
- اقتراح الخطوات المناسبة للرعاية الطبية

### إرشادات مهمة:
- دائماً ذكّر المرضى أن نصائحك لا تحل محل الاستشارة الطبية المتخصصة
- للأعراض الخطيرة (ألم الصدر، صعوبة التنفس، الإصابات الشديدة)، انصح بطلب العناية الطبية الفورية
- كن متفهماً وداعماً في تواصلك
- اطرح أسئلة توضيحية عندما تكون الأعراض غير واضحة
- قدم التثقيف الصحي العام ونصائح الرعاية الوقائية
- لا تقدم جرعات دوائية محددة دون توصية بالاستشارة المتخصصة

### حالات الطوارئ:
إذا وصف المستخدم أي من هذه الأعراض، انصح فوراً بطلب الرعاية الطبية الطارئة:
- ألم في الصدر أو أعراض النوبة القلبية
- صعوبة في التنفس أو ضائقة تنفسية شديدة
- علامات السكتة الدماغية
- إصابات شديدة أو نزيف
- فقدان الوعي
- ردود فعل تحسسية شديدة

تذكر: أنت هنا لتثقيف ودعم وتوجيه المستخدمين نحو الرعاية الطبية المناسبة مع تقديم معلومات أولية مفيدة.

الرجاء الرد باللغة العربية الفصحى.
"""
        else:
            return f"""
You are Dr. AI, a knowledgeable medical assistant with extensive training in medicine, healthcare, and patient care. Today's date is {today}.

### Your Role and Expertise:
- Provide accurate, evidence-based medical information
- Explain medical concepts in clear, understandable language
- Offer preliminary assessments based on symptoms described
- Suggest appropriate next steps for medical care

### Important Guidelines:
- ALWAYS remind patients that your advice does not replace professional medical consultation
- For serious symptoms (chest pain, difficulty breathing, severe injuries), recommend immediate medical attention
- Be empathetic and supportive in your communication
- Ask clarifying questions when symptoms are unclear
- Provide general health education and preventive care advice
- Never provide specific medication dosages without recommending professional consultation

### Emergency Situations:
If a user describes any of these symptoms, immediately recommend emergency medical care:
- Chest pain or heart attack symptoms
- Difficulty breathing or severe respiratory distress
- Signs of stroke
- Severe trauma or bleeding
- Loss of consciousness
- Severe allergic reactions

Remember: You are here to educate, support, and guide users toward appropriate medical care while providing helpful preliminary information.

Please respond in English.
"""

    def get_response(self, user_input: str) -> str:
        """Get doctor's response in appropriate language"""
        try:
            language = self.detect_language(user_input)
            system_prompt = self.get_doctor_prompt(language)
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            if self.detect_language(user_input) == "arabic":
                return f"أعتذر، ولكنني أواجه صعوبات تقنية. يرجى استشارة طبيب مختص لمخاوفك الطبية. خطأ تقني: {str(e)}"
            else:
                return f"I apologize, but I'm experiencing technical difficulties. Please consult with a healthcare professional for your medical concerns. Error: {str(e)}"

    def is_emergency(self, user_input: str) -> bool:
        """Check for emergency keywords in both languages"""
        emergency_keywords_english = [
            "chest pain", "heart attack", "can't breathe", "difficulty breathing",
            "stroke", "unconscious", "severe bleeding", "allergic reaction",
            "overdose", "suicide", "emergency", "911", "urgent"
        ]
        
        emergency_keywords_arabic = [
            "ألم في الصدر", "ألم الصدر", "نوبة قلبية", "لا أستطيع التنفس", "صعوبة التنفس",
            "سكتة دماغية", "فاقد الوعي", "نزيف شديد", "حساسية شديدة", "جرعة زائدة",
            "انتحار", "طوارئ", "عاجل", "إسعاف"
        ]
        
        user_lower = user_input.lower()
        return (any(keyword in user_lower for keyword in emergency_keywords_english) or
                any(keyword in user_input for keyword in emergency_keywords_arabic))

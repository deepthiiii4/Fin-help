import re
from typing import Dict, Tuple, Any

def analyze_stock_sentiment(news_content: str) -> Dict[str, Any]:
    """
    Analyzes stock-related news to determine sentiment percentages and provide reasoning.
    
    Args:
        news_content (str): The news content containing information about a stock
        
    Returns:
        Dict with buy_percent, hold_percent, sell_percent, recommendation, and reasoning
    """
    # Analyze text sentiment directly without looking for analyst recommendations
    buy_percent, hold_percent, sell_percent = analyze_text_sentiment(news_content)
    
    # Determine the main recommendation
    recommendation = determine_recommendation(buy_percent, hold_percent, sell_percent)
    
    # Generate reasoning based on the content and recommendation
    reasoning = generate_reasoning(news_content, recommendation)
    
    return {
        "buy_percent": buy_percent,
        "hold_percent": hold_percent,
        "sell_percent": sell_percent,
        "recommendation": recommendation,
        "reasoning": reasoning
    }

def simple_tokenize(text: str) -> list:
    """Simple word tokenization without NLTK"""
    # Clean the text - keep alphanumeric, spaces and sentence punctuation
    text = re.sub(r'[^\w\s.!?]', ' ', text)
    # Split by whitespace
    return text.lower().split()

def simple_stem(word: str) -> str:
    """Simple stemming function without NLTK"""
    if len(word) > 4:
        if word.endswith('ing'):
            return word[:-3]
        elif word.endswith('ed'):
            return word[:-2]
        elif word.endswith('es'):
            return word[:-2]
        elif word.endswith('s') and not word.endswith('ss'):
            return word[:-1]
    return word

def analyze_text_sentiment(text: str) -> Tuple[float, float, float]:
    """
    Analyze sentiment in the text using keyword matching, contextual clues,
    and basic text processing techniques.
    """
    # Define keyword dictionaries for different sentiments with weights
    buy_keywords = {
        "growth": 2, "grow": 2, "growing": 2, "grew": 2,
        "rally": 2, "rallied": 2, "rallying": 2,
        "outperform": 3, "outperformed": 3, "outperforming": 3,
        "bullish": 3, "bull": 2,
        "upside": 2, "up": 1, "upward": 2,
        "strong performance": 2, "performed strongly": 2, "strong": 1,
        "beat expectations": 3, "exceeded expectations": 3, "better than expected": 3,
        "increase": 1, "increased": 1, "increasing": 1, 
        "milestone": 1, "boom": 2, "booming": 2,
        "dominance": 2, "dominant": 2, "dominating": 2,
        "optimistic": 2, "optimism": 2,
        "rise": 1, "rising": 1, "rose": 1,
        "valuable": 1, "value": 1, "positive outlook": 3,
        "potential": 1, "innovation": 1, "innovative": 1,
        "leadership": 1, "leader": 1, "leading": 1,
        "success": 1, "successful": 1, "succeeded": 1,
        "opportunity": 1, "promising": 2, "exceed": 2, "expand": 1, "expanded": 1,
        "profit": 2, "profitable": 2, "gains": 2
    }
    
    sell_keywords = {
        "decline": 2, "declined": 2, "declining": 2,
        "downgrade": 3, "downgraded": 3,
        "underperform": 3, "underperformed": 3, "underperforming": 3,
        "bearish": 3, "bear": 2,
        "downside": 2, "down": 1, "downward": 2,
        "weak performance": 2, "performed weakly": 2, "weak": 1,
        "miss expectations": 3, "missed expectations": 3, "worse than expected": 3,
        "decrease": 1, "decreased": 1, "decreasing": 1,
        "drop": 1, "dropped": 1, "dropping": 1,
        "plummet": 3, "plummeted": 3, "plummeting": 3,
        "fall": 1, "falling": 1, "fell": 1,
        "risk": 1, "risky": 1, "risks": 1,
        "concern": 1, "concerning": 1, "concerned": 1, "concerns": 1,
        "negative outlook": 3, "negative": 2,
        "overvalued": 2, "overpriced": 2, "expensive": 1,
        "competition": 1, "competitive": 1, "competitor": 1,
        "pressure": 1, "pressured": 1, "under pressure": 2,
        "challenge": 1, "challenged": 1, "challenging": 1,
        "struggle": 2, "struggled": 2, "struggling": 2,
        "slowdown": 2, "slowing": 2, "slowed": 2,
        "disappointing": 2, "disappointed": 2, "disappointment": 2,
        "loss": 2, "losing": 2, "lost": 2, "losses": 2,
        "trouble": 2, "troubled": 2, "troubling": 2
    }
    
    hold_keywords = {
        "stable": 2, "stability": 2,
        "maintain": 2, "maintained": 2, "maintaining": 2,
        "mixed signals": 3, "mixed": 2,
        "fair value": 2, "fairly valued": 2,
        "balanced": 2, "balance": 2,
        "wait and see": 3, "waiting": 1,
        "uncertain": 2, "uncertainty": 2,
        "volatile": 1, "volatility": 1,
        "hold": 3, "holding": 3,
        "steady": 2, "steadily": 2,
        "neutral outlook": 3, "neutral": 2,
        "cautious": 1, "caution": 1,
        "moderate": 1, "moderately": 1,
        "patience": 1, "patient": 1,
        "sideways": 2, "consolidation": 2, "consolidating": 2,
        "even": 1, "unchanged": 1, "flat": 1, 
        "consistent": 1, "consistently": 1
    }
    
    # Tokenize and stem the text
    words = simple_tokenize(text)
    stemmed_words = [simple_stem(word) for word in words]
    stemmed_text = ' '.join(stemmed_words)
    
    # Count keyword occurrences with weights using stemmed text
    buy_score = 0
    sell_score = 0
    hold_score = 0
    
    # Process the text to find sentiment clues
    sentences = re.split(r'[.!?]\s+', text)
    for sentence in sentences:
        sentence_lower = sentence.lower()
        words = simple_tokenize(sentence_lower)
        stemmed_sentence = ' '.join([simple_stem(word) for word in words])
        
        # Check for negation in the sentence
        has_negation = any(neg in sentence_lower for neg in ["not ", "n't ", "no ", "never ", "without "])
        
        # Analyze each sentiment category
        for keyword, weight in buy_keywords.items():
            stemmed_keyword = ' '.join([simple_stem(word) for word in simple_tokenize(keyword.lower())])
            count = stemmed_sentence.count(stemmed_keyword)
            if count > 0:
                # Check if negation is close to the keyword
                if has_negation:
                    # Simple proximity check for negation
                    sentence_parts = sentence_lower.split()
                    keyword_parts = keyword.lower().split()
                    
                    for i, part in enumerate(sentence_parts):
                        if any(neg in part for neg in ["not", "n't", "no", "never", "without"]):
                            # Check if keyword is within 5 words of negation
                            nearby_words = ' '.join(sentence_parts[max(0, i-5):min(len(sentence_parts), i+6)])
                            if keyword.lower() in nearby_words:
                                # Reverse sentiment if negation is nearby
                                buy_score -= weight * count
                                sell_score += weight * count * 0.5
                                break
                    else:  # No negation found nearby
                        buy_score += weight * count
                else:
                    buy_score += weight * count
        
        for keyword, weight in sell_keywords.items():
            stemmed_keyword = ' '.join([simple_stem(word) for word in simple_tokenize(keyword.lower())])
            count = stemmed_sentence.count(stemmed_keyword)
            if count > 0:
                # Check if negation is close to the keyword
                if has_negation:
                    # Simple proximity check for negation
                    sentence_parts = sentence_lower.split()
                    keyword_parts = keyword.lower().split()
                    
                    for i, part in enumerate(sentence_parts):
                        if any(neg in part for neg in ["not", "n't", "no", "never", "without"]):
                            # Check if keyword is within 5 words of negation
                            nearby_words = ' '.join(sentence_parts[max(0, i-5):min(len(sentence_parts), i+6)])
                            if keyword.lower() in nearby_words:
                                # Reverse sentiment if negation is nearby
                                sell_score -= weight * count
                                buy_score += weight * count * 0.5
                                break
                    else:  # No negation found nearby
                        sell_score += weight * count
                else:
                    sell_score += weight * count
        
        for keyword, weight in hold_keywords.items():
            stemmed_keyword = ' '.join([simple_stem(word) for word in simple_tokenize(keyword.lower())])
            count = stemmed_sentence.count(stemmed_keyword)
            if count > 0:
                hold_score += weight * count
    
    # Look for phrases and contextual clues
    phrase_patterns = {
        "buy": [
            r"(strong|positive|promising)\s+(outlook|future|prospect)",
            r"(growth|profit|revenue)\s+(increas|improv|expand)",
            r"(hit|reach)\s+(record|all-time|new)\s+(high|level)",
            r"(bull|upward)\s+trend",
            r"(gain|jump|leap)\s+(in|of)\s+(value|price|stock)"
        ],
        "sell": [
            r"(weak|negative|poor)\s+(outlook|future|prospect)",
            r"(decline|drop|decrease)\s+(in|of)\s+(revenue|profit|growth)",
            r"(hit|reach)\s+(record|all-time|new)\s+(low|bottom)",
            r"(bear|downward)\s+trend",
            r"(lose|loss|plunge)\s+(in|of)\s+(value|price|stock)"
        ],
        "hold": [
            r"(stable|steady|consistent)\s+(outlook|future|prospect)",
            r"(maintain|sustain|preserve)\s+(level|position|status)",
            r"(balanced|fair|reasonable)\s+(value|price|assessment)",
            r"(cautious|careful|prudent)\s+(approach|view|outlook)",
            r"wait\s+and\s+see"
        ]
    }
    
    # Check for complex phrases
    for category, patterns in phrase_patterns.items():
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if category == "buy":
                buy_score += len(matches) * 3  # Complex phrases get higher weight
            elif category == "sell":
                sell_score += len(matches) * 3
            else:  # hold
                hold_score += len(matches) * 3
    
    # Ensure we have some sentiment scores
    total = buy_score + sell_score + hold_score
    if total == 0:
        # Default to balanced if no keywords found
        return 33.33, 33.33, 33.33
    
    # Calculate percentages
    buy_percent = max(0, round((buy_score / total) * 100, 2))
    sell_percent = max(0, round((sell_score / total) * 100, 2))
    hold_percent = max(0, round((hold_score / total) * 100, 2))
    
    # Normalize percentages to ensure they sum to 100%
    total_percent = buy_percent + sell_percent + hold_percent
    if total_percent != 100:
        buy_percent = round((buy_percent / total_percent) * 100, 2)
        sell_percent = round((sell_percent / total_percent) * 100, 2)
        hold_percent = round((hold_percent / total_percent) * 100, 2)
    
    return buy_percent, hold_percent, sell_percent

def determine_recommendation(buy_percent: float, hold_percent: float, sell_percent: float) -> str:
    """
    Determine the overall recommendation based on sentiment percentages.
    """
    if buy_percent >= hold_percent and buy_percent >= sell_percent:
        return "BUY"
    elif sell_percent >= buy_percent and sell_percent >= hold_percent:
        return "SELL"
    else:
        return "HOLD"

def generate_reasoning(text: str, recommendation: str) -> str:
    """
    Generate context-aware reasoning based on the recommendation and news content.
    """
    # Extract key sentences that might contain important information
    sentences = re.split(r'[.!?]\s+', text)
    relevant_sentences = []
    
    # Keywords specific to each recommendation type - expanded for better matching
    if recommendation == "BUY":
        keywords = ["growth", "rally", "increase", "positive", "rise", "milestone", 
                   "outperform", "bullish", "dominance", "valuable", "optimistic",
                   "boom", "profit", "strong", "beat", "exceed", "gain", "upside",
                   "trillion", "high", "record", "success", "innovation", "leader"]
    elif recommendation == "SELL":
        keywords = ["decline", "drop", "decrease", "negative", "fall", "concern", 
                   "underperform", "bearish", "risk", "weak", "downgrade", "loss",
                   "trouble", "plummet", "challenge", "struggle", "pressure",
                   "disappointing", "slowdown", "overvalued", "expensive", "low"]
    else:  # HOLD
        keywords = ["stable", "maintain", "neutral", "balanced", "mixed", 
                   "uncertain", "volatile", "steady", "wait", "cautious", "fair", 
                   "moderate", "patience", "consolidation", "unchanged", "flat"]
    
    # Score each sentence based on relevance to recommendation and factual content
    sentence_scores = []
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        # Skip sentences that look like headers, labels, or citations
        if len(sentence.split()) <= 3 or sentence.strip().startswith('.'):
            continue
            
        # Skip sentences explicitly mentioning analysts or recommendations
        if any(term in sentence.lower() for term in ["analyst", "recommendation", "recommend"]):
            continue
            
        # Score based on relevant keywords
        keyword_score = sum(2 for keyword in keywords if keyword.lower() in sentence.lower())
        
        # Score based on factual content indicators
        fact_indicators = ["achieved", "reported", "announced", "launched", 
                          "grew by", "increased by", "decreased by", "fell by",
                          "percent", "%", "billion", "million", "trillion", "market cap"]
        fact_score = sum(3 for indicator in fact_indicators if indicator.lower() in sentence.lower())
        
        # Prioritize sentences with numbers as they often contain concrete facts
        number_score = 2 if re.search(r'\d+', sentence) else 0
        
        # Prioritize sentences with company name/ticker mentioned
        company_score = 3 if re.search(r'company|stock|shares|market|corporation|inc\.?|ltd\.?', 
                                       sentence.lower()) else 0
        
        # Calculate total score and store with the sentence
        total_score = keyword_score + fact_score + number_score + company_score
        sentence_scores.append((sentence.strip(), total_score, i))
    
    # Sort sentences by score (higher first) and then by original position
    sentence_scores.sort(key=lambda x: (-x[1], x[2]))
    
    # Take top scoring sentences
    top_sentences = [s[0] for s in sentence_scores[:3]]
    
    if top_sentences:
        reasoning = " ".join(top_sentences)
    else:
        reasoning = "Based on the overall sentiment analysis of available information."
    
    return reasoning


    

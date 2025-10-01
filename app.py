"""
AI Product Advisor - Streamlit Web App
A beautiful web interface for product research using local LLMs
"""

import streamlit as st
import time
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="AI Product Advisor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'advisor' not in st.session_state:
    st.session_state.advisor = None
    st.session_state.results = []

class SmartProductAdvisor:
    """AI-Powered Product Research Assistant"""
    
    def __init__(self, model="gpt-oss:20b", ollama_url="http://localhost:11434/v1"):
        self.model = model
        self.client = OpenAI(base_url=ollama_url, api_key='ollama')
    
    def research_products(self, query, budget=None, requirements=None, num_products=5):
        """Generate comprehensive product research"""
        context = f"Product Category: {query}"
        if budget:
            context += f"\nBudget: {budget}"
        if requirements:
            context += f"\nSpecial Requirements: {requirements}"
        
        prompt = f"""You are an expert product researcher and shopping advisor. Provide a comprehensive buying guide for:

{context}

Generate a detailed guide with the following structure:

## 🎯 PRODUCT OVERVIEW
Brief introduction to the product category and what buyers should know.

## 🏆 TOP {num_products} RECOMMENDED PRODUCTS
For each product, provide:
**{num_products}. [Brand + Model Name]** - $[Price]
- ⭐ Rating: [X.X/5.0]
- 🔑 Key Features: [List 3-4 standout features]
- ✅ Pros: [2-3 advantages]
- ❌ Cons: [1-2 disadvantages]
- 👤 Best For: [Target user profile]

## 💰 PRICE BREAKDOWN
- Budget Range ($X-$Y): [Description]
- Mid-Range ($X-$Y): [Description]  
- Premium ($X+): [Description]

## 🛒 BUYING GUIDE
### What to Look For:
- [Key feature 1 and why it matters]
- [Key feature 2 and why it matters]
- [Key feature 3 and why it matters]

### Common Mistakes to Avoid:
- [Mistake 1]
- [Mistake 2]

## 🎖️ FINAL VERDICT
- **🥇 Best Overall**: [Product name] - [One sentence why]
- **💵 Best Value**: [Product name] - [One sentence why]
- **✨ Best Premium**: [Product name] - [One sentence why]

Make recommendations realistic, specific, and based on actual 2024 market knowledge."""

        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            elapsed = time.time() - start_time
            guide = response.choices[0].message.content
            
            return {
                "query": query,
                "budget": budget,
                "requirements": requirements,
                "guide": guide,
                "model": self.model,
                "generation_time": elapsed,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info(f"💡 Make sure Ollama is running and {self.model} is installed")
            return None
    
    def compare_products(self, product1, product2):
        """Direct comparison between two products"""
        prompt = f"""Compare these two products in detail:

Product A: {product1}
Product B: {product2}

Provide a comprehensive comparison with:

## 📊 SPECIFICATIONS COMPARISON
| Feature | {product1} | {product2} |
|---------|------------|------------|
[Fill in key specs side by side]

## ⚔️ HEAD-TO-HEAD ANALYSIS
### Performance
[Compare performance aspects]

### Value for Money
[Compare value proposition]

### Build Quality & Design
[Compare quality and design]

### User Experience
[Compare usability]

## 🏁 THE VERDICT
**Winner**: [Product name]
**Reason**: [Detailed explanation]

**When to choose {product1}**: [Scenarios]
**When to choose {product2}**: [Scenarios]

Be objective, detailed, and help the buyer make an informed decision."""

        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            elapsed = time.time() - start_time
            comparison = response.choices[0].message.content
            
            return {
                "comparison": comparison,
                "generation_time": elapsed
            }
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return None

# Header
st.markdown('<h1 class="main-header">🛍️ AI Product Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Smart product research powered by local AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_choice = st.selectbox(
        "Select Model",
        ["gpt-oss:20b", "llama3:latest", "qwen3:30b"],
        help="Choose the AI model for product research"
    )
    
    ollama_url = st.text_input(
        "Ollama URL",
        "http://localhost:11434/v1",
        help="URL of your Ollama server"
    )
    
    if st.button("🔄 Initialize Advisor"):
        with st.spinner("Initializing AI advisor..."):
            st.session_state.advisor = SmartProductAdvisor(model=model_choice, ollama_url=ollama_url)
            st.success("✅ Advisor initialized!")
    
    st.divider()
    
    st.header("📊 About")
    st.info("""
    **Features:**
    - 🔍 Product Research
    - ⚔️ Product Comparison
    - 💰 Price Analysis
    - 🎯 Smart Recommendations
    
    **Powered by:**
    - Ollama (Local LLM)
    - Streamlit
    - Python
    """)

# Main tabs
tab1, tab2 = st.tabs(["🔍 Product Research", "⚔️ Product Comparison"])

with tab1:
    st.header("Research Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_query = st.text_input(
            "Product Category",
            placeholder="e.g., wireless headphones, laptop, coffee maker",
            help="What product are you researching?"
        )
        
        budget = st.text_input(
            "Budget (Optional)",
            placeholder="e.g., under $500, $200-$800",
            help="What's your budget range?"
        )
    
    with col2:
        requirements = st.text_area(
            "Special Requirements (Optional)",
            placeholder="e.g., good battery life, noise cancellation, beginner-friendly",
            help="Any specific features you need?",
            height=100
        )
        
        num_products = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5,
            help="How many products to recommend?"
        )
    
    if st.button("🚀 Generate Product Guide", key="research_btn"):
        if not st.session_state.advisor:
            st.warning("⚠️ Please initialize the advisor first (see sidebar)")
        elif not product_query:
            st.warning("⚠️ Please enter a product category")
        else:
            with st.spinner(f"🤖 Researching {product_query}... This may take 30-60 seconds"):
                result = st.session_state.advisor.research_products(
                    query=product_query,
                    budget=budget if budget else None,
                    requirements=requirements if requirements else None,
                    num_products=num_products
                )
                
                if result:
                    st.success(f"✅ Research completed in {result['generation_time']:.1f} seconds")
                    
                    # Display results
                    st.markdown("---")
                    st.markdown(result['guide'])
                    
                    # Metadata
                    with st.expander("📊 Research Details"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Model Used", result['model'])
                        with col2:
                            st.metric("Generation Time", f"{result['generation_time']:.1f}s")
                        with col3:
                            st.metric("Timestamp", result['timestamp'])

with tab2:
    st.header("Compare Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product1 = st.text_input(
            "Product 1",
            placeholder="e.g., Sony WH-1000XM5",
            help="First product to compare"
        )
    
    with col2:
        product2 = st.text_input(
            "Product 2",
            placeholder="e.g., Bose QuietComfort Ultra",
            help="Second product to compare"
        )
    
    if st.button("⚔️ Compare Products", key="compare_btn"):
        if not st.session_state.advisor:
            st.warning("⚠️ Please initialize the advisor first (see sidebar)")
        elif not product1 or not product2:
            st.warning("⚠️ Please enter both products to compare")
        else:
            with st.spinner(f"🤖 Comparing {product1} vs {product2}..."):
                result = st.session_state.advisor.compare_products(product1, product2)
                
                if result:
                    st.success(f"✅ Comparison completed in {result['generation_time']:.1f} seconds")
                    
                    # Display comparison
                    st.markdown("---")
                    st.markdown(result['comparison'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Made with ❤️ using Ollama and Streamlit</p>
    <p style='font-size: 0.9rem;'>Running locally on your machine • No API keys required • Your data stays private</p>
</div>
""", unsafe_allow_html=True)


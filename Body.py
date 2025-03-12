
import openai
import streamlit as st
from serpapi import GoogleSearch
from newspaper import Article

#API Keys 
OPENAI_API_KEY = "your-api-key"
SERP_API_KEY = "your-serpapi-key"

def search_google(query):
    """Fetch top search results."""
    params = {"engine": "google", "q": query, "api_key": SERP_API_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()
    return [result['link'] for result in results.get('organic_results', [])[:3]]

def extract_text_from_url(url):
    """Extract text from a news article."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:2000]  #Limited text size for better processing
    except:
        return ""

def query_llm(claim, evidence):
    """Ask LLM to fact-check the claim."""
    prompt = f"""
    Claim: "{claim}"

    Evidence:
    {evidence}

    Evaluate this claim based on the evidence and give a truthfulness score (0-100), plus an explanation.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a fact-checking assistant."},
                  {"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

def fact_check(claim):
    """Main fact-checking function."""
    sources = search_google(claim)
    extracted_texts = [extract_text_from_url(url) for url in sources]
    combined_evidence = "\n\n".join(extracted_texts[:2])  # Use top 2 sources, (need to find better way)

    if not combined_evidence:
        return "No reliable sources found."

    return query_llm(claim, combined_evidence), sources

# --------- STREAMLIT UI --------- #
st.title("Fact-Checker")
st.write("Enter a claim below to verify its truthfulness.")

claim = st.text_input("Enter a claim:")
if st.button("Check Fact"):
    with st.spinner("Verifying..."):
        result, sources = fact_check(claim)
        
        # Extract score (if available)
        score = None
        for word in result.split():
            if word.isdigit() and 0 <= int(word) <= 100:
                score = int(word)
                break

        # Display results with color coding
        if score is not None:
            if score >= 75:
                st.success(f"✅ Likely True ({score}/100)")
            elif score >= 50:
                st.warning(f"⚠️ Uncertain ({score}/100)")
            else:
                st.error(f"❌ Likely False ({score}/100)")
        else:
            st.warning("⚠️ Unable to determine truth score.")

        st.write("### Explanation:")
        st.write(result)

        st.write("### Sources Used:")
        for url in sources:
            st.markdown(f"- [{url}]({url})")

st.caption("Powered by OpenAI & Google Search")

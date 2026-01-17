import streamlit as st
import anthropic
from duckduckgo_search import DDGS
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Be Newsie | AI Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# Header
st.title("📰 Be Newsie")
st.markdown("### AI-Powered Newsletter Generator for Nonprofits")
st.markdown("*Generate engaging newsletters in minutes, not hours.*")
st.divider()

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Anthropic API Key", type="password", help="Get your key at console.anthropic.com")
    st.divider()
    st.markdown("**Built for Community Hero PA**")
    st.markdown("Serving African American women in the Philadelphia region")

# Main inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Newsletter Focus")
    theme = st.text_input(
        "Theme/Topic for this edition",
        placeholder="e.g., Summer health equity resources, Financial literacy month"
    )
    
    ceo_bullets = st.text_area(
        "CEO Notes (bullet points about what you want to share)",
        placeholder="• Excited about our upcoming community event\n• Reflecting on maternal health awareness\n• Grateful for our volunteers",
        height=150
    )

with col2:
    st.subheader("🎯 Customize Sectors")
    st.markdown("*Default sectors for Community Hero PA:*")
    
    health_focus = st.text_input(
        "Health focus",
        value="health equity, maternal health, chronic disease, mental health",
    )
    
    wealth_focus = st.text_input(
        "Wealth focus", 
        value="financial literacy, entrepreneurship, career development, homeownership"
    )
    
    civic_focus = st.text_input(
        "Civic Engagement focus",
        value="voting, advocacy, local government, community organizing"
    )

st.divider()

# Search for articles function
def search_articles(sector, focus_terms, num_results=3):
    """Search for recent articles using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            query = f"{focus_terms} Philadelphia Black women 2024 2025"
            results = list(ddgs.news(query, max_results=num_results))
            if not results:
                results = list(ddgs.text(query, max_results=num_results))
            return results
    except Exception as e:
        st.warning(f"Could not fetch {sector} articles: {str(e)}")
        return []

# Generate newsletter function
def generate_newsletter(theme, ceo_bullets, articles_by_sector, api_key):
    """Generate newsletter using Claude"""
    
    # Format articles for prompt
    articles_text = ""
    for sector, articles in articles_by_sector.items():
        articles_text += f"\n\n{sector.upper()} ARTICLES:\n"
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            url = article.get('url') or article.get('href', 'No URL')
            body = article.get('body', article.get('description', 'No description'))
            articles_text += f"{i}. {title}\n   URL: {url}\n   Summary: {body[:200]}...\n"
    
    prompt = f"""You are writing a newsletter for Community Hero PA, a nonprofit serving African American women in the Philadelphia region.

THEME FOR THIS EDITION: {theme}

CEO'S PERSONAL NOTES/BULLET POINTS:
{ceo_bullets}

RECENT ARTICLES FOUND:
{articles_text}

Write a complete newsletter following this EXACT structure:

1. **SUBJECT LINES** — Provide 3 options. Curiosity-driven, 5-8 words each.

2. **OPENING HOOK** — A story, question, or bold statement (2-3 sentences) that grabs attention and connects to the theme.

3. **ONE MAIN THING** — The single most important takeaway for this edition. Make it clear and actionable.

4. **CEO NOTE** — Personal, warm, 3-4 sentences. Use the bullet points provided to craft an authentic message from the CEO. First person voice.

5. **QUICK HITS** — One insight per sector (Health, Wealth, Civic Engagement). Keep each scannable—2-3 sentences max. Reference the articles found and include the URLs.

6. **ONE CTA** — A single clear action: donate, attend, or share. Make it specific.

7. **P.S.** — "Catch the latest episode of Her Health Matters: [include a compelling teaser about health topics]"

TONE: Warm, direct, empowering. Like a smart friend sharing what matters. Write for African American women in Philadelphia who are busy but care deeply about their community.

FORMAT: Use clear headers and keep it scannable. This should be ready to paste into Mailchimp."""

    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

# Generate button
if st.button("🚀 Generate Newsletter", type="primary", use_container_width=True):
    
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
    elif not theme:
        st.error("Please enter a theme for your newsletter.")
    else:
        with st.spinner("🔍 Searching for recent articles..."):
            # Search for articles in each sector
            articles_by_sector = {
                "Health": search_articles("Health", health_focus),
                "Wealth": search_articles("Wealth", wealth_focus),
                "Civic Engagement": search_articles("Civic", civic_focus)
            }
            
            # Display found articles
            st.subheader("📚 Articles Found")
            for sector, articles in articles_by_sector.items():
                with st.expander(f"{sector} ({len(articles)} articles)"):
                    for article in articles:
                        title = article.get('title', 'No title')
                        url = article.get('url') or article.get('href', 'No URL')
                        st.markdown(f"- [{title}]({url})")
        
        with st.spinner("✍️ Writing your newsletter..."):
            try:
                newsletter = generate_newsletter(theme, ceo_bullets, articles_by_sector, api_key)
                
                st.divider()
                st.subheader("📰 Your Newsletter Draft")
                st.markdown(newsletter)
                
                # Copy button
                st.divider()
                st.download_button(
                    label="📋 Download Newsletter as Text",
                    data=newsletter,
                    file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Please check your Anthropic API key.")
            except Exception as e:
                st.error(f"Error generating newsletter: {str(e)}")

# Footer
st.divider()
st.markdown("---")
st.markdown("*Be Newsie — Built with ❤️ for nonprofits who want to communicate better, faster.*")
st.markdown("**Ready to automate your newsletter?** [Book a demo](https://cal.com) | [Learn more](https://benewsie.carrd.co)")

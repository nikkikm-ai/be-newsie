import streamlit as st
import anthropic
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Be Newsie | AI Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# Brand colors
NAVY = "#2C3E50"
BLUE = "#4F9DCB"
GOLD = "#F7C548"
CHARCOAL = "#2C3E50"
GRAY = "#7C7C7C"

# Header
st.title("📰 Be Newsie")
st.markdown("### AI-Powered Newsletter Generator for Nonprofits")
st.markdown("*Generate beautiful, ready-to-send newsletters in minutes.*")
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
    
    podcast_topic = st.text_input(
        "Latest Her Health Matters episode topic",
        placeholder="e.g., Managing stress during the holidays"
    )

with col2:
    st.subheader("🎯 This Edition's Content")
    
    health_news = st.text_area(
        "Health insight or news to feature",
        placeholder="e.g., New maternal health clinic opening in West Philly",
        height=80
    )
    
    wealth_news = st.text_area(
        "Wealth insight or news to feature",
        placeholder="e.g., Free tax prep services available through April",
        height=80
    )
    
    civic_news = st.text_area(
        "Civic Engagement insight or news to feature",
        placeholder="e.g., Voter registration deadline approaching",
        height=80
    )
    
    cta_text = st.text_input(
        "Call to Action",
        placeholder="e.g., Register for our Feb 15 wellness workshop"
    )
    
    cta_link = st.text_input(
        "CTA Link/URL",
        placeholder="e.g., https://communityhero.org/register"
    )

st.divider()

# Generate newsletter function
def generate_newsletter(theme, ceo_bullets, health_news, wealth_news, civic_news, cta_text, cta_link, podcast_topic, api_key):
    """Generate styled HTML newsletter using Claude"""
    
    prompt = f"""You are writing a newsletter for Community Hero PA, a nonprofit serving African American women in the Philadelphia region.

THEME: {theme}

CEO'S PERSONAL NOTES: {ceo_bullets}

CONTENT TO INCLUDE:
- Health: {health_news}
- Wealth: {wealth_news}  
- Civic Engagement: {civic_news}
- Call to Action: {cta_text} (Link: {cta_link})
- Podcast topic: {podcast_topic}

Generate a newsletter with this EXACT structure. Return ONLY the content for each section, no HTML tags:

SUBJECT_LINE_1: [Curiosity-driven, 5-8 words]
SUBJECT_LINE_2: [Different angle, 5-8 words]
SUBJECT_LINE_3: [Third option, 5-8 words]

OPENING_HOOK: [2-3 sentences - a story, question, or bold statement that grabs attention]

ONE_MAIN_THING: [Single key takeaway, 2-3 sentences]

CEO_NOTE: [Personal, warm, 3-4 sentences in first person using the bullet points provided]

HEALTH_TITLE: [Short catchy title for health section]
HEALTH_CONTENT: [2-3 sentences about the health topic]

WEALTH_TITLE: [Short catchy title for wealth section]
WEALTH_CONTENT: [2-3 sentences about the wealth topic]

CIVIC_TITLE: [Short catchy title for civic section]
CIVIC_CONTENT: [2-3 sentences about the civic topic]

CTA_BUTTON_TEXT: [3-5 words for the button]

PS_TEXT: [Teaser for Her Health Matters podcast episode on: {podcast_topic}]

TONE: Warm, direct, empowering. Like a smart friend sharing what matters."""

    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def parse_newsletter_content(content):
    """Parse the generated content into sections"""
    sections = {}
    current_key = None
    current_value = []
    
    for line in content.split('\n'):
        line = line.strip()
        if ':' in line and any(line.startswith(key) for key in ['SUBJECT_LINE', 'OPENING_HOOK', 'ONE_MAIN_THING', 'CEO_NOTE', 'HEALTH_', 'WEALTH_', 'CIVIC_', 'CTA_', 'PS_']):
            if current_key:
                sections[current_key] = ' '.join(current_value).strip()
            parts = line.split(':', 1)
            current_key = parts[0].strip()
            current_value = [parts[1].strip()] if len(parts) > 1 else []
        elif current_key:
            current_value.append(line)
    
    if current_key:
        sections[current_key] = ' '.join(current_value).strip()
    
    return sections

def create_html_newsletter(sections, cta_link):
    """Create beautifully styled HTML newsletter"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Georgia, serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background-color: {NAVY}; padding: 30px 40px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: 1px;">COMMUNITY HERO PA</h1>
                            <p style="color: {GOLD}; margin: 10px 0 0 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">Health • Wealth • Civic Power</p>
                        </td>
                    </tr>
                    
                    <!-- Opening Hook -->
                    <tr>
                        <td style="padding: 40px 40px 20px 40px;">
                            <p style="font-size: 18px; line-height: 1.7; color: {CHARCOAL}; margin: 0;">
                                {sections.get('OPENING_HOOK', '')}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- One Main Thing -->
                    <tr>
                        <td style="padding: 20px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="background-color: #FFF9E6; border-left: 4px solid {GOLD}; padding: 20px 25px;">
                                        <p style="color: {GOLD}; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 8px 0;">✨ The One Thing</p>
                                        <p style="font-size: 16px; line-height: 1.6; color: {CHARCOAL}; margin: 0;">
                                            {sections.get('ONE_MAIN_THING', '')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- CEO Note -->
                    <tr>
                        <td style="padding: 20px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="background-color: #F8F9FA; border-radius: 8px; padding: 25px;">
                                        <p style="color: {NAVY}; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 12px 0;">A Note From Our CEO</p>
                                        <p style="font-size: 15px; line-height: 1.7; color: {CHARCOAL}; margin: 0; font-style: italic;">
                                            {sections.get('CEO_NOTE', '')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Section Divider -->
                    <tr>
                        <td style="padding: 10px 40px;">
                            <p style="color: {NAVY}; font-size: 18px; font-weight: 700; text-align: center; margin: 0;">— Quick Hits —</p>
                        </td>
                    </tr>
                    
                    <!-- Health Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="border-bottom: 2px solid {BLUE}; padding-bottom: 15px;">
                                        <p style="color: {BLUE}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">🏥 Health</p>
                                        <p style="color: {NAVY}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{sections.get('HEALTH_TITLE', 'Health Update')}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {CHARCOAL}; margin: 0;">
                                            {sections.get('HEALTH_CONTENT', '')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Wealth Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="border-bottom: 2px solid {GOLD}; padding-bottom: 15px;">
                                        <p style="color: {GOLD}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">💰 Wealth</p>
                                        <p style="color: {NAVY}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{sections.get('WEALTH_TITLE', 'Wealth Update')}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {CHARCOAL}; margin: 0;">
                                            {sections.get('WEALTH_CONTENT', '')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Civic Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding-bottom: 15px;">
                                        <p style="color: {NAVY}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">🗳️ Civic Engagement</p>
                                        <p style="color: {NAVY}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{sections.get('CIVIC_TITLE', 'Civic Update')}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {CHARCOAL}; margin: 0;">
                                            {sections.get('CIVIC_CONTENT', '')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- CTA Button -->
                    <tr>
                        <td style="padding: 30px 40px; text-align: center;">
                            <a href="{cta_link or '#'}" style="display: inline-block; background-color: {GOLD}; color: {NAVY}; font-size: 16px; font-weight: 700; text-decoration: none; padding: 15px 40px; border-radius: 5px; text-transform: uppercase; letter-spacing: 1px;">
                                {sections.get('CTA_BUTTON_TEXT', 'Take Action')}
                            </a>
                        </td>
                    </tr>
                    
                    <!-- PS Section -->
                    <tr>
                        <td style="padding: 20px 40px 30px 40px; border-top: 1px solid #eee;">
                            <p style="font-size: 14px; line-height: 1.6; color: {GRAY}; margin: 0;">
                                <strong>P.S.</strong> 🎙️ {sections.get('PS_TEXT', 'Catch the latest episode of Her Health Matters!')}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: {NAVY}; padding: 25px 40px; text-align: center;">
                            <p style="color: #ffffff; font-size: 12px; margin: 0 0 10px 0;">Community Hero PA | Philadelphia, PA</p>
                            <p style="color: {GRAY}; font-size: 11px; margin: 0;">
                                <a href="#" style="color: {BLUE}; text-decoration: none;">Unsubscribe</a> · 
                                <a href="#" style="color: {BLUE}; text-decoration: none;">View in browser</a>
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return html

# Generate button
if st.button("🚀 Generate Newsletter", type="primary", use_container_width=True):
    
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
    elif not theme:
        st.error("Please enter a theme for your newsletter.")
    else:
        with st.spinner("✍️ Writing your newsletter..."):
            try:
                # Generate content
                raw_content = generate_newsletter(
                    theme, ceo_bullets, health_news, wealth_news, 
                    civic_news, cta_text, cta_link, podcast_topic, api_key
                )
                
                # Parse into sections
                sections = parse_newsletter_content(raw_content)
                
                # Display subject line options
                st.divider()
                st.subheader("📧 Subject Line Options")
                st.markdown(f"1. **{sections.get('SUBJECT_LINE_1', '')}**")
                st.markdown(f"2. **{sections.get('SUBJECT_LINE_2', '')}**")
                st.markdown(f"3. **{sections.get('SUBJECT_LINE_3', '')}**")
                
                # Create HTML
                html_newsletter = create_html_newsletter(sections, cta_link)
                
                # Preview
                st.divider()
                st.subheader("👀 Newsletter Preview")
                st.components.v1.html(html_newsletter, height=1200, scrolling=True)
                
                # Download buttons
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download HTML",
                        data=html_newsletter,
                        file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        label="📄 Download Raw Text",
                        data=raw_content,
                        file_name=f"newsletter_text_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                st.success("✅ Copy the HTML and paste into Mailchimp's HTML block, or download and send!")
                
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Please check your Anthropic API key.")
            except Exception as e:
                st.error(f"Error generating newsletter: {str(e)}")

# Footer
st.divider()
st.markdown("---")
st.markdown("*Be Newsie — Beautiful newsletters for nonprofits, powered by AI.*")

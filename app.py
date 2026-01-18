import streamlit as st
import anthropic
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Be Newsie | AI Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# Initialize session state for generated content
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'sections' not in st.session_state:
    st.session_state.sections = {}

# Header
st.title("📰 Be Newsie")
st.markdown("### AI-Powered Newsletter Generator for Nonprofits")
st.markdown("*Generate beautiful, ready-to-send newsletters in minutes.*")
st.divider()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ API Settings")
    api_key = st.text_input("Anthropic API Key", type="password", help="Get your key at console.anthropic.com")
    
    st.divider()
    st.header("🏢 Your Organization")
    
    org_name = st.text_input("Organization Name", value="", placeholder="Community Hero PA")
    org_tagline = st.text_input("Tagline", value="", placeholder="Health • Wealth • Civic Power")
    org_website = st.text_input("Website", value="", placeholder="https://yourorg.org")
    org_logo_url = st.text_input("Logo URL (optional)", value="", placeholder="https://yoursite.com/logo.png")
    
    st.divider()
    st.header("🎨 Brand Colors")
    col1, col2 = st.columns(2)
    with col1:
        primary_color = st.color_picker("Primary", "#2C3E50")
        accent_color = st.color_picker("Accent", "#F7C548")
    with col2:
        secondary_color = st.color_picker("Secondary", "#4F9DCB")
        text_color = st.color_picker("Text", "#2C3E50")

# Main inputs (Step 1)
if not st.session_state.generated:
    st.subheader("📝 Step 1: Tell us about this edition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.text_input(
            "Theme/Topic for this edition",
            placeholder="e.g., Summer health equity resources"
        )
        
        ceo_bullets = st.text_area(
            "CEO Notes (bullet points)",
            placeholder="• Excited about our upcoming event\n• Reflecting on our community impact\n• Grateful for our supporters",
            height=120
        )
        
        podcast_topic = st.text_input(
            "Podcast/Media episode topic (optional)",
            placeholder="e.g., Managing stress during the holidays"
        )
    
    with col2:
        health_news = st.text_area(
            "Health content to feature",
            placeholder="e.g., New maternal health clinic opening",
            height=70
        )
        
        wealth_news = st.text_area(
            "Wealth content to feature",
            placeholder="e.g., Free tax prep services available",
            height=70
        )
        
        civic_news = st.text_area(
            "Civic Engagement content to feature",
            placeholder="e.g., Voter registration deadline approaching",
            height=70
        )
        
        cta_text = st.text_input(
            "Call to Action",
            placeholder="e.g., Register for our wellness workshop"
        )
        
        cta_link = st.text_input(
            "CTA Link/URL",
            placeholder="e.g., https://yourorg.org/register"
        )
    
    st.divider()
    
    # Generate button
    if st.button("🚀 Generate Draft", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Anthropic API key in the sidebar.")
        elif not theme:
            st.error("Please enter a theme for your newsletter.")
        elif not org_name:
            st.error("Please enter your organization name in the sidebar.")
        else:
            with st.spinner("✍️ Writing your newsletter draft..."):
                try:
                    prompt = f"""You are writing a newsletter for {org_name}, a nonprofit organization.

THEME: {theme}
CEO'S NOTES: {ceo_bullets}
CONTENT TO INCLUDE:
- Health: {health_news}
- Wealth: {wealth_news}  
- Civic Engagement: {civic_news}
- Call to Action: {cta_text}
- Podcast topic: {podcast_topic}

Generate newsletter content. Return ONLY the content for each section in this EXACT format:

SUBJECT_LINE_1: [Curiosity-driven, 5-8 words]
SUBJECT_LINE_2: [Different angle, 5-8 words]
SUBJECT_LINE_3: [Third option, 5-8 words]
OPENING_HOOK: [2-3 engaging sentences - a story, question, or bold statement]
ONE_MAIN_THING: [Single key takeaway, 2-3 sentences]
CEO_NOTE: [Personal, warm, 3-4 sentences in first person]
HEALTH_TITLE: [Short catchy title]
HEALTH_CONTENT: [2-3 sentences]
WEALTH_TITLE: [Short catchy title]
WEALTH_CONTENT: [2-3 sentences]
CIVIC_TITLE: [Short catchy title]
CIVIC_CONTENT: [2-3 sentences]
CTA_BUTTON_TEXT: [3-5 words for button]
PS_TEXT: [Teaser for podcast/media mention]

TONE: Warm, direct, empowering."""

                    client = anthropic.Anthropic(api_key=api_key)
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    # Parse response
                    content = message.content[0].text
                    sections = {}
                    current_key = None
                    current_value = []
                    
                    for line in content.split('\n'):
                        line = line.strip()
                        if ':' in line:
                            for key in ['SUBJECT_LINE_1', 'SUBJECT_LINE_2', 'SUBJECT_LINE_3', 'OPENING_HOOK', 'ONE_MAIN_THING', 'CEO_NOTE', 'HEALTH_TITLE', 'HEALTH_CONTENT', 'WEALTH_TITLE', 'WEALTH_CONTENT', 'CIVIC_TITLE', 'CIVIC_CONTENT', 'CTA_BUTTON_TEXT', 'PS_TEXT']:
                                if line.startswith(key):
                                    if current_key:
                                        sections[current_key] = ' '.join(current_value).strip()
                                    parts = line.split(':', 1)
                                    current_key = key
                                    current_value = [parts[1].strip()] if len(parts) > 1 else []
                                    break
                        elif current_key:
                            current_value.append(line)
                    
                    if current_key:
                        sections[current_key] = ' '.join(current_value).strip()
                    
                    # Store in session state
                    st.session_state.sections = sections
                    st.session_state.cta_link = cta_link
                    st.session_state.generated = True
                    st.rerun()
                    
                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Please check your Anthropic API key.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Step 2: Edit generated content
else:
    st.subheader("✏️ Step 2: Edit Your Newsletter")
    st.markdown("*Make any changes you want, then create the final version.*")
    
    # Reset button
    if st.button("← Start Over"):
        st.session_state.generated = False
        st.session_state.sections = {}
        st.rerun()
    
    st.divider()
    
    sections = st.session_state.sections
    
    # Subject lines
    st.markdown("**📧 Subject Line Options**")
    subj1 = st.text_input("Option 1", value=sections.get('SUBJECT_LINE_1', ''), key="subj1")
    subj2 = st.text_input("Option 2", value=sections.get('SUBJECT_LINE_2', ''), key="subj2")
    subj3 = st.text_input("Option 3", value=sections.get('SUBJECT_LINE_3', ''), key="subj3")
    
    st.divider()
    
    # Opening hook
    st.markdown("**🎣 Opening Hook**")
    opening_hook = st.text_area("Grabs attention", value=sections.get('OPENING_HOOK', ''), height=100, key="hook")
    
    # One main thing
    st.markdown("**✨ The One Thing**")
    one_main_thing = st.text_area("Key takeaway", value=sections.get('ONE_MAIN_THING', ''), height=100, key="main")
    
    # CEO Note
    st.markdown("**👤 CEO Note**")
    ceo_note = st.text_area("Personal message", value=sections.get('CEO_NOTE', ''), height=120, key="ceo")
    
    st.divider()
    st.markdown("**📰 Quick Hits Sections**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("🏥 **Health**")
        health_title = st.text_input("Title", value=sections.get('HEALTH_TITLE', ''), key="htitle")
        health_content = st.text_area("Content", value=sections.get('HEALTH_CONTENT', ''), height=100, key="hcontent")
        health_image = st.text_input("Image URL (optional)", value="", key="himage", placeholder="https://...")
    
    with col2:
        st.markdown("💰 **Wealth**")
        wealth_title = st.text_input("Title", value=sections.get('WEALTH_TITLE', ''), key="wtitle")
        wealth_content = st.text_area("Content", value=sections.get('WEALTH_CONTENT', ''), height=100, key="wcontent")
        wealth_image = st.text_input("Image URL (optional)", value="", key="wimage", placeholder="https://...")
    
    with col3:
        st.markdown("🗳️ **Civic**")
        civic_title = st.text_input("Title", value=sections.get('CIVIC_TITLE', ''), key="ctitle")
        civic_content = st.text_area("Content", value=sections.get('CIVIC_CONTENT', ''), height=100, key="ccontent")
        civic_image = st.text_input("Image URL (optional)", value="", key="cimage", placeholder="https://...")
    
    st.divider()
    
    # CTA
    st.markdown("**🎯 Call to Action**")
    col1, col2 = st.columns(2)
    with col1:
        cta_button = st.text_input("Button Text", value=sections.get('CTA_BUTTON_TEXT', ''), key="ctabtn")
    with col2:
        cta_link = st.text_input("Button Link", value=st.session_state.get('cta_link', ''), key="ctalink")
    
    # PS
    st.markdown("**📌 P.S.**")
    ps_text = st.text_area("Closing teaser", value=sections.get('PS_TEXT', ''), height=80, key="ps")
    
    st.divider()
    
    # Create final newsletter
    if st.button("✨ Create Final Newsletter", type="primary", use_container_width=True):
        
        # Build HTML with edited content
        logo_html = f'<img src="{org_logo_url}" alt="{org_name}" style="max-height: 60px; margin-bottom: 15px;">' if org_logo_url else ''
        
        def get_image_html(image_url, section_name):
            if image_url:
                return f'<img src="{image_url}" alt="{section_name}" style="width: 100%; max-width: 520px; height: 150px; object-fit: cover; border-radius: 6px; margin-bottom: 15px;">'
            else:
                return f'<div style="width: 100%; height: 120px; background-color: #f0f0f0; border-radius: 6px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px;">[ Add {section_name} image ]</div>'
        
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
                        <td style="background-color: {primary_color}; padding: 30px 40px; text-align: center;">
                            {logo_html}
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: 1px;">{org_name.upper()}</h1>
                            <p style="color: {accent_color}; margin: 10px 0 0 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">{org_tagline}</p>
                        </td>
                    </tr>
                    
                    <!-- Opening Hook -->
                    <tr>
                        <td style="padding: 40px 40px 20px 40px;">
                            <p style="font-size: 18px; line-height: 1.7; color: {text_color}; margin: 0;">
                                {opening_hook}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- One Main Thing -->
                    <tr>
                        <td style="padding: 20px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="background-color: #FFF9E6; border-left: 4px solid {accent_color}; padding: 20px 25px;">
                                        <p style="color: {accent_color}; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 8px 0;">✨ The One Thing</p>
                                        <p style="font-size: 16px; line-height: 1.6; color: {text_color}; margin: 0;">
                                            {one_main_thing}
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
                                        <p style="color: {primary_color}; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 12px 0;">A Note From Our CEO</p>
                                        <p style="font-size: 15px; line-height: 1.7; color: {text_color}; margin: 0; font-style: italic;">
                                            {ceo_note}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Section Divider -->
                    <tr>
                        <td style="padding: 20px 40px 10px 40px;">
                            <p style="color: {primary_color}; font-size: 18px; font-weight: 700; text-align: center; margin: 0;">— Quick Hits —</p>
                        </td>
                    </tr>
                    
                    <!-- Health Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            {get_image_html(health_image, "Health")}
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="border-bottom: 2px solid {secondary_color}; padding-bottom: 15px;">
                                        <p style="color: {secondary_color}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">🏥 Health</p>
                                        <p style="color: {primary_color}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{health_title}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {text_color}; margin: 0;">
                                            {health_content}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Wealth Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            {get_image_html(wealth_image, "Wealth")}
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="border-bottom: 2px solid {accent_color}; padding-bottom: 15px;">
                                        <p style="color: {accent_color}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">💰 Wealth</p>
                                        <p style="color: {primary_color}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{wealth_title}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {text_color}; margin: 0;">
                                            {wealth_content}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Civic Section -->
                    <tr>
                        <td style="padding: 15px 40px;">
                            {get_image_html(civic_image, "Civic")}
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding-bottom: 15px;">
                                        <p style="color: {primary_color}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 5px 0;">🗳️ Civic Engagement</p>
                                        <p style="color: {primary_color}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{civic_title}</p>
                                        <p style="font-size: 14px; line-height: 1.6; color: {text_color}; margin: 0;">
                                            {civic_content}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- CTA Button -->
                    <tr>
                        <td style="padding: 30px 40px; text-align: center;">
                            <a href="{cta_link or '#'}" style="display: inline-block; background-color: {accent_color}; color: {primary_color}; font-size: 16px; font-weight: 700; text-decoration: none; padding: 15px 40px; border-radius: 5px; text-transform: uppercase; letter-spacing: 1px;">
                                {cta_button}
                            </a>
                        </td>
                    </tr>
                    
                    <!-- PS Section -->
                    <tr>
                        <td style="padding: 20px 40px 30px 40px; border-top: 1px solid #eee;">
                            <p style="font-size: 14px; line-height: 1.6; color: #7C7C7C; margin: 0;">
                                <strong>P.S.</strong> 🎙️ {ps_text}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: {primary_color}; padding: 25px 40px; text-align: center;">
                            <p style="color: #ffffff; font-size: 12px; margin: 0 0 10px 0;">{org_name} | {org_website}</p>
                            <p style="color: #7C7C7C; font-size: 11px; margin: 0;">
                                <a href="#" style="color: {secondary_color}; text-decoration: none;">Unsubscribe</a> · 
                                <a href="#" style="color: {secondary_color}; text-decoration: none;">View in browser</a>
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
        
        # Display subject lines
        st.divider()
        st.subheader("📧 Your Subject Line Options")
        st.markdown(f"1. **{subj1}**")
        st.markdown(f"2. **{subj2}**")
        st.markdown(f"3. **{subj3}**")
        
        # Preview
        st.divider()
        st.subheader("👀 Final Preview")
        st.components.v1.html(html, height=1400, scrolling=True)
        
        # Download buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download HTML",
                data=html,
                file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
        with col2:
            # Plain text version
            plain_text = f"""SUBJECT OPTIONS:
1. {subj1}
2. {subj2}
3. {subj3}

---

{opening_hook}

THE ONE THING:
{one_main_thing}

FROM OUR CEO:
{ceo_note}

--- QUICK HITS ---

HEALTH: {health_title}
{health_content}

WEALTH: {wealth_title}
{wealth_content}

CIVIC: {civic_title}
{civic_content}

---

{cta_button}: {cta_link}

P.S. {ps_text}

---
{org_name} | {org_website}
"""
            st.download_button(
                label="📄 Download Plain Text",
                data=plain_text,
                file_name=f"newsletter_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.success("✅ Your newsletter is ready! Download the HTML and paste into your email platform.")

# Footer
st.divider()
st.markdown("---")
st.markdown("*Be Newsie — Beautiful newsletters for nonprofits, powered by AI.*")
st.markdown(f"[Get Help](mailto:support@benewsie.com) · [Book a Demo](https://cal.com)")

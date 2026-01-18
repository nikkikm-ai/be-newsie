import streamlit as st
import anthropic
from datetime import datetime
import base64

# Page config
st.set_page_config(
    page_title="Be Newsie | AI Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# Initialize session state
if 'preview_generated' not in st.session_state:
    st.session_state.preview_generated = False
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Store editable content
for field in ['subj1', 'subj2', 'subj3', 'hook', 'main_thing', 'ceo_note', 
              'p1_title', 'p1_content', 'p2_title', 'p2_content', 'p3_title', 'p3_content',
              'cta_btn', 'ps']:
    if field not in st.session_state:
        st.session_state[field] = ""

# Helper functions
def get_image_src(uploaded_file, url):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        return f"data:{uploaded_file.type};base64,{b64}"
    elif url and url.strip():
        return url.strip()
    return None

def get_image_html(image_src, section_name):
    if image_src:
        return f'<img src="{image_src}" alt="{section_name}" style="width: 100%; height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 12px;">'
    return f'<div style="width: 100%; height: 120px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; color: #adb5bd; font-size: 13px; border: 2px dashed #dee2e6;">📷 Add {section_name} image</div>'

def build_html(org_name, org_tagline, org_website, org_logo, primary, secondary, accent, text_color,
               section_label, hook, main_thing, ceo_note,
               p1_name, p1_title, p1_content, p1_img,
               p2_name, p2_title, p2_content, p2_img,
               p3_name, p3_title, p3_content, p3_img,
               cta_btn, cta_link, ps):
    
    logo_html = f'<img src="{org_logo}" alt="{org_name}" style="max-height: 50px; margin-bottom: 10px;">' if org_logo else ''
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Georgia, 'Times New Roman', serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">

<!-- Header -->
<tr>
<td style="background-color: {primary}; padding: 35px 40px; text-align: center;">
{logo_html}
<h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 0.5px;">{org_name.upper() if org_name else 'YOUR ORGANIZATION'}</h1>
<p style="color: {accent}; margin: 8px 0 0 0; font-size: 13px; letter-spacing: 2px;">{org_tagline if org_tagline else ''}</p>
</td>
</tr>

<!-- Opening Hook -->
<tr>
<td style="padding: 35px 40px 25px 40px;">
<p style="font-size: 17px; line-height: 1.75; color: {text_color}; margin: 0;">{hook}</p>
</td>
</tr>

<!-- One Main Thing -->
<tr>
<td style="padding: 10px 40px 25px 40px;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td style="background-color: #fffbf0; border-left: 4px solid {accent}; padding: 22px 25px; border-radius: 0 8px 8px 0;">
<p style="color: {accent}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 10px 0;">✨ The One Thing</p>
<p style="font-size: 15px; line-height: 1.65; color: {text_color}; margin: 0;">{main_thing}</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- CEO Note -->
<tr>
<td style="padding: 10px 40px 25px 40px;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td style="background-color: #f8f9fa; border-radius: 8px; padding: 25px;">
<p style="color: {primary}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 12px 0;">A Note From Our Team</p>
<p style="font-size: 15px; line-height: 1.7; color: {text_color}; margin: 0; font-style: italic;">{ceo_note}</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- Section Label -->
<tr>
<td style="padding: 15px 40px 5px 40px;">
<p style="color: {primary}; font-size: 16px; font-weight: 700; text-align: center; margin: 0;">— {section_label} —</p>
</td>
</tr>

<!-- Pillar 1 -->
<tr>
<td style="padding: 20px 40px 15px 40px;">
{get_image_html(p1_img, p1_name)}
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td style="border-bottom: 2px solid {secondary}; padding-bottom: 18px;">
<p style="color: {secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 6px 0;">{p1_name}</p>
<p style="color: {primary}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{p1_title}</p>
<p style="font-size: 14px; line-height: 1.65; color: {text_color}; margin: 0;">{p1_content}</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- Pillar 2 -->
<tr>
<td style="padding: 20px 40px 15px 40px;">
{get_image_html(p2_img, p2_name)}
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td style="border-bottom: 2px solid {accent}; padding-bottom: 18px;">
<p style="color: {accent}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 6px 0;">{p2_name}</p>
<p style="color: {primary}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{p2_title}</p>
<p style="font-size: 14px; line-height: 1.65; color: {text_color}; margin: 0;">{p2_content}</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- Pillar 3 -->
<tr>
<td style="padding: 20px 40px 15px 40px;">
{get_image_html(p3_img, p3_name)}
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td style="padding-bottom: 18px;">
<p style="color: {primary}; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 6px 0;">{p3_name}</p>
<p style="color: {primary}; font-size: 16px; font-weight: 700; margin: 0 0 8px 0;">{p3_title}</p>
<p style="font-size: 14px; line-height: 1.65; color: {text_color}; margin: 0;">{p3_content}</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- CTA Button -->
<tr>
<td style="padding: 25px 40px 30px 40px; text-align: center;">
<a href="{cta_link or '#'}" style="display: inline-block; background-color: {accent}; color: {primary}; font-size: 15px; font-weight: 700; text-decoration: none; padding: 16px 45px; border-radius: 6px; letter-spacing: 0.5px;">{cta_btn}</a>
</td>
</tr>

<!-- PS Section -->
<tr>
<td style="padding: 20px 40px 30px 40px; border-top: 1px solid #eee;">
<p style="font-size: 14px; line-height: 1.6; color: #7C7C7C; margin: 0;"><strong>P.S.</strong> {ps}</p>
</td>
</tr>

<!-- Footer -->
<tr>
<td style="background-color: {primary}; padding: 25px 40px; text-align: center;">
<p style="color: #ffffff; font-size: 12px; margin: 0 0 8px 0;">{org_name} {('| ' + org_website) if org_website else ''}</p>
<p style="color: #aaa; font-size: 11px; margin: 0;">
<a href="#" style="color: {secondary}; text-decoration: none;">Unsubscribe</a> · 
<a href="#" style="color: {secondary}; text-decoration: none;">View in browser</a>
</p>
</td>
</tr>

</table>
</td></tr>
</table>
</body>
</html>"""

# ============ SIDEBAR ============
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Anthropic API Key", type="password")
    
    st.divider()
    st.header("🏢 Organization")
    org_name = st.text_input("Name", placeholder="Type your Org Name Here")
    org_tagline = st.text_input("Tagline", placeholder="Your mission in a few words")
    org_website = st.text_input("Website", placeholder="https://yourorg.org")
    org_logo_url = st.text_input("Logo URL", placeholder="https://yoursite.com/logo.png")
    
    st.divider()
    st.header("🎨 Brand Colors")
    c1, c2 = st.columns(2)
    with c1:
        primary_color = st.color_picker("Primary", "#2C3E50")
        accent_color = st.color_picker("Accent", "#F7C548")
    with c2:
        secondary_color = st.color_picker("Secondary", "#4F9DCB")
        text_color = st.color_picker("Text", "#2C3E50")

# ============ MAIN FORM ============
if not st.session_state.preview_generated:
    
    st.markdown("**📝 Newsletter Details**")
    st.caption("Fill in the details below. AI will write your newsletter, then you can edit anything.")
    
    st.divider()
    
    # Theme and basics
    st.markdown("**Theme & Message**")
    theme = st.text_input("What's this newsletter about?", placeholder="e.g., January wellness resources, Spring fundraising update")
    
    ceo_bullets = st.text_area("Key points you want to share (bullet points)", 
                               placeholder="• What's on your mind\n• Recent wins or updates\n• What you're grateful for",
                               height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        cta_text = st.text_input("Call to Action", placeholder="e.g., Register for our March workshop")
    with col2:
        cta_link = st.text_input("CTA Link", placeholder="https://yourorg.org/register")
    
    ps_input = st.text_input("P.S. message (optional)", placeholder="e.g., Catch our latest podcast episode on...")
    
    st.divider()
    
    # Content pillars - user defined
    st.markdown("**📰 Your Content Sections**")
    st.caption("Customize your three content pillars. These can be anything relevant to your audience.")
    
    section_label = st.text_input("Section header label", value="What's New", placeholder="e.g., What's New, Updates, This Week")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Section 1**")
        pillar1_name = st.text_input("Section name", value="Health", key="p1n", placeholder="e.g., Health, Programs")
        pillar1_topic = st.text_area("What to cover", placeholder="Topic or news for this section", height=80, key="p1t")
        st.caption("Image (optional)")
        pillar1_upload = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], key="p1u", label_visibility="collapsed")
        pillar1_url = st.text_input("Or paste URL", key="p1url", placeholder="https://...", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Section 2**")
        pillar2_name = st.text_input("Section name", value="Wealth", key="p2n", placeholder="e.g., Wealth, Events")
        pillar2_topic = st.text_area("What to cover", placeholder="Topic or news for this section", height=80, key="p2t")
        st.caption("Image (optional)")
        pillar2_upload = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], key="p2u", label_visibility="collapsed")
        pillar2_url = st.text_input("Or paste URL", key="p2url", placeholder="https://...", label_visibility="collapsed")
    
    with col3:
        st.markdown("**Section 3**")
        pillar3_name = st.text_input("Section name", value="Community", key="p3n", placeholder="e.g., Civic, Community")
        pillar3_topic = st.text_area("What to cover", placeholder="Topic or news for this section", height=80, key="p3t")
        st.caption("Image (optional)")
        pillar3_upload = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], key="p3u", label_visibility="collapsed")
        pillar3_url = st.text_input("Or paste URL", key="p3url", placeholder="https://...", label_visibility="collapsed")
    
    st.divider()
    
    # Length preference
    length_option = st.radio("Content length", ["Standard (2-3 sentences per section)", "Detailed (4-5 sentences per section)"], horizontal=True)
    length_instruction = "2-3 sentences" if "Standard" in length_option else "4-5 sentences"
    
    st.divider()
    
    # Generate button
    if st.button("🚀 Generate Newsletter", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Anthropic API key in the sidebar.")
        elif not theme:
            st.error("Please enter a theme for your newsletter.")
        elif not org_name:
            st.error("Please enter your organization name in the sidebar.")
        else:
            with st.spinner("✨ Writing your newsletter..."):
                try:
                    prompt = f"""Write a newsletter for {org_name}.

THEME: {theme}
KEY POINTS FROM LEADERSHIP: {ceo_bullets}
CALL TO ACTION: {cta_text}
P.S. TOPIC: {ps_input}

CONTENT SECTIONS:
1. {pillar1_name}: {pillar1_topic}
2. {pillar2_name}: {pillar2_topic}
3. {pillar3_name}: {pillar3_topic}

Return content in this EXACT format (no extra text, just the labels and content):

SUBJECT_LINE_1: [Curiosity-driven, 5-8 words]
SUBJECT_LINE_2: [Different angle, 5-8 words]
SUBJECT_LINE_3: [Third option, 5-8 words]
OPENING_HOOK: [2-3 engaging sentences to open the newsletter]
ONE_MAIN_THING: [{length_instruction} - the key takeaway]
CEO_NOTE: [Personal, warm, {length_instruction} in first person voice]
PILLAR1_TITLE: [Catchy headline for {pillar1_name}]
PILLAR1_CONTENT: [{length_instruction} about {pillar1_name}]
PILLAR2_TITLE: [Catchy headline for {pillar2_name}]
PILLAR2_CONTENT: [{length_instruction} about {pillar2_name}]
PILLAR3_TITLE: [Catchy headline for {pillar3_name}]
PILLAR3_CONTENT: [{length_instruction} about {pillar3_name}]
CTA_BUTTON: [3-5 words for button]
PS_TEXT: [Engaging P.S. message]

TONE: Warm, direct, empowering. Like a trusted friend sharing what matters."""

                    client = anthropic.Anthropic(api_key=api_key)
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    # Parse response
                    content = message.content[0].text
                    parsed = {}
                    lines = content.split('\n')
                    current_key = None
                    current_val = []
                    
                    keys = ['SUBJECT_LINE_1', 'SUBJECT_LINE_2', 'SUBJECT_LINE_3', 'OPENING_HOOK', 
                            'ONE_MAIN_THING', 'CEO_NOTE', 'PILLAR1_TITLE', 'PILLAR1_CONTENT',
                            'PILLAR2_TITLE', 'PILLAR2_CONTENT', 'PILLAR3_TITLE', 'PILLAR3_CONTENT',
                            'CTA_BUTTON', 'PS_TEXT']
                    
                    for line in lines:
                        line = line.strip()
                        matched = False
                        for key in keys:
                            if line.startswith(key + ':'):
                                if current_key:
                                    parsed[current_key] = ' '.join(current_val).strip()
                                current_key = key
                                current_val = [line.split(':', 1)[1].strip()] if ':' in line else []
                                matched = True
                                break
                        if not matched and current_key:
                            current_val.append(line)
                    
                    if current_key:
                        parsed[current_key] = ' '.join(current_val).strip()
                    
                    # Store in session state
                    st.session_state.subj1 = parsed.get('SUBJECT_LINE_1', '')
                    st.session_state.subj2 = parsed.get('SUBJECT_LINE_2', '')
                    st.session_state.subj3 = parsed.get('SUBJECT_LINE_3', '')
                    st.session_state.hook = parsed.get('OPENING_HOOK', '')
                    st.session_state.main_thing = parsed.get('ONE_MAIN_THING', '')
                    st.session_state.ceo_note = parsed.get('CEO_NOTE', '')
                    st.session_state.p1_title = parsed.get('PILLAR1_TITLE', '')
                    st.session_state.p1_content = parsed.get('PILLAR1_CONTENT', '')
                    st.session_state.p2_title = parsed.get('PILLAR2_TITLE', '')
                    st.session_state.p2_content = parsed.get('PILLAR2_CONTENT', '')
                    st.session_state.p3_title = parsed.get('PILLAR3_TITLE', '')
                    st.session_state.p3_content = parsed.get('PILLAR3_CONTENT', '')
                    st.session_state.cta_btn = parsed.get('CTA_BUTTON', '')
                    st.session_state.ps = parsed.get('PS_TEXT', '')
                    
                    # Store other inputs
                    st.session_state.org_name = org_name
                    st.session_state.org_tagline = org_tagline
                    st.session_state.org_website = org_website
                    st.session_state.org_logo = org_logo_url
                    st.session_state.primary = primary_color
                    st.session_state.secondary = secondary_color
                    st.session_state.accent = accent_color
                    st.session_state.text_color = text_color
                    st.session_state.section_label = section_label
                    st.session_state.p1_name = pillar1_name
                    st.session_state.p2_name = pillar2_name
                    st.session_state.p3_name = pillar3_name
                    st.session_state.cta_link = cta_link
                    st.session_state.p1_img = get_image_src(pillar1_upload, pillar1_url)
                    st.session_state.p2_img = get_image_src(pillar2_upload, pillar2_url)
                    st.session_state.p3_img = get_image_src(pillar3_upload, pillar3_url)
                    
                    st.session_state.preview_generated = True
                    st.rerun()
                    
                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Please check your Anthropic API key.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============ PREVIEW + EDIT MODE ============
else:
    # Start over button
    if st.button("← Start Over"):
        st.session_state.preview_generated = False
        st.rerun()
    
    # Subject lines
    st.subheader("📧 Subject Line Options")
    st.markdown(f"1. **{st.session_state.subj1}**")
    st.markdown(f"2. **{st.session_state.subj2}**")
    st.markdown(f"3. **{st.session_state.subj3}**")
    
    st.divider()
    
    # Build and show preview
    html = build_html(
        st.session_state.org_name, st.session_state.org_tagline, 
        st.session_state.org_website, st.session_state.org_logo,
        st.session_state.primary, st.session_state.secondary, 
        st.session_state.accent, st.session_state.text_color,
        st.session_state.section_label,
        st.session_state.hook, st.session_state.main_thing, st.session_state.ceo_note,
        st.session_state.p1_name, st.session_state.p1_title, st.session_state.p1_content, st.session_state.p1_img,
        st.session_state.p2_name, st.session_state.p2_title, st.session_state.p2_content, st.session_state.p2_img,
        st.session_state.p3_name, st.session_state.p3_title, st.session_state.p3_content, st.session_state.p3_img,
        st.session_state.cta_btn, st.session_state.cta_link, st.session_state.ps
    )
    
    st.subheader("👀 Preview")
    st.components.v1.html(html, height=1400, scrolling=True)
    
    # Download buttons
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download HTML", html, f"newsletter_{datetime.now().strftime('%Y%m%d')}.html", "text/html", use_container_width=True)
    with col2:
        plain = f"""SUBJECT OPTIONS:\n1. {st.session_state.subj1}\n2. {st.session_state.subj2}\n3. {st.session_state.subj3}\n\n{st.session_state.hook}\n\nTHE ONE THING:\n{st.session_state.main_thing}\n\nFROM OUR TEAM:\n{st.session_state.ceo_note}\n\n{st.session_state.p1_name}: {st.session_state.p1_title}\n{st.session_state.p1_content}\n\n{st.session_state.p2_name}: {st.session_state.p2_title}\n{st.session_state.p2_content}\n\n{st.session_state.p3_name}: {st.session_state.p3_title}\n{st.session_state.p3_content}\n\n{st.session_state.cta_btn}: {st.session_state.cta_link}\n\nP.S. {st.session_state.ps}"""
        st.download_button("📄 Download Text", plain, f"newsletter_{datetime.now().strftime('%Y%m%d')}.txt", "text/plain", use_container_width=True)
    
    st.divider()
    
    # Editable sections
    st.subheader("✏️ Edit Content")
    st.caption("Make changes below, then click 'Update Preview' to see them.")
    
    st.markdown("**Subject Lines**")
    st.session_state.subj1 = st.text_input("Option 1", value=st.session_state.subj1, key="ed_s1")
    st.session_state.subj2 = st.text_input("Option 2", value=st.session_state.subj2, key="ed_s2")
    st.session_state.subj3 = st.text_input("Option 3", value=st.session_state.subj3, key="ed_s3")
    
    st.markdown("**Opening Hook**")
    st.session_state.hook = st.text_area("Grabs reader attention", value=st.session_state.hook, height=100, key="ed_hook")
    
    st.markdown("**The One Thing**")
    st.session_state.main_thing = st.text_area("Key takeaway", value=st.session_state.main_thing, height=100, key="ed_main")
    
    st.markdown("**Team Note**")
    st.session_state.ceo_note = st.text_area("Personal message", value=st.session_state.ceo_note, height=120, key="ed_ceo")
    
    st.markdown("**Content Sections**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{st.session_state.p1_name}**")
        st.session_state.p1_title = st.text_input("Title", value=st.session_state.p1_title, key="ed_p1t")
        st.session_state.p1_content = st.text_area("Content", value=st.session_state.p1_content, height=100, key="ed_p1c")
    
    with col2:
        st.markdown(f"**{st.session_state.p2_name}**")
        st.session_state.p2_title = st.text_input("Title", value=st.session_state.p2_title, key="ed_p2t")
        st.session_state.p2_content = st.text_area("Content", value=st.session_state.p2_content, height=100, key="ed_p2c")
    
    with col3:
        st.markdown(f"**{st.session_state.p3_name}**")
        st.session_state.p3_title = st.text_input("Title", value=st.session_state.p3_title, key="ed_p3t")
        st.session_state.p3_content = st.text_area("Content", value=st.session_state.p3_content, height=100, key="ed_p3c")
    
    st.markdown("**Call to Action**")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.cta_btn = st.text_input("Button text", value=st.session_state.cta_btn, key="ed_cta")
    with col2:
        st.session_state.cta_link = st.text_input("Button link", value=st.session_state.cta_link, key="ed_link")
    
    st.markdown("**P.S.**")
    st.session_state.ps = st.text_area("Closing message", value=st.session_state.ps, height=80, key="ed_ps")
    
    if st.button("🔄 Update Preview", type="primary", use_container_width=True):
        st.rerun()

# Footer
st.divider()
st.caption("Be Newsie — Beautiful newsletters for nonprofits, powered by AI.")

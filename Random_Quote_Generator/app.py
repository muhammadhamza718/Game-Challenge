import streamlit as st
import requests
import json
import pyperclip
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from deep_translator import GoogleTranslator
import urllib.parse

# Ye line SSL verification warnings ko disable karta hai
urllib3.disable_warnings()

# Ye line page configuration ko set karta hai
st.set_page_config(
    page_title="Random Quote Generator",
    page_icon="💭",
    layout="centered"
)

# Ye Section Streamlit ki classes par CSS apply karta hai
st.markdown("""
    <style>
        /* Theme variables */
        :root {
            --background-primary: #ffffff;
            --background-secondary: #f8f9fa;
            --text-primary: #1a1a2e;
            --text-secondary: #666666;
            --accent-color: #4ecca3;
            --quote-bg: #ffffff;
            --quote-border: #4ecca3;
        }

        /* Dark theme overrides */
        @media (prefers-color-scheme: dark) {
            :root {
                --background-primary: #1B1B2F;
                --background-secondary: #1F1F3A;
                --text-primary: #ffffff;
                --text-secondary: rgba(255, 255, 255, 0.7);
                --quote-bg: rgba(31, 31, 58, 0.95);
            }
        }

        header{
            background-color: var(--background-primary) !important;
        }

        .stApp {
            background: linear-gradient(180deg, var(--background-primary) 0%, var(--background-secondary) 100%);
            color: var(--text-primary);
        }

        .st-an{
            background-color: var(--background-primary) !important;
        }
        
        .header-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 0.5rem;
            color: var(--accent-color);
            font-size: 2.5em !important;
        }

        .st-emotion-cache-1cvow4s{
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
    .quote-text {
        font-size: 28px;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        margin: 20px 0;
            padding: 30px;
            border-left: 5px solid var(--quote-border);
            background: var(--quote-bg);
            border-radius: 10px;
            color: var(--text-primary);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
    .author {
        font-size: 20px;
            color: var(--text-secondary);
        font-style: italic;
            margin: 20px 0;
            padding-left: 30px;
    }
        
    .category {
            font-size: 14px;
            color: var(--accent-color);
        text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 10px;
            padding-left: 30px;
    }
        
    .stButton button {
        width: 100%;
            border-radius: 8px !important;
        height: 3em;
            font-weight: 600;
            background-color: var(--accent-color) !important;
            color: var(--background-primary) !important;
            border: none !important;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Style the expander */
        .streamlit-expanderHeader {
            background: var(--quote-bg) !important;
            border-radius: 8px !important;
            border: 1px solid var(--accent-color) !important;
            color: var(--text-primary) !important;
        }
        
        .streamlit-expanderContent {
            background: var(--quote-bg) !important;
            border-radius: 0 0 8px 8px !important;
        }

        /* Footer styling */
        footer {
            color: var(--text-secondary);
        }
    </style>
    """, unsafe_allow_html=True)

# App title
st.markdown("""
    <div class="header-title">
        <span>✨</span>
        <span>Random Quote Generator</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("Get inspired with random quotes from great minds!")

def get_available_tags():
    """Quotable API se available tags fetch karta hai. Ye tags quotes ko categorize karne ke liye use hote hain"""
    try:
        response = requests.get(
            "https://api.quotable.io/tags",
            verify=False
        )
        if response.status_code == 200:
            tags = response.json()
            return [tag["name"] for tag in tags]
        return []
    except:
        return []

def get_quote(tags=None, min_length=None, max_length=None):    # Quote fetch karne ka function, 3 optional parameters leta hai
    """
    Quotable API se random quote fetch karta hai
    Parameters:
        tags: Quote ki category filter karne ke liye
        min_length: Minimum length ki filtering ke liye
        max_length: Maximum length ki filtering ke liye
    """
    try:                            # Error handling block shuru karta hai
        params = {"limit": 1}       # API parameters ka dictionary, limit=1 se ek hi quote mangwayenge
        if tags:                    # Agar tags parameter provide kiya gaya hai
            params["tags"] = ",".join(tags)    # Tags ko comma-separated string me convert karke paramaters me add karta hai
        if min_length:             # Agar minimum length specify ki gayi hai
            params["minLength"] = min_length    # Minimum length ko paramaters me add karta hai
        if max_length:             # Agar maximum length specify ki gayi hai
            params["maxLength"] = max_length    # Maximum length ko paramaters me add karta hai
            
        response = requests.get(    # GET request bhejta hai Quotable API ko
            "https://api.quotable.io/quotes/random",    # Random quote ka API endpoint
            verify=False,           # SSL verification disable ye agar enable hoga to error aayega
            params=params          # Upar banaye gaye parameters pass karta hai
        )
        
        if response.status_code == 200:    # Agar request successful hui
            quotes = response.json()        # JSON response ko Python object me convert karta hai
            if not quotes:                  # Agar koi quote nahi mila (empty list)
                st.warning("No quotes found with the selected filters. Try different filters.")    # Warning message dikhata hai
                return None                 # None return karta hai
            return quotes[0]               # Pehla quote return karta hai (kyunki limit=1 hai)
        else:                              # Agar request fail hui
            st.error(f"Error: API returned status code {response.status_code}")    # Error message dikhata hai
            return None                     # None return karta hai
    except Exception as e:                 # Kisi bhi error ko catch karta hai
        st.error(f"Error fetching quote: {str(e)}")    # Error message user ko dikhata hai
        return None                         # None return karta hai

def copy_quote(quote_text, author, tags=None):    # Quote ko clipboard pe copy karne ka function
    """Quote ko system clipboard pe copy karta hai, tags ke sath"""
    try:
        full_quote = f'"{quote_text}" - {author}'    # Quote text aur author ko format karta hai
        if tags:                                     # Agar tags available hain
            full_quote += f'\nCategories: {", ".join(tags)}'    # Tags ko new line me add karta hai
        pyperclip.copy(full_quote)                  # Formatted text ko clipboard pe copy karta hai
        st.toast("Quote copied to clipboard! ✨")    # Success message dikhata hai
    except Exception as e:
        st.warning("Unable to copy to clipboard. Please copy manually:")    # Warning message dikhata hai
        st.code(full_quote)    # Quote ko code block me display karta hai taki user manually copy kar sake

def translate_text(text, dest_language):    # Text translation ka function, original text aur target language ko parameters ke tor par leta hai
    """
    Text ko specified language me translate karta hai
    Parameters:
        text: Translate karne ke liye text
        dest_language: Target language ka code (e.g., 'hi' for Hindi)
    """
    try:                                    # Error handling block shuru karta hai
        if dest_language == 'en':           # Agar target language English hai
            return text                     # Original text hi return kar deta hai, translation ki zarurat nahi
        translator = GoogleTranslator(       # Google Translator ka instance create karta hai
            source='auto',                  # Source language auto-detect ke liye set karta hai
            target=dest_language            # Target language set karta hai jo parameter me di gayi hai
        )
        return translator.translate(text) or text    # Text ko translate karta hai, agar translation fail ho to original text return karta hai
    except Exception as e:                  # Kisi bhi error ko catch karta hai
        st.error(f"Translation error: {str(e)}")    # Error message user ko dikhata hai
        return text                         # Error ki situation me original text return karta hai

# ---------- SESSION STATE INITIALIZATION ----------
# Session state Streamlit ka feature hai jo page refresh ke baad bhi data ko preserve rakhta hai

# Tags ko session state me store karta hai agar pehle se nahi hain
if 'tags' not in st.session_state:          # Check karta hai ke tags pehle se exist karte hain ya nahi
    st.session_state.tags = get_available_tags()    # Available tags ko fetch karke store karta hai

# Selected language ko session state me store karta hai
if 'selected_language' not in st.session_state:    # Check karta hai ke selected language pehle se exist karti hai ya nahi
    st.session_state.selected_language = 'en'      # Default language English set karta hai

# Translated quote ko session state me store karta hai
if 'translated_quote' not in st.session_state:     # Check karta hai ke translated quote pehle se exist karta hai ya nahi
    st.session_state.translated_quote = None       # Initially None set karta hai

# ---------- FILTERS SECTION ----------
with st.expander("Quote Filters 🔍", expanded=False):    # Expandable section banata hai jo click karne par open/close hota hai
    col1, col2, col3 = st.columns(3)    # Screen ko 3 equal columns me divide karta hai, har filter ke liye ek column

    with col1:    # Pehle column me category selector rakhta hai
        selected_tag = st.selectbox(     # Dropdown menu create karta hai categories ke liye
            "Select Category",           # Dropdown ka label
            options=["All"] + st.session_state.tags,    # "All" option + available tags ki list
            help="Choose a category to filter quotes"    # Hover karne par dikhne wala help text
        )
    
    with col2:    # Dusre column me length slider rakhta hai
        length_range = st.slider(        # Range slider create karta hai quote length filter ke liye
            "Quote Length",              # Slider ka label
            min_value=0,                # Minimum possible value
            max_value=300,              # Maximum possible value
            value=(0, 300),             # Default selected range
            help="Filter quotes by character length"    # Hover help text
        )
    
    with col3:    # Teesre column me language selector rakhta hai
        languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)    # Available languages ki dictionary get karta hai
        languages_dict = {k.title(): v for k, v in languages_dict.items()}    # Language names ko Title Case me convert karta hai
        language_names = list(languages_dict.keys())    # Language names ki list banata hai dropdown ke liye
        
        english_index = 0    # English ka index track karne ke liye variable
        for i, lang in enumerate(language_names):    # Har language ko check karta hai
            if lang.lower() == 'english':    # English dhoondhta hai (case insensitive)
                english_index = i            # English ka index store karta hai
                break
        
        selected_language = st.selectbox(    # Language selection ke liye dropdown create karta hai
            "Select Language",              # Dropdown ka label
            options=language_names,         # Available languages ki list
            index=english_index,           # Default selected language (English)
            help="Choose the language for the quote"    # Hover help text
        )
        st.session_state.selected_language = languages_dict[selected_language]    # Selected language code ko session state me save karta hai

# ---------- QUOTE GENERATION ----------
if st.button("Generate New Quote 🎲"):    # Quote generate karne ka button
    # Length filter ke parameters set karta hai
    min_length = length_range[0] if length_range[0] > 0 else None    # Minimum length, agar 0 se bada hai to
    max_length = length_range[1] if length_range[1] < 300 else None    # Maximum length, agar 300 se chota hai to
    selected_tags = [selected_tag] if selected_tag != "All" else None    # Category filter, agar "All" nahi hai to

    # Naya quote fetch karta hai selected filters ke sath
    st.session_state.quote = get_quote(
        tags=selected_tags,        # Selected category/tag
        min_length=min_length,    # Minimum length filter
        max_length=max_length     # Maximum length filter
    )
    st.session_state.translated_quote = None    # Purana translated quote clear kar deta hai

# First time visit par ek quote fetch karta hai
if 'quote' not in st.session_state:    # Check karta hai ke quote pehle se exist karta hai ya nahi
    st.session_state.quote = get_quote()    # Naya random quote fetch karta hai

# ---------- QUOTE DISPLAY ----------
if st.session_state.quote:    # Agar quote successfully fetch hua hai
    quote_container = st.container()    # Quote display ke liye ek container create karta hai
    with quote_container:    # Container ke andar content add karta hai
        
        # Translation logic
        if (st.session_state.selected_language != 'en' and     # Agar English ke alawa koi language select hui hai
            (st.session_state.translated_quote is None or      # Aur ya to translated quote nahi hai
             st.session_state.translated_quote.get('lang') != st.session_state.selected_language)):    # Ya fir different language me hai
            
            # Quote content ko translate karta hai
            translated_content = translate_text(
                st.session_state.quote["content"],            # Original quote text
                st.session_state.selected_language            # Target language
            )
            # Author name ko translate karta hai
            translated_author = translate_text(
                st.session_state.quote["author"],             # Original author name
                st.session_state.selected_language            # Target language
            )
            # Translated content ko session state me store karta hai
            st.session_state.translated_quote = {
                'content': translated_content,    # Translated quote text
                'author': translated_author,      # Translated author name
                'lang': st.session_state.selected_language    # Translation ki language
            }
        
        # Display content selection
        if st.session_state.selected_language == 'en' or st.session_state.translated_quote is None:    # Agar English hai ya translation nahi hai
            content = st.session_state.quote["content"]    # Original content use karta hai
            author = st.session_state.quote["author"]      # Original author use karta hai
        else:
            content = st.session_state.translated_quote["content"]    # Translated content use karta hai
            author = st.session_state.translated_quote["author"]      # Translated author use karta hai
        
        # Quote text display
        st.markdown(f'<div class="quote-text">"{content}"</div>', 
                   unsafe_allow_html=True)    # Quote text ko styled div me display karta hai
        
        # Author display
        st.markdown(f'<div class="author">— {author}</div>', 
                   unsafe_allow_html=True)    # Author name ko styled div me display karta hai
        
        # Tags display
        if "tags" in st.session_state.quote and st.session_state.quote["tags"]:    # Agar quote me tags hain
            tags = st.session_state.quote["tags"]    # Original tags get karta hai
            if st.session_state.selected_language != 'en':    # Agar English ke alawa koi language hai
                tags = [translate_text(tag, st.session_state.selected_language) for tag in tags]    # Har tag ko translate karta hai
            st.markdown(f'<div class="category">{", ".join(tags)}</div>', 
                       unsafe_allow_html=True)    # Tags ko comma separated list me display karta hai
    
    # ---------- ACTION BUTTONS ----------
    # Single Copy Quote button
    if st.button("Copy Quote 📋"):    # Copy button create karta hai
        copy_quote(    # Copy function ko call karta hai
            content,    # Current quote text
            author,     # Current author name
            st.session_state.quote.get("tags", [])    # Tags, agar available hain to
        )
    
    # Share section with social media buttons
    share_text = f'"{content}" - {author}'    # Share karne ke liye text format karta hai
    st.markdown("<p style='color: var(--text-secondary); margin-bottom: 5px;'>Share Quote:</p>", unsafe_allow_html=True)
    
    # Social Media Share Buttons in a single row with minimal gaps
    st.markdown(f'''
        <div class="share-buttons-container">
            <a href="https://wa.me/?text={urllib.parse.quote(share_text)}" target="_blank" style="flex: 1; padding: 10px 15px; border-radius: 5px; background-color: #4CD080; color: #ffffff; font-size: 16px; font-weight: 600; text-align: center; text-decoration: none; display: inline-block; min-width: 120px; text-shadow: none;">WhatsApp</a>
            <a href="https://telegram.me/share/url?url={urllib.parse.quote(share_text)}" target="_blank" style="flex: 1; padding: 10px 15px; border-radius: 5px; background-color: #0088cc; color: #ffffff; font-size: 16px; font-weight: 600; text-align: center; text-decoration: none; display: inline-block; min-width: 120px; text-shadow: none;">Telegram</a>
            <a href="https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}" target="_blank" style="flex: 1; padding: 10px 15px; border-radius: 5px; background-color: #1DA1F2; color: #ffffff; font-size: 16px; font-weight: 600; text-align: center; text-decoration: none; display: inline-block; min-width: 120px; text-shadow: none;">Twitter</a>
        </div>
    ''', unsafe_allow_html=True)

else:    # Agar quote fetch nahi ho paya
    st.warning("Unable to fetch quote. Please try again.")    # Warning message dikhata hai

# ---------- FOOTER ----------
st.markdown("---")    # Horizontal line add karta hai
st.markdown("Made by [@muhammadhamza718](https://github.com/muhammadhamza718)")    # Footer text with GitHub link 
import streamlit as st
import requests
import json
import pyperclip
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from deep_translator import GoogleTranslator

# Disable SSL verification warnings
urllib3.disable_warnings()

# Page configuration
st.set_page_config(
    page_title="Random Quote Generator",
    page_icon="💭",
    layout="centered"
)

# Custom CSS with theme support
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
        
        a {
            color: var(--accent-color) !important;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
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
    """Fetch available tags from the API"""
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

def get_quote(tags=None, min_length=None, max_length=None):
    """Fetch a random quote from the Quotable API with filters"""
    try:
        params = {"limit": 1}
        if tags:
            params["tags"] = ",".join(tags)
        if min_length:
            params["minLength"] = min_length
        if max_length:
            params["maxLength"] = max_length
            
        response = requests.get(
            "https://api.quotable.io/quotes/random",
            verify=False,
            params=params
        )
        
        if response.status_code == 200:
            quotes = response.json()
            if not quotes:  # If empty list returned
                st.warning("No quotes found with the selected filters. Try different filters.")
                return None
            return quotes[0]
        else:
            st.error(f"Error: API returned status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching quote: {str(e)}")
        return None

def copy_quote(quote_text, author, tags=None):
    """Copy the quote and author to clipboard"""
    full_quote = f'"{quote_text}" - {author}'
    if tags:
        full_quote += f'\nCategories: {", ".join(tags)}'
    pyperclip.copy(full_quote)
    st.toast("Quote copied to clipboard! ✨")

def translate_text(text, dest_language):
    """Translate text to the specified language"""
    try:
        if dest_language == 'en':
            return text
        translator = GoogleTranslator(source='auto', target=dest_language)
        return translator.translate(text) or text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Initialize session state
if 'tags' not in st.session_state:
    st.session_state.tags = get_available_tags()
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'en'
if 'translated_quote' not in st.session_state:
    st.session_state.translated_quote = None

# Filters section
with st.expander("Quote Filters 🔍", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_tag = st.selectbox(
            "Select Category",
            options=["All"] + st.session_state.tags,
            help="Choose a category to filter quotes"
        )
    
    with col2:
        length_range = st.slider(
            "Quote Length",
            min_value=0,
            max_value=300,
            value=(0, 300),
            help="Filter quotes by character length"
        )
    
    with col3:
        # Language selector
        languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        # Convert to title case and create a new dictionary
        languages_dict = {k.title(): v for k, v in languages_dict.items()}
        language_names = list(languages_dict.keys())
        # Find the index of English (it might be 'english' in the original list)
        english_index = 0  # default to first item if not found
        for i, lang in enumerate(language_names):
            if lang.lower() == 'english':
                english_index = i
                break
                
        selected_language = st.selectbox(
            "Select Language",
            options=language_names,
            index=english_index,
            help="Choose the language for the quote"
        )
        st.session_state.selected_language = languages_dict[selected_language]

# Generate Quote button
if st.button("Generate New Quote 🎲"):
    min_length = length_range[0] if length_range[0] > 0 else None
    max_length = length_range[1] if length_range[1] < 300 else None
    selected_tags = [selected_tag] if selected_tag != "All" else None
    st.session_state.quote = get_quote(
        tags=selected_tags,
        min_length=min_length,
        max_length=max_length
    )
    st.session_state.translated_quote = None

# Initialize first quote if needed
if 'quote' not in st.session_state:
    st.session_state.quote = get_quote()

# Display quote if available
if st.session_state.quote:
    quote_container = st.container()
    with quote_container:
        # Get or create translated quote
        if (st.session_state.selected_language != 'en' and 
            (st.session_state.translated_quote is None or 
             st.session_state.translated_quote.get('lang') != st.session_state.selected_language)):
            
            translated_content = translate_text(
                st.session_state.quote["content"],
                st.session_state.selected_language
            )
            translated_author = translate_text(
                st.session_state.quote["author"],
                st.session_state.selected_language
            )
            st.session_state.translated_quote = {
                'content': translated_content,
                'author': translated_author,
                'lang': st.session_state.selected_language
            }
        
        # Display original or translated quote
        if st.session_state.selected_language == 'en' or st.session_state.translated_quote is None:
            content = st.session_state.quote["content"]
            author = st.session_state.quote["author"]
        else:
            content = st.session_state.translated_quote["content"]
            author = st.session_state.translated_quote["author"]
        
        st.markdown(f'<div class="quote-text">"{content}"</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="author">— {author}</div>', 
                   unsafe_allow_html=True)
        if "tags" in st.session_state.quote and st.session_state.quote["tags"]:
            tags = st.session_state.quote["tags"]
            if st.session_state.selected_language != 'en':
                tags = [translate_text(tag, st.session_state.selected_language) for tag in tags]
            st.markdown(f'<div class="category">{", ".join(tags)}</div>', 
                       unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Copy Quote 📋"):
            copy_quote(
                content,
                author,
                st.session_state.quote.get("tags", [])
            )
    
    with col2:
        if st.button("Share Quote 🔗"):
            share_text = f'"{content}" - {author}'
            st.toast("Share link copied to clipboard! 🔗")
            pyperclip.copy(share_text)

else:
    st.warning("Unable to fetch quote. Please try again.")

# Footer
st.markdown("---")
st.markdown("Made by [@muhammadhamza718](https://github.com/muhammadhamza718)") 
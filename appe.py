# -*- coding: utf-8 -*-
"""Untitled25.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1psKb6Cb2ZCH0Es_wuq8bu41Y6tzEGV2P
"""

import streamlit as st
import json
from collections import defaultdict
import google.generativeai as genai
from datetime import datetime

# Initialize session state
if 'selected_emojis' not in st.session_state:
    st.session_state.selected_emojis = []
if 'stories' not in st.session_state:
    st.session_state.stories = []
if 'votes' not in st.session_state:
    st.session_state.votes = defaultdict(int)

# Configure Google Gemini API (Move inside function to prevent context errors)
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Initialize Gemini Model
@st.cache_resource
def get_gemini_model():
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-pro')

model = get_gemini_model()

# Function to clear emoji selection
def clear_selection():
    st.session_state.selected_emojis = []

# Function to generate story from emojis
@st.cache_data
def generate_story_from_emojis(emoji_sequence):
    """Generate a humorous story from selected emojis."""
    try:
        prompt = f"""Create a short, dark humorous story (3-4 sentences) based on these emojis: {emoji_sequence}.
        The story should have:
        - Dark humor with unexpected twists.
        - Ironic or satirical elements.
        - Clever wordplay or double meanings.
        - A surprising way to connect all emojis.
        - No explicit content (keep it tasteful).

        Example (for 🐶🔥🚗➡️):
        'A dog, tired of chasing cars, decided to become one by stealing a firefighter’s truck. Turns out, being a terrible driver runs in the species.'

        Example (for 🐱📱💻😭):
        'A cat learned to code and hacked its owner's phone to delete all dating apps. "If I can't have a social life," thought the owner through tears, "at least my cat is becoming a successful tech entrepreneur."'

        Make it clever and unexpected!
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating story: {str(e)}"

# Function to add story to session state
def add_story(emoji_sequence, story_text):
    st.session_state.stories.append({
        'emojis': emoji_sequence,
        'story': story_text,
        'votes': 0,
        'timestamp': datetime.now().isoformat()
    })

# UI Header
st.title("🎭 Dark Emoji Storyteller")
st.write("Create darkly humorous tales with emojis! Select emojis and let’s generate a story with a twist.")

# Sample emoji categories (keeping it short for example)
EMOJI_DATA = {
    "Faces & Emotions": ["😀", "😂", "🥲", "😇", "😈", "🤯"],
    "Animals": ["🐶", "🐱", "🐍", "🦄", "🐸", "🐒"],
    "Food": ["🍎", "🍕", "🍔", "🍩", "🍉", "🥑"],
}

# Display emoji categories
tabs = st.tabs(list(EMOJI_DATA.keys()))
for tab, (category, emojis) in zip(tabs, EMOJI_DATA.items()):
    with tab:
        cols = st.columns(6)  # Arrange in 6 columns
        for i, emoji in enumerate(emojis):
            if cols[i % 6].button(emoji, key=f"{category}_{emoji}"):
                st.session_state.selected_emojis.append(emoji)

# Show selected emojis
st.subheader("Selected Emojis")
st.write(" ".join(st.session_state.selected_emojis) if st.session_state.selected_emojis else "No emojis selected!")

# Buttons for actions
col1, col2 = st.columns(2)
with col1:
    if st.button("Clear Selection"):
        clear_selection()
with col2:
    if st.button("Generate Story"):
        if st.session_state.selected_emojis:
            with st.spinner("Crafting your darkly humorous tale..."):
                emoji_sequence = "".join(st.session_state.selected_emojis)
                story = generate_story_from_emojis(emoji_sequence)
                add_story(emoji_sequence, story)
                clear_selection()
        else:
            st.warning("Please select some emojis first!")

# Display generated stories
st.subheader("Generated Stories")
if st.session_state.stories:
    sorted_stories = sorted(st.session_state.stories, key=lambda x: (-x['votes'], x['timestamp']))

    for idx, story in enumerate(sorted_stories):
        with st.container():
            st.markdown(f"**Emojis:** {story['emojis']}")
            st.write(f"**Story:** {story['story']}")
            col1, col2 = st.columns([1, 8])
            with col1:
                if st.button("⬆️ Upvote", key=f"vote_{idx}"):
                    story['votes'] += 1
            with col2:
                st.write(f"Votes: {story['votes']}")
            st.markdown("---")
else:
    st.write("No stories generated yet! Be the first to create one.")
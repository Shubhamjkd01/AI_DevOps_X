import os

with open('dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect markers
# We want to replace lines from `st.markdown("""\n<style>\ndiv[data-testid="stRadio"]` up to `if nav_page == ...:`
# and remove `elif nav_page == ...` lines, dedenting their contents back by 4 spaces.

radio_start_marker = 'st.markdown("""\n<style>\ndiv[data-testid="stRadio"]'
radio_end_marker = 'if nav_page == "⚡ Live Self-Healing Engine":\n'

pre_radio = code.split(radio_start_marker)[0]
post_radio = code.split(radio_end_marker)[1]

# In post_radio:
# We have:
# hero section (indented by 4 spaces)
# elif nav_page == "📖 Documentation & Laptop Setup Guide":
# docs section (indented by 4 spaces)
# elif nav_page == "🛡️ Data & Code Security Guarantee":
# security section (indented by 4 spaces)
# elif nav_page == "👨‍💻 About Developer":
# about section (indented by 4 spaces)

m_docs = 'elif nav_page == "📖 Documentation & Laptop Setup Guide":\n'
m_sec = 'elif nav_page == "🛡️ Data & Code Security Guarantee":\n'
m_about = 'elif nav_page == "👨‍💻 About Developer":\n'

part_hero = post_radio.split(m_docs)[0]
rest_after_hero = post_radio.split(m_docs)[1]

part_docs = rest_after_hero.split(m_sec)[0]
rest_after_docs = rest_after_hero.split(m_sec)[1]

part_sec = rest_after_docs.split(m_about)[0]
part_about = rest_after_docs.split(m_about)[1]

def dedent_block(text, spaces=4):
    lines = text.split("\n")
    dedented = []
    prefix = " " * spaces
    for line in lines:
        if line.startswith(prefix):
            dedented.append(line[spaces:])
        else:
            dedented.append(line)
    return "\n".join(dedented)

# Also ensure html { scroll-behavior: smooth; } is present in pre_radio CSS
if "scroll-behavior: smooth;" not in pre_radio:
    pre_radio = pre_radio.replace("html, body, [class*=\"css\"] {", "html { scroll-behavior: smooth; }\nhtml, body, [class*=\"css\"] {")

final_code = (
    pre_radio.rstrip() + "\n\n" +
    "# ==========================================\n" +
    "# 1. HERO & REAL-TIME ENGINE SECTION\n" +
    "# ==========================================\n" +
    dedent_block(part_hero).strip() + "\n\n" +
    dedent_block(part_docs).strip() + "\n\n" +
    dedent_block(part_sec).strip() + "\n\n" +
    dedent_block(part_about).strip() + "\n"
)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(final_code)

print("SUCCESS: Unified into ONE single top navbar with smooth scrolling!")

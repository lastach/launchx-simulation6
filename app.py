import streamlit as st
import random
import math

# =============================================================================
# Page Config
# =============================================================================
st.set_page_config(
    page_title="The Fundraise Simulation",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# =============================================================================
# Custom CSS: Light theme, purple/indigo accents
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #6C3CE1;
    --primary-light: #8B5CF6;
    --primary-bg: #F3F0FF;
    --accent-green: #10B981;
    --accent-amber: #F59E0B;
    --accent-red: #EF4444;
    --accent-blue: #3B82F6;
    --text-dark: #1E1B4B;
    --text-mid: #4B5563;
    --text-light: #9CA3AF;
    --card-bg: #FFFFFF;
    --page-bg: #FAFAFA;
    --border: #E5E7EB;
}

.stApp {
    background-color: var(--page-bg);
    font-family: 'Inter', sans-serif;
}

.sim-header {
    background: linear-gradient(135deg, #6C3CE1 0%, #4F46E5 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    text-align: center;
}
.sim-header h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    color: white;
}
.sim-header p {
    font-size: 1.05rem;
    opacity: 0.9;
    margin: 0;
}

.phase-badge {
    display: inline-block;
    background: var(--primary-bg);
    color: var(--primary);
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 0.8rem;
    letter-spacing: 0.03em;
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.card-highlight {
    border-left: 4px solid var(--primary);
}

.investor-card {
    background: var(--card-bg);
    border: 2px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.investor-card:hover {
    border-color: var(--primary-light);
}
.investor-card h3 {
    color: var(--text-dark);
    margin: 0 0 0.3rem 0;
}
.investor-card .subtitle {
    color: var(--text-light);
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
}

.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.metric-box {
    flex: 1;
    min-width: 120px;
    background: var(--primary-bg);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-box .value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--primary);
}
.metric-box .label {
    font-size: 0.8rem;
    color: var(--text-mid);
    margin-top: 0.2rem;
}

.progress-bar-container {
    background: #E5E7EB;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 0.3rem 0;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.4s ease;
}

.score-badge {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.85rem;
}
.score-high { background: #D1FAE5; color: #065F46; }
.score-mid { background: #FEF3C7; color: #92400E; }
.score-low { background: #FEE2E2; color: #991B1B; }

.term-option {
    background: var(--card-bg);
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
}
.term-option:hover {
    border-color: var(--primary-light);
    box-shadow: 0 2px 8px rgba(108, 60, 225, 0.1);
}

.token-display {
    background: linear-gradient(135deg, #6C3CE1 0%, #4F46E5 100%);
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-weight: 700;
    display: inline-block;
    font-size: 1.1rem;
}

.qa-question {
    background: #FEF3C7;
    border-left: 4px solid #F59E0B;
    padding: 1rem 1.2rem;
    border-radius: 0 10px 10px 0;
    margin: 1rem 0;
    font-style: italic;
}

.qa-good { background: #D1FAE5; border-left-color: #10B981; }
.qa-weak { background: #FEE2E2; border-left-color: #EF4444; }

.final-score {
    background: linear-gradient(135deg, #6C3CE1 0%, #4F46E5 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 16px;
    text-align: center;
    margin: 1rem 0;
}
.final-score .big-number {
    font-size: 3.5rem;
    font-weight: 800;
}
.final-score .subtitle {
    opacity: 0.85;
    font-size: 1rem;
}

.cta-section {
    background: var(--primary-bg);
    border: 2px solid var(--primary);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Session State
# =============================================================================
def init_state():
    defaults = {
        "stage": "intro",
        # Startup selection
        "startup_key": None,
        # Pitch prep: allocation of 20 prep hours
        "prep_hours_total": 20,
        "prep_alloc": {"problem_market": 0, "product_traction": 0, "business_model": 0, "team_story": 0, "financials_ask": 0},
        # Confidence self-assessment
        "confidence": {"problem_market": 5, "product_traction": 5, "business_model": 5, "team_story": 5, "financials_ask": 5},
        # Investor meetings
        "current_investor": 0,
        "investor_scores": [],
        "qa_history": [],
        "meeting_choices": {},
        # Term sheets
        "offers": [],
        "chosen_offer": None,
        "negotiation_choices": {},
        # Results
        "results": None,
        # Email capture
        "email": "",
        "name": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()ns, raise amount, and use of funds",
        "low_risk": "You state the ask but projections feel like guesses and use of funds is vague.",
        "high_prep": "You present bottom-up projections, clear milestones for the raise, and specific use of every dollar.",
    },
}

# =============================================================================
# Investor Archetypes
# =============================================================================
INVESTORS = [
    {
        "name": "Maya Blackwell",
        "type": "Angel Investor",
        "icon": "👼",
        "style": "Former founder, invests based on people and passion",
        "priorities": {"team_story": 0.35, "problem_market": 0.25, "product_traction": 0.20, "business_model": 0.10, "financials_ask": 0.10},
        "personality": "warm but probing",
        "tough_area": "team_story",
        "questions": {
            "team_story": [
                "Tell me about a time your co-founder and you deeply disagreed. How did you resolve it?",
                "What happens to this company if you get hit by a bus tomorrow?",
                "Why are YOU the person to solve this? What is it about your lived experience?",
            ],
            "problem_market": [
                "Who is your most passionate user and what would they say about you right now?",
                "How did you personally discover this problem?",
            ],
            "product_traction": [
                "What is the one metric that keeps you up at night?",
                "What would make you shut this down and walk away?",
            ],
            "business_model": [
                "How do you think about pricing as you scale?",
            ],
            "financials_ask": [
                "What is your plan if this round takes 6 months instead of 6 weeks?",
            ],
        },
        "offer_base": {"valuation": 3.5, "equity": 8, "board_seat": False, "pro_rata": True, "special": "Hands-on mentorship, intro to 20+ founders in network"},
    },
    {
        "name": "David Chen, Vertex Ventures",
        "type": "Institutional VC (Seed Fund)",
        "icon": "🏢",
        "style": "Data-driven, focused on market size and scalable traction",
        "priorities": {"problem_market": 0.30, "product_traction": 0.30, "business_model": 0.20, "financials_ask": 0.15, "team_story": 0.05},
        "personality": "analytical and fast-paced",
        "tough_area": "product_traction",
        "questions": {
            "product_traction": [
                "Walk me through your cohort retention. What does month-3 look like?",
                "What is your current growth rate and what is driving it organically vs. paid?",
                "If I gave you $100K tomorrow just for growth, where would you spend it?",
            ],
            "problem_market": [
                "Why is this a $100M+ revenue opportunity and not a nice lifestyle business?",
                "Who are the top 3 competitors and why will you win?",
            ],
            "business_model": [
                "What are your unit economics today and where do they need to be at Series A?",
                "What is your LTV to CAC ratio?",
            ],
            "financials_ask": [
                "Walk me through your use of funds line by line.",
                "What milestones will this round help you hit before your next raise?",
            ],
            "team_story": [
                "What key hire do you make first with this capital?",
            ],
        },
        "offer_base": {"valuation": 4.5, "equity": 15, "board_seat": True, "pro_rata": True, "special": "Follow-on reserved for Series A, portfolio network of 40 companies"},
    },
    {
        "name": "Priya Anand, ClimateTech Partners",
        "type": "Strategic Investor",
        "icon": "🌍",
        "style": "Mission-aligned, focused on product depth and strategic fit",
        "priorities": {"product_traction": 0.25, "business_model": 0.25, "problem_market": 0.25, "team_story": 0.15, "financials_ask": 0.10},
        "personality": "thoughtful and detail-oriented",
        "tough_area": "business_model",
        "questions": {
            "business_model": [
                "How does your business model create incentives for sustainable behavior, not just profit?",
                "What happens to your margins if your biggest supplier raises prices 30%?",
                "Can you walk me through a scenario where this business is profitable but not impactful?",
            ],
            "product_traction": [
                "What is the hardest technical problem you have solved so far?",
                "How do you measure impact beyond revenue?",
            ],
            "problem_market": [
                "How does climate regulation risk affect your market opportunity?",
                "Who are the incumbents and what is their likely response to you?",
            ],
            "team_story": [
                "What domain expertise does your team have that outsiders can not replicate?",
            ],
            "financials_ask": [
                "How does your cap table look today and what does it look like post-round?",
            ],
        },
        "offer_base": {"valuation": 3.5, "equity": 12, "board_seat": True, "pro_rata": True, "special": "Distribution partnership, access to pilot sites, industry credibility"},
    },
]

# =============================================================================
# Q&A Response Options
# =============================================================================
def generate_qa_options(area, prep_level, investor_idx):
    """Generate 3 response options for a Q&A question based on prep level."""
    # Response quality depends on prep allocation
    options = {
        "problem_market": {
            "strong": "Reference specific customer research, cite TAM/SAM with sources, and connect to a clear wedge strategy.",
            "medium": "Share the general market opportunity and mention a few customer conversations you have had.",
            "weak": "Acknowledge it is a big market and promise to follow up with more detailed research.",
        },
        "product_traction": {
            "strong": "Pull up your metrics dashboard, walk through cohort data, and highlight the inflection point in your growth curve.",
            "medium": "Share top-line growth numbers and mention that retention has been improving month over month.",
            "weak": "Talk about how excited users are and mention you are working on better analytics.",
        },
        "business_model": {
            "strong": "Present a unit economics breakdown showing current vs. target margins, with clear assumptions and sensitivity analysis.",
            "medium": "Describe your pricing model and share rough estimates of customer acquisition cost and lifetime value.",
            "weak": "Explain your revenue model at a high level and note that you plan to optimize pricing over time.",
        },
        "team_story": {
            "strong": "Tell a genuine founder story that connects your unique background to this problem, including a vulnerable moment that shaped your conviction.",
            "medium": "Highlight your relevant experience and explain why you care about this problem personally.",
            "weak": "List your professional backgrounds and mention you are committed to making this work.",
        },
        "financials_ask": {
            "strong": "Walk through a bottom-up financial model showing monthly projections, key hiring milestones, and exactly how every dollar of the raise maps to specific outcomes.",
            "medium": "Share your burn rate, runway expectations, and a general allocation of the raise across hiring, product, and growth.",
            "weak": "State your fundraising target and mention you will use it for team growth and product development.",
        },
    }

    area_options = options.get(area, options["problem_market"])

    # If prep is high enough, all 3 options are available
    # If prep is low, the "strong" option is locked
    available = []
    if prep_level >= 4:
        available.append({"text": area_options["strong"], "quality": "strong", "points": 3})
    available.append({"text": area_options["medium"], "quality": "medium", "points": 2})
    available.append({"text": area_options["weak"], "quality": "weak", "points": 1})

    return available


# =============================================================================
# Scoring Helpers
# =============================================================================
def calc_prep_score(area):
    """Score 0-10 based on prep allocation."""
    alloc = st.session_state.prep_alloc.get(area, 0)
    # 0 hours -> 2, 2 hours -> 5, 4 hours -> 8, 6+ hours -> 9-10
    # Slightly more generous so balanced prep feels rewarding
    return min(10, max(2, round(alloc * 1.5 + 2)))

def calc_meeting_score(investor_idx):
    """Calculate overall meeting score for an investor."""
    investor = INVESTORS[investor_idx]
    total = 0
    for area, weight in investor["priorities"].items():
        prep_score = calc_prep_score(area)
        qa_bonus = 0
        key = f"qa_{investor_idx}_{area}"
        if key in st.session_state.meeting_choices:
            qa_bonus = st.session_state.meeting_choices[key]
        # Prep weighted more heavily (60%) since it represents real preparation
        area_score = prep_score * 0.6 + qa_bonus * 10 * 0.4
        total += area_score * weight
    return round(total, 1)

def score_badge(score, max_score=10):
    ratio = score / max_score
    if ratio >= 0.7:
        return "score-high"
    elif ratio >= 0.4:
        return "score-mid"
    return "score-low"


# =============================================================================
# Progress Tracker
# ====================================================================================
def render_progress_bar():
    """Show a visual progress tracker across the top of every stage."""
    stage = st.session_state.stage
    stages_order = ["intro", "choose_startup", "pitch_prep", "investor_meeting", "term_sheets", "negotiation", "email_capture", "results"]
    stage_labels = ["Start", "Pick Startup", "Pitch Prep", "Investor Meetings", "Term Sheets", "Negotiate", "Almost There", "Results"]

    current_idx = stages_order.index(stage) if stage in stages_order else 0
    total = len(stages_order) - 1
    pct = int((current_idx / total) * 100)

    if stage not in ("intro", "results"):
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9CA3AF; margin-bottom: 0.3rem;">
                <span>{stage_labels[current_idx]}</span>
                <span>{pct}% complete</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {pct}%; background: linear-gradient(90deg, #6C3CE1, #8B5CF6);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# STAGES
# =============================================================================

def render_intro():
    st.markdown("""
    <div class="sim-header">
        <h1>💰 The Fundraise</h1>
        <p>Pitch investors, handle tough questions, and negotiate your seed round</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-highlight">
        <h3 style="color: #1E1B4B; margin-top: 0;">Your Mission</h3>
        <p style="color: #4B5563; font-size: 1.05rem;">
            You have spent months validating your problem, running experiments, and building traction.
            Now it is time to raise your seed round. You will prepare your pitch, meet three very different
            investors, handle their toughest questions, and decide which term sheet to accept.
        </p>
        <p style="color: #4B5563; font-size: 1.05rem;">
            Every choice has trade-offs. There is no perfect pitch and no perfect deal. The goal is to
            learn how fundraising really works and discover your natural strengths and blind spots.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-row">
        <div class="metric-box">
            <div class="value">⏱️</div>
            <div class="label">~20-25 minutes</div>
        </div>
        <div class="metric-box">
            <div class="value">1</div>
            <div class="label">Pitch Prep</div>
        </div>
        <div class="metric-box">
            <div class="value">2</div>
            <div class="label">Investor Meetings</div>
        </div>
        <div class="metric-box">
            <div class="value">3</div>
            <div class="label">Term Sheet Negotiation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start the Simulation →", type="primary", use_container_width=True):
        st.session_state.stage = "choose_startup"
        st.rerun()


def render_choose_startup():
    st.markdown('<div class="phase-badge">PHASE 0</div>', unsafe_allow_html=True)
    st.markdown("### Choose Your Startup")
    st.markdown("Each company has validated its problem and built early traction. Pick the one you want to take into fundraising.")

    cols = st.columns(3)
    for i, (key, s) in enumerate(STARTUPS.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="investor-card">
                <h3>{s['icon']} {s['name']}</h3>
                <div class="subtitle">{s['tagline']}</div>
                <p style="font-size: 0.85rem; color: #4B5563;">
                    <strong>Stage:</strong> {s['stage']}<br>
                    <strong>Traction:</strong> {s['traction']}<br>
                    <strong>Team:</strong> {s['team']}<br>
                    <strong>Raising:</strong> {s['ask']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Choose {s['name']}", key=f"choose_{key}", use_container_width=True):
                st.session_state.startup_key = key
                st.session_state.stage = "pitch_prep"
                st.rerun()


def render_pitch_prep():
    startup = STARTUPS[st.session_state.startup_key]
    st.markdown('<div class="phase-badge">PHASE 1: PITCH PREP</div>', unsafe_allow_html=True)
    st.markdown(f"### Preparing the {startup['name']} Pitch")

    spent = sum(st.session_state.prep_alloc.values())
    remaining = st.session_state.prep_hours_total - spent

    st.markdown(f"""
    <div class="card card-highlight">
        <p style="color: #4B5563; margin: 0 0 0.5rem 0;">
            You have <span class="token-display">{remaining} prep hours</span> remaining out of {st.session_state.prep_hours_total}.
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Allocate hours across your five pitch areas. More hours means stronger answers when investors probe that area.
            You can not prepare everything equally, so choose wisely.
        </p>
    </div>
    """, unsafe_allow_html=True)

    for area_key, area_info in PREP_AREAS.items():
        current = st.session_state.prep_alloc[area_key]
        col1, col2 = st.columns([3, 1])
        with col1:
            new_val = st.slider(
                f"{area_info['icon']} {area_info['label']}",
                min_value=0,
                max_value=min(8, current + remaining),
                value=current,
                key=f"slider_{area_key}",
                help=area_info["desc"],
            )
            st.session_state.prep_alloc[area_key] = new_val
        with col2:
            prep_score = calc_prep_score(area_key)
            badge_class = score_badge(prep_score)
            st.markdown(f'<div style="padding-top: 2rem;"><span class="score-badge {badge_class}">Readiness: {prep_score}/10</span></div>', unsafe_allow_html=True)

    # Recalculate remaining after slider changes
    spent = sum(st.session_state.prep_alloc.values())
    remaining = st.session_state.prep_hours_total - spent

    if remaining < 0:
        st.error("You have allocated more hours than available. Adjust your sliders.")
    else:
        st.markdown("---")
        st.markdown("#### Quick self-check: How confident do you feel in each area?")
        st.markdown("*Rate your confidence before the meetings. We will compare this to your actual performance afterward.*")
        areas_list = list(PREP_AREAS.items())
        # Row 1: first 3
        conf_cols1 = st.columns(3)
        for i in range(3):
            area_key, area_info = areas_list[i]
            with conf_cols1[i]:
                st.session_state.confidence[area_key] = st.slider(
                    f"{area_info['icon']} {area_info['label']}",
                    1, 10,
                    st.session_state.confidence[area_key],
                    key=f"conf_{area_key}",
                )
        # Row 2: last 2
        conf_cols2 = st.columns(3)
        for i in range(3, 5):
            area_key, area_info = areas_list[i]
            with conf_cols2[i - 3]:
                st.session_state.confidence[area_key] = st.slider(
                    f"{area_info['icon']} {area_info['label']}",
                    1, 10,
                    st.session_state.confidence[area_key],
                    key=f"conf_{area_key}",
                )

        if st.button("Lock in Prep & Meet Investors →", type="primary", use_container_width=True, disabled=remaining < 0):
            st.session_state.stage = "investor_meeting"
            st.session_state.current_investor = 0
            st.rerun()


def render_investor_meeting():
    idx = st.session_state.current_investor
    if idx >= len(INVESTORS):
        st.session_state.stage = "term_sheets"
        st.rerun()
        return

    investor = INVESTORS[idx]
    startup = STARTUPS[st.session_state.startup_key]

    st.markdown(f'<div class="phase-badge">PHASE 2: INVESTOR MEETING {idx + 1} of {len(INVESTORS)}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-left: 4px solid {'#F59E0B' if idx == 0 else '#3B82F6' if idx == 1 else '#10B981'};">
        <h3 style="color: #1E1B4B; margin-top: 0;">{investor['icon']} {investor['name']}</h3>
        <div style="color: #6B7280; font-size: 0.95rem; margin-bottom: 0.5rem;">{investor['type']}</div>
        <p style="color: #4B5563;">{investor['style']}</p>
        <p style="color: #6B7280; font-size: 0.85rem;">Personality: {investor['personality'].capitalize()}</p>
    </div>
    """, unsafe_allow_html=True)

    # Show what this investor cares about
    st.markdown("**What this investor prioritizes:**")
    priority_cols = st.columns(5)
    sorted_priorities = sorted(investor["priorities"].items(), key=lambda x: x[1], reverse=True)
    for i, (area, weight) in enumerate(sorted_priorities):
        with priority_cols[i]:
            pct = int(weight * 100)
            area_info = PREP_AREAS[area]
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 1.3rem;">{area_info['icon']}</div>
                <div style="font-size: 0.75rem; color: #6B7280;">{area_info['label']}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: {pct}%; background: {'#6C3CE1' if pct >= 25 else '#A78BFA'};"></div>
                </div>
                <div style="font-size: 0.75rem; color: #9CA3AF;">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Q&A Section: ask 2 questions from this investor
    tough_area = investor["tough_area"]
    questions_for_tough = investor["questions"][tough_area]
    # Pick a secondary area
    other_areas = [a for a in investor["questions"] if a != tough_area and len(investor["questions"][a]) > 0]
    secondary_area = random.Random(idx + 42).choice(other_areas) if other_areas else tough_area
    secondary_questions = investor["questions"][secondary_area]

    q1 = random.Random(idx + 100).choice(questions_for_tough)
    q2 = random.Random(idx + 200).choice(secondary_questions)

    st.markdown("### The Tough Questions")
    st.markdown(f"*{investor['name'].split(',')[0]} leans forward...*")

    # Question 1
    st.markdown(f"""
    <div class="qa-question">
        "{q1}"
    </div>
    """, unsafe_allow_html=True)

    prep_level_1 = st.session_state.prep_alloc.get(tough_area, 0)
    options_1 = generate_qa_options(tough_area, prep_level_1, idx)

    key1 = f"qa_{idx}_{tough_area}"
    choice_labels_1 = [opt["text"] for opt in options_1]
    selected_1 = st.radio(
        "Your response:",
        choice_labels_1,
        key=f"radio_q1_{idx}",
        index=None,
    )

    # Question 2
    st.markdown(f"""
    <div class="qa-question">
        "{q2}"
    </div>
    """, unsafe_allow_html=True)

    prep_level_2 = st.session_state.prep_alloc.get(secondary_area, 0)
    options_2 = generate_qa_options(secondary_area, prep_level_2, idx)

    key2 = f"qa_{idx}_{secondary_area}"
    choice_labels_2 = [opt["text"] for opt in options_2]
    selected_2 = st.radio(
        "Your response:",
        choice_labels_2,
        key=f"radio_q2_{idx}",
        index=None,
    )

    st.markdown("---")

    # Pitch delivery style choice
    st.markdown("### Pitch Delivery Style")
    st.markdown("*How do you approach this meeting overall?*")
    delivery = st.radio(
        "Choose your approach:",
        [
            "Lead with data: Open with your strongest metrics and let the numbers tell the story.",
            "Lead with narrative: Start with a compelling customer story and weave data in naturally.",
            "Lead with vision: Paint the big picture of where this market is going and why you will win.",
        ],
        key=f"delivery_{idx}",
        index=None,
    )

    if st.button(f"{'Next Meeting →' if idx < len(INVESTORS) - 1 else 'Review Offers →'}", type="primary", use_container_width=True):
        # Score this meeting
        q1_score = 0
        q2_score = 0
        if selected_1:
            for opt in options_1:
                if opt["text"] == selected_1:
                    q1_score = opt["points"] / 3.0
        if selected_2:
            for opt in options_2:
                if opt["text"] == selected_2:
                    q2_score = opt["points"] / 3.0

        st.session_state.meeting_choices[key1] = q1_score
        st.session_state.meeting_choices[key2] = q2_score

        # Delivery style bonus
        delivery_bonus = 0
        if delivery:
            if idx == 0 and "narrative" in delivery.lower():
                delivery_bonus = 0.5  # Angel loves stories
            elif idx == 1 and "data" in delivery.lower():
                delivery_bonus = 0.5  # VC loves data
            elif idx == 2 and "vision" in delivery.lower():
                delivery_bonus = 0.5  # Strategic loves vision
            else:
                delivery_bonus = 0.2  # Any deliberate choice is okay

        meeting_score = calc_meeting_score(idx) + delivery_bonus
        st.session_state.investor_scores.append(min(10, meeting_score))

        # Record QA history for debrief
        st.session_state.qa_history.append({
            "investor": investor["name"],
            "q1": q1, "q1_area": tough_area, "q1_score": q1_score,
            "q2": q2, "q2_area": secondary_area, "q2_score": q2_score,
            "delivery": delivery,
            "delivery_bonus": delivery_bonus,
            "total": min(10, meeting_score),
        })

        st.session_state.current_investor = idx + 1
        st.rerun()


def render_term_sheets():
    startup = STARTUPS[st.session_state.startup_key]
    st.markdown('<div class="phase-badge">PHASE 3: THE TERM SHEETS</div>', unsafe_allow_html=True)
    st.markdown("### Compare Your Offers")
    st.markdown("Each investor has extended a term sheet based on how your meeting went. Better meetings unlock better terms.")

    # Generate offers based on meeting scores
    if not st.session_state.offers:
        for idx, investor in enumerate(INVESTORS):
            score = st.session_state.investor_scores[idx] if idx < len(st.session_state.investor_scores) else 5
            base = investor["offer_base"]

            # Score affects valuation and equity
            score_mult = score / 7.0  # normalize around "good" performance
            val = round(base["valuation"] * score_mult, 1)
            val = max(2.0, min(6.0, val))  # clamp

            eq = base["equity"]
            if score >= 7:
                eq = max(eq - 3, 5)  # better score = less dilution
            elif score < 4:
                eq = min(eq + 4, 25)  # worse score = more dilution

            st.session_state.offers.append({
                "investor_name": investor["name"],
                "investor_type": investor["type"],
                "investor_icon": investor["icon"],
                "valuation": val,
                "equity": eq,
                "board_seat": base["board_seat"],
                "pro_rata": base["pro_rata"],
                "special": base["special"],
                "meeting_score": score,
            })

    cols = st.columns(3)
    for i, offer in enumerate(st.session_state.offers):
        with cols[i]:
            badge = score_badge(offer["meeting_score"])
            st.markdown(f"""
            <div class="investor-card">
                <h3>{offer['investor_icon']} {offer['investor_name']}</h3>
                <div class="subtitle">{offer['investor_type']}</div>
                <div style="margin: 0.8rem 0;">
                    <span class="score-badge {badge}">Meeting Score: {offer['meeting_score']:.1f}/10</span>
                </div>
                <table style="width: 100%; font-size: 0.9rem; color: #4B5563;">
                    <tr><td><strong>Valuation</strong></td><td>${offer['valuation']}M pre-money</td></tr>
                    <tr><td><strong>Equity</strong></td><td>{offer['equity']}%</td></tr>
                    <tr><td><strong>Board Seat</strong></td><td>{'Yes' if offer['board_seat'] else 'No'}</td></tr>
                    <tr><td><strong>Pro-rata Rights</strong></td><td>{'Yes' if offer['pro_rata'] else 'No'}</td></tr>
                </table>
                <p style="font-size: 0.85rem; color: #6B7280; margin-top: 0.8rem;">
                    <strong>Strategic Value:</strong> {offer['special']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Accept {offer['investor_name'].split(',')[0]}'s Offer", key=f"accept_{i}", use_container_width=True):
                st.session_state.chosen_offer = i
                st.session_state.stage = "negotiation"
                st.rerun()

    st.markdown("---")

    # Term Sheet Glossary/Decoder
    with st.expander("📋 Term Sheet Decoder - Plain Language Explanations"):
        st.markdown("""
        #### **Pre-Money Valuation**
        This is what the investor thinks your company is worth *before* they invest.

        **Example:** If the valuation is $3M and they're investing $750K, they get 20% of the company.

        **Why it matters:** A higher valuation means less dilution for you and other early shareholders.

        ---

        #### **Equity %**
        The percentage of your company the investor owns after the investment.

        **Example:** If you have 10M shares outstanding and an investor gets 8% equity, they receive 800K shares.

        **Why it matters:** More equity = more dilution. You give up ownership, but you also raise capital.

        ---

        #### **Board Seat**
        The right to have a representative on your company's board of directors.

        **What this means:** The investor gets a vote on major decisions (hiring, budget, strategy, additional fundraising).

        **Why it matters:** Board seats give investors governance power. Good investors mentor; bad ones micromanage.

        ---

        #### **Pro-Rata Rights**
        The right to invest in future rounds to maintain their ownership percentage.

        **Example:** If an investor has 8% and you raise a Series A, they can invest enough to stay at 8%.

        **Why it matters:** Pro-rata rights can be valuable (the investor doubles down on you) or frustrating (prevents new investors).

        ---

        #### **Liquidation Preferences**
        The order investors get paid if your company is sold or fails.

        **Non-participating preferred:** Investors choose either their equity stake OR 1x their investment (whichever is higher), but not both.

        **Participating preferred:** Investors get their money back PLUS their equity stake (more investor-friendly, less founder-friendly).

        **Why it matters:** In a mediocre exit ($5M), 1x liquidation pref may not cover the investor's full stake.

        ---

        #### **Anti-Dilution Protection**
        Protection for investors if you raise at a lower valuation in the future (a "down round").

        **Broad-based weighted average:** If you raise at a lower valuation, the investor's shares are adjusted down slightly.

        **Narrow-based weighted average:** Harsher adjustment; rarely negotiated by founders.

        **Why it matters:** Down rounds happen. Investors want protection; you want to minimize the damage to your cap table.
        """)

    st.markdown("""
    <div class="card">
        <h4 style="color: #1E1B4B; margin-top: 0;">💡 Things to Consider</h4>
        <p style="color: #4B5563; font-size: 0.9rem;">
            Higher valuation means less dilution, but a strategic investor might add more value than a few extra percentage points.
            A board seat gives the investor governance power but also signals commitment.
            Think about what your startup needs most at this stage: money, mentorship, or market access.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_negotiation():
    offer = st.session_state.offers[st.session_state.chosen_offer]
    investor = INVESTORS[st.session_state.chosen_offer]

    st.markdown('<div class="phase-badge">PHASE 3B: NEGOTIATION</div>', unsafe_allow_html=True)
    st.markdown(f"### Negotiating with {offer['investor_name']}")
    st.markdown(f"*You have chosen to move forward with {offer['investor_name']}. Now you can negotiate specific terms.*")

    st.markdown("---")

    # Negotiation Point 1: Valuation
    st.markdown("#### 1. Valuation Counter")
    st.markdown(f"They offered **${offer['valuation']}M pre-money**. Do you counter?")
    val_choice = st.radio(
        "Your move:",
        [
            f"Accept ${offer['valuation']}M as offered. (Safe: maintains goodwill)",
            f"Counter at ${offer['valuation'] + 0.5}M with justification. (Moderate: might improve terms)",
            f"Push hard for ${offer['valuation'] + 1.5}M. (Aggressive: risks the deal)",
        ],
        key="val_negotiate",
        index=None,
    )

    # Negotiation Point 2: Board dynamics
    st.markdown("#### 2. Board Structure")
    if offer["board_seat"]:
        board_choice = st.radio(
            "They want a board seat. Your response:",
            [
                "Accept the board seat. (Shows trust, gives them governance)",
                "Accept board observer seat instead. (Compromise: they attend but can not vote)",
                "Push for no board seat. (Preserves founder control, may offend)",
            ],
            key="board_negotiate",
            index=None,
        )
    else:
        board_choice = st.radio(
            "They are not requesting a board seat. Do you offer one?",
            [
                "Keep things as is. (Simple and founder-friendly)",
                "Offer an advisory role with quarterly check-ins. (Shows maturity)",
                "Proactively offer a board observer seat. (Builds trust and signals openness)",
            ],
            key="board_negotiate",
            index=None,
        )

    # Negotiation Point 3: Key Terms
    st.markdown("#### 3. Special Terms")
    terms_choice = st.radio(
        "What additional term is most important to you?",
        [
            "Anti-dilution protection: Protect your equity in future down rounds.",
            "Information rights: Limit what financial data the investor can share.",
            "Strategic milestone clause: Tie follow-on funding to specific growth targets you choose.",
        ],
        key="terms_negotiate",
        index=None,
    )

    if st.button("Finalize the Deal →", type="primary", use_container_width=True):
        # Score negotiation choices
        neg_score = 0

        if val_choice:
            if "Accept" in val_choice:
                neg_score += 2  # safe
            elif "Counter" in val_choice and "justification" in val_choice:
                neg_score += 3  # best
            else:
                neg_score += 1  # risky

        if board_choice:
            if "observer" in board_choice.lower() or "advisory" in board_choice.lower():
                neg_score += 3  # nuanced
            elif "Accept" in board_choice or "Proactively" in board_choice:
                neg_score += 2  # reasonable
            else:
                neg_score += 1  # aggressive

        if terms_choice:
            if "milestone" in terms_choice.lower():
                neg_score += 3  # strategic
            elif "Anti-dilution" in terms_choice:
                neg_score += 2  # defensive
            else:
                neg_score += 1  # conservative

        st.session_state.negotiation_choices = {
            "val": val_choice,
            "board": board_choice,
            "terms": terms_choice,
            "score": neg_score,
        }

        # Compute final results
        compute_results()
        st.session_state.stage = "email_capture"
        st.rerun()


def compute_results():
    """Aggregate all scores into final results."""
    # Prep effectiveness (how well they allocated)
    prep_scores = {area: calc_prep_score(area) for area in PREP_AREAS}
    avg_prep = sum(prep_scores.values()) / len(prep_scores)

    # Meeting performance
    avg_meeting = sum(st.session_state.investor_scores) / len(st.session_state.investor_scores) if st.session_state.investor_scores else 5

    # Negotiation skill
    neg_score = st.session_state.negotiation_choices.get("score", 5)
    neg_normalized = neg_score / 9.0 * 10  # max is 9

    # Self-awareness gap
    gaps = {}
    for area in PREP_AREAS:
        actual = prep_scores[area]
        confidence = st.session_state.confidence.get(area, 5)
        gaps[area] = abs(confidence - actual)
    avg_gap = sum(gaps.values()) / len(gaps)
    self_awareness = max(0, 10 - avg_gap * 1.5)  # lower gap = higher score

    # Overall
    overall = avg_prep * 0.2 + avg_meeting * 0.35 + neg_normalized * 0.25 + self_awareness * 0.2

    # Deal quality
    chosen = st.session_state.offers[st.session_state.chosen_offer]
    # Higher valuation + lower equity + strategic value = better deal
    deal_score = (chosen["valuation"] / 6.0) * 3 + ((25 - chosen["equity"]) / 20.0) * 4 + 3  # base 3 for strategic value

    st.session_state.results = {
        "prep_scores": prep_scores,
        "avg_prep": avg_prep,
        "meeting_scores": st.session_state.investor_scores,
        "avg_meeting": avg_meeting,
        "neg_score": neg_normalized,
        "self_awareness": self_awareness,
        "confidence_gaps": gaps,
        "overall": overall,
        "deal_score": min(10, deal_score),
        "chosen_offer": st.session_state.offers[st.session_state.chosen_offer],
    }


def render_email_capture():
    render_progress_bar()
    overall = st.session_state.results["overall"]
    grade = "A" if overall >= 8 else "B+" if overall >= 7 else "B" if overall >= 6 else "C+" if overall >= 5 else "C"

    st.markdown(f"""
    <div class="sim-header">
        <h1>🎉 Simulation Complete!</h1>
        <p>Your fundraise grade: <strong>{grade}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-highlight">
        <h3 style="color: #1E1B4B; margin-top: 0;">See Your Full Results</h3>
        <p style="color: #4B5563;">
            Enter your name and email to unlock your detailed performance breakdown,
            personalized insights, and real-world action steps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.name = st.text_input("Your name", value=st.session_state.name, placeholder="First name")
    with col2:
        st.session_state.email = st.text_input("Your email", value=st.session_state.email, placeholder="you@email.com")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("View My Results →", type="primary", use_container_width=True):
            st.session_state.stage = "results"
            st.rerun()
    with col_b:
        if st.button("Skip for now", use_container_width=True):
            st.session_state.stage = "results"
            st.rerun()


def render_results():
    r = st.session_state.results
    startup = STARTUPS[st.session_state.startup_key]

    st.markdown("""
    <div class="sim-header">
        <h1>📊 Your Fundraise Results</h1>
        <p>Here is how you performed across every dimension of the fundraise</p>
    </div>
    """, unsafe_allow_html=True)

    # Overall Score
    overall = r["overall"]
    grade = "A" if overall >= 8 else "B+" if overall >= 7 else "B" if overall >= 6 else "C+" if overall >= 5 else "C" if overall >= 4 else "D"
    st.markdown(f"""
    <div class="final-score">
        <div class="big-number">{overall:.1f}/10</div>
        <div class="subtitle">Overall Fundraise Performance (Grade: {grade})</div>
    </div>
    """, unsafe_allow_html=True)

    # Dimension Scores
    st.markdown("### Performance Breakdown")
    dim_cols = st.columns(4)
    dims = [
        ("🏃 Pitch Prep", r["avg_prep"], "How well you allocated your preparation time"),
        ("🤝 Investor Meetings", r["avg_meeting"], "How you handled Q&A and delivery across all meetings"),
        ("⚖️ Negotiation", r["neg_score"], "How strategically you negotiated terms"),
        ("🧠 Self-Awareness", r["self_awareness"], "How accurately your confidence matched reality"),
    ]
    for i, (label, score, desc) in enumerate(dims):
        with dim_cols[i]:
            badge = score_badge(score)
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #6C3CE1;">{score:.1f}</div>
                <div style="font-weight: 600; color: #1E1B4B; margin: 0.3rem 0;">{label}</div>
                <div style="font-size: 0.8rem; color: #9CA3AF;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Prep Detail
    st.markdown("### Pitch Prep Analysis")
    st.markdown("*How your time allocation translated to readiness:*")
    for area_key, area_info in PREP_AREAS.items():
        prep_s = r["prep_scores"][area_key]
        hours = st.session_state.prep_alloc[area_key]
        conf = st.session_state.confidence[area_key]
        gap = r["confidence_gaps"][area_key]

        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            pct = prep_s * 10
            st.markdown(f"""
            <div style="margin-bottom: 0.3rem;">
                <strong>{area_info['icon']} {area_info['label']}</strong>
                <span style="color: #9CA3AF; font-size: 0.85rem;"> ({hours} hours)</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {pct}%; background: #6C3CE1;"></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            badge = score_badge(prep_s)
            st.markdown(f'<span class="score-badge {badge}">{prep_s}/10</span>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<span style="color: #6B7280; font-size: 0.85rem;">Confidence: {conf}</span>', unsafe_allow_html=True)
        with col4:
            if gap <= 1:
                st.markdown('<span style="color: #10B981; font-size: 0.85rem;">✓ Well calibrated</span>', unsafe_allow_html=True)
            elif conf > prep_s:
                st.markdown(f'<span style="color: #F59E0B; font-size: 0.85rem;">⚠ Overconfident by {gap:.0f} points</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color: #3B82F6; font-size: 0.85rem;">↑ Underconfident by {gap:.0f} points</span>', unsafe_allow_html=True)

    # Meeting Recap
    st.markdown("### Meeting Recaps")
    for i, recap in enumerate(st.session_state.qa_history):
        badge = score_badge(recap["total"])
        delivery_match = "✓ Great style match" if recap["delivery_bonus"] >= 0.5 else "Okay approach"
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #1E1B4B;">{INVESTORS[i]['icon']} {recap['investor']}</h4>
                <span class="score-badge {badge}">{recap['total']:.1f}/10</span>
            </div>
            <p style="color: #6B7280; font-size: 0.85rem; margin-top: 0.5rem;">
                Delivery: {delivery_match} |
                Strongest on: {PREP_AREAS[recap['q1_area']]['label'] if recap['q1_score'] > recap['q2_score'] else PREP_AREAS[recap['q2_area']]['label']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Deal Summary
    st.markdown("### Your Deal")
    chosen = r["chosen_offer"]
    st.markdown(f"""
    <div class="card card-highlight">
        <h4 style="color: #1E1B4B; margin-top: 0;">{chosen['investor_icon']} Deal with {chosen['investor_name']}</h4>
        <div class="metric-row">
            <div class="metric-box">
                <div class="value">${chosen['valuation']}M</div>
                <div class="label">Pre-money Valuation</div>
            </div>
            <div class="metric-box">
                <div class="value">{chosen['equity']}%</div>
                <div class="label">Equity Given</div>
            </div>
            <div class="metric-box">
                <div class="value">{r['deal_score']:.1f}</div>
                <div class="label">Deal Quality Score</div>
            </div>
        </div>
        <p style="color: #4B5563; font-size: 0.9rem;">Strategic value: {chosen['special']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Insights
    st.markdown("### Key Takeaways")

    insights = []
    # Prep balance insight
    prep_vals = list(r["prep_scores"].values())
    if max(prep_vals) - min(prep_vals) >= 6:
        insights.append("⚠️ **Lopsided preparation.** You over-invested in some areas and left others dangerously weak. Real investors notice gaps quickly. Try spreading prep more evenly next time.")
    elif max(prep_vals) - min(prep_vals) <= 2:
        insights.append("📖 **Even preparation.** You spread your time evenly, which means no catastrophic gaps but also no standout area. Sometimes going deep on 2 to 3 areas and accepting weakness elsewhere is more strategic.")
    else:
        insights.append("✅ **Strategic preparation.** You made deliberate trade-offs in how you prepared. That is exactly how real founders operate with limited time.")

    # Self-awareness insight
    if r["self_awareness"] >= 7:
        insights.append("🧠 **Strong self-awareness.** Your confidence closely matched your actual readiness. This is a critical founder skill because it helps you know when to ask for help.")
    elif r["self_awareness"] >= 4:
        insights.append("🧠 **Moderate self-awareness.** Your confidence was sometimes off from reality. Pay attention to where you overestimate yourself; those blind spots can surprise you in real meetings.")
    else:
        insights.append("🧠 **Self-awareness gap detected.** There was a significant mismatch between how confident you felt and how ready you actually were. This is the most important thing to work on because it affects every decision you make.")

    # Negotiation insight
    if r["neg_score"] >= 7:
        insights.append("⚖️ **Skilled negotiator.** You balanced assertiveness with relationship-building. You pushed for better terms without burning bridges.")
    elif r["neg_score"] >= 4:
        insights.append("⚖️ **Safe negotiator.** You made reasonable choices but left value on the table. In real fundraising, the founders who negotiate thoughtfully often end up with 20 to 30% better outcomes.")
    else:
        insights.append("⚖️ **Negotiation opportunity.** You either played it too safe or too aggressive. The best negotiations create value for both sides.")

    for insight in insights:
        st.markdown(insight)

    # Real World Application
    st.markdown("---")
    st.markdown("### Apply This to the Real World")
    st.markdown("""
    <div class="card">
        <p style="color: #4B5563;">Based on your simulation, here are three things to do <strong>this week</strong>:</p>
        <p style="color: #4B5563;"><strong>1. Practice your weakest area.</strong> Look at where you scored lowest in prep. Find a friend and practice answering tough questions on that topic for 10 minutes.</p>
        <p style="color: #4B5563;"><strong>2. Talk to a real investor.</strong> Even if you are not raising yet, having coffee with an angel investor or VC will demystify the process. Ask them what they look for first.</p>
        <p style="color: #4B5563;"><strong>3. Calibrate your confidence.</strong> Before your next big meeting or presentation, write down how confident you feel on each section. Afterward, note where reality diverged. This practice builds the self-awareness muscle.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div class="cta-section">
        <h3 style="color: #1E1B4B; margin-top: 0;">Ready to keep building?</h3>
        <p style="color: #4B5563;">Explore more founder simulations and resources to accelerate your entrepreneurial journey.</p>
        <p style="color: #6C3CE1; font-weight: 600;">[CTA Placeholder: Add specific call to action]</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# =============================================================================
# Main Router
# =============================================================================
stage = st.session_state.stage

if stage == "intro":
    render_intro()
elif stage == "choose_startup":
    render_progress_bar()
    render_choose_startup()
elif stage == "pitch_prep":
    render_progress_bar()
    render_pitch_prep()
elif stage == "investor_meeting":
    render_progress_bar()
    render_investor_meeting()
elif stage == "term_sheets":
    render_progress_bar()
    render_term_sheets()
elif stage == "negotiation":
    render_progress_bar()
    render_negotiation()
elif stage == "email_capture":
    render_email_capture()
elif stage == "results":
    render_results()

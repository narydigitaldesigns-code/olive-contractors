import streamlit as st
import pandas as pd

# Page configuration with dark theme
st.set_page_config(
    page_title="Olive Contractors Cost Estimator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and mobile responsiveness
st.markdown("""
<style>
    /* Dark theme styling */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .company-name {
        font-size: 2.5rem;
        font-weight: bold;
        color: #10B981;
        margin-bottom: 0.5rem;
    }
    
    .company-tagline {
        font-size: 1.2rem;
        color: #9CA3AF;
    }
    
    /* Results section styling */
    .results-container {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .cost-breakdown {
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .final-total {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 6px 12px rgba(5, 150, 105, 0.4);
    }
    
    .final-total h2 {
        color: white;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .final-price {
        font-size: 3rem;
        font-weight: bold;
        color: #D1FAE5;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .company-name {
            font-size: 1.8rem;
        }
        
        .company-tagline {
            font-size: 1rem;
        }
        
        .final-price {
            font-size: 2rem;
        }
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load CSV data files
@st.cache_data
def load_data():
    try:
        project_types = pd.read_csv('PROJECT_TYPES.csv')
        finish_levels = pd.read_csv('FINISH_LEVELS.csv')
        structural_complexity = pd.read_csv('STRUCTURAL_COMPLEXITY.csv')
        add_ons = pd.read_csv('ADD_ONS.csv')
        config = pd.read_csv('CONFIG.csv')
        
        # Convert config to dictionary
        config_dict = dict(zip(config['Key'], config['Value']))
        
        return project_types, finish_levels, structural_complexity, add_ons, config_dict
    except Exception as e:
        st.error(f"Error loading data files: {e}")
        return None, None, None, None, None

# Load data
project_types_df, finish_levels_df, complexity_df, add_ons_df, config = load_data()

# Header section
st.markdown("""
<div class="main-header">
    <div class="company-name">🏗️ Olive Contractors</div>
    <div class="company-tagline">Professional Construction Cost Estimator</div>
</div>
""", unsafe_allow_html=True)

# Check if data loaded successfully
if project_types_df is None:
    st.error("Failed to load data files. Please ensure all CSV files are present.")
    st.stop()

# Initialize session state
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Main form
st.markdown("### Project Details")

# Project Type Selection
project_type_options = dict(zip(project_types_df['name'], project_types_df['project_type_id']))
selected_project_name = st.selectbox(
    "Select Project Type",
    options=list(project_type_options.keys()),
    help="Choose the type of construction project"
)
selected_project_id = project_type_options[selected_project_name]

# Get project details
project_info = project_types_df[project_types_df['project_type_id'] == selected_project_id].iloc[0]

# Show project description
st.info(f"📋 {project_info['description']}")

# Square Footage Input
st.markdown("### Project Size")
square_footage = st.number_input(
    "Square Footage",
    min_value=1,
    value=500,
    step=50,
    help="Enter the total square footage of the project"
)

# Finish Level Selection
st.markdown("### Finish Level")
finish_level_options = dict(zip(finish_levels_df['label'], finish_levels_df['finish_level_id']))
selected_finish_label = st.selectbox(
    "Select Finish Level",
    options=list(finish_level_options.keys()),
    index=1,  # Default to "Standard"
    help="Choose the quality level of finishes"
)
selected_finish_id = finish_level_options[selected_finish_label]

# Show finish level description
finish_info = finish_levels_df[finish_levels_df['finish_level_id'] == selected_finish_id].iloc[0]
st.caption(f"ℹ️ {finish_info['description']} (Multiplier: {finish_info['multiplier']}x)")

# Structural Complexity Selection
st.markdown("### Structural Complexity")
complexity_options = dict(zip(complexity_df['label'], complexity_df['complexity_id']))
selected_complexity_label = st.selectbox(
    "Structural Changes",
    options=list(complexity_options.keys()),
    help="Select the level of structural modifications required"
)
selected_complexity_id = complexity_options[selected_complexity_label]

# Show complexity description
complexity_info = complexity_df[complexity_df['complexity_id'] == selected_complexity_id].iloc[0]
st.caption(f"ℹ️ {complexity_info['description']} (Multiplier: {complexity_info['multiplier']}x)")

# Add-ons Section
st.markdown("### Add-ons & Upgrades")

# Filter add-ons for selected project type
relevant_addons = add_ons_df[add_ons_df['project_type_id'] == selected_project_id]
selected_addons = []
addon_sqft_inputs = {}

if len(relevant_addons) > 0:
    st.markdown("**Select additional features:**")
    
    for idx, addon in relevant_addons.iterrows():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            is_selected = st.checkbox(
                f"{addon['name']} (${addon['low']:,.0f} - ${addon['high']:,.0f} CAD)",
                key=f"addon_{addon['addon_id']}"
            )
            st.caption(f"💡 {addon['notes']}")
        
        with col2:
            # If pricing type is per_sqft or per_unit, add quantity input
            if is_selected and addon['pricing_type'] in ['per_sqft', 'per_unit']:
                qty = st.number_input(
                    f"Qty",
                    min_value=1,
                    value=50 if addon['pricing_type'] == 'per_sqft' else 1,
                    key=f"qty_{addon['addon_id']}"
                )
                addon_sqft_inputs[addon['addon_id']] = qty
        
        if is_selected:
            selected_addons.append(addon)
else:
    st.info("No add-ons available for this project type.")

# Calculate Button
st.markdown("---")
if st.button("📊 CALCULATE ESTIMATE", type="primary", use_container_width=True):
    st.session_state.show_results = True

# Results Section
if st.session_state.show_results:
    st.markdown("---")
    st.markdown("## 💰 Cost Estimate Breakdown")
    
    # Get configuration values
    contingency_percent = float(config['default_contingency_percent'])
    markup_percent = float(config['default_contractor_markup_percent'])
    currency = config['currency']
    
    # Calculate base cost
    base_cost_low = max(
        square_footage * project_info['base_cost_per_sqft_low'],
        project_info['min_project_cost']
    )
    base_cost_high = max(
        square_footage * project_info['base_cost_per_sqft_high'],
        project_info['min_project_cost']
    )
    
    # Apply finish level multiplier
    finish_multiplier = finish_info['multiplier']
    after_finish_low = base_cost_low * finish_multiplier
    after_finish_high = base_cost_high * finish_multiplier
    
    # Apply structural complexity multiplier
    complexity_multiplier = complexity_info['multiplier']
    after_complexity_low = after_finish_low * complexity_multiplier
    after_complexity_high = after_finish_high * complexity_multiplier
    
    # Calculate add-ons total
    addons_total_low = 0
    addons_total_high = 0
    addon_details = []
    
    for addon in selected_addons:
        if addon['pricing_type'] == 'flat':
            addon_low = addon['low']
            addon_high = addon['high']
        elif addon['pricing_type'] in ['per_sqft', 'per_unit']:
            qty = addon_sqft_inputs.get(addon['addon_id'], 1)
            addon_low = addon['low'] * qty
            addon_high = addon['high'] * qty
        else:
            addon_low = addon['low']
            addon_high = addon['high']
        
        addons_total_low += addon_low
        addons_total_high += addon_high
        addon_details.append({
            'name': addon['name'],
            'low': addon_low,
            'high': addon_high
        })
    
    # Subtotal before contingency and markup
    subtotal_low = after_complexity_low + addons_total_low
    subtotal_high = after_complexity_high + addons_total_high
    
    # Apply contingency
    contingency_low = subtotal_low * (contingency_percent / 100)
    contingency_high = subtotal_high * (contingency_percent / 100)
    
    after_contingency_low = subtotal_low + contingency_low
    after_contingency_high = subtotal_high + contingency_high
    
    # Apply contractor markup
    markup_low = after_contingency_low * (markup_percent / 100)
    markup_high = after_contingency_high * (markup_percent / 100)
    
    final_total_low = after_contingency_low + markup_low
    final_total_high = after_contingency_high + markup_high
    
    # Display breakdown
    st.markdown('<div class="cost-breakdown">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Low Estimate**")
        st.write(f"Base Construction Cost: ${base_cost_low:,.2f} {currency}")
        st.write(f"× Finish Level ({finish_info['label']}): ${after_finish_low:,.2f} {currency}")
        st.write(f"× Structural ({complexity_info['label']}): ${after_complexity_low:,.2f} {currency}")
        
        if len(addon_details) > 0:
            st.write(f"**Add-ons:**")
            for addon in addon_details:
                st.write(f"  • {addon['name']}: ${addon['low']:,.2f} {currency}")
        
        st.write(f"**Subtotal: ${subtotal_low:,.2f} {currency}**")
        st.write(f"+ Contingency ({contingency_percent}%): ${contingency_low:,.2f} {currency}")
        st.write(f"+ Contractor Markup ({markup_percent}%): ${markup_low:,.2f} {currency}")
    
    with col2:
        st.markdown("**High Estimate**")
        st.write(f"Base Construction Cost: ${base_cost_high:,.2f} {currency}")
        st.write(f"× Finish Level ({finish_info['label']}): ${after_finish_high:,.2f} {currency}")
        st.write(f"× Structural ({complexity_info['label']}): ${after_complexity_high:,.2f} {currency}")
        
        if len(addon_details) > 0:
            st.write(f"**Add-ons:**")
            for addon in addon_details:
                st.write(f"  • {addon['name']}: ${addon['high']:,.2f} {currency}")
        
        st.write(f"**Subtotal: ${subtotal_high:,.2f} {currency}**")
        st.write(f"+ Contingency ({contingency_percent}%): ${contingency_high:,.2f} {currency}")
        st.write(f"+ Contractor Markup ({markup_percent}%): ${markup_high:,.2f} {currency}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cost Distribution - Simple version without Plotly
    st.markdown("### Cost Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Construction Cost", f"${(after_complexity_low + after_complexity_high)/2:,.0f} {currency}")
        st.metric("Add-ons", f"${(addons_total_low + addons_total_high)/2:,.0f} {currency}")
    
    with col2:
        st.metric("Contingency", f"${(contingency_low + contingency_high)/2:,.0f} {currency}")
        st.metric("Contractor Margin", f"${(markup_low + markup_high)/2:,.0f} {currency}")
    
    # Final Total Display
    st.markdown(f"""
    <div class="final-total">
        <h2>TOTAL PROJECT ESTIMATE</h2>
        <div class="final-price">${final_total_low:,.0f} - ${final_total_high:,.0f} {currency}</div>
        <p style="color: #D1FAE5; margin-top: 1rem; font-size: 1.1rem;">
            {project_info['name']} • {square_footage:,} sq ft • Toronto / GTA
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Notes
    st.markdown("---")
    st.markdown("### 📝 Important Notes")
    st.info(f"""
    - This is a rough budget estimate for planning purposes
    - Prices shown in {currency} for Toronto / GTA region
    - Final costs may vary based on site conditions, material selection, and unforeseen circumstances
    - Does not include appliances, furniture, or decorative items unless specified
    - Permits and design fees may apply separately
    - Valid for 30 days from estimate date
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>© 2024 Olive Contractors • Professional Construction Services • Toronto / GTA</p>
    <p style="font-size: 0.9rem;">This estimate is for budgeting purposes only and does not constitute a binding quote</p>
</div>
""", unsafe_allow_html=True)
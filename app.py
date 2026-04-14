import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Laboratory Testing Services Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== DATABASE CONNECTION =====
class DatabaseConnection:
    """Manage MySQL database connections"""
    
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            st.error(f"Database connection error: {e}")
            return False
    
    def fetch_query(self, query, params=None):
        """Fetch data from database"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            st.error(f"Query error: {e}")
            return None

# ===== INITIALIZE DATABASE =====
@st.cache_resource
def get_database():
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'laboratory_db')
    }
    db = DatabaseConnection(db_config)
    if db.connect():
        return db
    return None

db = get_database()

# ===== HELPER FUNCTIONS =====
def get_all_laboratories():
    """Get all laboratories"""
    query = "SELECT * FROM laboratory ORDER BY lab_name"
    result = db.fetch_query(query)
    return pd.DataFrame(result) if result else pd.DataFrame()

def get_laboratory_details(lab_id):
    """Get detailed information for a laboratory"""
    lab_query = "SELECT * FROM laboratory WHERE lab_id = %s"
    lab = db.fetch_query(lab_query, (lab_id,))
    
    location_query = "SELECT * FROM location_sorter WHERE lab_id = %s"
    location = db.fetch_query(location_query, (lab_id,))
    
    services_query = """
    SELECT s.service_id, s.service_name, s.service_category, s.estimated_turnaround_days,
           lsj.service_price, lsj.max_capacity
    FROM service s
    JOIN lab_service_junction lsj ON s.service_id = lsj.service_id
    WHERE lsj.lab_id = %s AND lsj.available = TRUE
    """
    services = db.fetch_query(services_query, (lab_id,))
    
    equipment_query = "SELECT * FROM equipment WHERE lab_id = %s ORDER BY equipment_type"
    equipment = db.fetch_query(equipment_query, (lab_id,))
    
    certification_query = "SELECT * FROM certification WHERE lab_id = %s ORDER BY certification_name"
    certifications = db.fetch_query(certification_query, (lab_id,))
    
    accreditation_query = "SELECT * FROM accreditation WHERE lab_id = %s ORDER BY accreditation_name"
    accreditations = db.fetch_query(accreditation_query, (lab_id,))
    
    return {
        'lab': lab[0] if lab else None,
        'location': location[0] if location else None,
        'services': pd.DataFrame(services) if services else pd.DataFrame(),
        'equipment': pd.DataFrame(equipment) if equipment else pd.DataFrame(),
        'certifications': pd.DataFrame(certifications) if certifications else pd.DataFrame(),
        'accreditations': pd.DataFrame(accreditations) if accreditations else pd.DataFrame()
    }

def search_labs_by_location(province=None, city=None):
    """Search labs by location"""
    query = """
    SELECT l.lab_id, l.lab_name, l.description, l.contact_email, l.contact_phone,
           loc.province, loc.city, loc.district, loc.address
    FROM laboratory l
    LEFT JOIN location_sorter loc ON l.lab_id = loc.lab_id
    WHERE 1=1
    """
    params = []
    
    if province:
        query += " AND loc.province = %s"
        params.append(province)
    if city:
        query += " AND loc.city = %s"
        params.append(city)
    
    query += " ORDER BY l.lab_name"
    result = db.fetch_query(query, params) if params else db.fetch_query(query)
    return pd.DataFrame(result) if result else pd.DataFrame()

def search_labs_by_service(service_category=None):
    """Search labs by service offered"""
    query = """
    SELECT DISTINCT l.lab_id, l.lab_name, l.description, l.contact_email,
           s.service_name, s.service_category, lsj.service_price, lsj.max_capacity
    FROM laboratory l
    JOIN lab_service_junction lsj ON l.lab_id = lsj.lab_id
    JOIN service s ON lsj.service_id = s.service_id
    WHERE lsj.available = TRUE
    """
    params = []
    
    if service_category:
        query += " AND s.service_category = %s"
        params.append(service_category)
    
    query += " ORDER BY l.lab_name"
    result = db.fetch_query(query, params) if params else db.fetch_query(query)
    return pd.DataFrame(result) if result else pd.DataFrame()

def get_all_provinces():
    """Get all provinces"""
    query = "SELECT DISTINCT province FROM location_sorter ORDER BY province"
    result = db.fetch_query(query)
    return [row['province'] for row in result] if result else []

def get_cities_by_province(province):
    """Get cities in province"""
    query = "SELECT DISTINCT city FROM location_sorter WHERE province = %s ORDER BY city"
    result = db.fetch_query(query, (province,))
    return [row['city'] for row in result] if result else []

def get_service_categories():
    """Get service categories"""
    query = "SELECT DISTINCT service_category FROM service ORDER BY service_category"
    result = db.fetch_query(query)
    return [row['service_category'] for row in result] if result else []

# ===== PAGE LAYOUT =====
st.title("🔬 Laboratory Testing Services Platform Indonesia")
st.markdown("**Integrated Search and Comparison Platform for Specialized Laboratory Testing Services**")
st.divider()

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choose a page:",
        ["🏠 Home", "🔍 Search by Location", "🧪 Search by Service", "📊 View Statistics", "ℹ️ About"]
    )

# ===== PAGE: HOME =====
if page == "🏠 Home":
    st.header("Welcome to Laboratory Testing Services Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📍 Laboratories", len(get_all_laboratories()))
    
    with col2:
        services_query = "SELECT COUNT(*) as count FROM service"
        services_count = db.fetch_query(services_query)
        st.metric("🧪 Services Available", services_count[0]['count'] if services_count else 0)
    
    with col3:
        provinces = get_all_provinces()
        st.metric("📊 Provinces Covered", len(provinces))
    
    st.divider()
    
    st.subheader("All Available Laboratories")
    labs = get_all_laboratories()
    
    if not labs.empty:
        for idx, lab in labs.iterrows():
            with st.expander(f"📌 {lab['lab_name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Status:** {lab['operational_status']}")
                    st.write(f"**Email:** {lab['contact_email']}")
                    st.write(f"**Phone:** {lab['contact_phone']}")
                
                with col2:
                    st.write(f"**Website:** {lab['website'] if lab['website'] else 'N/A'}")
                    st.write(f"**Established:** {lab['established_year']}")
                    
                if st.button(f"View Details", key=f"home_detail_{lab['lab_id']}"):
                    st.session_state.selected_lab = lab['lab_id']
                    st.session_state.page = "detail"
    else:
        st.info("No laboratories found.")

# ===== PAGE: SEARCH BY LOCATION =====
elif page == "🔍 Search by Location":
    st.header("Search Laboratories by Location")
    
    provinces = get_all_provinces()
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_province = st.selectbox("Select Province:", ["All"] + provinces, key="province_select")
    
    with col2:
        if selected_province != "All":
            cities = get_cities_by_province(selected_province)
            selected_city = st.selectbox("Select City:", ["All"] + cities, key="city_select")
        else:
            selected_city = None
    
    # Search
    if st.button("🔍 Search", use_container_width=True):
        province_param = selected_province if selected_province != "All" else None
        city_param = selected_city if selected_city and selected_city != "All" else None
        
        results = search_labs_by_location(province_param, city_param)
        
        if not results.empty:
            st.success(f"Found {len(results)} laboratory/laboratories")
            
            for idx, lab in results.iterrows():
                with st.expander(f"📌 {lab['lab_name']} - {lab.get('city', 'N/A')}, {lab.get('province', 'N/A')}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Address:** {lab.get('address', 'N/A')}")
                        st.write(f"**Email:** {lab['contact_email']}")
                    
                    with col2:
                        st.write(f"**Phone:** {lab['contact_phone']}")
                        st.write(f"**District:** {lab.get('district', 'N/A')}")
                    
                    if st.button(f"📋 View Full Details", key=f"location_detail_{lab['lab_id']}"):
                        st.session_state.selected_lab = lab['lab_id']
        else:
            st.warning("No laboratories found in selected location.")

# ===== PAGE: SEARCH BY SERVICE =====
elif page == "🧪 Search by Service":
    st.header("Search Laboratories by Service Type")
    
    categories = get_service_categories()
    
    selected_category = st.selectbox("Select Service Category:", ["All"] + categories, key="service_select")
    
    if st.button("🔍 Search", use_container_width=True):
        category_param = selected_category if selected_category != "All" else None
        results = search_labs_by_service(category_param)
        
        if not results.empty:
            st.success(f"Found {len(results)} results")
            
            for idx, result in results.iterrows():
                with st.expander(f"🧪 {result['lab_name']} - {result['service_name']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Service Category:** {result['service_category']}")
                        st.write(f"**Laboratory:** {result['lab_name']}")
                    
                    with col2:
                        st.write(f"**Service Price:** Rp {result['service_price']:,.0f}")
                        st.write(f"**Max Capacity:** {result['max_capacity']} samples")
                    
                    with col3:
                        st.write(f"**Contact:** {result['contact_email']}")
                    
                    if st.button(f"📋 View Lab Details", key=f"service_detail_{result['lab_id']}"):
                        st.session_state.selected_lab = result['lab_id']
        else:
            st.warning("No laboratories offering this service.")

# ===== PAGE: STATISTICS =====
elif page == "📊 View Statistics":
    st.header("Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    labs_count = len(get_all_laboratories())
    services_query = "SELECT COUNT(*) as count FROM service"
    services_count = db.fetch_query(services_query)[0]['count']
    provinces = get_all_provinces()
    
    accreditation_query = "SELECT COUNT(DISTINCT lab_id) as count FROM accreditation WHERE accreditation_status = 'active'"
    accredited_labs = db.fetch_query(accreditation_query)[0]['count']
    
    with col1:
        st.metric("Total Laboratories", labs_count)
    with col2:
        st.metric("Total Services", services_count)
    with col3:
        st.metric("Provinces", len(provinces))
    with col4:
        st.metric("Accredited Labs", accredited_labs)
    
    st.divider()
    
    # Labs by province
    st.subheader("Laboratories by Province")
    province_query = """
    SELECT loc.province, COUNT(DISTINCT l.lab_id) as count
    FROM laboratory l
    LEFT JOIN location_sorter loc ON l.lab_id = loc.lab_id
    GROUP BY loc.province
    ORDER BY count DESC
    """
    province_data = db.fetch_query(province_query)
    if province_data:
        province_df = pd.DataFrame(province_data)
        st.bar_chart(province_df.set_index('province')['count'])
    
    st.divider()
    
    # Services by category
    st.subheader("Services by Category")
    category_query = """
    SELECT service_category, COUNT(*) as count
    FROM service
    GROUP BY service_category
    ORDER BY count DESC
    """
    category_data = db.fetch_query(category_query)
    if category_data:
        category_df = pd.DataFrame(category_data)
        st.bar_chart(category_df.set_index('service_category')['count'])

# ===== PAGE: ABOUT =====
elif page == "ℹ️ About":
    st.header("About This Platform")
    
    st.markdown("""
    ## 🔬 Laboratory Testing Services Platform Indonesia
    
    ### Project Overview
    This platform is an **Integrated Search and Comparison Platform for Specialized Laboratory Testing Services in Indonesia**.
    
    ### Objective
    To establish a centralized and structured platform that compiles information on laboratory testing services in Indonesia, 
    thereby addressing persistent difficulties in locating suitable laboratories.
    
    ### Key Features
    - 🔍 **Search & Filter** laboratories by location, service type, and accreditation
    - 📊 **Compare** services, pricing, and capabilities
    - 📍 **Geographic Information** for logistics planning
    - 🏆 **Accreditation Status** verification
    - ⚙️ **Equipment** and certification details
    
    ### Database Structure
    - **9 Tables** including:
      - Laboratory Information
      - Location Details
      - Services Offered
      - Equipment Inventory
      - Certifications
      - Accreditations
      - Sample Records
      - User Management
    
    ### Technology Stack
    - **Frontend:** Streamlit
    - **Backend:** Jupyter Notebook (Python)
    - **Database:** MySQL
    
    ### By
    - Audrey Keeva Clara Natali
    - Christopher Edward Collin
    - Elaine Louise
    - Fadhil Nadjib Harharah
    
    **School of Life Sciences - i3L University Jakarta, Indonesia**
    """)
    
    st.divider()
    st.info("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ===== FOOTER =====
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
© 2026 Laboratory Testing Services Platform | i3L University Jakarta
</div>
""", unsafe_allow_html=True)

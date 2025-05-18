import streamlit as st

st.set_page_config(
    page_title="Test Page",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Test Page")

st.write("This is a test page to demonstrate multi-page functionality in Streamlit.")

# Add some example content
col1, col2 = st.columns(2)

with col1:
    st.header("Column 1")
    st.write("This is some test content in column 1")
    test_slider = st.slider("Test Slider", 0, 100, 50)
    st.write(f"Selected value: {test_slider}")

with col2:
    st.header("Column 2")
    st.write("This is some test content in column 2")
    test_button = st.button("Test Button")
    if test_button:
        st.success("Button clicked!")

# Add some metrics
st.subheader("Test Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Humidity", "85%", "-5%")
col3.metric("Wind", "9 mph", "8 mph") 
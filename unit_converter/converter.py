import streamlit as st

# Custom Styling
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
        }
        .result-text {
            font-size: 24px;
            font-weight: bold;
            color: #FF5722;
        }
        .stSelectbox label, .stNumber_input label {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Distance Converter Function
def distance_converter(from_unit, to_unit, value):
    units = {"Meters": 1, "Kilometers": 1000, "Feet": 0.3048, "Miles": 1609.34}
    return value * units[from_unit] / units[to_unit]

# Temperature Converter Function
def temperature_converter(from_unit, to_unit, value):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    return value

# Weight Converter Function
def weight_converter(from_unit, to_unit, value):
    units = {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495}
    return value * units[from_unit] / units[to_unit]

# Pressure Converter Function
def pressure_converter(from_unit, to_unit, value):
    units = {"Pascals": 1, "Hectopascals": 100, "Kilopascals": 1000, "Bar": 100000}
    return value * units[from_unit] / units[to_unit]

# Streamlit UI
st.markdown("<h1 class='main-title'>⚡ Unit Converter 🌎</h1>", unsafe_allow_html=True)

category = st.selectbox("🔍 Select Category", ["📏 Distance", "🌡️ Temperature", "⚖️ Weight", "💨 Pressure"])

from_unit, to_unit, value = None, None, 0

if category == "📏 Distance":
    from_unit = st.selectbox("🔄 From", ["Meters", "Kilometers", "Feet", "Miles"])
    to_unit = st.selectbox("🔄 To", ["Meters", "Kilometers", "Feet", "Miles"])
    value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.2f")
    result = distance_converter(from_unit, to_unit, value)

elif category == "🌡️ Temperature":
    from_unit = st.selectbox("🔄 From", ["Celsius", "Fahrenheit"])
    to_unit = st.selectbox("🔄 To", ["Celsius", "Fahrenheit"])
    value = st.number_input("✏️ Enter Value", format="%.2f")
    result = temperature_converter(from_unit, to_unit, value)

elif category == "⚖️ Weight":
    from_unit = st.selectbox("🔄 From", ["Kilograms", "Grams", "Pounds", "Ounces"])
    to_unit = st.selectbox("🔄 To", ["Kilograms", "Grams", "Pounds", "Ounces"])
    value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.2f")
    result = weight_converter(from_unit, to_unit, value)

elif category == "💨 Pressure":
    from_unit = st.selectbox("🔄 From", ["Pascals", "Hectopascals", "Kilopascals", "Bar"])
    to_unit = st.selectbox("🔄 To", ["Pascals", "Hectopascals", "Kilopascals", "Bar"])
    value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.2f")
    result = pressure_converter(from_unit, to_unit, value)

st.markdown(f"<p class='result-text'>🎯 {value} {from_unit} is equal to {result:.2f} {to_unit} 🎯</p>", unsafe_allow_html=True)

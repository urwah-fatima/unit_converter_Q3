import streamlit as st
import re

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "show_calculator" not in st.session_state:
    st.session_state.show_calculator = False

# Dictionary of conversion factors
conversion_factors = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Mile": 0.000621371,
        "Yard": 1.09361,
        "Foot": 3.28084,
        "Inch": 39.3701
    },
    "Weight": {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1e6,
        "Pound": 2.20462,
        "Ounce": 35.274
    },
    "Temperature": {
        "Celsius": lambda x: x,
        "Fahrenheit": lambda x: (x * 9/5) + 32,
        "Kelvin": lambda x: x + 273.15
    }
}

# Mapping for shorthand units (for smart input)
unit_aliases = {
    "m": "Meter", "km": "Kilometer", "cm": "Centimeter", "mm": "Millimeter",
    "mi": "Mile", "yd": "Yard", "ft": "Foot", "in": "Inch",
    "kg": "Kilogram", "g": "Gram", "mg": "Milligram", "lb": "Pound", "oz": "Ounce",
    "c": "Celsius", "f": "Fahrenheit", "k": "Kelvin"
}

st.title("🧠 Smart Unit Converter")

# Smart Input Toggle
if not st.session_state.show_calculator:
    smart_input = st.text_input("Type a conversion (e.g., '10 kg to lb', '25 C to F'):")

    # Try to parse smart input
    match = re.match(r"([\d.]+)\s*([a-zA-Z]+)\s*(to|in)?\s*([a-zA-Z]+)", smart_input)
    if match:
        value = float(match.group(1))
        from_raw = match.group(2).lower()
        to_raw = match.group(4).lower()

        from_unit = unit_aliases.get(from_raw, from_raw.capitalize())
        to_unit = unit_aliases.get(to_raw, to_raw.capitalize())
        conversion_type = None

        # Detect conversion type
        for category, units in conversion_factors.items():
            if from_unit in units and to_unit in units:
                conversion_type = category
                break

        # Perform conversion
        result = None
        if conversion_type:
            if conversion_type == "Temperature":
                if from_unit == "Celsius":
                    result = conversion_factors[conversion_type][to_unit](value)
                elif from_unit == "Fahrenheit":
                    celsius = (value - 32) * 5/9
                    result = conversion_factors[conversion_type][to_unit](celsius)
                elif from_unit == "Kelvin":
                    celsius = value - 273.15
                    result = conversion_factors[conversion_type][to_unit](celsius)
            else:
                try:
                    result = value * (conversion_factors[conversion_type][to_unit] / conversion_factors[conversion_type][from_unit])
                except:
                    st.error("Conversion failed. Please check the units.")
        else:
            st.warning("Could not identify the correct conversion type.")

        if result is not None:
            output = f"{value} {from_unit} = {result:.4f} {to_unit}"
            st.success(output)
            if output not in st.session_state.history:
                st.session_state.history.insert(0, output)
                st.session_state.history = st.session_state.history[:10]

    st.button("🔁 Back to Calculator", on_click=lambda: st.session_state.update({"show_calculator": True}))

else:
    # Classic Calculator UI
    conversion_type = st.selectbox("Choose a category:", list(conversion_factors.keys()))
    units = list(conversion_factors[conversion_type].keys())
    from_unit = st.selectbox("From:", units)
    to_unit = st.selectbox("To:", units)
    value = st.number_input(f"Enter value in {from_unit}:", value=0.0, step=0.1, format="%.2f")

    result = None
    if conversion_type == "Temperature":
        if from_unit == "Celsius":
            result = conversion_factors[conversion_type][to_unit](value)
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
            result = conversion_factors[conversion_type][to_unit](celsius)
        elif from_unit == "Kelvin":
            celsius = value - 273.15
            result = conversion_factors[conversion_type][to_unit](celsius)
    else:
        result = value * (conversion_factors[conversion_type][to_unit] / conversion_factors[conversion_type][from_unit])

    if result is not None:
        output = f"{value} {from_unit} = {result:.4f} {to_unit}"
        st.success(output)
        if output not in st.session_state.history:
            st.session_state.history.insert(0, output)
            st.session_state.history = st.session_state.history[:10]

    st.button("🧠 Try Smart Input Instead", on_click=lambda: st.session_state.update({"show_calculator": False}))

# Show history
if st.session_state.history:
    with st.expander("🕘 Conversion History (last 10)"):
        for item in st.session_state.history:
            st.write(item)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Smart Input + Classic Calculator Mode")

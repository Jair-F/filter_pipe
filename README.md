# 🔗 filter_pipe

A powerful and flexible Python library for building data processing pipelines with filters and mathematical operations. Chain multiple filters together to process numerical data in a clean, intuitive way.

[![PyPI Version](https://img.shields.io/pypi/v/filter-pipe.svg)](https://pypi.org/project/filter-pipe/) ![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)

---

## ✨ Features

- ⛓️ **Chainable Pipelines** - Combine filters seamlessly using pipe syntax
- 📊 **Signal Processing Filters** - Moving average, low-pass, high-pass, band-pass, notch filters
- 🧮 **Mathematical Operations** - Add, subtract, multiply, divide operations
- 🎯 **Flexible Configuration** - Easy-to-read pipeline syntax with customizable parameters
- 🔍 **Regex-based Validation** - Robust pattern matching for pipeline chunks

---

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from src.pipeline.pipeline import Pipeline

# Create a pipeline with multiple filters
pipeline = Pipeline('mavg(n=10) | lpass(alpha=0.2) | str(ndigits=2)')

# Process a value through the pipeline
result = pipeline.calc(2134.1231231)
print(result)  # Output: '2064.17'
```

### Mathematical Operations

```python
from src.pipeline.math_ops import Divide, Multiply, Add

# Use mathematical operations
divider = Divide(' / 2')
result = divider.calc(10)
print(result)  # Output: 5.0

# Combine in a pipeline
pipeline = Pipeline('*2 | +5 | /3')
result = pipeline.calc(10)  # (10 * 2 + 5) / 3 = 25/3 ≈ 8.33
```

### Advanced Pipeline Example

```python
# Signal smoothing pipeline: moving average → low-pass filter → round to 2 decimals
pipeline = Pipeline('mavg(n=5) | lpass(alpha=0.3) | str(ndigits=2)')
values = [100.2, 101.5, 99.8, 102.1, 100.9]

for value in values:
    smoothed = pipeline.calc(value)
    print(f"Input: {value:6.1f} → Output: {smoothed}")
```

---

## 📦 Available Pipeline Chunks

### 🎯 Filters

| Chunk | Syntax | Description | Parameters |
|-------|--------|-------------|------------|
| **Moving Average** | `mavg(n=N)` | Calculates the average of the last N values | `n` - window size (integer) |
| **Low-Pass Filter** | `lpass(alpha=A)` | Smooths data by attenuating high frequencies | `alpha` - smoothing factor (0-1) |
| **High-Pass Filter** | `hpass(alpha=A)` | Attenuates low frequencies, preserves high frequencies | `alpha` - smoothing factor (0-1) |
| **Band-Pass Filter** | `bpass(low_alpha=A,high_alpha=B)` | Passes frequencies within a band | `low_alpha`, `high_alpha` - bounds (0-1) |
| **Notch Filter** | `notch(low_alpha=A,high_alpha=B)` | Removes frequencies within a band | `low_alpha`, `high_alpha` - bounds (0-1) |
| **High Cut** | `hcut(cut=C)` | Caps maximum value | `cut` - maximum threshold |
| **Low Cut** | `lcut(cut=C)` | Caps minimum value | `cut` - minimum threshold |
| **To String** | `str(ndigits=N)` | Converts to formatted string | `ndigits` - decimal places (optional, default=0) |

### 🧮 Math Operations

| Chunk | Syntax | Description | Parameters |
|-------|--------|-------------|------------|
| **Divide** | `/ D` | Divides value by D | `D` - divisor (number) |
| **Multiply** | `* M` | Multiplies value by M | `M` - multiplier (number) |
| **Add** | `+ V` | Adds V to value | `V` - value to add (number) |
| **Subtract** | `- S` | Subtracts S from value | `S` - value to subtract (number) |

---

## 💡 Examples

### Example 1: Temperature Smoothing
Smooth noisy temperature sensor readings:

```python
from src.pipeline.pipeline import Pipeline

# Combine moving average with low-pass filter
pipeline = Pipeline('mavg(n=3) | lpass(alpha=0.5) | str(ndigits=1)')

temperatures = [20.1, 25.3, 19.8, 21.2, 20.9]
for temp in temperatures:
    smoothed = pipeline.calc(temp)
    print(f"Temperature: {temp}°C → Smoothed: {smoothed}°C")
```

### Example 2: Financial Data Processing
Process stock price data:

```python
# 10-period moving average → normalize → round to 2 decimals
pipeline = Pipeline('mavg(n=10) | str(ndigits=2)')

stock_prices = [150.25, 149.80, 151.10, 150.95, 149.50]
for price in stock_prices:
    avg = pipeline.calc(price)
    print(f"${price} → MA: ${avg}")
```

### Example 3: Signal Processing
Apply advanced filtering:

```python
# Remove noise with band-pass → apply notch → convert to string
pipeline = Pipeline('bpass(low_alpha=0.2,high_alpha=0.8) | notch(low_alpha=0.3,high_alpha=0.7) | str(ndigits=3)')

signal_data = [0.5, 0.6, 0.55, 0.58, 0.52]
for signal in signal_data:
    filtered = pipeline.calc(signal)
    print(f"Signal: {signal} → Filtered: {filtered}")
```

### Example 4: Value Constraints
Bound values within a range:

```python
# Scale value, then apply min/max constraints
pipeline = Pipeline('*10 | lcut(cut=0) | hcut(cut=100)')

raw_values = [-1.5, 5.3, 12.8, -0.2]
for val in raw_values:
    bounded = pipeline.calc(val)
    print(f"{val} → {bounded} (0-100 range)")
```

---

## 🧪 Running Tests

Execute the test suite to verify functionality:

```bash
python3 -m pytest
```

Tests are located in the `tests/` directory:
- `test_filters.py` - Filter functionality tests
- `test_math.py` - Math operations tests
- `test_pipeline.py` - Pipeline chaining tests

---

## 🔗 Resources

- **📦 PyPI Package**: Find this project on [PyPI](https://pypi.org/project/filter-pipe/)
- **�💼 Regex Patterns**: Learn and test regex patterns used in this project at [regex101.com](https://regex101.com/)
- **📚 Tools**: See `tools/index.html` for playing around with the filters and learn how to calibrate the gains.

---

## 📝 License

This project is open-source and available for educational and commercial use.

---

**Built with ❤️ for data processing pipelines**

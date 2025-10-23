# 🌱 City Pollution Reduction Plan

### A Numerical Optimization Project using the Simplex Method

---

## 📘 Project Overview

The **City of Greenvale** has been mandated by the national government to **drastically reduce its pollution footprint** within the next year.  
The **Environmental Commission** identified **ten priority pollutants** that must meet annual reduction targets:

- CO₂ (tons)  
- NOₓ (tons)  
- SO₂ (tons)  
- PM2.5 (tons)  
- CH₄ (tons)  
- VOC (tons)  
- CO (tons)  
- NH₃ (tons)  
- Black Carbon (BC) (tons)  
- N₂O (tons)

To achieve these reductions, Greenvale can select from **30 mitigation options**, including renewable energy projects, reforestation, and public transport improvements.  
Each option:
- Reduces a unique mix of pollutants.
- Incurs a specific implementation cost.

---

## 🎯 Objective

Determine the **optimal number of units** for each mitigation option to:
1. **Meet or exceed** the pollutant reduction targets for all ten pollutants.  
2. **Minimize the total cost** of implementation.

This problem was modeled and solved using **Linear Programming** via the **Simplex Method**.

---

## ⚙️ Methodology

1. **Model Formulation**
   - Decision Variables: Units of each mitigation option to implement.
   - Objective Function: Minimize total cost.
   - Constraints: Achieve or surpass target reductions for each pollutant.

2. **Solution Approach**
   - Used the **Simplex Method** to solve the linear optimization problem.
   - Conducted data preprocessing and matrix setup using **NumPy** and **Pandas**.
   - Built an interactive interface for visualization and parameter adjustment using **Streamlit**.

---

## 🧠 Tech Stack

| Tool / Library | Purpose |
|----------------|----------|
| **Python** | Core programming language |
| **NumPy** | Matrix and numerical computations |
| **Pandas** | Data manipulation and structuring |
| **Streamlit** | Web-based interactive user interface |

---

## 💡 Example Features

- Adjustable pollutant targets and cost coefficients.
- Visual summary of pollutant reductions achieved.
- Optimal solution table showing cost-minimized implementation plan.
- Real-time solver display using the Simplex algorithm.

---

## 🧾 Course Information

**Course:** Numerical and Symbolic Computation  
**Project Title:** City Pollution Reduction Plan  
**Method Used:** Simplex Method  
**Student:** *[Your Name]*

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/greenvale-pollution-plan.git
   cd greenvale-pollution-plan
2. install dependencies
   ```bash
   pip install -r requirements.txt
3. Run the streamlitapp
   ```bash
   streamlit run app.py


## 📊 Results
# The model provides:
# The minimum total cost required to meet all reduction targets.
# The optimal allocation of mitigation options.
# Insights into trade-offs between pollutant reduction and expenditure.



🏆 Developed as part of my Numerical and Symbolic Computation Course.

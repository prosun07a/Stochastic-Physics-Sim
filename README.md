# Stochastic Modeling of Radioactive Decay using Monte Carlo Simulation
**Independent Research Project** **Author:** Prosun Kanti Datta (HSC Class 11)  
**Environment:** Ubuntu 24.04 LTS | Python 3.11.2

---

## 1. Project Overview
This project is my first deep dive into **Computational Physics**. The goal was to see if I could re-create the standard exponential decay law ($N = N_0 e^{-\lambda t}$) not by using calculus, but by simulating thousands of individual random atoms.

In high school, we learn the formula as a smooth line. But in this simulation, I used the **Monte Carlo approach** to show that "laws of physics" are actually just the result of billions of tiny, random events adding up.

---

## 2. My Learning Journey & Logic
I didn't start with the final code. I had to build this in stages:

* **Phase 1 (The Loop):** I started with a simple `for` loop, checking every atom one by one. It worked but was very slow for large populations.
* **Phase 2 (Optimization):** I learned how to use `NumPy` to check all 10,000 atoms at once using "vectorization." This made the simulation 100x faster.
* **Phase 3 (Persistence):** I realized that seeing a graph once isn't enough for a real researcher. I added `Pandas` to log every second of the simulation into a `.csv` file so I could visualize the data later.

### Why Monte Carlo?
Instead of a fixed equation, my code "flips a coin" for every atom. If the random roll is less than my decay constant ($\lambda$), the atom is removed. This is a **stochastic process**.

---

## 3. Results & What I Found
I ran the simulation with $N_0 = 10,000$ and $\lambda = 0.03$. 

* **Theoretical Half-Life:** $ln(2) / 0.03 \approx 23.10$ seconds.
* **My Simulation Result:** I consistently got between 22 and 24 seconds.
* **Accuracy:** ~98%

**The Big Lesson:** When I tried the simulation with only 50 atoms, the graph was a jagged mess. It taught me that **The Law of Large Numbers** is what makes physics predictable. You need a lot of data for the "noise" to disappear.

---

## 4. Challenges & Troubleshooting (The Hard Parts)
This wasn't a "plug and play" project. I ran into several walls:
1.  **The "Headless" Error:** On Ubuntu, my terminal couldn't open a window to show the plot (`UserWarning: FigureCanvasAgg`). I had to learn how to save the plots directly to a folder instead of trying to "show" them.
2.  **Path Confusion:** I struggled with where the files were being saved. I had to learn how to use `os.path.abspath` so the code works no matter where the folder is located.
3.  **Environment Setup:** Setting up a `.venv` (Virtual Environment) on Linux was new to me, but it helped keep my system clean from library conflicts.

---

## 5. Repository Structure
* `core/`: The "Engine" (Logic for the simulation and analysis).
* `data/`: Where the raw numbers are stored after a run.
* `results/`: The final scientific plots (saved at 300 DPI).
* `research_report.py`: The main script that runs the whole story from start to finish.

---

## 6. How to Run
```bash
source .venv/bin/activate
pip install -r requirements.txt
python3 research_report.py






---

### **A Note on Why I Built This**
As an HSC student in Sylhet, I often find that our physics curriculum is limited to solving equations on paper. I wanted to see if I could "touch" the physics through code'(basically i love to code). This project started when I heard two words Monte Carlo and learned about this Monte Carlo method or simulation then after somedays while learning a topic in my academic physics book suddenly wondered why a random process like decay always results in the same smooth curve. 

I didn't have a formal lab or a CS teacher to guide me, so I treated this project as my own independent "Computational Lab." I used AI as a 24/7 research mentor—not to write the code for me, but to explain complex concepts like **Vectorization** and **Stochastic Sampling** until I could implement them myself on my Linux-Ubuntu computer. Every error I faced, from broken paths to library conflicts, taught me more about the reality of scientific research than a textbook ever could. I built this to prove that with enough curiosity and the right digital tools, a high school student can contribute to the world of computational science.
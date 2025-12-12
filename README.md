# Contiguous Memory Allocation Simulator

A visual, interactive simulator that demonstrates how **First Fit**, **Best Fit**, and **Worst Fit** allocation strategies place processes into contiguous memory blocks.

The tool helps learners clearly understand memory allocation, fragmentation, and why different strategies produce different outcomes.

---

## 🚀 Features

* Input memory block sizes and process queue.
* Visual block-based representation of allocated and free memory.
* Simulation of:

  * **First Fit**
  * **Best Fit**
  * **Worst Fit**
* Calculation of:

  * Internal fragmentation
  * External fragmentation
* Clean, intuitive UI built with HTML/CSS/JS.
* Backend powered by **Flask** to process allocations and render results.

---

### Project Flow:

Input Page

*(User enters memory blocks and process queue)*

### Simulation Results

*(Side‑by‑side comparison of First Fit, Best Fit, and Worst Fit)*

### Detailed Allocation View

*(Allocated blocks, fragmentation, and failed processes)*

---

## 🧠 How It Works

1. User provides:

   * Memory block sizes (e.g., `100, 500, 200, 300, 600`)
   * Process sizes (e.g., `212, 417, 112, 426`)
2. The backend (Flask) runs all three allocation strategies.
3. The frontend displays:

   * Allocated blocks
   * Remaining free space
   * Internal + external fragmentation
   * Failed allocations
4. Users can rerun the simulation instantly.

---

## 🛠️ Technologies Used

* **HTML**, **CSS**, **JavaScript** (Frontend UI)
* **Flask (Python)** — Backend calculation engine
* **Jinja2 Templates** — Rendering dynamic HTML results

---

## 📂 Project Structure

```
MEM_SIMULATOR/
├─ static/
│  ├─ script.js
│  ├─ results.js
│  ├─ style.css
├─ templates/
│  ├─ index.html
│  ├─ results.html
├─ app.py               # Flask backend
├─ requirements.txt     # Python dependencies
```

---

## ▶️ Running the Project

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Start the Flask server:

   ```bash
   python app.py
   ```


## 👩‍💻 Team Members

* **Ishita Singh**
* **Dharshini M K**
* **Sreenidhi R**

---



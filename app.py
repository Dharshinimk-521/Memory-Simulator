from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json # We will need this to pass data to the template

app = Flask(__name__)
# A secret key is required for 'flashing' error messages
app.secret_key = 'your_secret_key_here' # Change this to a random string

# --- Algorithm Logic (No Change) ---
# The first_fit, best_fit, and worst_fit functions are identical
# to the previous version. I'm omitting them here for brevity,
# just copy/paste them directly into this file.
def first_fit(original_blocks, processes):
    # Create a copy of the blocks to modify
    blocks = [{'id': i, 'size': size, 'process_id': None, 'process_size': 0, 'internal_frag': 0} for i, size in enumerate(original_blocks)]
    allocations = []
    failed = []

    for pid, process_size in enumerate(processes):
        process_id_str = f"P{pid + 1}"
        allocated = False
        
        for block in blocks:
            # Check if block is free and large enough
            if block['process_id'] is None and block['size'] >= process_size:
                # Allocate process to this block
                block['process_id'] = process_id_str
                block['process_size'] = process_size
                block['internal_frag'] = block['size'] - process_size
                
                allocations.append(f"{process_id_str} ({process_size}KB) -> Block {block['id']} ({block['size']}KB)")
                allocated = True
                break  # Stop searching (First-Fit)
        
        if not allocated:
            failed.append(f"{process_id_str} ({process_size}KB)")

    total_internal = sum(b['internal_frag'] for b in blocks if b['process_id'] is not None)
    total_external = sum(b['size'] for b in blocks if b['process_id'] is None)
    
    return {
        "memory_map": blocks,
        "allocations": allocations,
        "failed": failed,
        "internal": total_internal,
        "external": total_external
    }

def best_fit(original_blocks, processes):
    blocks = [{'id': i, 'size': size, 'process_id': None, 'process_size': 0, 'internal_frag': 0} for i, size in enumerate(original_blocks)]
    allocations = []
    failed = []

    for pid, process_size in enumerate(processes):
        process_id_str = f"P{pid + 1}"
        best_block = None
        min_fragment = float('inf')

        # Find the best block
        for block in blocks:
            if block['process_id'] is None and block['size'] >= process_size:
                fragment = block['size'] - process_size
                if fragment < min_fragment:
                    min_fragment = fragment
                    best_block = block
        
        if best_block is not None:
            # Allocate to the best block found
            best_block['process_id'] = process_id_str
            best_block['process_size'] = process_size
            best_block['internal_frag'] = min_fragment
            allocations.append(f"{process_id_str} ({process_size}KB) -> Block {best_block['id']} ({best_block['size']}KB)")
        else:
            failed.append(f"{process_id_str} ({process_size}KB)")

    total_internal = sum(b['internal_frag'] for b in blocks if b['process_id'] is not None)
    total_external = sum(b['size'] for b in blocks if b['process_id'] is None)
    
    return {
        "memory_map": blocks,
        "allocations": allocations,
        "failed": failed,
        "internal": total_internal,
        "external": total_external
    }

def worst_fit(original_blocks, processes):
    blocks = [{'id': i, 'size': size, 'process_id': None, 'process_size': 0, 'internal_frag': 0} for i, size in enumerate(original_blocks)]
    allocations = []
    failed = []

    for pid, process_size in enumerate(processes):
        process_id_str = f"P{pid + 1}"
        worst_block = None
        max_fragment = -1

        # Find the worst block
        for block in blocks:
            if block['process_id'] is None and block['size'] >= process_size:
                fragment = block['size'] - process_size
                if fragment > max_fragment:
                    max_fragment = fragment
                    worst_block = block
        
        if worst_block is not None:
            # Allocate to the worst block found
            worst_block['process_id'] = process_id_str
            worst_block['process_size'] = process_size
            worst_block['internal_frag'] = max_fragment
            allocations.append(f"{process_id_str} ({process_size}KB) -> Block {worst_block['id']} ({worst_block['size']}KB)")
        else:
            failed.append(f"{process_id_str} ({process_size}KB)")

    total_internal = sum(b['internal_frag'] for b in blocks if b['process_id'] is not None)
    total_external = sum(b['size'] for b in blocks if b['process_id'] is None)
    
    return {
        "memory_map": blocks,
        "allocations": allocations,
        "failed": failed,
        "internal": total_internal,
        "external": total_external
    }
# --- End of Algorithm Logic ---


def parse_form_input(input_string):
    """Helper function to parse comma-separated numbers."""
    try:
        return [int(s.strip()) for s in input_string.split(',') if s.strip().isdigit() and int(s.strip()) > 0]
    except:
        return []

# --- API Routes ---

@app.route("/")
def index():
    """Serve the main input page (index.html)."""
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    """
    Handle the form submission, run simulations, 
    and render the results page (results.html).
    """
    # Get data from the HTML form (not JSON)
    blocks_str = request.form.get("blocks", "")
    processes_str = request.form.get("processes", "")

    # Parse and validate inputs
    blocks = parse_form_input(blocks_str)
    processes = parse_form_input(processes_str)

    if not blocks or not processes:
        # If input is bad, send an error message
        # and redirect back to the index page.
        flash("Invalid input. Please provide positive, comma-separated numbers.", "error")
        return redirect(url_for("index"))

    # Run all three algorithms
    results = {
        "first_fit": first_fit(blocks, processes),
        "best_fit": best_fit(blocks, processes),
        "worst_fit": worst_fit(blocks, processes),
    }
    
    # We pass the results as a regular Python dict.
    # We will also pass a JSON-dumped version for our JavaScript.
    return render_template("results.html", results_data=results)


if __name__ == "__main__":
    app.run(debug=True)
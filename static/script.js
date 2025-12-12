document.addEventListener("DOMContentLoaded", () => {
    // Check if the resultsData variable exists (it was embedded in results.html)
    if (typeof resultsData !== 'undefined') {
        // Run the UI update functions immediately on page load
        updateUI("ff", resultsData.first_fit);
        updateUI("bf", resultsData.best_fit);
        updateUI("wf", resultsData.worst_fit);
    } else {
        console.error("Simulation data not found!");
    }
});

/**
 * Updates the UI for a specific algorithm.
 * This function is identical to the previous version.
 */
function updateUI(prefix, data) {
    const mapEl = document.getElementById(`${prefix}-map`);
    const metricsEl = document.getElementById(`${prefix}-metrics`);
    const allocEl = document.getElementById(`${prefix}-allocations`);
    const failedEl = document.getElementById(`${prefix}-failed`);

    // Update Metrics
    metricsEl.innerHTML = `
        <strong>Internal Fragmentation:</strong> ${data.internal} KB<br>
        <strong>External Fragmentation:</strong> ${data.external} KB
    `;

    // Update Allocation & Failed Lists
    allocEl.innerHTML = data.allocations.length > 0 ? data.allocations.join('<br>') : 'None';
    failedEl.innerHTML = data.failed.length > 0 ? data.failed.join('<br>') : 'None';

    // Clear and build Memory Map
    mapEl.innerHTML = '';
    data.memory_map.forEach(block => {
        const blockDiv = document.createElement('div');
        blockDiv.className = 'memory-block';

        if (block.process_id) {
            // Block is ALLOCATED
            blockDiv.classList.add('allocated');
            const processPercent = (block.process_size / block.size) * 100;
            const fragmentPercent = (block.internal_frag / block.size) * 100;

            const processFill = document.createElement('div');
            processFill.className = 'process-fill';
            processFill.style.width = `${processPercent}%`;
            processFill.textContent = `${block.process_id} (${block.process_size}KB)`;
            
            const fragmentFill = document.createElement('div');
            fragmentFill.className = 'fragment-fill';
            fragmentFill.style.width = `${fragmentPercent}%`;
            if(block.internal_frag > 0) {
               fragmentFill.textContent = `Frag (${block.internal_frag}KB)`;
            }

            blockDiv.appendChild(processFill);
            blockDiv.appendChild(fragmentFill);
        } else {
            // Block is FREE
            blockDiv.classList.add('free');
            blockDiv.textContent = `Free (${block.size}KB)`;
        }

        // Add the total size label
        const label = document.createElement('div');
        label.className = 'block-label';
        label.textContent = `Block ${block.id} (Total: ${block.size}KB)`;
        blockDiv.appendChild(label);

        mapEl.appendChild(blockDiv);
    });
}
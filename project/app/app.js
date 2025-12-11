const inputArea = document.getElementById('input-area');
const suggestionStrip = document.getElementById('suggestion-strip');
const autoAcceptCheckbox = document.getElementById('auto-accept');
const statusDisplay = document.getElementById('status-display');

let debounceTimer;
const DEBOUNCE_DELAY = 300; // ms

// --- Event Listeners ---

inputArea.addEventListener('input', (e) => {
    // Basic debounce
    clearTimeout(debounceTimer);

    // If user hit space and auto-accept is on, handled in 'keydown' ideally or here?
    // 'input' fires after the content changes. 
    // Usually auto-accept on space is handled in keydown to INTERCEPT the space.
    // But for simplicity let's just trigger suggestion fetch here.

    debounceTimer = setTimeout(() => {
        const text = inputArea.value;
        if (text.trim().length > 0) {
            fetchSuggestions(text);
        } else {
            clearSuggestions();
        }
    }, DEBOUNCE_DELAY);
});

inputArea.addEventListener('keydown', (e) => {
    if (e.key === ' ' && autoAcceptCheckbox.checked) {
        // If there's a top suggestion, accept it
        const topSuggestion = suggestionStrip.querySelector('.suggestion-chip');
        if (topSuggestion) {
            e.preventDefault(); // Prevent the space for a moment
            applySuggestion(topSuggestion.dataset.word);
            // Re-add space? 
            // Typically auto-complete replaces the current word.
            // Then adds a space.
        }
    }
});

// --- API Interaction ---

async function fetchSuggestions(text) {
    statusDisplay.textContent = "Fetching...";
    try {
        const response = await fetch('http://localhost:8000/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        statusDisplay.textContent = "Ready";
        renderSuggestions(data);
    } catch (error) {
        console.error(error);
        statusDisplay.textContent = "Error fetching suggestions. Is server running?";
    }
}

// --- UI Rendering ---

function renderSuggestions(data) {
    // data = { corrected: "...", suggestions: [{word, score}, ...] }

    // You could optionally show the "Autocorrected" preview somewhere
    // For now, just show the next-word suggestions

    suggestionStrip.innerHTML = '';

    if (data.suggestions.length === 0) {
        suggestionStrip.innerHTML = '<div class="placeholder-text">No suggestions</div>';
        return;
    }

    data.suggestions.forEach(item => {
        const chip = document.createElement('div');
        chip.className = 'suggestion-chip';
        chip.textContent = item.word;
        chip.dataset.word = item.word;

        chip.addEventListener('click', () => {
            applySuggestion(item.word);
        });

        suggestionStrip.appendChild(chip);
    });
}

function clearSuggestions() {
    suggestionStrip.innerHTML = '<div class="placeholder-text">Suggestions will appear here...</div>';
}

function applySuggestion(word) {
    const text = inputArea.value;
    const cursorPos = inputArea.selectionStart; // Simple cursor handling

    // Inserting at cursor is complex because we need to know if we are replacing the current word or appending.
    // Text prediction typically works on the END of the stream for this prototype.
    // Let's assume we append to the end for simplicity, or try to be smart.

    // Simplest approach: Append word + space
    // Check if we need leading space
    const needsSpace = text.length > 0 && text[text.length - 1] !== ' ';

    inputArea.value = text + (needsSpace ? ' ' : '') + word + ' ';
    inputArea.focus();

    // Trigger new prediction immediately
    clearTimeout(debounceTimer); // clear pending
    fetchSuggestions(inputArea.value);
}
